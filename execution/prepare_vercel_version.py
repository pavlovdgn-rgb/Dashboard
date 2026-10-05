"""Create an isolated, source-only Vercel edition once; never overwrite an edited edition."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'vercel-app'


def main():
    if DEST.exists():
        raise SystemExit('vercel-app already exists; edit it directly rather than overwrite it.')
    DEST.mkdir()
    ignored = shutil.ignore_patterns('node_modules', 'dist', '__pycache__', '*.tsbuildinfo', '*.stories.*')
    for name in ('src', 'public', 'assets'):
        shutil.copytree(ROOT / name, DEST / name, ignore=ignored)
    for name in ('package.json', 'package-lock.json', 'index.html', 'tsconfig.json', 'tsconfig.app.json', 'tsconfig.node.json'):
        shutil.copy2(ROOT / name, DEST / name)
    target = DEST / 'participant'
    target.mkdir()
    for name in ('src', 'public'):
        shutil.copytree(ROOT / 'integrations/Leed-generation' / name, target / name, ignore=ignored)
    for name in ('package.json', 'package-lock.json', 'index.html', 'tsconfig.json', 'tsconfig.app.json', 'tsconfig.node.json'):
        shutil.copy2(ROOT / 'integrations/Leed-generation' / name, target / name)
    execution = DEST / 'execution'
    execution.mkdir()
    for name in ('serve_heatmap.py', 'live_project.py', 'project_reports.py', 'session_video.py',
                 'study_tasks.py', 'study_task_plan.py', 'success_criteria.py', 'leed_page_labels.json'):
        shutil.copy2(ROOT / 'execution' / name, execution / name)
    for base in (DEST, target):
        config = json.loads(re.sub(r'/\*.*?\*/', '', (base / 'tsconfig.app.json').read_text(encoding='utf-8'), flags=re.S))
        config['include'] = ['src']
        config['exclude'] = ['src/storybook', 'src/**/*.stories.tsx']
        (base / 'tsconfig.app.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    print('Created vercel-app without credentials, local databases, node_modules or temporary files.')


if __name__ == '__main__':
    main()
