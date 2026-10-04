"""Isolated comparison of secondary button treatments; no master restyling."""
import json
import sys
from grow_ui_kit import COMMON

START=COMMON+r'''
await figma.setCurrentPageAsync(page);
const NAME='Secondary contrast — comparison 2026-09-23';
const radius=await figma.variables.getVariableByIdAsync('VariableID:202:3805');
function largeRadius(n){for(const p of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])n.setBoundVariable(p,radius);}
'''
BOARD=r'''
let board=page.children.find(n=>n.name===NAME);if(board)return {boardId:board.id,existing:true};
board=frame(NAME,page,'VERTICAL',1976,'lg');board.x=16800;board.y=80;spacing(board,'lg','lg');fill(board,'background/canvas');largeRadius(board);
const h=await figma.importStyleByKeyAsync('a0fb5401c910ccd1871625995412cdd09c8f0c3b');await figma.loadFontAsync(h.fontName);styles.heading=h;
await text(board,'Title','Secondary — сравнение контрастности','heading');
await text(board,'Description','Выбран A без обводки; применён к Secondary на страницах продукта. D — прежний стиль для сравнения.','body','text/secondary');
const cols=frame('Options',board,'HORIZONTAL',1928);spacing(cols,'lg');cols.counterAxisAlignItems='MIN';
await text(board,'Decision','A — принят без контура. B и C сохранены для сравнения.','small','text/secondary');
return {boardId:board.id,createdNodeIds:created};
'''
COLUMN=r'''
const board=page.children.find(n=>n.name===NAME);const cols=board.findOne(n=>n.name==='Options');
const config=CONFIG;let card=cols.children.find(n=>n.name===config.key);if(card)return {columnId:card.id,existing:true};
card=frame(config.key,cols,'VERTICAL',464,'base');spacing(card,'base','base');fill(card,'background/surface');largeRadius(card);card.strokes=[paint('border/subtle')];card.strokesIncludedInLayout=false;
await text(card,'OptionTitle',config.title,'medium');const desc=await text(card,'OptionDescription',config.description,'small','text/secondary');desc.textAutoResize='NONE';desc.resize(432,72);
return {columnId:card.id,createdNodeIds:created};
'''
SAMPLES=r'''
const board=page.children.find(n=>n.name===NAME);const config=CONFIG;const card=board.findOne(n=>n.name===config.key);
const master=await figma.getNodeByIdAsync('125:319');
for(const [label,color]of [['Белая карточка','background/surface'],['Фон страницы','background/canvas'],['Выбранная строка','accent/soft']]){
 if(card.children.some(n=>n.name===label))continue;
 const context=frame(label,card,'VERTICAL',432,'base');spacing(context,'base','base');fill(context,color);largeRadius(context);
 await text(context,'SurfaceLabel',label,'small','text/secondary');
 const button=master.createInstance();created.push(button.id);context.appendChild(button);button.name='Участники и записи';await fonts(button);button.resize(320,40);button.fills=[];
 const control=button.children.find(n=>n.type==='INSTANCE'&&n.name==='Control');control.setProperties({'Text#30956:4':'Участники и записи','Icon left#30956:3':false,'Icon right#30956:5':false});
 if(!config.current){control.fills=config.fill?[paint(config.fill)]:[];control.strokes=config.border?[paint(config.border)]:[];control.strokeWeight=1;control.strokeAlign='INSIDE';for(const t of control.findAllWithCriteria({types:['TEXT']}))fill(t,'text/primary');}
}
return {columnId:card.id,createdNodeIds:[...new Set(created.concat(card.findAll().map(n=>n.id)))]};
'''
CONFIGS=[dict(key='A',title='A · Выбран — без контура',description='Принят: тёплая серая заливка без контура.',fill='border/subtle',border=None),dict(key='B',title='B · Только контур',description='Прозрачный фон и серая граница. Самый лёгкий по заливке вариант.',fill=None,border='border/control'),dict(key='C',title='C · Оливковый фон',description='Оливковая заливка и контур. Сильнее использует цвет продукта, но близок к выделению.',fill='accent/soft',border='accent/strong')]
CONFIGS.append(dict(key='D',title='D · Прежний стиль',description='Прежний стиль: очень светлый тёплый серый фон без контура.',fill='background/sidebar',border=None))
EXPAND=r'''
const board=page.children.find(n=>n.name===NAME);await fonts(board);const cols=board.findOne(n=>n.name==='Options');
board.resize(1976,board.height);cols.resize(1928,cols.height);
const desc=board.findOne(n=>n.name==='Description');desc.characters='Выбран A без обводки; применён к Secondary на страницах продукта. D — прежний стиль для сравнения.';
const note=board.findOne(n=>n.name==='Decision');note.characters='A — принят без контура. B/C/D сохранены для сравнения.';
return {boardId:board.id,mutatedNodeIds:[board.id,cols.id,desc.id,note.id]};
'''
if __name__=='__main__':
    stage=sys.argv[1]
    code=BOARD if stage=='board' else EXPAND if stage=='expand' else (COLUMN if stage=='column' else SAMPLES).replace('CONFIG',json.dumps(CONFIGS[int(sys.argv[2])],ensure_ascii=False))
    print(json.dumps({'code':START+code},ensure_ascii=False))
