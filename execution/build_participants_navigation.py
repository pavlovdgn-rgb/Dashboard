"""Build participant-table compositions and NavMenu from existing product tokens.

Creation and combineAsVariants are separate phases; receipts keep exact IDs.
"""
import json
import sys
from pathlib import Path
from build_analytics_components import START

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / '.tmp/participants-navigation'
COMMON = START.replace("'UI Kit — analytics blocks'", "'UI Kit — participants and navigation'").replace('section.x=3500', 'section.x=6500').replace('section.resizeWithoutConstraints(2800,5000)', 'section.resizeWithoutConstraints(4000,8000)') + r'''
Object.assign(iconKeys,{user:'14a6e843515c0545fe6cc8ab9707735d21fc7a6d',users:'297df35096cfdd7b8c88a465d0cd8c485dcda540',play:'aea59ee7c483a452dc32d2bab505ca600744090a',check:'4e4e7c90115e424c14d03e5056775912f8d0565f',minus:'96483a0fa795066bcdb9640003fa781760e2a561',flag:'21a80ed21bd18f9bcd29b9c0329a021d22c40065',down:'ad886ce4521200a238ffe46f2c3be231e9925c81',folder:'c6a917af682a76da42e866a6bbadffd36f715715',project:'af8f28f6e4634ed8887ebf1d687333e1addba45f',settings:'20ed4b0225fb57b2191bf6958dee413aece13aca',overview:'be2057ab53d55af106bb1fddf2a16a184a640ff3',heatmap:'e557d008bea964f44d9f20d2bded7e641d713f34',funnel:'3b8f958cff3af9880ab1290cdf44659b29097ea0',pdf:'989646b14b75559d38c73e2b550126a5f49c54b6'});
async function instance(parent,setName,props,name){const s=page.findOne(n=>n.type==='COMPONENT_SET'&&n.name===setName);if(!s)throw Error('Missing '+setName);const b=s.children.find(c=>Object.entries(props).every(([k,v])=>c.variantProperties[k]===v));if(!b)throw Error('Missing variant '+setName);const i=b.createInstance();parent.appendChild(i);i.name=name||setName;i.isExposedInstance=true;created.push(i.id);await fonts(i);return i;}
async function setCopy(n,name,value){const t=n.findOne(t=>t.type==='TEXT'&&t.name===name);if(!t)throw Error('Missing text '+name);for(const s of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);t.characters=value;}
async function flatButton(parent,label,kind='Secondary',state='Default',width=172){const s=await figma.getNodeByIdAsync('125:450');const b=s.children.find(c=>c.variantProperties.Kind===kind&&c.variantProperties.State===state);const i=b.createInstance();parent.appendChild(i);await fonts(i);const ctl=i.findOne(n=>n.type==='INSTANCE'&&n.name==='Control');ctl.setProperties({'Text#30956:4':label.replace(/[▾▿▼⌄]/g,'').trim()});if(/[▾▿▼⌄]/.test(label)){const down=await figma.importComponentByKeyAsync('ad886ce4521200a238ffe46f2c3be231e9925c81');ctl.setProperties({'Icon right#30956:5':true,'⮑  Icon right#31056:0':down.id});for(const n of ctl.findAll(n=>n.type==='VECTOR'||n.type==='BOOLEAN_OPERATION')){if(n.fills.length)n.fills=[paint('text/primary')];if(n.strokes.length)n.strokes=[paint('text/primary')];}}i.resize(width,i.height);created.push(i.id);return i;}
'''

