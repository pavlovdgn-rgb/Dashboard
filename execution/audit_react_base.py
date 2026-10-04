"""Verify generated coverage and CSS token references without changing the DS."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'src/components/catalog.json').read_text(encoding='utf-8'))
manifest = json.loads((ROOT / 'src/tokens/manifest.json').read_text(encoding='utf-8'))
css_files = list((ROOT / 'src').rglob('*.css'))
definitions = set()
for file in css_files:
    definitions.update(re.findall(r'(--[\w-]+)\s*:', file.read_text(encoding='utf-8')))
missing_tokens = {}
hardcoded_colors = {}
for file in css_files:
    text = file.read_text(encoding='utf-8')
    unknown = sorted(set(re.findall(r'var\((--[\w-]+)', text)) - definitions)
    if unknown:
        missing_tokens[str(file.relative_to(ROOT))] = unknown
    if 'tokens' not in file.parts:
        colors = re.findall(r'#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)', text)
        if colors:
            hardcoded_colors[str(file.relative_to(ROOT))] = colors

registry = (ROOT / 'src/components/registry.ts').read_text(encoding='utf-8')
missing_components = [entry['id'] for entry in catalog if entry['id'] not in registry]
result = {
    'components': len(catalog),
    'elastic': sum(entry['source'] == 'elastic' for entry in catalog),
    'product': sum(entry['source'] == 'product' for entry in catalog),
    'variants': sum(len(entry['variants']) for entry in catalog),
    'tokens': len(manifest['tokens']),
    'textStyles': len(manifest['textStyles']),
    'missingRegistryEntries': missing_components,
    'missingCssVariables': missing_tokens,
    'hardcodedComponentColors': hardcoded_colors,
    'scope': 'Registry and token checks; not pixel-level proof of every Figma variant.',
}
target = ROOT / '.tmp/react-base/structure-audit.json'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
raise SystemExit(bool(missing_components or missing_tokens or hardcoded_colors))
