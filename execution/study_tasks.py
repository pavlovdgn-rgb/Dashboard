"""Explicit task outcomes from confirmed prototype actions; never inferred from click labels."""
from study_task_plan import CRITERIA,definitions,validate_tasks,get_run,record,enrich
import study_task_plan


def initialize(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS study_task_runs (
        study TEXT NOT NULL, session TEXT NOT NULL, criterion TEXT NOT NULL, scenario TEXT NOT NULL,
        status TEXT NOT NULL, startedAt INTEGER NOT NULL, updatedAt INTEGER NOT NULL,
        completedAt INTEGER, finishedAt INTEGER, vw INTEGER NOT NULL, vh INTEGER NOT NULL,
        PRIMARY KEY(study,session));
      CREATE TABLE IF NOT EXISTS study_task_events (
        id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL, kind TEXT NOT NULL,
        timestamp INTEGER NOT NULL, page TEXT NOT NULL, vw INTEGER NOT NULL, vh INTEGER NOT NULL);
    ''')

    study_task_plan.initialize(db)
