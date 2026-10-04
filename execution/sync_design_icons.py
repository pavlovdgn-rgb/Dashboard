"""Register original EUI SVG components locally, preserving their source artwork."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'node_modules/@elastic/eui/es/components/icon/icon_map.js'
pairs=re.findall(r"^\s+(\w+): '([^']+)'",source.read_text(encoding='utf-8'),re.M)
lines=["// Original Elastic UI assets; no substitutes or dynamic remote imports.","import { appendIconComponentCache } from '@elastic/eui/es/components/icon/icon';"]
for i,(_,filename) in enumerate(pairs):
    lines.append(f"import {{ icon as Icon{i} }} from '@elastic/eui/es/components/icon/assets/{filename}';")
lines.append('appendIconComponentCache({'+','.join(f'{name}:Icon{i}' for i,(name,_) in enumerate(pairs))+'});')
(ROOT/'src/icons.tsx').write_text('\n'.join(lines)+'\n',encoding='utf-8')
# IconPlaceholder was an explicit React Base temporary slot. All calls now use
# the original library component, with semantic overrides at product callsites.
for p in (ROOT/'src/components/_shared').glob('*.tsx'):
    s=p.read_text(encoding='utf-8').replace('IconPlaceholder','DesignIcon')
    p.write_text(s,encoding='utf-8')
print(json.dumps({'registeredOriginalEuiIcons':len(pairs)}))
