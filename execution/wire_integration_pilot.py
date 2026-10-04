"""Idempotently wire the isolated pilot and shared SDK into existing entry points."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def replace(path, old, new):
    file=ROOT/path;text=file.read_text(encoding='utf-8')
    if new in text:return
    if old not in text:raise RuntimeError(f'Expected anchor missing: {path}')
    file.write_text(text.replace(old,new,1),encoding='utf-8')


def main():
    replace('src/main.tsx',"import { ThemeFrame } from './storybook/ThemeFrame';", "import { ThemeFrame } from './storybook/ThemeFrame';\nimport { ConnectionPilot } from './connections/ConnectionPilot';")
    replace('src/main.tsx',".render(screen==='heatmap-export'?", ".render(screen==='connections'?<ThemeFrame mode=\"light\" scale=\"medium\" product><ConnectionPilot/></ThemeFrame>:screen==='heatmap-export'?")
    replace('src/live/LiveViews.tsx','<p className={w.muted}>{data.project.url}</p></Card>', '<p className={w.muted}>{data.project.url}</p><EuiLink href=\"/?screen=connections\">Проверить подключение другого интерфейса</EuiLink></Card>')
    replace('execution/serve_heatmap.py',"            if path.path == '/collector.js':", "            if path.path == '/sdk.js':\n                source='\\n'.join((ROOT/'public'/name).read_text(encoding='utf-8') for name in ('ux-lab-collector.js','ux-lab-sdk-bootstrap.js'))\n                return self.reply(200,source,'application/javascript; charset=utf-8')\n            if path.path == '/collector.js':")
    replace('integrations/Leed-generation/src/ux-lab/install.ts',"script.src='/ux-lab-collector.js'", "script.src='http://127.0.0.1:5174/sdk.js'")
    replace('execution/start_local_heatmap.py',"    services=[('collector'", "    services=[('integration-pilot',ROOT,[sys.executable,'-X','utf8','execution/serve_integration_pilot.py'],'http://127.0.0.1:5176/health'),\n        ('collector'")
    print('Integration pilot entry points wired.')


if __name__=='__main__':main()
