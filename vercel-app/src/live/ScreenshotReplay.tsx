import {useEffect,useState} from 'react';
import {EuiCallOut} from '@elastic/eui';
import {ProductButton} from '../components';
import {Card} from '../screens/WorkspaceUI';
import {CapturedHeatmap} from '../heatmap/CapturedHeatmap';
import {pageLabels} from '../heatmap/types';
import {liveApi} from './api';
import type {ReplayFrame} from './types';
import s from './ScreenshotReplay.module.css';

const label=(frame:ReplayFrame)=>frame.kind==='screen'?`Открыт экран: ${pageLabels[frame.page]||frame.page}`:frame.kind==='click'?`Нажатие: ${frame.label}`:frame.kind==='scroll'?'Прокрутка экрана':'Состояние после действия';
const elapsed=(value:number)=>`${Math.floor(value/60000)}:${String(Math.floor(value/1000)%60).padStart(2,'0')}`;
export function ScreenshotReplay({session,requestedTime=0}:{session:string;requestedTime?:number}){
  const [frames,setFrames]=useState<ReplayFrame[]>([]),[error,setError]=useState(''),[loaded,setLoaded]=useState(false),[position,setPosition]=useState(0),[playing,setPlaying]=useState(false);
  useEffect(()=>{let disposed=false,busy=false;const read=async()=>{if(busy)return;busy=true;try{const result=await liveApi<{frames:ReplayFrame[]}>(`/frames?session=${encodeURIComponent(session)}`);if(!disposed){setFrames(result.frames);setError('');}}catch{if(!disposed)setError('Не удалось загрузить снимки. Повторяем подключение.');}finally{busy=false;if(!disposed)setLoaded(true);}};void read();const timer=setInterval(()=>void read(),2000);return()=>{disposed=true;clearInterval(timer);};},[session]);
  useEffect(()=>{if(requestedTime&&frames.length)setPosition(Math.max(0,frames.findIndex(frame=>frame.timestamp>=requestedTime)));},[requestedTime,frames.length]);
  useEffect(()=>{if(!playing)return;if(position>=frames.length-1){setPlaying(false);return;}const timer=setTimeout(()=>setPosition(value=>value+1),1000);return()=>clearTimeout(timer);},[playing,position,frames.length]);
  const index=Math.min(position,Math.max(0,frames.length-1)),frame=frames[index],first=frames[0];
  const select=(value:number)=>{setPlaying(false);setPosition(value);};
  return <Card><h2>Скриншоты действий</h2>{error?<EuiCallOut color="warning" title={error}/>:null}
    {!frame?<p>{loaded?'В этой сессии пока нет снимков действий. Они появятся после включения этого формата записи и новых действий участника.':'Загружаем снимки…'}</p>:<>
      <p>{label(frame)} · {new Date(frame.timestamp).toLocaleTimeString('ru-RU')} · кадр {index+1} из {frames.length}</p>
      <div className={s.layout}><div className={s.viewer}><CapturedHeatmap onlySaved group={{layout:frame.id,page:frame.page,version:'leed-local-v2',vw:frame.vw,vh:frame.vh,rw:frame.vw,rh:frame.vh,clicks:0,sessions:1,context:{signature:frame.snapshot,scrolls:[],snapshot:frame.snapshot}}} points={[]} highlightPoints={frame.kind==='click'&&frame.target.x!==undefined?[{x:frame.target.x,y:frame.target.y!,target:frame.id,count:1,sessions:[frame.session],...(frame.target.rect?{element:{label:frame.label,rect:frame.target.rect}}:{})}]:[]}/></div>
        <div className={s.frames} aria-label="Снимки по времени">{frames.map((item,i)=><button key={item.id} aria-current={i===index?'step':undefined} onClick={()=>select(i)}><time>{elapsed(item.timestamp-first.timestamp)}</time><span>{label(item)}</span></button>)}</div></div>
      <input className={s.timeline} type="range" min="0" max={frames.length-1} value={index} step="1" aria-label="Временная шкала снимков" aria-valuetext={`Кадр ${index+1} из ${frames.length}, ${elapsed(frame.timestamp-first.timestamp)}`} onChange={event=>select(Number(event.target.value))}/>
      <div className={s.controls}><ProductButton Kind="Secondary" icon={playing?'pause':'play'} State={frames.length<2?'Disabled':'Default'} onClick={()=>{if(!playing&&index===frames.length-1)setPosition(0);setPlaying(!playing);}}>{playing?'Пауза':'Воспроизвести снимки'}</ProductButton><ProductButton Kind="Tertiary" icon="arrowLeft" State={index===0?'Disabled':'Default'} onClick={()=>select(index-1)}>Предыдущий кадр</ProductButton><ProductButton Kind="Tertiary" iconRight="arrowRight" State={index===frames.length-1?'Disabled':'Default'} onClick={()=>select(index+1)}>Следующий кадр</ProductButton><span>{elapsed(frame.timestamp-first.timestamp)} · 1 кадр/с</span></div>
      <p>Сохранённые состояния интерфейса по действиям. Значения полей скрыты; это не непрерывное видео.</p>
    </>}
  </Card>;
}
