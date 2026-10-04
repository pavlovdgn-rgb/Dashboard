import { useRef, useState } from 'react';
import { DesignIcon, type VariantValues } from './CatalogComponent';
import { ProductAction } from './ProductComponent';
import { useVariantState } from './useVariantState';
import styles from './ProductComponent.module.css';

const seconds=(label:string)=>label.trim().split(':').reduce((total,n)=>total*60+Number(n),0);
const time=(value:number)=>`${String(Math.floor(value/60)).padStart(2,'0')}:${String(Math.floor(value%60)).padStart(2,'0')}`;
export function ReplayPreview({values:p}:{values:VariantValues}) {
  const root=useRef<HTMLElement>(null);
  const supplied=String(p.PositionLabel??Object.entries(p).find(([key])=>key.startsWith('PositionLabel#'))?.[1]??'02:18 / 04:32').split('/');
  const total=Number(p.duration??seconds(supplied[1]||'04:32'))||272;
  const [position,setPosition]=useVariantState(Math.min(total,Number(p.position??seconds(supplied[0]))||0));
  const [playing,setPlaying]=useVariantState(p.Playback==='Playing');
  const [speed,setSpeed]=useState(1);
  const [fullscreen,setFullscreen]=useState(false);
  const [fit,setFit]=useState(true);
  const notify=(key:string,value:unknown)=>{if(typeof p[key]==='function')p[key](value);};
  const seek=(next:number)=>{const value=Math.max(0,Math.min(total,next));setPosition(value);notify('onSeek',value);};
  const togglePlayback=()=>{setPlaying(!playing);notify('onPlaybackChange',!playing);notify('onChange',!playing);};
  const ticks=[0,48,96,144,192,total].filter((value,n,all)=>value<=total&&all.indexOf(value)===n);
  return <section ref={root} className={styles.card+' '+styles.replay}>
    <div className={styles.timeLabels}>{ticks.map(t=><span key={t} data-end={t===total} data-start={t===0} style={{left:`${t/total*100}%`}}>{time(t)}</span>)}</div>
    <div className={styles.timeline}>
      <span className={styles.played} style={{width:`${position/total*100}%`}}/>
      {p.Coverage==='Gap'?<span className={styles.gap} style={{left:`${100/total*100}%`,width:`${25/total*100}%`}}/>:null}
      {[48,96,126,144].filter(t=>t<=total).map(t=><span key={t} className={styles.replayEvent} style={{left:`${t/total*100}%`}}><DesignIcon type="dot"/></span>)}
      <span className={styles.playhead} style={{left:`${position/total*100}%`}}/>
      <input className={styles.seekInput} type="range" min={0} max={total} value={position} aria-label="Позиция записи" aria-valuetext={`${time(position)} из ${time(total)}`} onChange={e=>seek(Number(e.target.value))}/>
    </div>
    <p className={styles.coverageLegend}><span data-gap={p.Coverage==='Gap'}/>{p.Coverage==='Gap'?'Нет данных с 01:40 до 02:05 · разрыв записи сессии':'Запись доступна на всём интервале'}</p>
    <div className={styles.replayToolbar}><div className={styles.row}>
      <ProductAction kind="Playback" onClick={togglePlayback} icon={playing?'pause':'playFilled'}>{playing?'Пауза':'Воспроизвести'}</ProductAction>
      <ProductAction onClick={()=>seek(position-5)} icon="arrowLeft">−5 с</ProductAction><ProductAction onClick={()=>seek(position+5)} iconRight="arrowRight">+5 с</ProductAction>
      <output aria-label="Время записи">{time(position)} / {time(total)}</output>
    </div><div className={styles.row}>
      <span className={styles.muted}>Скорость:</span>{[1,1.5,2].map(s=><button key={s} className={styles.speed} aria-pressed={speed===s} onClick={()=>{setSpeed(s);notify('onSpeedChange',s);}}>{s}×</button>)}
      <button className={styles.viewAction} aria-pressed={fit} onClick={()=>{setFit(!fit);notify('onFitChange',!fit);}}><DesignIcon type="scale"/>Вписать</button>
      <ProductAction icon="fullScreen" onClick={()=>{if(typeof p.onFullscreen==='function'){notify('onFullscreen',!fullscreen);setFullscreen(!fullscreen);return;}if(document.fullscreenElement){void document.exitFullscreen();setFullscreen(false);}else if(root.current?.requestFullscreen){void root.current.requestFullscreen().then(()=>setFullscreen(true)).catch(()=>setFullscreen(false));}}}>{fullscreen?'Выйти из полного экрана':'На весь экран'}</ProductAction>
    </div></div>
    <p className={styles.muted}>Содержимое полей — демонстрационные данные. Камера и голос не записываются.</p>
  </section>;
}
