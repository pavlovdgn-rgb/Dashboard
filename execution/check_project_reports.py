"""Project-level report list, immutable options and real browser PDF download."""
import io
import json
import os
import subprocess
import unittest
from pathlib import Path
from urllib.request import urlopen
from pypdf import PdfReader
from check_heatmap_api import HeatmapApiTests
from check_live_project import LiveProjectTests
from serve_heatmap import connect
import project_reports

class ReportTests(unittest.TestCase):
    setUp=HeatmapApiTests.setUp
    tearDown=HeatmapApiTests.tearDown
    request=HeatmapApiTests.request
    event=HeatmapApiTests.event
    click=LiveProjectTests.click
    visit=LiveProjectTests.visit
    seed=LiveProjectTests.seed

    def test_options_and_snapshots(self):
        self.seed()
        for options in ({'sections':[]},{'sections':['wrong']},{'sections':['tasks','tasks']},{'title':''},{'title':'a'*161},{'unexpected':1}):
            self.assertEqual(self.request('/api/project/reports',options)[0],400)
        created=self.request('/api/project/reports',{'title':'Итоговый отчёт','sections':['sessions'],'device':'desktop'})[1]
        self.assertEqual(created['sections'],['sessions'])
        # A report from another project must not enter the catalog or be downloadable.
        with connect(self.db) as db:
            config=json.loads(db.execute("SELECT value FROM live_studies WHERE id='leed-local'").fetchone()[0]);config['studyId']='foreign';config['id']='foreign-project'
            db.execute('INSERT INTO live_studies VALUES (?,?,?,?)',('foreign','foreign-project',json.dumps(config),1))
            db.execute('INSERT INTO live_reports VALUES (?,?,?)',('foreign-report',json.dumps({**created,'id':'foreign-report'}),'foreign'))
        catalog=self.request('/api/project/reports')[1]['reports'];self.assertEqual(len(catalog),1)
        self.assertEqual(self.request('/api/project/report?id=foreign-report')[0],400)
        self.request('/api/project/config',{'studyTitle':'Changed later'})
        self.assertEqual(self.request('/api/project/report?id='+created['id'])[1]['project']['studyTitle'],created['project']['studyTitle'])
        with urlopen(self.url+'/api/project/report-pdf?id='+created['id']) as response:
            self.assertEqual(response.headers.get_content_type(),'application/pdf');raw=response.read()
        pdf=PdfReader(io.BytesIO(raw));text='\n'.join(p.extract_text() for p in pdf.pages)
        self.assertIn('Итоговый отчёт',text);self.assertIn('Сессии',text);self.assertNotIn('Воронка переходов',text)

    def test_browser_reports(self):
        self.seed()
        # Preserve an actual legacy report with no new metadata.
        old=self.request('/api/project/reports',{})[1]
        with connect(self.db) as db:
            old.pop('title');old.pop('sections');db.execute('UPDATE live_reports SET value=? WHERE id=?',(json.dumps(old,ensure_ascii=False),old['id']))
        other=self.request('/api/project/studies',{'studyTitle':'Мобильное исследование'})[1]
        self.request('/api/project/visit',self.visit(id='mobile-visit',study=other['studyId'],session='mobile-session',vw=390,vh=844))
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_project_reports.mjs'],env={**os.environ,'LIVE_TEST_API':self.url,'REPORT_TEST_STUDY':other['studyId']},check=True,timeout=180)

    def test_long_task_pdf(self):
        report=self.request('/api/project/reports',{'title':'Проверка длинных критериев','sections':['tasks','sessions']})[1]
        task={'taskId':'manual','revision':'v1','title':'Оценка сценария','scenario':'Подробная инструкция участнику. '*60,'criterionLabel':'Пользователь выполнил условие <успех>. '*45,'status':'needs_review'}
        report['sessions']=[{'id':'session-'+str(i),'lastAt':1000,'clicks':1,'task':{'tasks':[{**task,'status':status}]}} for i,status in enumerate(('succeeded','failed','needs_review','indeterminate','pending'))]
        report['total']['sessions']=5
        raw=project_reports.render_pdf(report,{})
        reader=PdfReader(io.BytesIO(raw));text='\n'.join(p.extract_text() for p in reader.pages)
        self.assertIn('1 из 5 (20%)',text);self.assertIn('Невозможно оценить',text);self.assertIn('session-4',text);self.assertIn('<успех>',text)
        out=Path('.tmp/project-reports/long-tasks.pdf');out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)

if __name__=='__main__':unittest.main(defaultTest='ReportTests')
