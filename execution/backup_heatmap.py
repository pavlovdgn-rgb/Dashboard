"""Take a consistent SQLite backup before a local schema migration, including WAL data."""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'.local/heatmap.sqlite3'
destination=ROOT/'.tmp/local-heatmap'/('before-multi-study-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.sqlite3')
destination.parent.mkdir(parents=True,exist_ok=True)
with sqlite3.connect(source.as_uri()+'?mode=ro',uri=True) as db,sqlite3.connect(destination) as backup:
    db.backup(backup)
    counts={table:backup.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for table in ('clicks','visits','snapshots','replay_frames','recordings','live_findings','live_reports')}
    migrated=backup.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='live_studies'").fetchone()
    query="SELECT value FROM live_studies WHERE id='leed-local'" if migrated else "SELECT value FROM live_settings WHERE id='project'"
    config=json.loads(backup.execute(query).fetchone()[0])
    baseline={'backup':str(destination),'counts':counts,'config':config}
    (ROOT/'.tmp/multi-study-baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'backup':str(destination),'counts':counts},ensure_ascii=False))
