"""Targeted, repeatable corrections to EUI adapter property mappings."""
from pathlib import Path

path = Path('src/components/_shared/ElasticComponent.tsx')
text = path.read_text(encoding='utf-8')
if "import { ElasticTablePart }" in text:
    raise SystemExit('This migration is already applied; later adapter refinements are preserved.')
def replace(old, new):
    global text
    if old in text:
        text = text.replace(old, new)

replace("import { ElasticPagePart }", "import { ElasticNotifications } from './ElasticNotifications';\nimport { ElasticPagePart }")
replace("const sizes: Record<string, string> = {", "const sizes: Record<string, string> = { none:'none', xs:'xs',s:'s',m:'m',l:'l',xl:'xl',xxl:'xxl','x small':'xs','xxx-small':'xxxs',")
replace("replace(/\\*.*/, '').split", "replace(/\\*.*/, '').trim().split")
replace("isOn(p['Checked?']));", "isOn(p['Checked?'])||isOn(p.Active)||isOn(p['Active?']));")
replace("const [page,setPage]=useState(p.Type==='Many is last'?9:0);", "const [page,setPage]=useVariantState(p.Type==='Many is last'?9:0);\n  const [paused,setPaused]=useVariantState(i===1?!isOn(p.On):isOn(p.Paused));")
replace("const [open,setOpen]=useVariantState(isOn(p.Expand));", "const [open,setOpen]=useVariantState(isOn(p.Expand)||isOn(p.Open));")
replace("label:p.Label==='False'?undefined:label", "label:p.Label==='False'||i===152||i===153?undefined:label")
replace("isInvalid:invalid,compressed,options:", "isInvalid:invalid,compressed,options:")
replace("size:['xs','s'].includes(size(p.Size))?'s':'m'", "size:size(p.Size)==='xs'?'s':size(p.Size)==='s'?'s':'m'")
replace("display:isOn(p['Column display'])?'columnCompressed':'row'", "display:isOn(p['Column display'])?'columnCompressed':compressed?'rowCompressed':'row'")
replace("compressed,align:p.Align", "compressed,textStyle:isOn(p.Reverse)?'reverse':'normal',align:p.Align")
replace("layout:p.Layout==='Horizontal'?'horizontal':'vertical',actions:button(true)", "layout:p.Layout==='Horizontal'||i===58?'horizontal':'vertical',paddingSize:size(p['Padding size']||p['Padding Size']),color:String(p.Color||'Transparent').toLowerCase().split(' + ')[0],hasBorder:p.Color==='Plain + Border',hasShadow:p.Color==='Plain + Shadow',actions:button(true)")
replace("description:<p>Параметры формы</p>},", "description:<p>Параметры формы</p>,ratio:String(p.Ratio||'Half').replace('*','').toLowerCase()},")
replace("fontSize:'m',paddingSize:'m'", "fontSize:size(p.Size)==='xs'?'s':size(p.Size),paddingSize:'m'")
replace("if(i===24)return ui('EuiCode',{},", "if(i===24)return ui('EuiCode',{fontSize:size(p.Size)},")
replace("palette,type:'fixed'});", "palette:p.Palette==='Color blind (natural)'?[...palette].reverse():palette,type:'fixed'});")
replace("label:isOn(p.Label)?'Загрузка':undefined", "label:isOn(p.Label)?'Загрузка':undefined")

def line(prefix,new):
    global text
    lines=text.splitlines()
    for n,line in enumerate(lines):
        if line.strip().startswith(prefix):
            lines[n]='  '+new
            text='\n'.join(lines)+'\n'
            return

