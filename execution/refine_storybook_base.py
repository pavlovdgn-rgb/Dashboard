"""Small additive base corrections for composable stories and original icons."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def edit(file,pairs):
    p=ROOT/file;s=p.read_text(encoding='utf-8')
    for old,new in pairs:
        if old in s:s=s.replace(old,new)
        elif new not in s:raise ValueError(f'Missing anchor in {file}: {old[:70]}')
    p.write_text(s,encoding='utf-8')
edit('src/components/_shared/ProductComponent.tsx',[
 ('<h3><DesignIcon/>','<h3><DesignIcon type="iInCircle" size="l"/>'),
 ('Посмотреть данные <DesignIcon/>','Посмотреть данные <DesignIcon type="arrowRight"/>'),
 ('<span className={styles.logo}><DesignIcon/></span>','<span className={styles.logo}><img src={logoUrl} width={24} height={24} alt=""/></span>'),
 ('<DesignIcon/>{title}</button>','<DesignIcon type={routeIcons[index]}/>{title}</button>'),
 ('<option>Первый вариант</option><option>Второй вариант</option>','{(Array.isArray(p.options)?p.options:[\'Первый вариант\',\'Второй вариант\']).map(option=><option key={String(option)}>{String(option)}</option>)}'),
])
edit('src/components/_shared/ParticipantsTableExample.tsx',[
 ("import type { VariantValues }", "import { DesignIcon, type VariantValues }"),
 ('>‹</button>', '><DesignIcon type="arrowLeft"/></button>'),
 ('>›</button>', '><DesignIcon type="arrowRight"/></button>'),
])
edit('src/components/_shared/ElasticComponent.tsx',[
 ('onPageClick:setPage','onPageClick:(next:number)=>{setPage(next);changed(next);}'),
 ("ui('EuiModalHeaderTitle',{id},'Диалог')", "ui('EuiModalHeaderTitle',{id},String(p.title||'Диалог'))"),
 ("ui('EuiModalBody',{},form('text'))", "ui('EuiModalBody',{},children||form('text'))"),
 ("ui('EuiModalFooter',{},ui('EuiButton',{onClick:()=>setOpen(false)},'Закрыть'))", "ui('EuiModalFooter',{},p.footer as ReactNode||ui('EuiButton',{onClick:()=>setOpen(false)},'Закрыть'))"),
 ("'Очистить значение',iconType:DesignIcon", "'Очистить значение',iconType:'cross'"),
 ("'Открыть меню',iconType:DesignIcon", "'Открыть меню',iconType:'menu'"),
])
edit('src/components/_shared/ElasticNotifications.tsx',[
 ('><button className={styles.textButton}>Наведите курсор</button></EuiToolTip>', '>{p.children as React.ReactElement||<button className={styles.textButton}>Наведите курсор</button>}</EuiToolTip>'),
 ('title="Изменения сохранены"','title={String(p.title||\'Изменения сохранены\')}'),
 ('isOn(p.Icon)?DesignIcon:undefined', "isOn(p.Icon)?(p.Type==='Success'?'checkInCircleFilled':p.Type==='Danger'?'error':'info'):undefined"),
 ("import { DesignIcon, type VariantValues }", "import type { VariantValues }"),
])
# Native EUI checkmarks are restored; remove only the temporary drawn indicators.
p=ROOT/'src/global.css';s=p.read_text(encoding='utf-8');s=s.split('/* Selection indicators convey state;')[0];p.write_text(s,encoding='utf-8')
