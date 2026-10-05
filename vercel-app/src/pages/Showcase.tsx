import { Component, useEffect, useState, type ReactNode } from 'react';
import { EuiProvider } from '@elastic/eui';
import { EuiThemeAmsterdam } from '@elastic/eui/lib/themes/amsterdam';
import catalog from '../components/catalog.json';
import { registry } from '../components/registry';
import tokenManifest from '../tokens/manifest.json';
import { ProductAction } from '../components/_shared/ProductComponent';
import type { CatalogProps } from '../components/_shared/CatalogComponent';
import { TaskResultControl } from '../patterns/TaskResultControl';
import styles from './Showcase.module.css';
import { elasticTheme } from '../tokens/elasticTheme';

class SampleBoundary extends Component<{children:ReactNode}, {error:string}> {
  state={error:''};
  static getDerivedStateFromError(error:Error) { return {error:error.message}; }
  render() { return this.state.error?<pre role="alert" data-render-error className={styles.error}>{this.state.error}</pre>:this.props.children; }
}
const batchSize=8;
const query=new URLSearchParams(location.search);
export function Showcase() {
  const [tab,setTab]=useState(query.get('tab')||'components');
  const [search,setSearch]=useState('');
  const [group,setGroup]=useState('all');
  const [selected,setSelected]=useState(query.get('component')||'125:450');
  const [page,setPage]=useState(Number(query.get('page')||0));
  const [mode,setMode]=useState<'light'|'dark'>('light');
  const [scale,setScale]=useState('medium');
  const [overrides,setOverrides]=useState<Record<string,string>>({});
  useEffect(()=>{document.documentElement.dataset.colorMode=mode;document.documentElement.dataset.typeScale=scale;},[mode,scale]);
  const entries=catalog.filter(c=>(group==='all'||c.source===group)&&c.name.toLowerCase().includes(search.toLowerCase()));
  const entry=catalog.find(c=>c.id===selected)||catalog[0];
  const Render=registry[entry.id as keyof typeof registry] as ComponentType;
  const palette=tokenManifest.tokens.filter(t=>t.type==='COLOR'&&!t.external);
  const changeComponent=(id:string)=>{setSelected(id);setPage(0);setOverrides({});const url=new URL(location.href);url.searchParams.set('component',id);history.replaceState(null,'',url);};
  const changeVariant=(key:string,value:string)=>{
    const current={...entry.defaults,...overrides} as Record<string,unknown>;
    const candidates=entry.variants.filter(variant=>(variant as Record<string,string>)[key]===value);
    const score=(variant:Record<string,string>)=>Object.entries(variant).filter(([axis,option])=>axis!==key&&current[axis]===option).length;
    const candidate=[...candidates].sort((a,b)=>score(b)-score(a))[0];
    if(candidate)setOverrides(previous=>({...previous,...candidate as Record<string,string>}));
  };
  return <EuiProvider theme={EuiThemeAmsterdam} colorMode={mode.toUpperCase() as 'LIGHT'|'DARK'} modify={elasticTheme(scale)}>
    <div className={styles.app}>
      <header className={styles.header}><div><span className={styles.eyebrow}>ДИЗАЙН-СИСТЕМА</span><h1>UX-Lab</h1><p>Компоненты, цвета и типографика</p></div><div className={styles.options}><label>Режим Elastic UI<select value={mode} onChange={e=>setMode(e.target.value as 'light'|'dark')}><option value="light">Light</option><option value="dark">Dark</option></select></label><label>Шкала текста<select value={scale} onChange={e=>setScale(e.target.value)}><option value="medium">Medium</option><option value="small">Small</option><option value="x-small">X-small</option></select></label></div></header>
      <nav className={styles.tabs} aria-label="Разделы дизайн-системы">{[['components','Компоненты · 227'],['palette',`Цвета · ${palette.length}`],['typography','Типографика · 29']].map(([id,title])=><button key={id} aria-current={tab===id?'page':undefined} onClick={()=>setTab(id)}>{title}</button>)}</nav>
      {tab==='palette'?<main className={styles.palette}>{palette.map(t=><article key={t.id} className={styles.swatch}><div style={{background:`var(${t.css})`}}/><strong>{t.name}</strong><code>{t.css}</code><small>{t.collection}</small></article>)}</main>:tab==='typography'?<main className={styles.typeList}>{tokenManifest.textStyles.map(t=><article key={t.id}><code>{t.name}</code><p className={t.className}>Исследуйте. Наблюдайте. Улучшайте.</p></article>)}</main>:<div className={styles.workspace}>
        <aside className={styles.sidebar}><label>Найти компонент<input type="search" value={search} placeholder="Button, Table, Field…" onChange={e=>setSearch(e.target.value)}/></label><select aria-label="Источник компонентов" value={group} onChange={e=>setGroup(e.target.value)}><option value="all">Весь каталог</option><option value="product">UX-Lab · 23</option><option value="elastic">Elastic UI · 204</option></select><div className={styles.componentList}>{entries.map(c=><button key={c.id} aria-current={selected===c.id?'page':undefined} data-catalog-select={c.id} onClick={()=>changeComponent(c.id)}><span>{c.name}</span><small>{c.variants.length}</small></button>)}</div></aside>
        <main className={styles.detail} data-current-component={entry.id}><div className={styles.detailHeading}><span className={styles.eyebrow}>{entry.source==='product'?'UX-Lab':'Elastic UI · Amsterdam'}</span><h2>{entry.name}</h2><p>{entry.variants.length} вариантов · <a href={`https://www.figma.com/design/${entry.source==='product'?'1LeVoicxDT7Sl8TpMPs4hr':'SNBSKtwsO81j3BdjRGFpAw'}?node-id=${entry.id.replace(':','-')}`} target="_blank" rel="noreferrer">Источник в Figma ↗</a></p>{entry.deprecated?<p className={styles.notice}>В исходном каталоге компонент помечен Deprecated. Сохранён для соответствия текущему UI Kit.</p>:null}</div>
          <section className={styles.interactive}><h3>Интерактивный пример</h3><div className={styles.axes}>{Object.entries(entry.properties).filter(([,v])=>v.type==='VARIANT').map(([key,prop])=><label key={key}>{key}<select aria-label={key} value={overrides[key]||String(prop.defaultValue)} onChange={e=>changeVariant(key,e.target.value)}>{('variantOptions' in prop?prop.variantOptions as string[]:[]).map(value=><option key={value}>{value}</option>)}</select></label>)}</div>
            {Object.values(entry.properties).some(prop=>prop.type==='TEXT'||prop.type==='BOOLEAN')?<details className={styles.properties}><summary>Текст и дополнительные свойства</summary><div className={styles.axes}>{Object.entries(entry.properties).filter(([,prop])=>prop.type==='TEXT'||prop.type==='BOOLEAN').map(([key,prop])=><label key={key}>{key.split('#')[0]}{prop.type==='BOOLEAN'?<select aria-label={key} value={overrides[key]??String(prop.defaultValue)} onChange={e=>setOverrides(previous=>({...previous,[key]:e.target.value}))}><option value="true">Показать</option><option value="false">Скрыть</option></select>:<input aria-label={key} value={overrides[key]??String(prop.defaultValue)} onChange={e=>setOverrides(previous=>({...previous,[key]:e.target.value}))}/>}</label>)}</div></details>:null}
            <div className={styles.preview}><SampleBoundary key={entry.id+JSON.stringify(overrides)}><Render {...overrides}/></SampleBoundary></div></section>
          <section><div className={styles.variantHeading}><h3>Матрица вариантов</h3><div className={styles.paging}><ProductAction state={page===0?'Disabled':'Default'} label="Предыдущие варианты" onClick={()=>setPage(page-1)}>‹</ProductAction><span>{page+1} / {Math.ceil(entry.variants.length/batchSize)}</span><ProductAction state={(page+1)*batchSize>=entry.variants.length?'Disabled':'Default'} label="Следующие варианты" onClick={()=>setPage(page+1)}>›</ProductAction></div></div><div className={styles.variants}>{entry.variants.slice(page*batchSize,(page+1)*batchSize).map((v,n)=><article key={entry.id+String(page)+n} className={styles.variant}><p className={styles.variantLabel}>{Object.entries(v).map(([key,value])=>`${key}: ${value}`).join(' · ')||'Default'}</p><div className={styles.preview}><SampleBoundary><Render {...v}/></SampleBoundary></div></article>)}</div></section>
          {entry.id==='125:450'?<section className={styles.interactive}><h3>Выбор результата и переход дальше</h3><TaskResultControl/></section>:null}
        </main></div>}
      <footer className={styles.footer}>Источник: ds/index.json и Figma · 204 элемента Elastic UI + 23 компонента UX-Lab. Иконки продукта пока представлены прозрачными местами по директиве React Base.</footer>
    </div>
  </EuiProvider>;
}
type ComponentType = React.ComponentType<CatalogProps>;
