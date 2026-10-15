"""Verify the owner-requested data change on isolated databases only."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'execution'))
import cloud_db
import live_project
from requested_study_20261015 import STUDY_ID,STUDY_TITLE,TASKS,create_once


class RequestedStudyTests(unittest.TestCase):
    def test_exact_tasks_idempotence_and_respected_deletion(self):
        with tempfile.TemporaryDirectory() as folder,patch.dict(os.environ,{'UXLAB_TEST_DB':str(Path(folder)/'study.sqlite3'),'VERCEL':''}):
            cloud_db.migrate()
            with cloud_db.connect() as db:
                saved=live_project.settings(db,STUDY_ID)
                self.assertEqual(saved['studyTitle'],STUDY_TITLE)
                self.assertFalse(saved['enabled'])
                self.assertEqual([task['title'] for task in saved['tasks']],[task[1] for task in TASKS])
                self.assertEqual([task['instruction'] for task in saved['tasks']],[task[1] for task in TASKS])
                self.assertTrue(all(task['verification']['method']=='automatic' for task in saved['tasks']))
                self.assertEqual(db.execute('SELECT COUNT(*) FROM study_task_sessions WHERE study=?',(STUDY_ID,)).fetchone()[0],0)
                other=db.execute('SELECT value FROM live_studies WHERE id=?',(live_project.STUDY,)).fetchone()[0]
                saved['studyTitle']='Отредактировано владельцем'
                db.execute('UPDATE live_studies SET value=? WHERE id=?',(json.dumps(saved),STUDY_ID))
            cloud_db.migrate()
            with cloud_db.connect() as db:
                self.assertEqual(live_project.settings(db,STUDY_ID)['studyTitle'],'Отредактировано владельцем')
                self.assertEqual(db.execute('SELECT value FROM live_studies WHERE id=?',(live_project.STUDY,)).fetchone()[0],other)
                self.assertFalse(create_once(db))
                live_project.delete_study(db,STUDY_ID)
                self.assertFalse(create_once(db))
            cloud_db.migrate()
            with cloud_db.connect() as db:
                self.assertIsNone(db.execute('SELECT 1 FROM live_studies WHERE id=?',(STUDY_ID,)).fetchone())

    def test_upgrade_from_version_three(self):
        with tempfile.TemporaryDirectory() as folder,patch.dict(os.environ,{'UXLAB_TEST_DB':str(Path(folder)/'study.sqlite3'),'VERCEL':''}):
            cloud_db.migrate()
            with cloud_db.connect() as db:
                db.execute('DELETE FROM live_studies WHERE id=?',(STUDY_ID,))
                db.execute('DELETE FROM cloud_schema WHERE version=4')
                old=db.execute('SELECT value FROM live_studies WHERE id=?',(live_project.STUDY,)).fetchone()[0]
            cloud_db.migrate()
            with cloud_db.connect() as db:
                self.assertEqual(len(live_project.settings(db,STUDY_ID)['tasks']),6)
                self.assertEqual(db.execute('SELECT value FROM live_studies WHERE id=?',(live_project.STUDY,)).fetchone()[0],old)


if __name__=='__main__':unittest.main(verbosity=2)
