import {useEffect,useRef,useState} from 'react'
import {beginVideo,finishVideo,flushVideos,saveVideoChunk,startVideoQueue,videoQueueState,type RecordingJob} from './videoQueue'
import {videoEnabled,recordingMode,studyInstructions} from './activity'
import './recording.css'
import {taskState} from './task'
import {StudyTask} from './StudyTask'

export function RecordingControls(){
  const [task,setTask]=useState(studyInstructions),[run,setRun]=useState(taskState)
  useEffect(()=>{const update=()=>setRun(taskState());addEventListener('ux-task-state',update);return()=>removeEventListener('ux-task-state',update)},[])
  useEffect(()=>{const update=()=>setTask(studyInstructions());addEventListener('ux-lab-policy',update);return()=>removeEventListener('ux-lab-policy',update)},[])
  if(new URLSearchParams(location.search).get('ux_preview')==='1'||!['127.0.0.1','localhost'].includes(location.hostname))return null
  return <div className="ux-participant-controls" data-ux-private="true" data-ux-overlay="true"><StudyTask studyTitle={task.studyTitle} scenario={run.run?.scenario||(task.mode==='scenario'?task.scenario:'')}/><RecordingControlsBody/></div>
}
function RecordingControlsBody(){
  const [allowed,setAllowed]=useState(videoEnabled),[mode,setMode]=useState(recordingMode)
  const [phase,setPhase]=useState<'idle'|'choosing'|'recording'|'saving'|'saved'>('idle'),[error,setError]=useState(''),[seconds,setSeconds]=useState(0),[queue,setQueue]=useState(videoQueueState),[recordedSession,setRecordedSession]=useState('')
  const recorder=useRef<MediaRecorder|null>(null),pending=useRef<Promise<void>>(Promise.resolve()),started=useRef(0),mounted=useRef(true)
  useEffect(()=>{mounted.current=true;startVideoQueue();const update=()=>setQueue(videoQueueState());addEventListener('ux-video-queue',update);const timer=setInterval(()=>{setAllowed(videoEnabled());setMode(recordingMode());if(recorder.current?.state==='recording'){setSeconds(Math.floor((performance.now()-started.current)/1000));if(!videoEnabled()||performance.now()-started.current>=1800000)recorder.current.stop()}},500);const leaving=(event:BeforeUnloadEvent)=>{if(recorder.current?.state==='recording'||videoQueueState().pending){event.preventDefault();event.returnValue=''}};addEventListener('beforeunload',leaving);return()=>{mounted.current=false;clearInterval(timer);removeEventListener('ux-video-queue',update);removeEventListener('beforeunload',leaving);if(recorder.current?.state==='recording')recorder.current.stop()}},[])
  const stop=()=>{if(recorder.current?.state==='recording'){setPhase('saving');recorder.current.stop()}}
  async function start(){
    const session=(window.__uxLabStatus as {session?:string}|undefined)?.session
    if(!session){setError('Сборщик ещё запускается. Повторите через несколько секунд.');return}
    if(!videoEnabled()){setError('Видеозапись выключена или сбор исследования приостановлен. Проверьте настройки в дашборде.');return}
    if(!navigator.mediaDevices?.getDisplayMedia||!window.MediaRecorder){setError('Для записи откройте приложение в Chrome или Edge на компьютере.');return}
    const mime=['video/webm;codecs=vp8','video/webm;codecs=vp9','video/webm'].find(type=>MediaRecorder.isTypeSupported(type))
    if(!mime){setError('Этот браузер не поддерживает запись WebM. Откройте Chrome или Edge.');return}
    setPhase('choosing');setError('');let stream:MediaStream|undefined
    try {
      const options:DisplayMediaStreamOptions&{preferCurrentTab:boolean}={video:{displaySurface:'browser',frameRate:15},audio:false,preferCurrentTab:true}
      stream=await navigator.mediaDevices.getDisplayMedia(options)
      if(!mounted.current){stream.getTracks().forEach(track=>track.stop());return}
      if(!videoEnabled()){stream.getTracks().forEach(track=>track.stop());setPhase('idle');setError('Видеозапись отключена в настройках исследования.');return}
      const capture=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:1000000})
      const job:RecordingJob={id:crypto.randomUUID(),study:sessionStorage.getItem('ux-lab-leed-study')||'leed-local',session,startedAt:Date.now(),mime,chunks:0,duration:0,finished:false,interrupted:false}
      await beginVideo(job)
      setRecordedSession(`${encodeURIComponent(session)}&study=${encodeURIComponent(job.study)}`)
      let bytes=0,failure=false
      recorder.current=capture;started.current=performance.now();pending.current=Promise.resolve()
      capture.ondataavailable=event=>{if(!event.data.size)return;bytes+=event.data.size;const end=(performance.now()-started.current)/1000;pending.current=pending.current.then(async()=>{job.duration=end;await saveVideoChunk(job,event.data)}).catch(()=>{failure=true;setError('Не удалось сохранить видео в браузере. Освободите место на диске и начните новую запись.');stop()});if(bytes>240*1024*1024)stop()}
      capture.onstop=()=>{stream!.getTracks().forEach(track=>track.stop());recorder.current=null;if(mounted.current)setPhase('saving');void pending.current.then(async()=>{if(!failure&&job.chunks){await finishVideo(job);if(mounted.current)setPhase('saved')}else if(mounted.current)setPhase('idle')}).catch(()=>{if(mounted.current){setError('Не удалось завершить сохранение видео.');setPhase('idle')}})}
      capture.onerror=()=>{job.interrupted=true;setError('Запись прервалась. Сохраняем доступную часть.');stop()}
      stream.getVideoTracks()[0].addEventListener('ended',stop)
      capture.start(2000);setSeconds(0);setPhase('recording')
    }catch(cause){stream?.getTracks().forEach(track=>track.stop());setPhase('idle');setError(cause instanceof DOMException&&cause.name==='NotAllowedError'?'Запись не началась: разрешение не выдано. Можно продолжать тест без видео.':'Не удалось начать запись. Проверьте разрешение на захват экрана.')}
  }
  if(new URLSearchParams(location.search).get('ux_preview')==='1'||!['127.0.0.1','localhost'].includes(location.hostname))return null
  if(mode==='screenshots'&&(phase==='idle'||phase==='saved')&&!queue.pending&&!queue.error)return null
  return <aside className="ux-recording" data-ux-private="true" data-ux-overlay="true" aria-label="Запись теста"><div><strong>{phase==='recording'?`Идёт запись · ${Math.floor(seconds/60)}:${String(seconds%60).padStart(2,'0')}`:'Запись теста'}</strong><span role="status">{error||queue.error||(phase==='saved'?(queue.pending?'Передаём видео, не закрывайте вкладку…':'Видео сохранено. Откройте сессию в дашборде.'):phase==='saving'?'Сохраняем видео…':phase==='recording'?'Записывается выбранная вкладка.':!allowed?'Видеозапись выключена или сбор приостановлен.':'Видео без звука. Видимое содержимое и текст полей попадут в запись.')}</span></div>{phase==='recording'?<button onClick={stop}>Завершить запись</button>:<button disabled={!allowed||phase==='choosing'||phase==='saving'||queue.pending>0} onClick={()=>void start()}>{phase==='choosing'?'Выберите вкладку…':'Начать запись теста'}</button>}{phase==='saved'&&!queue.pending&&!queue.error?<a href={`http://127.0.0.1:5173/#/participant?participant=${recordedSession}`} target="_blank" rel="noopener">Посмотреть запись</a>:null}{queue.error?<button onClick={()=>void flushVideos()}>Повторить отправку</button>:null}</aside>
}
