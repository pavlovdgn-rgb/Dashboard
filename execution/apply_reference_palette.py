"""Prepare a reproducible color-only Figma preview; preserve wireframe geometry."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    "background/canvas": "#F7F7F2",
    "background/surface": "#FFFFFF",
    "background/sidebar": "#F3F3EE",
    "background/subtle": "#FAFAF7",
    "border/subtle": "#E4E5DC",
    "border/control": "#85877A",
    "text/primary": "#22241F",
    "text/secondary": "#66695F",
    "text/inverse": "#FFFFFF",
    "action/primary": "#20221E",
    "accent/soft": "#ECEEDC",
    "accent/strong": "#626E32",
    "status/success/background": "#E8F4EC",
    "status/success/text": "#236744",
    "status/warning/background": "#FFF3DC",
    "status/warning/text": "#805619",
    "status/error/background": "#FBEAEA",
    "status/error/text": "#A13737",
    "status/info/background": "#EAF0FC",
    "status/info/text": "#385DA2",
}

JS = r'''
const palette = __PALETTE__;
const page = figma.createPage(); page.name = 'UX-Lab · Palette preview';
await figma.setCurrentPageAsync(page);
const source = await figma.getNodeByIdAsync('22:3');
for (const t of source.findAllWithCriteria({types:['TEXT']})) {
  for (const seg of t.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(seg.fontName);
}
const preview=source.clone(); page.appendChild(preview); preview.x=80;preview.y=80;
preview.name='ResultsOverview · Warm olive · Color preview';
const collection=figma.variables.createVariableCollection('UX-Lab · Reference palette');
collection.renameMode(collection.modes[0].modeId,'Light');
const vars={};
function rgb(h){return {r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255};}
for(const [name,hex] of Object.entries(palette)){
 const v=figma.variables.createVariable(name,collection,'COLOR');
 v.scopes=name.includes('text/')||name.endsWith('/text')?['TEXT_FILL']:name.startsWith('border/')?['STROKE_COLOR']:['FRAME_FILL','SHAPE_FILL'];
 v.setValueForMode(collection.modes[0].modeId,rgb(hex));
 v.setVariableCodeSyntax('WEB','var(--ux-'+name.replaceAll('/','-')+')');vars[name]=v;
}
function paint(key){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:rgb(palette[key])},'color',vars[key]);}
function fill(n,key){n.fills=[paint(key)];}
function stroke(n,key){if(n.strokes.length===0 && 'strokesIncludedInLayout' in n)n.strokesIncludedInLayout=false;n.strokes=[paint(key)];}
const all=[preview,...preview.findAll()];
for(const n of all){
 if(n.type==='TEXT') fill(n,n.fontSize<=15?'text/secondary':'text/primary');
 else if('strokes' in n&&n.strokes.length) stroke(n,'border/subtle');
}
fill(preview,'background/canvas');
for(const n of all.filter(x=>x.type==='FRAME')){
 if(n.name==='Header')fill(n,'background/surface');
 if(n.name==='Sidebar')fill(n,'background/sidebar');
 if(n.name==='Metric'){fill(n,'background/surface');stroke(n,'border/subtle');}
 if(n.name==='ScenariosTable'){fill(n,'background/surface');stroke(n,'border/subtle');}
 if(n.name==='TableHeader')fill(n,'background/subtle');
 if(n.name==='TableRow1')fill(n,'accent/soft');
 if(n.name==='NavigationItem'&&n.findAllWithCriteria({types:['TEXT']}).some(t=>t.characters.includes('Обзор результатов')))fill(n,'accent/soft');
 if(n.name==='Action'){
  const ts=n.findAllWithCriteria({types:['TEXT']});
  const primary=ts.some(t=>t.characters==='Экспорт в PDF');
  fill(n,primary?'action/primary':'background/surface');stroke(n,primary?'action/primary':'border/control');
  for(const t of ts)fill(t,primary?'text/inverse':'text/primary');
 }
}
for(const n of all.filter(x=>x.type==='TEXT')){
 if(n.characters==='Выбран'||n.characters==='Выбрать сценарий'||n.characters==='Посмотреть участников')fill(n,'accent/strong');
 if(n.characters==='2 из 20')fill(n,'status/warning/text');
}
figma.viewport.scrollAndZoomIntoView([preview]);
return {pageId:page.id,frameId:preview.id,collectionId:collection.id,variables:Object.fromEntries(Object.entries(vars).map(([k,v])=>[k,v.id])),createdNodeIds:[page.id,...all.map(n=>n.id)],sourceUnchanged:'22:3',geometry:'unchanged'};
'''


def main():
    if '--record' in sys.argv:
        delivery = {
            'fileKey': '1LeVoicxDT7Sl8TpMPs4hr', 'pageId': '67:2',
            'frameId': '67:3', 'sourceFrameId': '22:3',
            'collectionId': 'VariableCollectionId:67:106',
            'variableCount': 20, 'size': [1920, 1080],
            'scope': 'Color-only preview of existing wireframe; not final DS composition',
            'url': 'https://www.figma.com/design/1LeVoicxDT7Sl8TpMPs4hr/Dashboard?node-id=67-3',
        }
        (ROOT / 'ds' / 'palette-preview-delivery.json').write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        def luminance(h):
            channels = [int(h[i:i+2], 16)/255 for i in (1, 3, 5)]
            linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in channels]
            return sum(v*w for v,w in zip(linear, (.2126,.7152,.0722)))
        results = {}
        for foreground, background in [
            ('text/primary','background/canvas'),
            ('text/secondary','background/surface'),
            ('text/secondary','background/canvas'),
            ('text/inverse','action/primary'),
            ('accent/strong','accent/soft'),
            ('status/warning/text','background/surface'),
        ]:
            a,b = sorted([luminance(COLORS[foreground]),luminance(COLORS[background])])
            ratio=(b+.05)/(a+.05)
            assert ratio>=4.5, (foreground,background,ratio)
            results[foreground+' on '+background]=round(ratio,2)
        print(json.dumps({'recorded': True, 'textContrastRatios': results}))
        return
    out = ROOT / '.tmp' / 'reference-palette'
    out.mkdir(parents=True, exist_ok=True)
    script = JS.replace('__PALETTE__', json.dumps(COLORS, ensure_ascii=False))
    (out / 'apply.js').write_text(script, encoding='utf-8')
    (ROOT / 'ds' / 'product-palette.json').write_text(json.dumps({
        'status': 'Reference direction chosen; exact hex values are a proposed interpretation',
        'scope': 'Color only; no reference spacing, radius or typography adoption',
        'colors': COLORS,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    rows = '\n'.join(f'| `{k}` | `{v}` |' for k,v in COLORS.items())
    doc = '''# Палитра продукта

Пользователь выбрал цветовое направление приложенного референса Modsley: тёплая светлая основа, белые поверхности, графитовые текст и основные кнопки, приглушённый оливковый акцент. Отступы, радиусы, размеры и шрифты референса копировать не требуется: геометрия будущего UI определяется Elastic UI и задачами продукта.

Точные HEX ниже — предложенная интерпретация изображения, а не извлечённые исходные токены референса. Цветовой preview применён к копии существующего wireframe ResultsOverview без изменения его геометрии. Это примерка цветов, а не завершённая сборка экрана из компонентов Elastic UI. Исходный wireframe и файл библиотеки не перекрашиваются.

| Смысловой токен | HEX |
| --- | --- |
''' + rows + '''

Цвета статусов применяются по смыслу вместе с текстовой подписью. Оливковое выделение обозначает выбор и акцент; светлый оливковый не используется для мелкого текста. Тепловая карта кликов остаётся отдельным результатом исследования и требует отдельной последовательной шкалы интенсивности; её шкала этим решением не утверждается.

Источник библиотечных значений сохраняется в foundation.md и index.json; product-palette.json — отдельный слой цветов продукта. Данные реального применения в Figma сохраняются в palette-preview-delivery.json.
'''
    (ROOT / 'ds' / 'product-palette.md').write_text(doc, encoding='utf-8')
    print(json.dumps({'code': script}, ensure_ascii=False))


if __name__ == '__main__':
    main()
