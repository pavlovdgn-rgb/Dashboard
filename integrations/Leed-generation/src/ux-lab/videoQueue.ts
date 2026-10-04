const API='http://127.0.0.1:5174/api/recordings'
export type RecordingJob={id:string;study:string;session:string;startedAt:number;mime:string;chunks:number;duration:number;finished:boolean;interrupted:boolean}
type Chunk={key:string;id:string;seq:number;blob:Blob}
type QueueState={pending:number;error:string}
let database:Promise<IDBDatabase>|undefined,busy=false,initialized=false
let state:QueueState={pending:0,error:''}
const active=new Set<string>()
const releases=new Map<string,()=>void>()
export const videoQueueState=()=>state
const currentStudy=()=>sessionStorage.getItem('ux-lab-leed-study')||'leed-local'
const currentPending=(all:RecordingJob[])=>all.filter(job=>job.study===currentStudy()).length
function db(){return database??=new Promise<IDBDatabase>((resolve,reject)=>{const request=indexedDB.open('ux-lab-video',1);request.onupgradeneeded=()=>{request.result.createObjectStore('jobs',{keyPath:'id'});request.result.createObjectStore('chunks',{keyPath:'key'}).createIndex('recording','id')};request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error)})}
async function write(store:string,value:unknown,key?:string){const connection=await db();return new Promise<void>((resolve,reject)=>{const tx=connection.transaction(store,'readwrite');if(key)tx.objectStore(store).delete(key);else tx.objectStore(store).put(value);tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error)})}
async function jobs(){const connection=await db();return new Promise<RecordingJob[]>((resolve,reject)=>{const request=connection.transaction('jobs').objectStore('jobs').getAll();request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error)})}
async function chunks(id:string){const connection=await db();return new Promise<Chunk[]>((resolve,reject)=>{const request=connection.transaction('chunks').objectStore('chunks').index('recording').getAll(id);request.onsuccess=()=>resolve(request.result.sort((a:Chunk,b:Chunk)=>a.seq-b.seq));request.onerror=()=>reject(request.error)})}
function publish(next:QueueState){state=next;window.dispatchEvent(new Event('ux-video-queue'))}
async function send(path:string,body:BodyInit,type='application/json'){const response=await fetch(API+path,{method:'POST',headers:{'Content-Type':type},body,signal:AbortSignal.timeout(20000)});if(!response.ok)throw Error(`Не удалось передать запись (${response.status}). Она остаётся на этом компьютере; повторим отправку.`)}
export async function flushVideos(){if(busy)return;busy=true;try{const all=await jobs();let currentError='';publish({pending:currentPending(all),error:''});for(const job of all){
  if(!job.chunks)continue
  try {
  await send('/start',JSON.stringify({id:job.id,study:job.study,session:job.session,startedAt:job.startedAt,mime:job.mime}))
  for(const part of await chunks(job.id)){await send(`/chunk?id=${job.id}&seq=${part.seq}`,part.blob,'application/octet-stream');await write('chunks',null,part.key)}
  // Jobs are snapshotted before the upload; finishing is only allowed after the last Blob was stored.
  if(job.finished){await send('/finish',JSON.stringify({id:job.id,chunks:job.chunks,duration:job.duration,interrupted:job.interrupted}));await write('jobs',null,job.id)}
  }catch(error){if(job.study===currentStudy())currentError=error instanceof Error?error.message:'Не удалось передать запись.'}
}publish({pending:currentPending(await jobs()),error:currentError})}catch(error){publish({...state,error:error instanceof Error?error.message:'Не удалось сохранить очередь видео.'})}finally{busy=false}}
export async function beginVideo(job:RecordingJob){active.add(job.id);if(navigator.locks)await new Promise<void>(resolve=>{void navigator.locks.request(`ux-video-${job.id}`,async()=>{resolve();await new Promise<void>(release=>releases.set(job.id,release))})});await write('jobs',job)}
export async function saveVideoChunk(job:RecordingJob,blob:Blob){const connection=await db();for(let offset=0;offset<blob.size;offset+=4*1024*1024){const seq=job.chunks;job.chunks++;await new Promise<void>((resolve,reject)=>{const tx=connection.transaction(['jobs','chunks'],'readwrite');tx.objectStore('chunks').put({key:`${job.id}:${seq}`,id:job.id,seq,blob:blob.slice(offset,offset+4*1024*1024)});tx.objectStore('jobs').put({...job});tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error)})}void flushVideos()}
export async function finishVideo(job:RecordingJob){job.finished=true;await write('jobs',{...job});active.delete(job.id);releases.get(job.id)?.();releases.delete(job.id);void flushVideos()}
export function startVideoQueue(){if(initialized)return;initialized=true;void (async()=>{
  for(const job of await jobs()){if(!active.has(job.id)&&!job.finished&&navigator.locks)await navigator.locks.request(`ux-video-${job.id}`,{ifAvailable:true},async lock=>{if(!lock)return;job.finished=true;job.interrupted=true;if(job.chunks)await write('jobs',job);else await write('jobs',null,job.id)})}
  await flushVideos()
})().catch(()=>publish({pending:0,error:'Нет доступа к хранилищу видео в браузере.'}));setInterval(()=>void flushVideos(),5000);addEventListener('online',()=>void flushVideos())}
