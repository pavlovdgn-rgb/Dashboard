"""Generate token layers and typed component facades from the scanned Figma data.

Execution is deterministic and never changes Figma. Hand-written renderers live
in src/components/_shared and are deliberately not overwritten here.
"""
from pathlib import Path
import json
import re
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
TMP = ROOT / '.tmp/react-base'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def js(value):
    return json.dumps(value, ensure_ascii=False)

def main():
    data = read(ROOT / 'ds/index.json')
    product = read(TMP / 'product-tokens.json')
    external = sum([read(p) for p in sorted(TMP.glob('external-*.json'))], [])
    variables = data['variables'] + product['variables'] + external
    by_id = {v['id']: v for v in variables}
    names = {}
    used = set()
    for v in variables:
        # Elastic Text/Primary is blue, product text/primary is graphite. Keep
        # distinct namespaces instead of silently aliasing those two meanings.
        prefix = 'external-' if v in external else 'elastic-' if v in data['variables'] and v['type']=='COLOR' else ''
        name = '--' + prefix + slug(v['name'])
        if name in used:
            name += '-' + hashlib.sha1(v['id'].encode()).hexdigest()[:6]
        used.add(name)
        names[v['id']] = name
    collections = data['collections'] + product['collections']
    coll_by_id = {c['id']: c for c in collections}
    primitives = [':root {']
    semantic = [':root {']
    modifiers = {}
    token_rows = []

    def literal(value, variable):
        if isinstance(value, dict):
            rgba = [round(value[k] * 255) for k in 'rgb']
            return '#'+''.join(f'{x:02x}' for x in rgba) if value.get('a', 1) == 1 else f"rgb({' '.join(map(str,rgba))} / {value.get('a',1):.5g})"
        if isinstance(value, bool):
            return '1' if value else '0'
        if isinstance(value, (int, float)):
            suffix = '' if 'weight' in variable['name'].lower() else 'px'
            return f'{value:.6g}{suffix}'
        return js(value)

    def resolve(v, position=0, seen=None):
        seen = set() if seen is None else seen
        if v['id'] in seen:
            raise ValueError('Cyclic alias '+v['id'])
        seen.add(v['id'])
        vals = list(v['values'].values())
        value = vals[min(position, len(vals)-1)]
        if isinstance(value, dict) and value.get('type') == 'VARIABLE_ALIAS':
            return resolve(by_id[value['id']], position, seen)
        return literal(value, v)

    for v in variables:
        collection = coll_by_id.get(v.get('collectionId', v.get('collection')))
        mode_list = collection['modes'] if collection else [{'modeId': k, 'name': 'Light' if i==0 else 'Dark'} for i,k in enumerate(v['values'])]
        values = {}
        for i, mode in enumerate(mode_list):
            if mode['modeId'] not in v['values']:
                continue
            value = v['values'][mode['modeId']]
            if isinstance(value, dict) and value.get('type') == 'VARIABLE_ALIAS':
                if value['id'] not in names:
                    raise ValueError('Unresolved variable alias '+value['id'])
                ref = names[value['id']]
            else:
                ref = '--primitive-' + slug(v['id']) + '-' + str(i)
                primitives.append(f'  {ref}: {literal(value, v)};')
            decl = f"  {names[v['id']]}: var({ref});"
            values[mode['name']] = resolve(v, i)
            if i == 0:
                semantic.append(decl)
            else:
                attr = 'color-mode' if mode['name']=='Dark' else ('type-scale' if collection and collection['name']=='Typographic scale' else 'data-mode')
                modifiers.setdefault(f'[data-{attr}="{slug(mode["name"])}"]', []).append(decl)
        token_rows.append({'id':v['id'],'name':v['name'],'css':names[v['id']],'type':v['type'],'external':v in external,'collection':collection['name'].replace('UX Research','UX-Lab') if collection else 'External primitives','values':values})
    primitives += ['  --font-sans: Inter, sans-serif;', '}']
    semantic += ['}']
    for selector, lines in modifiers.items():
        semantic += [selector+' {', *lines, '}']
    styles = []
    typography = []
    for i, style in enumerate(data['textStyles']):
        cls = 'ds-text-' + slug(style['name'])
        bound = style.get('boundVariables', {})
        declarations = []
        for prop, field, fallback in [('font-family','fontFamily',js(style['font']['family'])),('font-size','fontSize',f"{style['size']:.6g}px"),('line-height','lineHeight',str(style['lineHeight'].get('value',100))+('px' if style['lineHeight']['unit']=='PIXELS' else '%')),('font-weight','fontWeight',str(style['font'].get('variationSettings',{}).get('wght',400)))]:
            if field in bound:
                value = 'var('+names[bound[field]['id']]+')'
            else:
                primitive = '--primitive-style-'+str(i)+'-'+prop
                primitives.insert(-1, f'  {primitive}: {fallback};')
                value = 'var('+primitive+')'
            declarations.append(f'{prop}: {value};')
        if 'Italic' in style['font']['style']:
            declarations.append('font-style: italic;')
        tracking = style.get('letterSpacing', {'unit':'PIXELS','value':0})
        if 'letterSpacing' in bound:
            declarations.append('letter-spacing: var('+names[bound['letterSpacing']['id']]+');')
        else:
            tracking_value = str(tracking['value'])+'px' if tracking['unit']=='PIXELS' else str(tracking['value']/100)+'em'
            tracking_token = '--primitive-style-'+str(i)+'-letter-spacing'
            primitives.insert(-1, f'  {tracking_token}: {tracking_value};')
            declarations.append(f'letter-spacing: var({tracking_token});')
        if 'underline' in style['name'].lower():
            declarations.append('text-decoration: underline;')
        typography.append('.'+cls+' { '+' '.join(declarations)+' }')
        styles.append({'name':style['name'],'className':cls,'id':style['id']})
    write(SRC/'tokens/primitives.css', '\n'.join(primitives)+'\n')
    write(SRC/'tokens/semantics.css', '\n'.join(semantic)+'\n')
    write(SRC/'tokens/typography.css', '\n'.join(typography)+'\n')
    write(SRC/'tokens/manifest.json', js({'tokens':token_rows,'textStyles':styles})+'\n')
    product_theme = {v['name']: resolve(v) for v in product['variables']}
    write(SRC/'tokens/product-theme.json', js(product_theme)+'\n')

    matrix = {c['id']: c for p in TMP.glob('matrix-*.json') for c in read(p)}
    products = sum([read(TMP/f'products-{i}.json') for i in range(3)], [])
    catalog = []
    exports = []
    imports = []
    registry = []
    used_names = set()
    for i, c in enumerate(data['components'] + products):
        name = ''.join(x[:1].upper()+x[1:] for x in re.findall(r'[a-zA-Z0-9]+', c['name']))
        if name[0].isdigit():
            name = 'Component'+name
        if name in used_names:
            name += 'Node'+c['id'].replace(':','_')
        used_names.add(name)
        props = c.get('properties') or {}
        default = {k:p.get('defaultValue') for k,p in props.items() if p.get('type')!='INSTANCE_SWAP'}
        if i < len(data['components']):
            m = matrix[c['id']]
            variants = [{k:props[k]['variantOptions'][row[j]] for j,k in enumerate(m['keys'])} for row in m['matrix']]
            if any(n<0 for row in m['matrix'] for n in row):
                raise ValueError('Invalid variant index '+c['id'])
            source = 'elastic'
        else:
            variants = [v.get('props', {}) for v in c['variants']]
            source = 'product'
        entry = {'id':c['id'],'name':c['name'],'exportName':name,'source':source,'sourceIndex':i if source=='elastic' else i-len(data['components']),'defaults':default,'properties':props,'variants':variants or [{}],'deprecated':'☠' in c['name'],'description':c.get('description','')}
        catalog.append(entry)
        fields = []
        for k,p in props.items():
            t = ' | '.join(js(o) for o in p['variantOptions']) if p['type']=='VARIANT' else 'boolean' if p['type']=='BOOLEAN' else 'string'
            fields.append('  '+js(k)+'?: '+t+';')
        content = "import { CatalogComponent, type CatalogProps } from '../_shared/CatalogComponent';\nimport styles from './"+name+".module.css';\nexport type "+name+"Props = CatalogProps & {\n"+'\n'.join(fields)+"\n};\nexport function "+name+"(props: "+name+"Props) { return <CatalogComponent catalogId="+js(c['id'])+" {...props} className={[styles.root, props.className].filter(Boolean).join(' ')} />; }\n"
        write(SRC/f'components/{name}/{name}.tsx', content)
        write(SRC/f'components/{name}/{name}.module.css', '.root { min-inline-size: 0; max-inline-size: 100%; }\n')
        write(SRC/f'components/{name}/index.ts', f"export {{ {name} }} from './{name}';\nexport type {{ {name}Props }} from './{name}';\n")
        exports.append(f"export * from './{name}';")
        imports.append(f"import {{ {name} }} from './{name}';")
        registry.append(js(c['id'])+': '+name)
    write(SRC/'components/index.ts', '\n'.join(exports)+'\n')
    write(SRC/'components/registry.ts', '\n'.join(imports)+'\nexport const registry = {\n'+',\n'.join(registry)+'\n};\n')
    write(SRC/'components/catalog.json', js(catalog)+'\n')
    write(ROOT/'ds/react-name-map.json', json.dumps([{'id':c['id'],'figma':c['name'],'react':c['exportName']} for c in catalog],ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'components':len(catalog),'variants':sum(len(c['variants']) for c in catalog),'tokens':len(token_rows),'textStyles':len(styles)}))

if __name__ == '__main__':
    main()
