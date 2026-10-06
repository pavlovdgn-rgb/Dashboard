import {collectionEnabled,studyInstructions} from './activity'
import {describeElement} from './element'

export type TaskAttempt={taskId:string;title:string;scenario:string;criterion:string;status:string;finishedAt:number|null;revision:string;ordinal:number;verification?:{method:string}}
type Run={scenario:string;criterion:string;status:string;finishedAt:number|null;activeTaskId?:string|null;tasks?:TaskAttempt[];totalTasks?:number;succeededTasks?:number;finishedTasks?:number;verification?:{method:string}}
type TaskState={run:Run|null;pending:boolean;error:string}
let state:TaskState={run:null,pending:false,error:''}
export const taskState=()=>state
const publish=(patch:Partial<TaskState>)=>{state={...state,...patch};dispatchEvent(new Event('ux-task-state'))}
export const finishTask=()=>dispatchEvent(new CustomEvent('ux-study-action',{detail:'finished'}))
/** Record successful domain actions only, with no message text or form values. */
export const taskAction=(kind:'chat_message_sent'|'lead_created')=>dispatchEvent(new CustomEvent('ux-study-action',{detail:kind}))
/** Prototype integration: emit only after the application confirms a successful action. */
export const successEvent=(name:string)=>dispatchEvent(new CustomEvent('ux-success-signal',{detail:{kind:'prototype_event',value:name}}))
export const taskElement=(value:string,label:string)=>dispatchEvent(new CustomEvent('ux-success-signal',{detail:{kind:'element_clicked',value,label}}))

export function startTaskTracking(study:string,session:string,routes:Map<string,string>){
  const key=`ux-task-events:${study}:${session}`
  type Event={id:string;study:string;session:string;kind:string;timestamp:number;page:string;vw:number;vh:number;taskId?:string;value?:string;label?:string}
  let queue:Event[]=[];try{queue=JSON.parse(sessionStorage.getItem(key)||'[]')}catch{/* memory queue remains available */}
  let busy=false,disposed=false,started=false
  let savedRun:Run|null=null;try{savedRun=JSON.parse(sessionStorage.getItem(key+':run')||'null')}catch{/* Load authoritative plan from the server. */}
  publish({run:savedRun,pending:queue.some(e=>e.kind==='finished'),error:''})
  const persist=()=>{try{sessionStorage.setItem(key,JSON.stringify(queue))}catch{/* Retry from memory. */}}
  function enqueue(kind:string,value='',label=''){
    if(!collectionEnabled())return
    if(kind==='finished'&&(!state.run||state.run.finishedAt||state.pending))return
    if(kind==='started'&&!state.run&&studyInstructions().mode!=='scenario')return
    const page=routes.get((location.pathname.replace(/^\/participant(?=\/|$)/,'')||'/'));if(!page)return
    queue.push({id:crypto.randomUUID(),study,session,kind,timestamp:Date.now(),page:`leed-${page}`,vw:innerWidth,vh:innerHeight,taskId:kind==='started'?'':state.run?.activeTaskId||'',value,label});persist()
    if(kind==='finished')publish({pending:true,error:''})
    void flush()
  }
  async function flush(){
    if(busy||disposed||!collectionEnabled())return
    busy=true
    try{while(queue.length&&!disposed){
      const response=await fetch('/api/project/task-events',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(queue[0]),signal:AbortSignal.timeout(20000)})
      if(!response.ok)throw Error('Не удалось передать результат. Повторим автоматически; оставьте вкладку открытой.')
      const result=await response.json();if(result.paused)break
      const previousTask=state.run?.activeTaskId;queue.shift();persist();try{sessionStorage.setItem(key+':run',JSON.stringify(result.run||null))}catch{/* Keep current plan in memory. */}publish({run:result.run||null,pending:queue.some(e=>e.kind==='finished'),error:''})
      // Observe the initial page once. A task transition is not a new page visit.
      if(result.run?.activeTaskId&&!previousTask)enqueue('screen_visited')
    }}catch(e){publish({error:e instanceof Error?e.message:'Нет связи со сборщиком. Повторим автоматически.'})}finally{busy=false}
  }
  const policy=()=>{if(!started&&collectionEnabled()&&(state.run||studyInstructions().mode==='scenario')){started=true;enqueue('started')}void flush()}
  const action=(event:globalThis.Event)=>{const kind=(event as CustomEvent).detail;if(['finished','chat_message_sent','lead_created'].includes(kind))enqueue(kind)}
  const signal=(event:globalThis.Event)=>{const d=(event as CustomEvent).detail;if(d&&['prototype_event','element_clicked'].includes(d.kind)&&typeof d.value==='string'&&d.value.length<=200)enqueue(d.kind,d.value,typeof d.label==='string'?d.label.slice(0,200):'')}
  const visit=()=>enqueue('screen_visited')
  // Success checks must work even when heatmap click collection is disabled.
  const click=(event:MouseEvent)=>{
    if(!collectionEnabled()||!(event.target instanceof Element)||event.target.closest('[data-ux-overlay],[data-ux-private]'))return
    const described=describeElement(event.target)
    taskElement(described.target,described.info.label)
  }
  document.addEventListener('click',click,true)
  let initialVisit=false;const firstVisit=()=>{if(collectionEnabled()&&!initialVisit){initialVisit=true;visit()}}
  addEventListener('ux-success-signal',signal);addEventListener('ux-lab-navigation',visit);addEventListener('ux-lab-policy',firstVisit)
  addEventListener('ux-lab-policy',policy);addEventListener('ux-study-action',action);policy()
  const timer=setInterval(()=>void flush(),2000)
  return()=>{disposed=true;clearInterval(timer);document.removeEventListener('click',click,true);removeEventListener('ux-lab-policy',policy);removeEventListener('ux-study-action',action);removeEventListener('ux-success-signal',signal);removeEventListener('ux-lab-navigation',visit);removeEventListener('ux-lab-policy',firstVisit)}
}
