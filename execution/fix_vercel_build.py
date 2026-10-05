"""Correct isolated edition build dependencies and EUI link event typing."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'vercel-app'
(DEST / 'ds').mkdir(exist_ok=True)
(DEST / 'ds/icon-source-map.json').write_bytes((ROOT / 'ds/icon-source-map.json').read_bytes())
file = DEST / 'src/live/SessionVideo.tsx'
text = file.read_text(encoding='utf-8')
text = text.replace('<EuiLink onClick={event=>', "<EuiLink onClick={(event:import('react').MouseEvent<HTMLAnchorElement>)=>")
file.write_text(text, encoding='utf-8')
for name in ('src/cloud/access.css', 'participant/src/cloud/access.css'):
    file = DEST / name
    text = file.read_text(encoding='utf-8').replace('--surface-default', '--background-canvas').replace('--space-600,24px', '--size-large,24px').replace('--space-300,12px', '--size-medium,12px').replace('--space-200,8px', '--size-small,8px').replace('--radius-control,8px', '--radius-medium,8px').replace('--text-danger,#b32232', '--status-error-text,#b32232')
    file.write_text(text, encoding='utf-8')
