"""Correct semantics discovered during visual review; keep edits reproducible."""
import json
from build_final_results import BASE
CODE=BASE+r'''
await figma.setCurrentPageAsync(figma.root.children.find(p=>p.id==='191:847'));
const roots=figma.currentPage.findAll(n=>n.type==='FRAME'&&n.name.startsWith('Screen/'));
const checked=await figma.importComponentByKeyAsync('572b87daf9f222bc7334d05432dced1f290965b4');
const unchecked=await figma.importComponentByKeyAsync('0b3b82aa455c43720b78e936b0b5e6b05b64954a');
const removed=[];
for(const root of roots){await fonts(root);
 for(const old of root.findAll(n=>n.type==='TEXT'&&/^[☑☐]/m.test(n.characters))){
  const parent=old.parent;const position=parent.children.indexOf(old);const wrap=frame('CheckboxGroup',parent,'VERTICAL',old.width);parent.insertChild(position,wrap);full(wrap);
  for(const line of old.characters.split('\n')){
   if(!/^[☑☐]/.test(line)){await text(wrap,'Note',line,'small','text/secondary');continue;}
   const n=(line.startsWith('☑')?checked:unchecked).createInstance();wrap.appendChild(n);created.push(n.id);await theme(n,'text/primary');n.name='Checkbox/'+line.slice(1).trim();const label=n.findOne(x=>x.type==='TEXT');await label.setTextStyleIdAsync(styles.body.id);label.characters=line.slice(1).trim();n.resize(wrap.width,n.height);full(n);
  }removed.push(old.id);old.remove();
 }
 for(const n of root.findAll(n=>n.type==='INSTANCE'&&/· выбран|· выбрана/.test(n.name))){const control=n.findOne(x=>x.type==='INSTANCE'&&x.name==='Control');if(control){n.fills=[];fill(control,'accent/soft');for(const t of control.findAllWithCriteria({types:['TEXT']}))fill(t,'accent/strong');mutated.push(n.id,...control.findAll().map(x=>x.id));}}
 if(root.name==='Screen/ReplayIncomplete'){for(const t of root.findAll(n=>n.type==='TEXT'&&n.characters.startsWith('01:52'))){t.characters='01:40–02:05\nРазрыв записи · действия неизвестны';mutated.push(t.id);}}
 if(root.name==='Screen/FindingSaved'){
  const wrap=root.children.find(n=>n.name==='FindingSavedNotice');if(wrap){const toast=wrap.children.find(n=>n.name==='FindingSavedNotice');const dim=wrap.children.find(n=>n.name==='ModalScrim');if(dim){removed.push(dim.id);dim.remove();}wrap.fills=[];root.appendChild(toast);toast.layoutPositioning='ABSOLUTE';toast.x=root.width-toast.width-32;toast.y=root.height-toast.height-32;mutated.push(toast.id);removed.push(wrap.id);wrap.remove();}
 }
 if(root.name==='Screen/Login'){const body=root.findOne(n=>n.name==='ParticipantBody');body.primaryAxisAlignItems='CENTER';mutated.push(body.id);}
}
return {createdNodeIds:created,mutatedNodeIds:mutated,removedNodeIds:removed};
'''
if __name__=='__main__':print(json.dumps({'code':CODE},ensure_ascii=False))
