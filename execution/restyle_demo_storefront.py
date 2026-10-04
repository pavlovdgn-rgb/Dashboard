"""Independent demo-storefront styling, scoped to PrototypePlaceholder frames.

This is an explicitly requested ad-hoc external website, not a product-kit theme.
Keep heatmap coordinates and the research application/replay controls unchanged.
"""
import json
import sys

CODE = r'''
await figma.setCurrentPageAsync(await figma.getNodeByIdAsync('191:847'));
figma.skipInvisibleInstanceChildren=false;
const roots=figma.currentPage.findAll(n=>n.type==='FRAME'&&['PrototypePlaceholder','LivePrototype'].includes(n.name));
const selected=__TARGETS__;
const targets=selected.length?roots.filter(n=>selected.includes(n.id)):roots;
const created=[],changed=[],stylesCreated=[],varsCreated=[];
const collection=await figma.variables.getVariableCollectionByIdAsync('VariableCollectionId:269:10323');
const variables=await figma.variables.getLocalVariablesAsync();
const defs={canvas:'#F4F2FA',surface:'#FFFFFF',tint:'#ECE6FA',field:'#F8F6FD',border:'#D5CCE7',text:'#252034',muted:'#686078',action:'#7C3AED',accent:'#6131B5',inverse:'#FFFFFF'};
const vars={};
function rgb(hex){return {r:parseInt(hex.slice(1,3),16)/255,g:parseInt(hex.slice(3,5),16)/255,b:parseInt(hex.slice(5,7),16)/255};}
for(const [key,hex] of Object.entries(defs)){
 let v=variables.find(v=>v.variableCollectionId===collection.id&&v.name==='demo/storefront/'+key);
 if(!v){v=figma.variables.createVariable('demo/storefront/'+key,collection,'COLOR');varsCreated.push(v.id);}
 v.scopes=['FRAME_FILL','SHAPE_FILL','TEXT_FILL','STROKE_COLOR'];v.setVariableCodeSyntax('WEB','var(--demo-storefront-'+key+')');v.setValueForMode(collection.defaultModeId,{...rgb(hex),a:1});vars[key]=v;
}
for(const [key,value] of Object.entries({radius:20,controlRadius:10,padding:20,gap:16})){
 let v=variables.find(v=>v.variableCollectionId===collection.id&&v.name==='demo/storefront/'+key);
 if(!v){v=figma.variables.createVariable('demo/storefront/'+key,collection,'FLOAT');varsCreated.push(v.id);}
 v.scopes=key.toLowerCase().includes('radius')?['CORNER_RADIUS']:['GAP'];v.setVariableCodeSyntax('WEB','var(--demo-storefront-'+key+')');v.setValueForMode(collection.defaultModeId,value);vars[key]=v;
}
const styles={};const local=await figma.getLocalTextStylesAsync();
for(const [key,size,weight,line] of [['body',14,'Regular',24],['label',13,'SemiBold',24],['title',22,'Bold',28],['section',17,'Bold',24],['price',28,'ExtraBold',32],['button',14,'Bold',20],['brand',15,'ExtraBold',24]]){
 const f={family:'Manrope',style:weight};await figma.loadFontAsync(f);
 let s=local.find(s=>s.name==='Demo storefront/'+key);if(!s){s=figma.createTextStyle();s.name='Demo storefront/'+key;stylesCreated.push(s.id);}
 s.fontName=f;s.fontSize=size;s.lineHeight={unit:'PIXELS',value:line};s.letterSpacing={unit:'PIXELS',value:key==='brand'?1.1:0};styles[key]=s;
}
function paint(key){return figma.variables.setBoundVariableForPaint({type:'SOLID',color:rgb(defs[key])},'color',vars[key]);}
function fill(n,key){n.fills=[paint(key)];changed.push(n.id);}
function radius(n,key='radius'){for(const p of ['topLeftRadius','topRightRadius','bottomLeftRadius','bottomRightRadius'])n.setBoundVariable(p,vars[key]);changed.push(n.id);}
async function styleText(t,key,color='text'){
 for(const seg of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);
 await t.setTextStyleIdAsync(styles[key].id);fill(t,color);
}
function under(n,name,root){for(let p=n.parent;p&&p!==root;p=p.parent)if(p.name===name)return true;return false;}
for(const root of targets){
 for(const t of root.findAllWithCriteria({types:['TEXT']}))for(const seg of t.getStyledTextSegments(['fontName']))await figma.loadFontAsync(seg.fontName);
 fill(root,'canvas');root.strokes=[paint('border')];radius(root);root.effects=[];
 const title=root.children.find(n=>n.type==='TEXT');await styleText(title,'brand','accent');
 title.characters='NOVA  /  '+(root.findOne(n=>n.name==='CheckoutContent')?'ОФОРМЛЕНИЕ ЗАКАЗА':'ГОРОДСКИЕ РЮКЗАКИ');
 for(const t of root.findAllWithCriteria({types:['TEXT']})){
  if(t===title||under(t,'Demo click layer',root))continue;
  const text=t.characters;
  let key=/4 900/.test(text)?'price':text==='Городской рюкзак'?'title':/^(Ваш заказ|Контактные данные|Выберите размер)$/.test(text)?'section':t.name==='InputValue'?'body':t.name==='Text'?'button':/^(Имя|Email|Размер)$/.test(text)?'label':'body';
  await styleText(t,key,/^(Имя|Email|Размер|Адрес:|Доставка:|Демонстрационное)/.test(text)?'muted':'text');
 }
 for(const n of root.findAll(n=>n.type==='FRAME'&&['FormPreview','OrderPreview','ProductImage','PrototypeSizeModal'].includes(n.name))){
  if(!(n.name==='ProductImage'&&n.fills.some(p=>p.type==='IMAGE')))fill(n,n.name==='OrderPreview'?'tint':'surface');radius(n);n.strokes=[];n.effects=[];
  if(n.name==='FormPreview'){for(const k of ['paddingLeft','paddingRight','paddingTop','paddingBottom'])n.setBoundVariable(k,vars.padding);n.layoutSizingVertical='HUG';}
 }
 const fields=root.findAll(n=>n.type==='INSTANCE'&&n.name.startsWith('Field/'));
 for(const field of fields){
  for(const n of field.findAll(n=>n.type!=='TEXT'&&'fills'in n)){
   if(Array.isArray(n.fills)&&n.fills.length)fill(n,'field');
   if('strokes'in n&&n.strokes.length){n.strokes=[paint('border')];changed.push(n.id);}
   if('cornerRadius'in n)radius(n,'controlRadius');
  }
 }
 const buttons=root.findAll(n=>n.type==='INSTANCE'&&['Отправить заказ','Добавить в корзину','Подтвердить размер','S','M · выбран','L'].includes(n.name));
 for(const b of buttons){
  const ctl=b.children.find(n=>n.name==='Control');if(!ctl)continue;
  const small=['S','M · выбран','L'].includes(b.name),selected=b.name==='M · выбран';
  fill(ctl,small&&!selected?'surface':'action');radius(ctl,'controlRadius');ctl.strokes=[];
  for(const t of ctl.findAllWithCriteria({types:['TEXT']}))await styleText(t,'button',small&&!selected?'accent':'inverse');
  b.resize(Math.max(b.width,small?56:190),b.height);changed.push(b.id);
 }
 const productImage=root.findOne(n=>n.type==='FRAME'&&n.name==='ProductImage');
 if(productImage){if(!productImage.fills.some(p=>p.type==='IMAGE'))fill(productImage,'tint');for(const n of productImage.findAll(n=>n.type==='VECTOR')){fill(n,'accent');if(n.strokes.length)n.strokes=[paint('accent')];}}
}
return {createdNodeIds:created,mutatedNodeIds:[...new Set(changed)],createdStyleIds:stylesCreated,createdVariableIds:varsCreated,roots:targets.map(n=>({id:n.id,w:n.width,h:n.height})),styles:Object.fromEntries(Object.entries(styles).map(([k,s])=>[k,s.id])),tokens:Object.fromEntries(Object.entries(vars).map(([k,v])=>[k,v.id]))};
'''

if __name__ == '__main__':
    print(json.dumps({'code': CODE.replace('__TARGETS__', json.dumps(sys.argv[1:]))}, ensure_ascii=False))
