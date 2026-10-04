"""Create isolated comparison frames using product component instances and tokens."""
import json
from grow_ui_kit import COMMON
CODE=COMMON+r'''
await figma.setCurrentPageAsync(page);
const varsById=Object.fromEntries(Object.values(colors).map(v=>[v.id,v]));
function resolve(v){const value=Object.values(v.valuesByMode)[0];return value.type==='VARIABLE_ALIAS'?resolve(varsById[value.id]):value;}
function paint(key){const v=colors[key],x=resolve(v);return figma.variables.setBoundVariableForPaint({type:'SOLID',color:{r:x.r,g:x.g,b:x.b}},'color',v);}
const old=page.children.find(n=>n.name==='Secondary button — surface proposals');if(old)return {existingId:old.id};
const board=frame('Secondary button — surface proposals',page,'VERTICAL',1920,'lg');board.x=Math.max(...page.children.filter(n=>n.id!==board.id).map(n=>n.x+n.width))+100;board.y=80;fill(board,'background/canvas');spacing(board,'lg','lg');
const h=await figma.importStyleByKeyAsync('a0fb5401c910ccd1871625995412cdd09c8f0c3b');await figma.loadFontAsync(h.fontName);styles.heading=h;
await text(board,'Title','Secondary-кнопка — варианты подложки','heading');
await text(board,'Description','Сравнение на трёх поверхностях. Иконки и размеры одинаковые. Это предложения: основные компоненты пока сохраняют текущий стиль.','body','text/secondary');
const cols=frame('Options',board,'HORIZONTAL',1872);spacing(cols,'lg');cols.counterAxisAlignItems='MIN';
const bs=await figma.getNodeByIdAsync('125:450');const attempt=await figma.getNodeByIdAsync('152:981');
const options=[['A · Плотный серый','Мягкий вариант без контура. Заметнее текущего, но граница на оливковом фоне остаётся слабой.','border/subtle',null],['B · Серый + контур','Рекомендую: границы кнопки различимы на всех трёх фонах, а primary сохраняет главный акцент.','background/sidebar','border/control'],['C · Оливковый + контур','Больше цветового акцента. Контур отделяет кнопку от активной строки, но сближает её со стилем выбора.','accent/soft','accent/strong']];
const results=[];
for(const [title,description,bg,border] of options){const card=frame(title,cols,'VERTICAL',608,'lg');spacing(card,'base','lg');fill(card,'background/surface');card.strokes=[paint('border/subtle')];radii(card);await text(card,'OptionTitle',title,'medium');const desc=await text(card,'OptionDescription',description,'small','text/secondary');desc.resize(560,72);desc.textAutoResize='NONE';
for(const [name,surface] of [['Белая поверхность','background/surface'],['Фон интерфейса','background/canvas'],['Активная строка','accent/soft']]){
 const context=frame(name,card,'VERTICAL',560,'base');spacing(context,'base','base');fill(context,surface);radii(context);await text(context,'ContextTitle',name,'small','text/secondary');
 const pair=frame('ButtonPair',context,'HORIZONTAL',528);spacing(pair,'base');
 const primary=bs.children.find(c=>c.variantProperties.Kind==='Primary'&&c.variantProperties.State==='Default').createInstance();pair.appendChild(primary);created.push(primary.id);await fonts(primary);primary.resize(232,40);primary.findOne(n=>n.name==='Control').setProperties({'Text#30956:4':'Открыть запись'});
 const secondary=attempt.createInstance();pair.appendChild(secondary);created.push(secondary.id);await fonts(secondary);secondary.resize(280,40);secondary.name='Secondary proposal';
 const button=secondary.findOne(n=>n.type==='INSTANCE'&&n.name==='ProductButton');button.resize(280,40);button.layoutSizingHorizontal='FILL';const ctl=secondary.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');ctl.fills=[paint(bg)];ctl.strokes=border?[paint(border)]:[];ctl.strokeWeight=1;ctl.strokeAlign='INSIDE';
}
results.push({id:card.id,title,fill:bg,border});}
await text(board,'DecisionNote','B — наиболее явная кнопка на разных фонах. A — спокойнее. C — сильнее использует цвет продукта. Все образцы остаются связанными с ProductButton.','small','text/secondary');
return {boardId:board.id,options:results,createdNodeIds:[...new Set(created.concat(board.findAll().map(n=>n.id)))]};
'''
if __name__=='__main__':print(json.dumps({'code':CODE}))
