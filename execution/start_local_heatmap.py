"""Start the local collector, UX-Lab and the supplied Lead Generation interface."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'integrations/Leed-generation'

def available(url):
    try:
        with urlopen(url,timeout=2) as response:
            return response.status==200
    except OSError:
        return False

def main():
    node=shutil.which('node') or str(Path(os.environ.get('ProgramFiles','C:/Program Files'))/'nodejs/node.exe')
    logs=ROOT/'.tmp/local-heatmap'
    logs.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'public/ux-lab-collector.js',TARGET/'public/ux-lab-collector.js')
    services=[('integration-pilot',ROOT,[sys.executable,'-X','utf8','execution/serve_integration_pilot.py'],'http://127.0.0.1:5176/health'),
        ('integration-demo',ROOT,[sys.executable,'-X','utf8','execution/serve_integration_demo.py'],'http://127.0.0.1:5177/'),
        ('collector',ROOT,[sys.executable,'-X','utf8','execution/serve_heatmap.py'],'http://127.0.0.1:5174/health'),
        ('dashboard',ROOT,[node,'node_modules/vite/bin/vite.js','--host','127.0.0.1','--port','5173','--strictPort'],'http://127.0.0.1:5173/'),
        ('leed',TARGET,[node,'node_modules/vite/bin/vite.js','--host','127.0.0.1','--port','5175','--strictPort'],'http://127.0.0.1:5175/')]
    for name,cwd,command,url in services:
        if not available(url):
            with (logs/f'{name}.log').open('ab') as log:
                process=subprocess.Popen(command,cwd=cwd,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            for _ in range(60):
                if available(url):break
                if process.poll() is not None:raise RuntimeError(f'{name} stopped; see {logs/name}.log')
                time.sleep(.5)
            else:raise RuntimeError(f'{name} did not respond; see {logs/name}.log')
        print(f'{name}: {url}',flush=True)
    print('Interface: http://127.0.0.1:5175/leads-table?ux_study=leed-local')
    print('Heatmap: http://127.0.0.1:5173/?screen=results-overview#/heatmap-live?link=leed-local')

if __name__=='__main__':main()
