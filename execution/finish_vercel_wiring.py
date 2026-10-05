"""Initial one-time wiring of cloud login, browser exports and bundled PDF fonts."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1] / 'vercel-app'


def edit(name, old, new):
    file = ROOT / name
    text = file.read_text(encoding='utf-8')
    if old not in text:
        raise ValueError(f'Missing source in {name}')
    file.write_text(text.replace(old, new), encoding='utf-8')


def main():
    access = ROOT / 'participant/src/cloud'
    access.mkdir(exist_ok=True)
    for name in ('access.ts', 'access.css'):
        (access / name).write_bytes((ROOT / 'src/cloud' / name).read_bytes())
    for folder, imports in [('src', "import './fonts';\nimport './tokens/primitives.css';\nimport './tokens/semantics.css';\nimport './global.css';\n"), ('participant/src', "import './index.css';\n")]:
        main_file = ROOT / folder / 'main.tsx'
        main_file.write_text(imports + "import './cloud/access.css';\n" + main_file.read_text(encoding='utf-8'), encoding='utf-8')
    file = ROOT / 'src/heatmap/LocalHeatmap.tsx'
    text = file.read_text(encoding='utf-8')
    first = text.index('      const response=await fetch(`${CLICK_API}/api/heatmap/export?')
    end = text.index('      const link=document.createElement', first)
    text = text[:first] + "      const {exportHeatmap}=await import('../cloud/exportHeatmap');\n      const url=URL.createObjectURL(await exportHeatmap(params));\n" + text[end:]
    file.write_text(text, encoding='utf-8')
    file = ROOT / 'src/live/SessionVideo.tsx'
    text = file.read_text(encoding='utf-8')
    text = "import {downloadVideo} from '../cloud/downloadVideo';\n" + text
    text = text.replace('<EuiLink href={`${CLICK_API}/api/recordings/media?', '<EuiLink onClick={event=>{event.preventDefault();void downloadVideo(event.currentTarget.href).catch(cause=>setError(cause instanceof Error?cause.message:\'Не удалось скачать запись.\'));}} href={`${CLICK_API}/api/recordings/media?')
    file.write_text(text, encoding='utf-8')
    edit('execution/project_reports.py', "Path('C:/Windows/Fonts/arial.ttf')", "Path(__file__).with_name('fonts')/'NotoSans-Regular.ttf'")
    edit('execution/project_reports.py', "Path('C:/Windows/Fonts/arialbd.ttf')", "Path(__file__).with_name('fonts')/'NotoSans-Bold.ttf'")
    config_file = ROOT / 'vercel.json'
    config = json.loads(config_file.read_text())
    config['functions']['api/index.py']['includeFiles'] = '{execution/**,public/**}'
    for route in config['rewrites'][:3]:
        route['destination'] += '?__path=' + route['source']
    config_file.write_text(json.dumps(config, indent=2) + '\n')
    print('Login, exports, video download, fonts and function routes wired.')


if __name__ == '__main__':
    main()
