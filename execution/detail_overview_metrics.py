"""Enrich existing SummaryMetric masters and overview instances without detaching them."""
import json
import sys
from pathlib import Path
from build_final_results import BASE

ROOT = Path(__file__).resolve().parents[1]
MASTER = r'''
await figma.setCurrentPageAsync(page);
const set=await figma.getNodeByIdAsync('171:1801');await fonts(set);
const h1=await figma.importStyleByKeyAsync('99abb7ac5c806691680484bfcb99a18653882ebf');await figma.loadFontAsync(h1.fontName);
function property(k,type,value){return Object.keys(set.componentPropertyDefinitions).find(x=>x.startsWith(k+'#'))||set.addComponentProperty(k,type,value);}
const detailKey=property('Detail','TEXT','18 с полными данными\n2 с неполными данными');
const badgeKey=property('Badge','TEXT','90%');
const showBadgeKey=property('ShowBadge','BOOLEAN',false);
const showProgressKey=property('ShowProgress','BOOLEAN',false);
for(const c of set.children){
 if(c.findOne(n=>n.name==='Detail'))continue;
 c.resize(c.width,248);c.primaryAxisSizingMode='FIXED';
 const value=c.findOne(n=>n.name==='Value');await value.setTextStyleIdAsync(h1.id);
 const valueRow=full(frame('ValueRow',c,'HORIZONTAL',464));c.insertChild(1,valueRow);valueRow.counterAxisAlignItems='CENTER';valueRow.appendChild(value);value.layoutSizingHorizontal='FILL';
 const badge=frame('MetricBadge',valueRow,'HORIZONTAL',80,'sm');badge.primaryAxisSizingMode='AUTO';radii(badge);fill(badge,'accent/soft');
 const bt=await text(badge,'BadgeLabel','90%','small','accent/strong');bt.layoutSizingHorizontal='HUG';
 badge.componentPropertyReferences={visible:showBadgeKey};badge.visible=false;bt.componentPropertyReferences={characters:badgeKey};
 const detail=await text(c,'Detail','18 с полными данными\n2 с неполными данными','small','text/secondary');detail.componentPropertyReferences={characters:detailKey};
 const link=c.findOne(n=>n.type==='INSTANCE'&&n.name==='Посмотреть участников');c.insertChild(c.children.indexOf(link),detail);
 const track=full(frame('CompletenessTrack',c,'HORIZONTAL',464));track.resize(464,8);track.counterAxisSizingMode='FIXED';track.itemSpacing=0;fill(track,'accent/soft');radii(track);track.componentPropertyReferences={visible:showProgressKey};track.visible=false;
 const bar=frame('CompletenessFill',track,'HORIZONTAL',417.6);bar.resize(417.6,8);bar.counterAxisSizingMode='FIXED';bar.setBoundVariable('height',dimensions.sm);fill(bar,'accent/strong');radii(bar);track.setBoundVariable('height',dimensions.sm);
 c.insertChild(c.children.indexOf(link),track);
 if(c.variantProperties.State!=='Ready')detail.characters=c.variantProperties.State==='Loading'?'Подробности появятся после загрузки.':'Доли не рассчитываются без наблюдений.';
 mutated.push(c.id,value.id,link.id);
}
set.parent.resizeWithoutConstraints(set.parent.width,480);
set.description='Study summary with a large value, sample basis, detail, optional badge and completeness bar. The bar describes recording/data completeness, never task success. White-card tertiary action remains an open design question.';
return {setId:set.id,createdNodeIds:created,mutatedNodeIds:[...new Set(mutated.concat(set.findAll().map(n=>n.id))),set.parent.id]};
'''

SCREEN = r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
figma.skipInvisibleInstanceChildren=false;
const screen=await figma.getNodeByIdAsync('175:614');await fonts(screen);
const set=await figma.getNodeByIdAsync('171:1801');
const cards=[];
for(const state of screen.findAll(n=>n.type==='FRAME'&&n.name.startsWith('State/'))){
 const summary=state.findOne(n=>n.name==='Summary');if(!summary)continue;
 const ready=['State/Ready','State/Selected','State/Overflow','State/FreeExploration'].includes(state.name);
 const free=state.name==='State/FreeExploration';
 for(let k=0;k<summary.children.length;k++){
  const c=summary.children[k];if(c.type!=='INSTANCE')continue;c.resize(c.width,248);
  const details=free?['Свободное изучение интерфейса\nБез сценариев и критериев успеха','18 с полными данными\n2 с неполными данными','Часть событий или записи отсутствует.\nЭто не оценка успеха участника.']:['Поиск и добавление в корзину\nКоличество товара · Оформление заказа','18 с полными данными\n2 с неполными данными','Часть событий или записи отсутствует.\nЭто не означает неуспех задания.'];
  const p={[propKey(set,'Detail')]:ready?details[k]:state.name==='State/Loading'?'Подробности появятся после загрузки.':k===0?'Сценарии настроены.\nРезультаты появятся после прохождений.':'Нет наблюдений в текущей выборке.\nДоли пока не рассчитываются.',[propKey(set,'ShowBadge')]:ready&&k>0,[propKey(set,'Badge')]:k===1?'90% полные':'10% выборки',[propKey(set,'ShowProgress')]:ready&&k===1};
  c.setProperties(p);
  const hint=c.findOne(n=>n.name==='Hint');hint.visible=true;hint.characters=ready?(k===0?(free?'Задания не используются':'В исследовании · режим заданий'):k===1?'Уникальные участники в текущей выборке':'Требуют проверки полноты данных'):hint.characters;
  if(k===2&&ready){const badge=c.findOne(n=>n.name==='MetricBadge');fill(badge,'status/warning/background');fill(badge.findOne(n=>n.type==='TEXT'),'status/warning/text');}
  if(k===1&&ready){const track=c.findOne(n=>n.name==='CompletenessTrack');const bar=c.findOne(n=>n.name==='CompletenessFill');bar.resize(track.width*.9,8);}
  const value=c.findOne(n=>n.name==='Value');if(ready)value.characters=k===0?(free?'Не применимо':'3'):k===1?'20':'2 из 20';
  cards.push({id:c.id,state:state.name,index:k,width:c.width,height:c.height});mutated.push(c.id,...c.findAll().map(n=>n.id));
 }
}
return {screenId:screen.id,cards,mutatedNodeIds:[...new Set(mutated)]};
'''

if __name__ == '__main__':
    stage=sys.argv[1]
    code=BASE+{'master':MASTER,'screen':SCREEN}[stage]
    target=ROOT/'.tmp/final-results'/f'detail-{stage}.js'
    target.write_text(code,encoding='utf-8')
    print(json.dumps({'code':code},ensure_ascii=False))
