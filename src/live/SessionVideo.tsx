import {useEffect,useRef,useState} from 'react';
import {EuiCallOut,EuiLink} from '@elastic/eui';
import {currentStudy} from './api';
import {ProductButton} from '../components';
import {ProductDropdown} from '../components/_shared/ProductDropdown';
import {Card} from '../screens/WorkspaceUI';
import {CLICK_API,pageLabels} from '../heatmap/types';
import type {LiveEvent} from './types';
import s from './SessionVideo.module.css';

type Video={id:string;session:string;startedAt:number;duration:number;status:'ready'|'uploading';interrupted:boolean};
const time=(seconds:number)=>`${Math.floor(seconds/60)}:${String(Math.floor(seconds%60)).padStart(2,'0')}`;
export function SessionVideo({session,events,requestedTime=0,hideIfEmpty=false}:{session:string;events:LiveEvent[];requestedTime?:number;hideIfEmpty?:boolean}){
  const [records,setRecords]=useState<Video[]>([]),[error,setError]=useState(''),[loaded,setLoaded]=useState(false),[selected,setSelected]=useState('');
  useEffect(()=>{let disposed=false,busy=false;const controller=new AbortController();async function read(){if(busy)return;busy=true;try{const response=await fetch(`${CLICK_API}/api/recordings?session=${encodeURIComponent(session)}&study=${encodeURIComponent(currentStudy())}`,{signal:controller.signal});if(!response.ok)throw Error('Не удалось загрузить видеозаписи.');const next=await response.json() as Video[];if(!disposed){setRecords(next);setError('');}}catch(e){if(!disposed)setError(e instanceof Error?e.message:'Не удалось загрузить видео.');}finally{busy=false;if(!disposed)setLoaded(true);}}void read();const timer=setInterval(()=>void read(),3000);return()=>{disposed=true;controller.abort();clearInterval(timer);};},[session]);
  const ready=records.filter(record=>record.status==='ready'),record=ready.find(item=>item.id===selected)||ready.find(item=>requestedTime>=item.startedAt&&requestedTime<=item.startedAt+item.duration*1000)||ready[0];
  if(hideIfEmpty&&!records.length&&!error)return null;
  return <Card><h2>Видеозапись теста</h2>{error?<EuiCallOut color="danger" title={error}/>:null}
    {ready.length>1?<ProductDropdown appearance="field" label="Фрагмент записи" value={record?.id||''} options={ready.map((item,index)=>({value:item.id,label:`Запись ${index+1} · ${new Date(item.startedAt).toLocaleTimeString('ru-RU')} · ${time(item.duration)}`}))} onChange={setSelected}/>:null}
    {record?<VideoPlayer key={record.id} record={record} events={events} requestedTime={requestedTime}/>:<><p>{!loaded?'Загружаем видео…':records.length?'Запись идёт или ещё передаётся. Плеер появится после завершения и сохранения.':'Для этой сессии видео не записывалось. Сохранены только события и отдельные снимки.'}</p><p>Для нового теста откройте интерфейс через раздел «Проверка и запуск». В Lead Generation нажмите «Начать запись теста», выберите вкладку в окне браузера, а после теста — «Завершить запись».</p></>}
    {record&&records.some(item=>item.status==='uploading')?<p role="status">Ещё один фрагмент записывается или передаётся.</p>:null}
  </Card>;
}
function VideoPlayer({record,events,requestedTime}:{record:Video;events:LiveEvent[];requestedTime:number}){
  const video=useRef<HTMLVideoElement>(null);const [position,setPosition]=useState(0),[playing,setPlaying]=useState(false),[ready,setReady]=useState(false),[rate,setRate]=useState('1'),[error,setError]=useState('');
  const relevant=events.filter(event=>event.timestamp>=record.startedAt&&event.timestamp<=record.startedAt+record.duration*1000);
  useEffect(()=>{if(ready&&video.current&&requestedTime>=record.startedAt&&requestedTime<=record.startedAt+record.duration*1000)video.current.currentTime=(requestedTime-record.startedAt)/1000;},[requestedTime,ready,record.startedAt,record.duration]);
  const seek=(value:number)=>{if(video.current){video.current.currentTime=Math.max(0,Math.min(record.duration,value));setPosition(video.current.currentTime);}};
  const toggle=async()=>{const el=video.current;if(!el)return;if(!el.paused)el.pause();else try{if(el.ended)el.currentTime=0;await el.play();}catch{setError('Не удалось воспроизвести видео. Повторите или скачайте запись.');}};
  return <div className={s.player}>
    {record.interrupted?<EuiCallOut color="warning" title="Сохранена доступная часть записи"><p>Запись завершилась неожиданно. Последние секунды могли не сохраниться.</p></EuiCallOut>:null}
    <video ref={video} className={s.video} aria-label="Видео прохождения теста" src={`${CLICK_API}/api/recordings/media?id=${record.id}&study=${encodeURIComponent(currentStudy())}`} playsInline preload="metadata" onLoadedMetadata={()=>{setReady(true);if(requestedTime>=record.startedAt)seek((requestedTime-record.startedAt)/1000);}} onTimeUpdate={()=>setPosition(video.current?.currentTime||0)} onPlay={()=>setPlaying(true)} onPause={()=>setPlaying(false)} onEnded={()=>setPlaying(false)} onError={()=>setError('Видео недоступно или формат не поддерживается браузером.')} onClick={()=>void toggle()}/>
    {error?<EuiCallOut color="danger" title={error}/>:null}
    <div className={s.timeline}><input type="range" min="0" max={record.duration} step="0.1" value={position} disabled={!ready} aria-label="Временная шкала записи" aria-valuetext={`${time(position)} из ${time(record.duration)}`} onChange={event=>seek(Number(event.target.value))}/><div className={s.markers} aria-label="Моменты событий">{relevant.map(event=><button key={event.id} style={{left:`${(event.timestamp-record.startedAt)/(record.duration*10)}%`}} title={`${time((event.timestamp-record.startedAt)/1000)} · ${event.context?.element?.label||pageLabels[event.page]||'Событие'}`} aria-label={`Перейти к событию ${time((event.timestamp-record.startedAt)/1000)}`} onClick={()=>seek((event.timestamp-record.startedAt)/1000)}/>)}</div></div>
    <div className={s.controls}><ProductButton Kind="Primary" State={ready?'Default':'Disabled'} icon={playing?'pause':'play'} onClick={()=>void toggle()}>{playing?'Пауза':'Воспроизвести'}</ProductButton><ProductButton Kind="Tertiary" State={ready?'Default':'Disabled'} onClick={()=>seek(position-10)}>−10 с</ProductButton><ProductButton Kind="Tertiary" State={ready?'Default':'Disabled'} onClick={()=>seek(position+10)}>+10 с</ProductButton><span>{time(position)} / {time(record.duration)}</span><ProductDropdown label="Скорость видео" value={rate} options={['0.5','1','1.5','2'].map(value=>({value,label:`${value}×`}))} onChange={value=>{setRate(value);if(video.current)video.current.playbackRate=Number(value);}}/><EuiLink href={`${CLICK_API}/api/recordings/media?id=${record.id}&study=${encodeURIComponent(currentStudy())}&download=1`}>Скачать видео</EuiLink></div>
    {relevant.length?<details><summary>События на временной шкале · {relevant.length}</summary><div className={s.events}>{relevant.map(event=><button key={event.id} onClick={()=>seek((event.timestamp-record.startedAt)/1000)}><time>{time((event.timestamp-record.startedAt)/1000)}</time><span>{event.kind==='visit'?`Открыт экран: ${pageLabels[event.page]||event.page}`:event.context?.element?.label||'Клик по области'}</span></button>)}</div></details>:null}
  </div>;
}
