import type {LiveConfig,LiveSummary,StudyTaskDefinition,TaskAttempt,TaskRun} from './types';

export const criterionOptions=[{value:'none',label:'Без автоматической проверки'},{value:'chat_message_sent',label:'Отправлено сообщение в чат'},{value:'lead_created',label:'Создан новый лид'}];
export function studyTasks(config:LiveConfig):StudyTaskDefinition[]{
 return config.tasks??(config.scenario?[{id:'legacy-task',title:'Задание 1',instruction:config.scenario,criterion:config.successCriterion||'none'}]:[]);
}
/** Old PDF snapshots stay readable; no task assignment is invented for untracked sessions. */
export function sessionTasks(run?:TaskRun):TaskAttempt[]{
 return run?.tasks??(run?[{...run,taskId:'legacy-task',revision:'legacy',title:'Задание 1',ordinal:0,startedAt:null}]:[]);
}
export function taskCounts(tasks:TaskAttempt[]){
 return {total:tasks.length,succeeded:tasks.filter(t=>t.status==='succeeded').length,failed:tasks.filter(t=>t.status==='failed').length,pending:tasks.filter(t=>t.status==='pending').length,notStarted:tasks.filter(t=>t.status==='not_started').length,unassessed:tasks.filter(t=>t.status==='unassessed').length,needsReview:tasks.filter(t=>t.status==='needs_review').length,indeterminate:tasks.filter(t=>t.status==='indeterminate').length};
}
export function taskGroups(data:Pick<LiveSummary,'project'|'sessions'>){
 const groups=new Map<string,{id:string;title:string;instruction:string;archived:boolean;attempts:TaskAttempt[]}>();
 for(const task of studyTasks(data.project))groups.set(task.id,{id:task.id,title:task.title,instruction:task.instruction,archived:false,attempts:[]});
 for(const session of data.sessions)for(const task of sessionTasks(session.task)){
   if(!groups.has(task.taskId))groups.set(task.taskId,{id:task.taskId,title:task.title,instruction:task.scenario,archived:true,attempts:[]});
   groups.get(task.taskId)!.attempts.push(task);
 }
 return [...groups.values()].map(group=>({...group,...taskCounts(group.attempts)}));
}