line("if(i>=1&&i<=3)", "if(i>=1&&i<=3)return ui(i===1?'EuiRefreshInterval':i===2?'EuiAutoRefresh':'EuiAutoRefreshButton',{isPaused:paused,refreshInterval:number*1000,onRefreshChange:({isPaused,refreshInterval}:{isPaused:boolean;refreshInterval:number})=>{setPaused(isPaused);setNumber(refreshInterval/1000);changed({isPaused,refreshInterval});},...(i===1?{}:{'aria-label':'Автообновление'})});")
line("if(i>=32&&i<=36)", "if(i>=32&&i<=36)return ui('EuiCollapsibleNavGroup',{title:'Навигация',isCollapsible:i!==35&&i!==36,initialIsOpen:p.Collapsed!=='Yes',background:String(p.Background||'None').toLowerCase()},i===36?undefined:list());")
line("if(i>=102&&i<=104)", "if(i===102)return list();\n  if(i===103||i===104)return ui('EuiListGroupItem',{label,size:size(p.Size),color:p.Color==='Default'?'text':color(p.Color),iconType:isOn(p.Icon)?IconPlaceholder:undefined,isActive:p.State==='Active'||checked,isDisabled:disabled,onClick:click,extraAction:isOn(p['Extra action'])?{iconType:IconPlaceholder,'aria-label':'Дополнительное действие',onClick:click}:undefined});")
line("if(i===125)", "if(i===125)return <E.EuiSplitPanel.Outer direction={p.Direction==='Horizontal'?'row':'column'} hasBorder={isOn(p.Border)} hasShadow={isOn(p.Shadow)} borderRadius={p['Border radius']==='False'?'none':'m'}><E.EuiSplitPanel.Inner>Первая область</E.EuiSplitPanel.Inner><E.EuiSplitPanel.Inner color=\"subdued\">Вторая область</E.EuiSplitPanel.Inner></E.EuiSplitPanel.Outer>;")
line("if(i===159)", "if(i===159)return p.Direction==='Horizontal'?<span className={styles.horizontalSpacer} style={{inlineSize:`var(--size-${({xs:'x-small',s:'small',m:'base',l:'large',xl:'x-large',xxl:'xx-large'} as Record<string,string>)[size(p.Size)]||'base'})`}}/>:ui('EuiSpacer',{size:size(p.Size)});")
line("if(i===157||i===158)", "if(i===158)return isOn(p.Show)?<span className={styles.nestedIndicator} data-last={isOn(p['Is last?'])} data-child={isOn(p['Is child?'])}/>:null;\n  if(i===157)return ui('EuiSideNav',{'aria-label':'Навигация',items:[{id:'group',name:'Раздел',items:[{id:'one',name:'Элемент',isSelected:checked,onClick:click,forceOpen:isOn(p['Open?']),icon:isOn(p['Icon?'])?<IconPlaceholder/>:undefined,items:isOn(p['Has child items?'])?[{id:'child',name:'Вложенный элемент',onClick:click}]:undefined}]}]},undefined);")
line("if(i===195)", "if(i>=195&&i<=197)return <ElasticNotifications key={i} index={i} values={p}/>;")
lines=text.splitlines()
text='\n'.join(line for line in lines if not line.strip().startswith(('if(i===196)', 'if(i===197)', 'const toast=')))+'\n'
replace("if(i>=181&&i<=189){", "if(i===188)return ui('EuiText',{},<p>Пример {p.Example==='Keyboard'?<kbd>Enter</kbd>:ui('EuiLink',{onClick:click},'ссылки')} в тексте.</p>);\n  if(i===189)return ui('EuiText',{size:size(p.Size)},<h3>Заголовок</h3>,<p>Текст параграфа.</p>);\n  if(i>=181&&i<=187){")
replace("icon:<IconPlaceholder/>});", "icon:<IconPlaceholder/>,image:isOn(p.Image)?<div className={styles.imagePlaceholder} role=\"img\" aria-label=\"Изображение карточки\"/>:undefined});")
replace("isActive:isOn(p.Active),onClick", "isActive:isOn(p.Active),isInvalid:invalid,onClick")
replace("numFilters:3,numActiveFilters", "numFilters:p.Count==='false'?undefined:3,numActiveFilters")
replace("hasActiveFilters:checked,isDisabled", "hasActiveFilters:checked,isSelected:checked,isDisabled")
replace("if(i===89)return ui('EuiFormLabel',{isInvalid:invalid},'Название поля');", "if(i===89)return <div className={styles.row}>{ui('EuiFormLabel',{isInvalid:invalid},'Название поля')}{p.Append==='Text'?ui('EuiText',{size:'xs'},'Необязательно'):p.Append==='Icon'?<IconPlaceholder/>:null}</div>;")
replace("size:'s'},ui('EuiFlyoutHeader'", "size:'s',type:p.Type==='Push'?'push':'overlay'},ui('EuiFlyoutHeader'")
replace("ui('EuiFlyoutBody',{},form('text'))", "ui('EuiFlyoutBody',{},isOn(p.Tabs)?tabs():null,form('text'))")
path.write_text(text,encoding='utf-8')
