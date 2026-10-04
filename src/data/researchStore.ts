import { createContext, useContext, useRef, useState } from 'react';
import { selectParticipants, selectScenarios, type Device, type ReportSection, type SavedReport } from './research';
import { useWorkspaceData } from './workspace';
import type { ParticipantFilters } from '../components/_shared/ParticipantsTableExample';

export type MockFailure='none'|'refresh-once'|'report-once'|'connection-once'|'launch-once'|'transfer-once';
type Operation='refresh'|'report'|'connection'|'launch'|'transfer';
export type MockOptions={failure?:MockFailure;empty?:boolean;live?:boolean};
export function useResearchStore({failure='none',empty=false,live=false}:MockOptions) {
  const workspace=useWorkspaceData(empty,failure==='none'&&!empty&&!live,live);
  const observations=workspace.data.observations[workspace.study.id]||[];
  const [updatedAt,setUpdatedAt]=useState('14:32');
  const [revision,setRevision]=useState(0);
  const reports=workspace.data.reports||[];
  const setReports=(updater:(previous:SavedReport[])=>SavedReport[])=>workspace.update(data=>({...data,reports:updater(data.reports||[])}));
  const [participantFilters,setParticipantFilters]=useState<Record<string,ParticipantFilters>>({});
  const [pending,setPending]=useState<Operation|null>(null);
  const busy=useRef(false);
  const failureConsumed=useRef(false);
  const perform=async(operation:Operation)=>{
    if(busy.current)throw new Error('Дождитесь завершения текущего действия.');
    busy.current=true;setPending(operation);
    try {
      await new Promise(resolve=>setTimeout(resolve,400));
      if(!failureConsumed.current&&failure===`${operation}-once`){failureConsumed.current=true;throw new Error({refresh:'Не удалось обновить результаты. Сохранены предыдущие данные.',report:'Не удалось сформировать отчёт. Выбранные разделы сохранены.',connection:'Не удалось проверить подключение. Повторите проверку.',launch:'Не удалось запустить исследование. Настройки сохранены.',transfer:'Не удалось передать результаты. Ответ сохранён, повторите отправку.'}[operation]);}
    } finally {busy.current=false;setPending(null);}
  };
  const refresh=async()=>{await perform('refresh');setUpdatedAt(new Date().toLocaleTimeString('ru-RU',{hour:'2-digit',minute:'2-digit',second:'2-digit'}));setRevision(value=>value+1);};
  const createReport=async(device:Device,scenarioId:string,sections:ReportSection[])=>{
    if(!sections.length)throw new Error('Выберите хотя бы один раздел отчёта.');
    const participants=selectParticipants(observations,device,scenarioId);
    const scenarios=selectScenarios(observations,device,workspace.study.tasks).filter(row=>!scenarioId||row.id===scenarioId);
    if(!participants.length)throw new Error('В текущей выборке нет данных для отчёта.');
    await perform('report');
    const report:SavedReport={id:crypto.randomUUID(),createdAt:new Date().toISOString(),studyId:workspace.study.id,studyTitle:workspace.study.title,device,scenarioId,sections:[...sections],scenarios,participants,findings:structuredClone(workspace.data.findings.filter(x=>x.studyId===workspace.study.id&&x.inReport&&(!scenarioId||x.scenarioId===scenarioId)))};
    setReports(previous=>[report,...previous]);return report;
  };
  return {...workspace,live,observations,updatedAt,revision,reports,pending,perform,refresh,createReport,participantFilters,setParticipantFilters};
}
export const ResearchContext=createContext<ReturnType<typeof useResearchStore>|null>(null);
export function useResearch() {const store=useContext(ResearchContext);if(!store)throw new Error('ResearchProvider is required');return store;}