STATUS = r'''
const defs=NAME==='TaskOutcome'?[['Achieved','Цель достигнута','check','status/success/text','status/success/background'],['NotAchieved','Цель не достигнута','error','status/error/text','status/error/background'],['NotAssessed','Нет оценки','minus','text/secondary',null]]:[['Complete','Полные','check','status/success/text',null],['Partial','Неполные','info','status/warning/text',null],['Unavailable','Недоступны','minus','text/secondary',null]];
for(const [value,label,ic,color,bg] of defs){const c=cell('Status='+value,224,32,'HORIZONTAL','sm');spacing(c,'sm','sm');c.counterAxisAlignItems='CENTER';c.fills=bg?[paint(bg)]:[];await icon(c,ic,color,16);await tx(c,'StatusLabel',label,184,'small',color);}
'''
ACTION = r'''
for(const mode of ['Single','Multiple','Unavailable']){const c=cell('Mode='+mode,232,64,'VERTICAL');c.fills=[];c.primaryAxisAlignItems='CENTER';spacing(c,'xs');
if(mode==='Unavailable'){await tx(c,'UnavailableLabel','Запись недоступна',232,'small','text/secondary');await tx(c,'UnavailableReason','Не получены данные записи',232,'small','text/secondary');}
else {await flatButton(c,mode==='Single'?'Открыть запись':'Выбрать попытку ▾',mode==='Single'?'Primary':'Secondary', 'Default',232);if(mode==='Single')await tx(c,'AttemptHint','Попытка 1',232,'small','text/secondary');}
}
'''
ROW = r'''
for(const state of ['Default','Hover','Focus']){const c=cell('State='+state,1360,96,'HORIZONTAL','base');spacing(c,'base','base');c.counterAxisAlignItems='CENTER';fill(c,state==='Hover'?'surface/hover':'background/surface');focus(c,state);
const id=frame('ParticipantIdentity',c,'HORIZONTAL',128);id.counterAxisAlignItems='CENTER';await icon(id,'user','text/secondary',20);const t=await tx(id,'ParticipantId','014',100,'medium');link(t,'ParticipantId','014');
const attempt=await tx(c,'Attempt','1',104,'body');link(attempt,'Attempt','1');
await instance(c,'TaskOutcome',{Status:'NotAchieved'});
const time=await tx(c,'Duration','04:32',104,'body');link(time,'Duration','04:32');
const signals=frame('SignalsCell',c,'HORIZONTAL',104);signals.counterAxisAlignItems='CENTER';await icon(signals,'flag','text/secondary',16);const cnt=await tx(signals,'SignalCount','4',72,'body');link(cnt,'SignalCount','4');
await instance(c,'RecordingCoverage',{Status:'Complete'});
await instance(c,'AttemptAction',{Mode:'Single'});
}
'''
TABLE = r'''
for(const state of ['Ready','Loading','Empty','FilteredEmpty','Error']){const c=cell('State='+state,1408,696,'VERTICAL','lg');spacing(c,'base','lg');c.strokes=[paint('border/subtle')];
const toolbar=frame('Toolbar',c,'HORIZONTAL',1360);toolbar.counterAxisAlignItems='CENTER';spacing(toolbar,'base');await tx(toolbar,'Count',state==='Ready'?'16 участников начали · показаны 4':'Участники сценария',568,'medium');
const searchSet=await figma.importComponentSetByKeyAsync('e20002c1de6f3f7fa720fd0080d8ac3701566932');const src=searchSet.children.find(n=>n.variantProperties.State==='Placeholder'&&n.variantProperties.Label==='False'&&n.variantProperties['Help text']==='False'&&n.variantProperties.Compressed==='True'&&n.variantProperties['Column display']==='False');const search=src.createInstance();toolbar.appendChild(search);await theme(search,'text/secondary','background/surface');search.name='SearchByParticipantId';search.resize(360,40);created.push(search.id);const texts=search.findAllWithCriteria({types:['TEXT']});for(const t of texts){t.characters='Поиск по ID';await t.setTextStyleIdAsync(styles.small.id);}
await flatButton(toolbar,'Все исходы ▾','Secondary','Default',192);await flatButton(toolbar,'Все данные ▾','Secondary','Default',192);
const header=frame('TableHeader',c,'HORIZONTAL',1360,'base');spacing(header,'base','base');fill(header,'background/subtle');const widths=[128,104,224,104,104,224,232];const labels=['УЧАСТНИК','ПОПЫТКА','ИСХОД ЗАДАНИЯ','ВРЕМЯ ↓','СИГНАЛЫ','ДАННЫЕ','ДЕЙСТВИЕ'];for(let i=0;i<labels.length;i++)await tx(header,'Column'+i,labels[i],widths[i],'small','text/secondary');
if(state==='Ready'){
const body=frame('ParticipantRows',c,'VERTICAL',1360);body.itemSpacing=0;
const entries=[['014','1','NotAchieved','04:32','4','Complete','Single'],['018','1','NotAssessed','03:10','2','Partial','Single'],['009','1 из 2','Achieved','02:48','3','Complete','Multiple'],['012','1','Achieved','03:24','2','Complete','Single']];
for(const [id,attempt,outcome,time,signals,coverage,action] of entries){const row=await instance(body,'ParticipantRow',{State:'Default'},'Participant '+id);const set=await row.getMainComponentAsync();const owner=set.parent;row.setProperties({[propKey(owner,'ParticipantId')]:id,[propKey(owner,'Attempt')]:attempt,[propKey(owner,'Duration')]:time,[propKey(owner,'SignalCount')]:signals});row.findOne(n=>n.type==='INSTANCE'&&n.name==='TaskOutcome').setProperties({Status:outcome});row.findOne(n=>n.type==='INSTANCE'&&n.name==='RecordingCoverage').setProperties({Status:coverage});row.findOne(n=>n.type==='INSTANCE'&&n.name==='AttemptAction').setProperties({Mode:action});}
for(let i=0;i<body.children.length;i++)fill(body.children[i],i%2?'background/canvas':'background/surface');
const footer=frame('Footer',c,'HORIZONTAL',1360);spacing(footer,'base');footer.counterAxisAlignItems='CENTER';await tx(footer,'Range','Участники 1–4 из 16',284,'small');await tx(footer,'AttemptScope','Время и показатели относятся к выбранной попытке.',548,'small','text/secondary');await flatButton(footer,'Назад','Secondary','Disabled',112);await flatButton(footer,'1 из 4','Tertiary','Default',112);await flatButton(footer,'Далее','Secondary','Default',112);
}else {await stateMessage(c,state,1360,'participants');if(state==='Empty')await setCopy(c,'StateDescription','Участники появятся после начала прохождения этого сценария.');}
await tx(c,'DataNote','Неполная запись и недостижение цели — разные признаки.',1360,'small','text/secondary');
}
'''
NAV = r'''
const defs=[['Projects','Все проекты','folder'],['Studies','Исследования проекта','project'],['Setup','Настройка исследования','settings'],['Launch','Проверка и запуск','play'],['Overview','Обзор результатов','overview'],['Heatmap','Тепловая карта','heatmap'],['Funnel','Воронка','funnel'],['Participants','Участники','users'],['Signals','Сигналы затруднений','flag'],['PDF','Отчёт PDF','pdf']];
const nav=await figma.getNodeByIdAsync('128:563');
for(const active of defs.map(d=>d[0])){const c=cell('Active='+active,320,1080,'VERTICAL','base');spacing(c,'lg','base');fill(c,'background/sidebar');
const brand=frame('Brand',c,'HORIZONTAL',288);brand.counterAxisAlignItems='CENTER';spacing(brand,'md');const logo=frame('ProductMark',brand,'HORIZONTAL',32,'sm');fixed(logo,32,32);fill(logo,'action/primary');radii(logo);await icon(logo,'users','text/inverse',16);await tx(brand,'ProductName','UX-Lab',244,'medium');
const top=frame('NavigationGroups',c,'VERTICAL',288);spacing(top,'lg');
async function group(label,items,propName){const g=frame(label,top,'VERTICAL',288);spacing(g,'xs');const title=await tx(g,'GroupLabel',label,288,'small','text/secondary');if(propName)link(title,propName,label);
for(const [key,label,ic] of items){const selected=key===active;const item=frame('Nav '+key,g,'HORIZONTAL',288,'xs');fixed(item,288,48);spacing(item,'xs','xs');item.counterAxisAlignItems='CENTER';item.fills=selected?[paint('accent/soft')]:[];radii(item);await icon(item,ic,selected?'accent/strong':'text/secondary',20);
const base=nav.children.find(x=>x.variantProperties.Selected===(selected?'True':'False')&&x.variantProperties.State==='Default');const n=base.createInstance();item.appendChild(n);n.name='NavigationItem';n.isExposedInstance=true;created.push(n.id);await fonts(n);n.resize(252,48);n.fills=[];const ctl=n.findOne(x=>x.type==='INSTANCE'&&x.name==='Control');ctl.fills=[];ctl.strokes=[];const t=ctl.findOne(x=>x.type==='TEXT');t.characters=label;await t.setTextStyleIdAsync(styles.small.id);fill(t,selected?'accent/strong':'text/primary');}
}
await group('РАБОЧЕЕ ПРОСТРАНСТВО',defs.slice(0,1));
if(active!=='Projects')await group('ПРОЕКТ: ИНТЕРНЕТ-МАГАЗИН',defs.slice(1,2),'ProjectLabel');
if(!['Projects','Studies'].includes(active))await group('ИССЛЕДОВАНИЕ: ПОКУПКА',defs.slice(2),'StudyLabel');
const spacer=frame('FlexibleSpace',c,'VERTICAL',288);spacer.layoutSizingVertical='FILL';spacer.fills=[];
const foot=frame('Footer',c,'VERTICAL',288);spacing(foot,'sm');const status=await tx(foot,'StudyStatus',active==='Projects'?'Рабочее пространство команды':active==='Studies'?'Все исследования проекта':'● Готово к тестированию',288,'small',!['Projects','Studies'].includes(active)?'accent/strong':'text/secondary');link(status,'FooterText',status.characters);
}
'''

