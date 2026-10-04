import { useEffect, useRef, useState } from 'react';
import { EuiCallOut, EuiLink, EuiTab, EuiTabs } from '@elastic/eui';
import { ProductButton } from '../components';
import { ProductDropdown } from '../components/_shared/ProductDropdown';
import { DesignIcon } from '../components/_shared/CatalogComponent';
import { Empty, Table } from '../screens/WorkspaceUI';
import { useResearch } from '../data/researchStore';
import { useWireRoute } from '../screens/useWireRoute';
import { CLICK_API, LOCAL_VERSION, pageLabels, targetLabels, type ClickData } from './types';
import s from './LocalHeatmap.module.css';
import w from '../screens/Workspace.module.css';
import { CapturedHeatmap } from './CapturedHeatmap';
import { HeatmapDownload } from './HeatmapDownload';

const empty:ClickData={groups:[],total:{clicks:0,sessions:0},points:[],sessions:[]};
export function LocalHeatmap({refreshRevision=0,onRefreshResult}:{refreshRevision?:number;onRefreshResult?:(revision:number,ok:boolean)=>void}) {
  const store=useResearch(),{route,navigate}=useWireRoute();
  const study=store.live?route.study:route.link||store.study.id;
  const session=route.heatmapSession;
  const [receivedData,setData]=useState<ClickData>(empty),[group,setGroup]=useState(''),[mode,setMode]=useState('all');
  const [error,setError]=useState(''),[loading,setLoading]=useState(true),[revision,setRevision]=useState(0),[updated,setUpdated]=useState('');
  const [target,setTarget]=useState(''),[layer,setLayer]=useState(true),[previewError,setPreviewError]=useState('');
  const [hoverTarget,setHoverTarget]=useState('');
  const [responseKey,setResponseKey]=useState(''),[scale,setScale]=useState(1);
  const matchingScope=responseKey.startsWith(`${study}:${session}:`);
  const data=matchingScope?receivedData:empty;
  const [exporting,setExporting]=useState<'png'|'zip'|''>(''),[exportError,setExportError]=useState('');
  const exportLock=useRef(false);
  const requestedPage=useRef('');
  const preview=useRef<HTMLDivElement>(null);
  const frame=useRef<HTMLIFrameElement>(null);
  const selected=data.groups.find(item=>item.layout===group);
  const origin=location.port==='6006'?'http://127.0.0.1:5173':location.origin;
  const leed=study.startsWith('leed')||selected?.page.startsWith('leed-');
  const previewOrigin=selected?.page.startsWith('leed-')?'http://127.0.0.1:5175':origin;
  const saveMap=async(format:'png'|'zip')=>{
    if(exportLock.current||!selected)return;
    exportLock.current=true;setExporting(format);setExportError('');
    try {
      const params=new URLSearchParams({study,session,mode,format,layer:layer?'1':'0'});
      if(format==='png'){params.set('group',selected.layout);if(target)params.set('target',target);}
      const response=await fetch(`${CLICK_API}/api/heatmap/export?${params}`,{signal:AbortSignal.timeout(190000)});
      if(!response.ok)throw Error(response.status===409?'Другая выгрузка ещё выполняется. Повторите чуть позже.':'Не удалось сохранить карты. Проверьте, что локальный сервер и тестовый интерфейс запущены, и повторите.');
      const url=URL.createObjectURL(await response.blob());
      const link=document.createElement('a');link.href=url;
      const scope=session?`-session-${session.slice(0,8)}`:'-all-sessions';
      link.download=format==='png'?`${selected.page}-${selected.vw}x${selected.vh}-${mode}${scope}.png`:`heatmaps-${study}-${mode}${scope}.zip`;
      document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);
    }catch(cause){setExportError(cause instanceof Error?cause.message:'Не удалось сохранить карты.');}
    finally {exportLock.current=false;setExporting('');}
  };
  const previewUrl=selected?(selected.path?`${previewOrigin}${selected.path}?ux_preview=1&parentOrigin=${encodeURIComponent(location.origin)}`:`${origin}/?screen=heatmap-target&preview=1&page=${selected.page}&parentOrigin=${encodeURIComponent(location.origin)}`):'';
  useEffect(()=>{
    let cancelled=false,busy=false;const controller=new AbortController();
    const read=async()=>{
      if(busy)return;busy=true;
      try {
        const response=await fetch(`${CLICK_API}/api/heatmap?${new URLSearchParams({study,session,group,mode,aggregation:'page'})}`,{signal:AbortSignal.any([controller.signal,AbortSignal.timeout(10000)])});
        if(!response.ok)throw Error('Локальный сервер не ответил. Проверьте его запуск.');
        const next=await response.json() as ClickData;
        if(cancelled)return;
        setData(next);setResponseKey(`${study}:${session}:${group}:${mode}`);setError('');setUpdated(new Date().toLocaleTimeString('ru-RU'));
        onRefreshResult?.(refreshRevision,true);
        if(route.item.startsWith('page:')&&requestedPage.current!==route.item){
          requestedPage.current=route.item;
          const requested=next.groups.find(item=>item.page===route.item.slice(5));
          if(requested){setGroup(requested.layout);setTarget('');return;}
        }
        if(!next.groups.some(item=>item.layout===group)){setGroup(next.groups[0]?.layout||'');setTarget('');}
      } catch(cause) {if(!cancelled){setError(cause instanceof Error?cause.message:'Не удалось загрузить клики');onRefreshResult?.(refreshRevision,false);}}
      finally {busy=false;if(!cancelled)setLoading(false);}
    };
    void read();const timer=setInterval(read,2000);
    return()=>{cancelled=true;controller.abort();clearInterval(timer);};
  },[study,session,group,mode,revision,refreshRevision,route.item,onRefreshResult]);
  const currentPoints=responseKey===`${study}:${session}:${group}:${mode}`?data.points:[];
  const points=target?currentPoints.filter(point=>point.target===target):currentPoints;
  const clicks=points.reduce((sum,point)=>sum+point.count,0),sessions=[...new Set(points.flatMap(point=>point.sessions))];
  const targets=[...new Set(currentPoints.map(point=>point.target))];
  const elementName=(id:string)=>{
    const name=currentPoints.find(point=>point.target===id&&point.element)?.element?.label||targetLabels[id];
    if(name){
      const peers=targets.filter(other=>currentPoints.find(point=>point.target===other&&point.element)?.element?.label===name);
      return peers.length>1?`${name} · ${peers.indexOf(id)+1}`:name;
    }
    const type=id.startsWith('button-')?'Кнопка без названия':/^(input|textarea)-/.test(id)?'Поле без названия':'Область без названия';
    return `${type} · ${targets.indexOf(id)+1}`;
  };
  const highlightPoints=currentPoints.filter(point=>point.target===(hoverTarget||target));
  const previewWidth=selected?.vw;
  useEffect(()=>{
    const element=preview.current;if(!element||!previewWidth)return;
    const measure=()=>setScale(Math.min(1,element.clientWidth/previewWidth));
    measure();const observer=new ResizeObserver(measure);observer.observe(element);
    return()=>observer.disconnect();
  },[previewWidth]);
  const send=()=>{
    const styles=preview.current?getComputedStyle(preview.current):null;
    const palette=['--heatmap-spot-core','--heatmap-spot-middle','--heatmap-spot-outer'].map(token=>styles?.getPropertyValue(token).trim());
    if(selected)frame.current?.contentWindow?.postMessage({type:'ux-lab-heatmap',points:layer?points:[],rw:selected.rw,rh:selected.rh,version:selected.version,context:selected.context,palette},previewOrigin);
  };
  useEffect(()=>{
    const receive=(event:MessageEvent)=>{
      if(event.origin!==previewOrigin||event.source!==frame.current?.contentWindow)return;
      if(event.data?.type==='ux-lab-preview-ready')send();
      if(event.data?.type==='ux-lab-preview-status')setPreviewError(event.data.matches?'':'Это состояние страницы отличается от исходного: например, открыта модалка или изменены данные. Клики сохранены в статистике; слой скрыт, поскольку фон не совпадает.');
    };
    addEventListener('message',receive);send();
    return()=>removeEventListener('message',receive);
  });
  return <>
    {!store.live?<div className={w.between}><EuiLink onClick={()=>navigate({screen:'heatmap',link:'',item:''})}>К демонстрационной карте</EuiLink><ProductButton Kind="Secondary" onClick={()=>setRevision(value=>value+1)}>Обновить клики</ProductButton></div>:null}
    <section className={s.filterPanel} aria-label="Параметры тепловой карты"><div className={s.filterFields}>
    <div title="Сессия — отдельное посещение во вкладке браузера. У одного участника может быть несколько сессий."><ProductDropdown appearance="field" label="Сессия участника" value={session} onChange={value=>{setTarget('');setHoverTarget('');setPreviewError('');setExportError('');navigate({heatmapSession:value,item:''});}} options={[
      {value:'',label:'Все участники (все сессии)'},
      ...(receivedData.availableSessions||[]).map(item=>({value:item.id,label:`Сессия ${item.id.slice(0,8)} · ${new Date(item.startedAt).toLocaleString('ru-RU',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'})} · ${item.clicks} кликов`})),
      ...(session&&!receivedData.availableSessions?.some(item=>item.id===session)?[{value:session,label:`Сессия ${session.slice(0,8)}`}]:[])
    ]}/></div>
      <ProductDropdown appearance="field" label="Экран" value={selected?.page||''} disabled={!data.groups.length} placeholder="Нет экранов" onChange={value=>{setGroup(data.groups.find(item=>item.page===value)?.layout||'');setTarget('');setPreviewError('');}} options={[...new Set(data.groups.map(item=>item.page))].map(page=>({value:page,label:`${pageLabels[page]||data.groups.find(item=>item.page===page)?.path||page} · ${data.groups.filter(item=>item.page===page).reduce((sum,item)=>sum+item.clicks,0)} кликов`}))}/>
      <ProductDropdown appearance="field" label="Размер окна" value={group} disabled={!selected} placeholder="Нет размеров" onChange={value=>{setGroup(value);setTarget('');}} options={data.groups.filter(item=>item.page===selected?.page).map(item=>({value:item.layout,label:`${item.vw} × ${item.vh} · ${item.clicks} кликов`}))}/>
    </div><div className={s.filterFooter}>
      <EuiTabs className={s.filterTabs} aria-label="Режим реальной карты" title="Все клики — все нажатия на экране. Первый клик — одно первое нажатие на экран за сессию."><EuiTab isSelected={mode==='all'} onClick={()=>{setMode('all');setTarget('');}}>Все клики</EuiTab><EuiTab isSelected={mode==='first'} onClick={()=>{setMode('first');setTarget('');}}>Первый клик</EuiTab></EuiTabs>
      <div className={s.filterStatus}><span className={s.selectionCount}>{responseKey===`${study}:${session}:${group}:${mode}`?`Клики: ${clicks} · Сессии: ${sessions.length}`:'Обновляем выборку…'}</span><span className={w.muted}>Обновлено {matchingScope?updated||'—':'—'}</span></div>
    </div></section>
    {error?<EuiCallOut color="danger" title="Нет связи с локальным сборщиком"><p>{error}</p><p>Запуск: python execution/serve_heatmap.py. Последние полученные данные сохранены на экране.</p></EuiCallOut>:null}
    {!data.groups.length?<Empty>{loading||!matchingScope?'Загружаем клики…':session?'В этой сессии нет собранных кликов. Выберите другую сессию или всех участников.':'Пока нет собранных кликов. Откройте подключённый интерфейс и выполните несколько действий.'}</Empty>:<>
      {previewError&&!leed?<EuiCallOut color="warning" title={previewError}/>:null}
      {exportError?<EuiCallOut color="danger" title="Не удалось скачать"><p>{exportError}</p></EuiCallOut>:null}
        <div className={`${w.between} ${s.mapHeading}`}><h2>{pageLabels[selected?.page||'']||selected?.path} · {clicks} кликов</h2><div className={s.exportActions}><EuiLink className={s.layerToggle} onClick={()=>setLayer(!layer)}><DesignIcon type={layer?'eyeClosed':'eye'}/>{layer?'Скрыть клики':'Показать клики'}</EuiLink>{leed?<HeatmapDownload busy={!!exporting} disabled={!selected} onDownload={format=>void saveMap(format)}/>:null}</div></div>
      <div className={`${w.columns} ${s.liveColumns}`}><div className={w.stack}>
        {leed&&selected?<CapturedHeatmap key={selected.layout} group={selected} points={layer?points:[]} highlightPoints={highlightPoints}/>:<div ref={preview} className={s.preview}>{selected?<div style={{position:'relative',width:selected.vw*scale,height:Math.max(selected.vh,selected.rh+80)*scale}}><iframe key={selected.layout} ref={frame} title="Карта реальных кликов NOVA" src={previewUrl} style={{position:'absolute',pointerEvents:'none',width:selected.vw,height:Math.max(selected.vh,selected.rh+80),transform:`scale(${scale})`,transformOrigin:'top left'}} onLoad={send}/></div>:null}</div>}
        <div className={s.densityLegend}><span>Меньше кликов</span><div/><span>Больше кликов</span></div>
        <p className={w.muted}>{leed?'Общая плотность по координатам окна, включая клики в открытых панелях. Фон — один сохранённый вид экрана; при его отсутствии используется исходный интерфейс.':`Фон — воспроизведение ${selected?.version||LOCAL_VERSION} в исходном размере окна.`}</p>
      </div><section className={s.elementsCard} aria-label="Элементы выбранной карты"><div className={s.elementsHeading}><h2>{target?elementName(target):'Вся страница'}</h2>
        <p aria-live="polite" data-testid="real-click-count">{clicks} кликов · {sessions.length} сессий</p></div>
        {target?<ProductButton Kind="Tertiary" onClick={()=>{setTarget('');setHoverTarget('');}}>Показать все клики</ProductButton>:null}
        <h3>Элементы</h3>
        <p className={w.muted}>Наведите на строку, чтобы подсветить область на карте. Нажмите на название, чтобы оставить её клики.</p>
        {leed&&currentPoints.some(point=>!point.element)?<p className={w.muted}>В старых записях название и границы не сохранены: для них подсвечиваются места кликов.</p>:null}
        <div className={s.elementRows}><Table label="Собранные клики по элементам" headers={['Элемент','Клики']}>{targets.map(id=><tr key={id} aria-selected={id===target} onClick={()=>setTarget(id)} onMouseEnter={()=>setHoverTarget(id)} onMouseLeave={()=>setHoverTarget('')} onFocus={()=>setHoverTarget(id)} onBlur={()=>setHoverTarget('')}><td><EuiLink onClick={()=>setTarget(id)}>{elementName(id)}</EuiLink></td><td>{currentPoints.filter(point=>point.target===id).reduce((sum,point)=>sum+point.count,0)}</td></tr>)}</Table></div>
        {!clicks?<p>Для этого представления нет кликов.</p>:null}
        <details className={s.sessionDetails}><summary>Сессии этой выборки · {sessions.length}</summary><ul className={s.sessionList}>{sessions.map(id=><li key={id}>{store.live?<EuiLink onClick={()=>navigate({screen:'participant',participant:id,item:''})}>{id}</EuiLink>:id}</li>)}</ul><p className={w.muted}>Сессия соответствует посещению в одной вкладке браузера.</p></details></section></div>
    </>}
  </>;
}
