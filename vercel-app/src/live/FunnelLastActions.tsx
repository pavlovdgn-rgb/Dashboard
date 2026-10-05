import {EuiLink} from '@elastic/eui';
import {Card,Table} from '../screens/WorkspaceUI';
import {useWireRoute} from '../screens/useWireRoute';
import {pageLabels} from '../heatmap/types';
import type {LiveSummary} from './types';
import s from './LiveWorkspace.module.css';

export function FunnelLastActions({steps}:{steps:LiveSummary['funnel']}){
 const {navigate}=useWireRoute();
 const losses=steps.slice(1).map((step,i)=>({step,index:i+1,loss:steps[i].sessions-step.sessions})).filter(item=>item.loss>0);
 if(!losses.length)return null;
 return <Card><h2>Последнее действие у не дошедших</h2><p className={s.lastActionsHint}>Сессии, дошедшие до предыдущего шага, но пока не достигшие следующего. Последнее сохранённое действие не объясняет причину остановки.</p>
   {losses.map(({step,index,loss})=><section className={s.lastActionsStep} key={index}><div className={s.lastActionsHeading}><h3>Шаг {index+1}. {pageLabels[step.page]||step.page}</h3><span>Пока не дошли: {loss}</span></div>
     {step.lastActions?.length?<div className={`${s.table} ${s.lastActionsTable}`}><Table label={`Последние действия перед шагом ${index+1}`} headers={['Последнее действие','Экран','Сессии']}>
       {step.lastActions.map((action,i)=><tr key={i}><td>{action.kind==='click'?`Нажатие: ${action.label}`:'Открыли экран'}</td><td>{pageLabels[action.page]||action.page}</td><td><EuiLink data-row-action onClick={()=>navigate({screen:'participants',item:`ids:${action.sessionIds.join(',')}`})}>{action.sessions} сессий</EuiLink></td></tr>)}
     </Table></div>:<p>Для этой версии отчёта последние действия не сохранены.</p>}
     {loss<5?<p className={s.lastActionsHint}>Малая выборка: изучите отдельные сессии, прежде чем делать выводы.</p>:null}
   </section>)}
 </Card>;
}