CONFIG = {
 'outcome': ('TaskOutcome',40,40,760,STATUS,'Три исхода задания. Полнота записи отображается отдельно.'),
 'coverage': ('RecordingCoverage',840,40,760,STATUS,'Компактный статус доступности данных, без фоновой плашки.'),
 'action': ('AttemptAction',1640,40,800,ACTION,'Single / Multiple / Unavailable. Выбор попытки обновляет все показатели строки.'),
 'row': ('ParticipantRow',40,480,1456,ROW,'Default / Hover / Focus. Исход, полнота и действие переключаются во вложенных компонентах.'),
 'table': ('ParticipantsTable',40,1100,1480,TABLE,'Ready / Loading / Empty / FilteredEmpty / Error. Пример данных для выбранного сценария.'),
 'nav': ('NavMenu',1640,480,2260,NAV,'Active: 10 пунктов. Ширина 320, высота 1080. ProductNavItem остаётся вложенным компонентом.'),
}

def build(stage):
    name,x,y,dw,body,note=CONFIG[stage]
    code=COMMON+body+r'''
section.resizeWithoutConstraints(section.width,Math.max(8000,...section.children.map(n=>n.y+n.height+48)));
return {name:NAME,documentationId:doc.id,sectionId:section.id,variantIds:variants.map(n=>n.id),links:propLinks.map(l=>({id:l.node.id,name:l.name,value:l.value,kind:l.kind})),createdNodeIds:[...new Set(created.concat(doc.findAll().map(n=>n.id)))]};
'''
    for key,value in dict(NAME=name,X=x,Y=y,DOCWIDTH=dw,NOTE=note).items():
        code=code.replace('__'+key+'__',str(value))
    return code

