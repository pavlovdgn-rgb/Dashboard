"""Idempotent final adapter sync. Exact source variants remain in catalog.json."""
from pathlib import Path

path = Path('src/components/_shared/ElasticComponent.tsx')
text = path.read_text(encoding='utf-8')
if "from './ElasticVariantParts'" not in text:
    text = text.replace("import moment from 'moment';", "import moment from 'moment';\nimport { ElasticRefresh, ElasticThumbnail, ElasticNestedNav, ElasticFileField } from './ElasticVariantParts';")
    lines = text.splitlines()
    replacements = {
        '  if(i>=1&&i<=3)': '  if(i>=1&&i<=3)return <ElasticRefresh index={i} values={p}/>;',
        '  if(i===53||i===54)': '  if(i===53||i===54)return <ElasticThumbnail index={i} values={p}/>;',
        '  if(i===85||i===86)': '  if(i===85||i===86)return <ElasticFileField index={i} values={p}/>;',
        '  if(i===157)': '  if(i===157)return <ElasticNestedNav values={p}/>;',
        '  if(i===110)': "  if(i===110)return ui('EuiMarkdownEditor',{'aria-label':'Редактор Markdown',value:text,onChange:setText,autoFocus:p.Type==='Focus',errors:p.Type==='Errors'?['Проверьте Markdown']:p.Type==='Attachment Error'?['Файл не поддерживается. Выберите другой файл.']:undefined});",
        '  if(i===96||i===97)': "  if(i===96||i===97)return ui('EuiHeader',{theme:i===96?'dark':'default',sections:[{items:isOn(p.Mobile)?[ui('EuiButtonIcon',{'aria-label':'Открыть меню',iconType:IconPlaceholder,onClick:click}),<span key=\"brand\">UX-Lab</span>]:[<span key=\"brand\">UX-Lab</span>,breadcrumbs()]}]});",
    }
    for n, line in enumerate(lines):
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                lines[n] = replacement
                break
    text='\n'.join(lines)+'\n'
    text=text.replace("  const [paused,setPaused]=useVariantState(i===1?!isOn(p.On):isOn(p.Paused));\n",'')
    text=text.replace("p.Type==='Many is last'?9:0", "p.Type==='Many is last'?9:p.Type==='Many in between'?4:0")
    text=text.replace("compressed:p.Type==='Compressed'", "compressed:p.Type==='Compressed'||p.Type==='Mobile / Indeterminate'")
    text=text.replace("checked,disabled,...(radio?{}", "checked,disabled,compressed:p.Size==='Small',...(radio?{}")
    text=text.replace("isLoading:isOn(p.Loading),isDisabled:disabled,arrowDisplay", "extraAction:flag('Extra action')?ui('EuiButtonIcon',{'aria-label':'Дополнительное действие',iconType:IconPlaceholder,onClick:click}):undefined,isLoading:isOn(p.Loading),isDisabled:disabled,arrowDisplay")
    text=text.replace("if([19,20,124].includes(i))return panel();", "if(i===19||i===20)return <div className={styles.panelBackground} data-disabled={disabled} data-checked={i===20&&checked}>{panel()}</div>;\n  if(i===124)return panel();")
    # Strip source asterisks before color mapping (Neutral* otherwise leaked to EUI).
    text=text.replace(".toLowerCase().replace(/\\*.*/, '');", ".toLowerCase().replace(/\\*.*/, '').trim();")
    text=text.replace("label:isOn(p.Label)?'Загрузка':undefined,valueText:isOn(p.Label)", "label:isOn(p.Label)?'Загрузка':undefined,valueText:isOn(p.Label),position:i===131?'absolute':'static'")
    path.write_text(text,encoding='utf-8')
print('Adapter synchronization applied (safe to repeat).')
