CREATE TABLE IF NOT EXISTS clicks (
                id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL,
                seq INTEGER NOT NULL, page TEXT NOT NULL, version TEXT NOT NULL,
                layout TEXT NOT NULL, target TEXT NOT NULL, x REAL NOT NULL, y REAL NOT NULL,
                vw INTEGER NOT NULL, vh INTEGER NOT NULL, rw REAL NOT NULL, rh REAL NOT NULL,
                scroll_x REAL NOT NULL, scroll_y REAL NOT NULL, timestamp INTEGER NOT NULL,
                received TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, context TEXT NOT NULL DEFAULT '',
                UNIQUE(study,session,seq)
            );
CREATE TABLE IF NOT EXISTS cloud_schema (version INTEGER PRIMARY KEY);
INSERT OR IGNORE INTO "cloud_schema" VALUES(1);
CREATE TABLE IF NOT EXISTS live_findings (id TEXT PRIMARY KEY, value TEXT NOT NULL, study TEXT NOT NULL DEFAULT 'leed-local');
CREATE TABLE IF NOT EXISTS live_reports (id TEXT PRIMARY KEY, value TEXT NOT NULL, study TEXT NOT NULL DEFAULT 'leed-local');
CREATE TABLE IF NOT EXISTS live_settings (id TEXT PRIMARY KEY, value TEXT NOT NULL);
INSERT OR IGNORE INTO "live_settings" VALUES('project','{"id": "leed-generation", "title": "Lead Generation", "studyId": "leed-local", "studyTitle": "\u0418\u0441\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u0435 Lead Generation", "url": "/participant/leads-table?ux_study=leed-local", "enabled": true, "funnel": [], "collectClicks": true, "collectVisits": true, "allowVideo": true, "recordingMode": "video", "scenario": "", "mode": "free", "successCriterion": "none"}');
CREATE TABLE IF NOT EXISTS live_studies (id TEXT PRIMARY KEY, project_id TEXT NOT NULL, value TEXT NOT NULL, created_at INTEGER NOT NULL);
INSERT OR IGNORE INTO "live_studies" VALUES('leed-local','leed-generation','{"id": "leed-generation", "title": "Lead Generation", "studyId": "leed-local", "studyTitle": "Исследование Lead Generation", "url": "/participant/leads-table?ux_study=leed-local", "enabled": true, "funnel": [], "collectClicks": true, "collectVisits": true, "allowVideo": true, "recordingMode": "video", "scenario": "", "mode": "free", "successCriterion": "none"}',0);
CREATE TABLE IF NOT EXISTS prototype_success_signals (
        project TEXT, type TEXT, value TEXT, page TEXT, label TEXT, lastAt INTEGER,
        PRIMARY KEY(project,type,value,page));
CREATE TABLE IF NOT EXISTS recording_chunks (recording TEXT NOT NULL, seq INTEGER NOT NULL, data BLOB NOT NULL,
        digest TEXT NOT NULL, PRIMARY KEY(recording,seq));
CREATE TABLE IF NOT EXISTS recordings (id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL,
        startedAt INTEGER NOT NULL, mime TEXT NOT NULL, duration REAL NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'uploading', chunks INTEGER NOT NULL DEFAULT 0, bytes INTEGER NOT NULL DEFAULT 0,
        interrupted INTEGER NOT NULL DEFAULT 0, media BLOB);
CREATE TABLE IF NOT EXISTS replay_frames (id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL,
        seq INTEGER NOT NULL, timestamp INTEGER NOT NULL, page TEXT NOT NULL, snapshot TEXT NOT NULL,
        vw INTEGER NOT NULL, vh INTEGER NOT NULL, kind TEXT NOT NULL, label TEXT NOT NULL, target TEXT NOT NULL DEFAULT '{}');
CREATE TABLE IF NOT EXISTS snapshots (
                id TEXT PRIMARY KEY, html TEXT NOT NULL, width INTEGER NOT NULL, height INTEGER NOT NULL
            );
CREATE TABLE IF NOT EXISTS study_task_attempts (
        study TEXT NOT NULL, session TEXT NOT NULL, taskId TEXT NOT NULL, revision TEXT NOT NULL,
        ordinal INTEGER NOT NULL, title TEXT NOT NULL, scenario TEXT NOT NULL, criterion TEXT NOT NULL,
        status TEXT NOT NULL, startedAt INTEGER, updatedAt INTEGER NOT NULL, completedAt INTEGER,
        finishedAt INTEGER, PRIMARY KEY(study,session,taskId));
CREATE TABLE IF NOT EXISTS study_task_events (
        id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL, kind TEXT NOT NULL,
        timestamp INTEGER NOT NULL, page TEXT NOT NULL, vw INTEGER NOT NULL, vh INTEGER NOT NULL, taskId TEXT NOT NULL DEFAULT '', value TEXT NOT NULL DEFAULT '', label TEXT NOT NULL DEFAULT '');
CREATE TABLE IF NOT EXISTS study_task_runs (
        study TEXT NOT NULL, session TEXT NOT NULL, criterion TEXT NOT NULL, scenario TEXT NOT NULL,
        status TEXT NOT NULL, startedAt INTEGER NOT NULL, updatedAt INTEGER NOT NULL,
        completedAt INTEGER, finishedAt INTEGER, vw INTEGER NOT NULL, vh INTEGER NOT NULL,
        PRIMARY KEY(study,session));
CREATE TABLE IF NOT EXISTS study_task_sessions (
        study TEXT NOT NULL, session TEXT NOT NULL, startedAt INTEGER NOT NULL,
        vw INTEGER NOT NULL, vh INTEGER NOT NULL, PRIMARY KEY(study,session));
CREATE TABLE IF NOT EXISTS task_criteria_snapshots (
        study TEXT, session TEXT, taskId TEXT, description TEXT NOT NULL,
        verification TEXT NOT NULL, reviewedAt INTEGER, PRIMARY KEY(study,session,taskId));
CREATE TABLE IF NOT EXISTS visits (id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL,
        page TEXT NOT NULL, timestamp INTEGER NOT NULL, vw INTEGER NOT NULL, vh INTEGER NOT NULL, context TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS clicks_study_layout ON clicks(study,layout);
CREATE INDEX IF NOT EXISTS task_attempts_study ON study_task_attempts(study,session,ordinal);
CREATE INDEX IF NOT EXISTS visits_study_session ON visits(study,session,timestamp);
CREATE UNIQUE INDEX IF NOT EXISTS replay_frames_sequence ON replay_frames(study,session,seq);
CREATE INDEX IF NOT EXISTS live_findings_study ON live_findings(study);
CREATE INDEX IF NOT EXISTS live_reports_study ON live_reports(study);
CREATE INDEX IF NOT EXISTS recordings_session ON recordings(study,session,startedAt);