def combine(receipt):
    return COMMON[:COMMON.index("const NAME=")] + r'''
const data=__RECEIPT__;
const doc=await figma.getNodeByIdAsync(data.documentationId);
const nodes=[];for(const id of data.variantIds)nodes.push(await figma.getNodeByIdAsync(id));
const set=figma.combineAsVariants(nodes,doc);set.name=data.name;set.layoutMode='HORIZONTAL';set.layoutWrap='WRAP';set.resize(doc.width-48,100);set.primaryAxisSizingMode='FIXED';set.counterAxisSizingMode='AUTO';spacing(set,'lg');set.setBoundVariable('counterAxisSpacing',dimensions.lg);set.fills=[];set.strokes=[];set.clipsContent=false;
for(const p of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])set[p]=0;
const props={};for(const l of data.links){const n=await figma.getNodeByIdAsync(l.id);for(const s of n.getStyledTextSegments(['fontName']))await figma.loadFontAsync(s.fontName);if(!props[l.name])props[l.name]=set.addComponentProperty(l.name,l.kind,l.value);n.componentPropertyReferences={...n.componentPropertyReferences,characters:props[l.name]};}
set.description='UX testing product component. Bound product colours and Elastic UI styles; nested library instances retained. See ds/participants-navigation.md. Counts and status examples are demonstration data.';
const section=await figma.getNodeByIdAsync(data.sectionId);section.resizeWithoutConstraints(section.width,Math.max(section.height,...section.children.map(n=>n.y+n.height+48)));
return {name:set.name,id:set.id,variants:set.children.map(n=>({id:n.id,name:n.name,width:n.width,height:n.height})),properties:set.componentPropertyDefinitions,createdNodeIds:[set.id],mutatedNodeIds:[doc.id,section.id,...data.variantIds,...data.links.map(l=>l.id)]};
'''.replace('__RECEIPT__', json.dumps(receipt, ensure_ascii=False))

if __name__=='__main__':
    TMP.mkdir(parents=True,exist_ok=True)
    if sys.argv[1]=='combine':
        code=combine(json.loads((TMP/(sys.argv[2]+'-created.json')).read_text(encoding='utf-8')))
    else:
        code=build(sys.argv[1])
    print(json.dumps({'code':code},ensure_ascii=False))
