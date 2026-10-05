"""Apply the initial cloud edition conversion only to vercel-app, leaving local code intact."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'vercel-app'


def replace(path, old, new):
    target = ROOT / path
    text = target.read_text(encoding='utf-8')
    if old not in text:
        raise ValueError(f'Missing expected source in {path}: {old[:70]}')
    target.write_text(text.replace(old, new), encoding='utf-8')


def main():
    marker = ROOT / '.cloud-edition-created'
    if marker.exists():
        raise SystemExit('Already adapted. Edit the cloud edition directly.')
    for base in (ROOT, ROOT / 'participant'):
        path = base / 'tsconfig.app.json'
        config = json.loads(re.sub(r'/\*.*?\*/', '', path.read_text(encoding='utf-8'), flags=re.S))
        config['include'] = ['src']
        path.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    replace('src/heatmap/types.ts', "export const CLICK_API='http://127.0.0.1:5174';", 'export const CLICK_API=location.origin;')
    replace('src/connections/api.ts', "export const API='http://127.0.0.1:5176';", 'export const API=location.origin;')
    replace('src/heatmap/CapturedHeatmap.tsx', 'http://127.0.0.1:5175 http://localhost:5175', "${location.origin}")
    replace('src/heatmap/CapturedHeatmap.tsx', 'policy.content="', 'policy.content=`')
    replace('src/heatmap/CapturedHeatmap.tsx', "base-uri 'none'\";", "base-uri 'none'`;")
    replace('src/heatmap/CapturedHeatmap.tsx', 'http://127.0.0.1:5175${group.path', '${location.origin}/participant${group.path')
    replace('src/heatmap/CapturedHeatmap.tsx', 'function inertDocument', 'export function inertDocument')
    replace('src/heatmap/LocalHeatmap.tsx', "location.port==='6006'?'http://127.0.0.1:5173':location.origin", 'location.origin')
    replace('src/heatmap/LocalHeatmap.tsx', "?'http://127.0.0.1:5175':origin", "?`${location.origin}/participant`:origin")
    replace('src/heatmap/LocalTarget.tsx', "['http://127.0.0.1:5173','http://localhost:5173','http://127.0.0.1:6006','http://localhost:6006']", '[location.origin]')
    # The unused demonstration workspace must not leak local URLs into a production bundle.
    replace('src/data/workspace.ts', 'http://127.0.0.1:5175/leads-table', '/participant/leads-table')
    for file in (ROOT / 'participant/src/ux-lab').glob('*'):
        if file.suffix not in ('.ts', '.tsx'):
            continue
        text = file.read_text(encoding='utf-8')
        text = text.replace('http://127.0.0.1:5174', '')
        text = text.replace('http://127.0.0.1:5173/#/', '/#/')
        text = text.replace("['localhost','127.0.0.1'].includes(location.hostname)", 'true')
        text = text.replace("['127.0.0.1','localhost'].includes(location.hostname)", 'true')
        text = text.replace("['http://127.0.0.1:5173','http://localhost:5173','http://127.0.0.1:6006','http://localhost:6006']", '[location.origin]')
        text = text.replace('location.pathname', "(location.pathname.replace(/^\\/participant(?=\\/|$)/,'')||'/')")
        # Cloud database chunks and all Vercel responses stay bounded.
        text = text.replace('4*1024*1024', '256*1024')
        text = text.replace('AbortSignal.timeout(2500)', 'AbortSignal.timeout(20000)').replace('AbortSignal.timeout(4000)', 'AbortSignal.timeout(20000)')
        file.write_text(text, encoding='utf-8')
    replace('participant/src/App.tsx', '<BrowserRouter>', '<BrowserRouter basename="/participant">')
    replace('participant/src/App.tsx', "&&['localhost','127.0.0.1'].includes(location.hostname)", '')
    replace('execution/live_project.py', "'http://127.0.0.1:5175/leads-table?ux_study=leed-local'", "'/participant/leads-table?ux_study=leed-local'")
    replacements = {
        'Локальное рабочее пространство': 'Облачное рабочее пространство',
        'Локально · Lead Generation': 'Lead Generation',
        'Запустите локальные серверы проекта.': 'Подключение недоступно. Повторите попытку после настройки сервера.',
        'Данные Lead Generation сохраняются на этом компьютере.': 'Данные исследования сохраняются в облачном хранилище.',
        'подключённая локальная версия': 'подключённый интерфейс',
        'локальный сборщик': 'облачный сборщик',
        'Сейчас тест доступен локально на этом компьютере.': 'Откройте ссылку на тест и войдите с паролем рабочего пространства.',
        'Сейчас это локальная ссылка: она работает только на этом компьютере. Для удалённых участников нужно разместить приложение и сборщик на доступном им сервере.': 'Передайте участнику ссылку и пароль рабочего пространства. В этой версии пароль даёт доступ и к дашборду.',
    }
    for file in (ROOT / 'src/live').glob('*.tsx'):
        text = file.read_text(encoding='utf-8')
        for old, new in replacements.items():
            text = text.replace(old, new)
        file.write_text(text, encoding='utf-8')
    replace('src/live/LiveViews.tsx', '<EuiLink href="/?screen=connections">Проверить подключение другого интерфейса</EuiLink>', '<p>Тестируемый интерфейс опубликован вместе с дашбордом.</p>')
    replace('src/live/api.ts', 'AbortSignal.timeout(10000)', 'AbortSignal.timeout(30000)')
    replace('src/live/api.ts', "if(!response.ok)throw Error(response.status===400?'Проверьте заполненные поля.':'Нет связи с локальным сервером. Данные сохранены; повторите попытку.');", "if(!response.ok){const failure=await response.json().catch(()=>({}));throw Error(failure.error||(response.status===400?'Проверьте заполненные поля.':'Нет связи с сервером. Повторите попытку.'));}")
    # Remove the local-only connection sandbox from the production entry point.
    replace('src/main.tsx', "import { ConnectionPilot } from './connections/ConnectionPilot';", '')
    replace('src/main.tsx', 'screen===\'connections\'?<ThemeFrame mode="light" scale="medium" product><ConnectionPilot/></ThemeFrame>:', '')
    for base in (ROOT, ROOT / 'participant'):
        (base / 'src/main.tsx').rename(base / 'src/bootstrap.tsx')
        (base / 'src/main.tsx').write_text("import {ensureAccess} from './cloud/access';\nvoid ensureAccess().then(()=>import('./bootstrap'));\n", encoding='utf-8')
    package = json.loads((ROOT / 'package.json').read_text(encoding='utf-8'))
    package['name'] = 'ux-lab-vercel'
    package['scripts']['build'] = 'node execution/build.mjs'
    package['dependencies'].update({'html-to-image': '1.11.13', 'fflate': '0.8.2'})
    (ROOT / 'package.json').write_text(json.dumps(package, indent=2) + '\n', encoding='utf-8')
    marker.write_text('Standalone Vercel edition, created 2026-10-05.\n', encoding='utf-8')
    # Generate a clean schema and default configuration, never copying the user's history.
    sys.path.insert(0, str(ROOT / 'execution'))
    import sqlite3
    import serve_heatmap
    import live_project
    import session_video
    db = sqlite3.connect(':memory:')
    db.row_factory = sqlite3.Row
    source = (ROOT / 'execution/serve_heatmap.py').read_text(encoding='utf-8')
    schema = re.search(r"db\.executescript\('''(.*?)'''\)", source, re.S)[1]
    db.executescript(schema)
    db.execute("ALTER TABLE clicks ADD COLUMN context TEXT NOT NULL DEFAULT ''")
    live_project.initialize(db)
    session_video.initialize(db)
    db.execute('CREATE TABLE cloud_schema (version INTEGER PRIMARY KEY)')
    db.execute('INSERT INTO cloud_schema VALUES (1)')
    lines = [line for line in db.iterdump() if line not in ('BEGIN TRANSACTION;', 'COMMIT;')]
    lines = [line.replace('CREATE TABLE ', 'CREATE TABLE IF NOT EXISTS ').replace('CREATE INDEX ', 'CREATE INDEX IF NOT EXISTS ').replace('CREATE UNIQUE INDEX ', 'CREATE UNIQUE INDEX IF NOT EXISTS ').replace('INSERT INTO ', 'INSERT OR IGNORE INTO ') for line in lines]
    (ROOT / 'execution/schema.sql').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    db.close()
    print('Cloud URLs, participant routes, bounded uploads, schema and cloud wording prepared.')


if __name__ == '__main__':
    main()
