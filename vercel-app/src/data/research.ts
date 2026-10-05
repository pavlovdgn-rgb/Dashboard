import type { ParticipantRecord } from '../components/_shared/ParticipantsTableExample';
import type { ScenarioRecord } from '../components/_shared/ScenarioResults';
import type { Finding } from './workspace';

export type Device='all'|'desktop'|'mobile';
export type ScenarioId='catalog'|'quantity'|'checkout';
export type Observation=ParticipantRecord & {scenarioId:string;device:'desktop'|'mobile';completed:boolean};
export type ReportSection='summary'|'scenarios'|'participants'|'heatmap'|'signals'|'findings';
export type SavedReport={id:string;createdAt:string;studyId:string;studyTitle:string;device:Device;scenarioId:string;sections:ReportSection[];scenarios:ScenarioRecord[];participants:ParticipantRecord[];findings:Finding[]};
export const study={id:'shopping',title:'Покупка в интернет-магазине',project:'Интернет-магазин',mode:'Задания',scenarioSummary:'Поиск и добавление в корзину\nКоличество товара · Оформление заказа'};
export const deviceLabels:Record<Device,string>={all:'Все устройства',desktop:'Компьютер',mobile:'Мобильное'};
export const scenarioDefinitions:{id:ScenarioId;title:string;description:string}[]=[
  {id:'catalog',title:'Найти товар и добавить в корзину',description:'Поиск → Карточка товара → В корзину'},
  {id:'quantity',title:'Изменить количество товара',description:'Количество товара в мини-корзине'},
  {id:'checkout',title:'Оформить заказ',description:'Контакты, доставка и подтверждение заказа'},
];
const ids=['014','018','009','012','001','002','003','004','005','006','007','008','010','011','013','015','016','017','019','020'];
// One deterministic fixture supplies the overview, participant list and reports.
// Completion and achievement are separate observations, as in the source design.
export function createObservations():Observation[] {
  return scenarioDefinitions.flatMap((scenario,index)=>{
    const people=ids.slice(0,[20,18,16][index]);
    const target=[14,12,10][index];
    const assessed=people.filter(id=>id!=='018'&&(index!==0||id!=='020'));
    const successful=assessed.filter(id=>id!=='014').slice(0,target);
    const completed=[...successful,...assessed.filter(id=>!successful.includes(id))].slice(0,[16,15,12][index]);
    return people.map((id,i)=>({id,scenarioId:scenario.id,device:'desktop',attempts:1,
      outcome:!assessed.includes(id)?'NotAssessed':successful.includes(id)?'Achieved':'NotAchieved',
      duration:['04:32','03:10','02:48','03:24'][i%4],signals:[4,2,3,2][i%4],
      coverage:id==='018'||id==='020'?'Partial':'Complete',completed:completed.includes(id),
    }));
  });
}
export function selectObservations(rows:Observation[],device:Device,scenarioId='') {
  return rows.filter(row=>(device==='all'||row.device===device)&&(!scenarioId||row.scenarioId===scenarioId));
}
export function selectParticipants(rows:Observation[],device:Device,scenarioId=''):ParticipantRecord[] {
  const byId=new Map<string,ParticipantRecord>();
  for(const row of selectObservations(rows,device,scenarioId))if(!byId.has(row.id))byId.set(row.id,row);
  return [...byId.values()];
}
export function selectScenarios(rows:Observation[],device:Device,definitions:{id:string;title:string;description:string}[]=scenarioDefinitions):ScenarioRecord[] {
  return definitions.flatMap(scenario=>{
    const people=selectObservations(rows,device,scenario.id);
    return people.length?[{...scenario,started:people.length,completed:people.filter(p=>p.completed).length,
      achieved:people.filter(p=>p.outcome==='Achieved').length,assessed:people.filter(p=>p.outcome!=='NotAssessed').length,
      incomplete:people.filter(p=>p.coverage!=='Complete').length}]:[];
  });
}
