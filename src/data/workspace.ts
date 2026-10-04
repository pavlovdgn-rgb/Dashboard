import { useEffect, useState } from 'react';
import { createObservations, scenarioDefinitions, type Observation, type SavedReport } from './research';

export type Task={id:string;title:string;description:string;instruction:string;criterion:'page'|'button'|'sequence';steps:string[]};
export type Study={id:string;projectId:string;title:string;mode:'tasks'|'free';status:'draft'|'active'|'finished';url:string;connected:boolean;checked:boolean;tasks:Task[]};
export type Evidence={participantId:string;scenarioId:string;time:number;attempt:number};
export type Finding={id:string;studyId:string;scenarioId:string;title:string;observation:string;hypothesis:string;verification:string;priority:string;status:string;evidence:Evidence[];inReport:boolean};
export type SessionEvent={name:string;time:number;target:string};
export type Session={id:string;studyId:string;participantId:string;type:'guided'|'clean';control:boolean;events:SessionEvent[];results:Record<string,string>;startedAt:number;finished:boolean};
export type WorkspaceData={reports:SavedReport[];projects:{id:string;title:string;description:string}[];studies:Study[];activeStudyId:string;activeProjectId:string;observations:Record<string,Observation[]>;findings:Finding[];sessions:Session[]};
const taskSeeds:Task[]=scenarioDefinitions.map((task,i)=>({...task,instruction:['Найдите городской рюкзак и добавьте его в корзину.','Измените количество рюкзаков в корзине.','Оформите заказ на выбранный товар с доставкой в пункт выдачи.'][i],criterion:i===2?'sequence':'button',steps:i===2?['/checkout','checkout_details_completed','place-order']:[i===0?'add-to-cart':'change-quantity']}));
export const taskTemplates=taskSeeds;
const storageKey='ux-lab-workspace-v1';
export function liveWorkspace():WorkspaceData {
  return {projects:[{id:'leed-generation',title:'Lead Generation',description:'Лиды, канбан и аналитика'}],
    studies:[{id:'leed-local',projectId:'leed-generation',title:'Исследование Lead Generation',mode:'free',status:'active',
      url:'http://127.0.0.1:5175/leads-table?ux_study=leed-local',connected:true,checked:true,tasks:[]}],
    activeProjectId:'leed-generation',activeStudyId:'leed-local',reports:[],observations:{},sessions:[],findings:[]};
}
export function initialWorkspace(empty=false):WorkspaceData {
  const common={projectId:'shop',url:'https://prototype.example.test/catalog',connected:true,checked:true,tasks:taskSeeds};
  return {reports:[],projects:[{id:'shop',title:'Интернет-магазин',description:'Каталог, корзина и оформление'},{id:'account',title:'Личный кабинет',description:'Профиль и настройки'},{id:'mobile',title:'Мобильный каталог',description:'Интерфейс для смартфонов'}],studies:[{...common,id:'shopping',title:'Покупка в интернет-магазине',mode:'tasks',status:'active'},{...common,id:'navigation',title:'Навигация каталога',mode:'tasks',status:'draft',tasks:taskSeeds.slice(0,2)},{...common,id:'exploration',title:'Первое знакомство с магазином',mode:'free',status:'finished',tasks:[]},{...common,id:'profile',projectId:'account',title:'Изменение профиля',mode:'tasks',status:'draft',connected:false,checked:false,tasks:[]}],activeStudyId:'shopping',activeProjectId:'shop',observations:{shopping:empty?[]:createObservations(),exploration:empty?[]:createObservations().filter(x=>x.scenarioId==='catalog').slice(0,12).map(x=>({...x,scenarioId:'free',outcome:'NotAssessed'}))},sessions:[],findings:empty?[]:[{id:'delivery',studyId:'shopping',scenarioId:'checkout',title:'Не замечают выбор доставки',observation:'3 из 15 участников возвращались к блоку доставки и повторяли действия перед продолжением.',hypothesis:'Вариант доставки недостаточно заметен. Требует проверки.',verification:'Повторить задание после изменения; проверить, находят ли участники выбор доставки без повторных действий.',priority:'Высокий',status:'Проверено по записям',evidence:[{participantId:'014',scenarioId:'checkout',attempt:1,time:112},{participantId:'009',scenarioId:'checkout',attempt:1,time:76},{participantId:'012',scenarioId:'checkout',attempt:1,time:125}],inReport:true},{id:'contacts',studyId:'shopping',scenarioId:'checkout',title:'Возвращаются к контактным данным',observation:'4 из 15 участников возвращались к контактным данным.',hypothesis:'',verification:'Проверить контекст записи.',priority:'Средний',status:'Нужно проверить',evidence:[{participantId:'014',scenarioId:'checkout',attempt:1,time:96}],inReport:true}]};
}
function read(empty:boolean,persist:boolean):WorkspaceData {try {const raw=persist&&!empty?localStorage.getItem(storageKey):null;return raw?JSON.parse(raw):initialWorkspace(empty);}catch{return initialWorkspace(empty);}}
export function useWorkspaceData(empty=false,persist=true,live=false) {
  const [data,setData]=useState(()=>live?liveWorkspace():read(empty,persist));
  useEffect(()=>{if(!persist)return;const listener=(event:StorageEvent)=>{if(event.key===storageKey&&event.newValue){try{setData(JSON.parse(event.newValue));}catch{/* Keep the last valid demo state. */}}};addEventListener('storage',listener);return()=>removeEventListener('storage',listener);},[persist]);
  const update=(fn:(previous:WorkspaceData)=>WorkspaceData)=>setData(previous=>{const next=fn(previous);if(persist)localStorage.setItem(storageKey,JSON.stringify(next));return next;});
  const study=data.studies.find(x=>x.id===data.activeStudyId)||data.studies[0];
  const project=data.projects.find(x=>x.id===data.activeProjectId)||data.projects[0];
  const saveStudy=(next:Study)=>update(d=>({...d,studies:d.studies.some(x=>x.id===next.id)?d.studies.map(x=>x.id===next.id?next:x):[...d.studies,next]}));
  const activateStudy=(id:string)=>update(d=>{const selected=d.studies.find(x=>x.id===id);return selected?{...d,activeStudyId:id,activeProjectId:selected.projectId}:d;});
  return {data,update,study,project,saveStudy,activateStudy};
}
export const formatTime=(time:number)=>`${String(Math.floor(time/60)).padStart(2,'0')}:${String(Math.floor(time%60)).padStart(2,'0')}`;
export const demoEvents:SessionEvent[]=[{name:'Открыл оформление',target:'/checkout',time:0},{name:'Длительная пауза',target:'Оформление',time:48},{name:'Возврат',target:'Контактные данные',time:96},{name:'Клик без результата',target:'Область «Доставка»',time:112},{name:'Ввод email',target:'anna@example.test',time:126},{name:'Повторные клики',target:'Отправить заказ',time:138}];
