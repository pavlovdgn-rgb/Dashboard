"""Rename the product without changing generic references to UX testing."""
import argparse,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CODE=r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('PAGE_ID'));
const changed=[];
if(figma.currentPage.name.includes('UX Research')){figma.currentPage.name=figma.currentPage.name.replaceAll('UX Research','UX-Lab');changed.push(figma.currentPage.id);}
for(const n of figma.currentPage.findAllWithCriteria({types:['TEXT']})){
 if(n.characters!=='UX-тесты'&&!n.characters.includes('UX Research'))continue;
 let inside=false;for(let p=n.parent;p&&p.type!=='PAGE';p=p.parent)if(p.type==='INSTANCE')inside=true;
 if(inside)continue;
 for(const s of n.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);
 n.characters=n.characters==='UX-тесты'?'UX-Lab':n.characters.replaceAll('UX Research','UX-Lab');changed.push(n.id);
}
if(figma.currentPage.id==='82:3')for(const c of await figma.variables.getLocalVariableCollectionsAsync())if(c.name.includes('UX Research')){c.name=c.name.replaceAll('UX Research','UX-Lab');changed.push(c.id);}
return {page:figma.currentPage.id,mutatedNodeIds:changed};
'''

def local():
    changed=[]
    for base in ['ds','ia','prompts','execution','directives']:
        for p in (ROOT/base).rglob('*'):
            if p.suffix not in ['.md','.json','.py','.mmd'] or '__pycache__' in p.parts or p.name=='rename_ux_lab.py':continue
            t=p.read_text(encoding='utf-8-sig');new=t.replace('UX Research','UX-Lab')
            for a,b in [("'UX-тесты'","'UX-Lab'"),('"UX-тесты"','"UX-Lab"'),('«UX-тесты»','«UX-Lab»')]:new=new.replace(a,b)
            if new!=t:p.write_text(new,encoding='utf8');changed.append(str(p.relative_to(ROOT)))
    p=ROOT/'ds/source.md';t=p.read_text(encoding='utf8');mark='<!-- product-name-ux-lab -->'
    if mark not in t:p.write_text(t.rstrip()+'\n\n'+mark+'\n## Название продукта\n\nПользователь утвердил **UX-Lab**. Это имя интерфейса, React-проекта и демонстрационной страницы. Обычные упоминания UX-тестов как вида исследования сохраняются. NOVA — имя отдельного тестируемого магазина.\n',encoding='utf8')
    print(json.dumps({'changed':changed},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['figma','local']);p.add_argument('--page');a=p.parse_args()
    if a.stage=='local':local()
    else:
        if a.page not in ['8:2','20:2','67:2','82:3','191:847']:raise SystemExit('Unexpected page')
        print(json.dumps({'code':CODE.replace('PAGE_ID',a.page)},ensure_ascii=False))
