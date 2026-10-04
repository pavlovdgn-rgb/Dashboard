import type { Meta, StoryObj } from '@storybook/react-vite';
import { ResultsOverview } from '../pages/ResultsOverview';
const meta={title:'Sandboxes/Экраны/Обзор результатов',id:'sandbox-results-overview',component:ResultsOverview,args:{failure:'none',empty:false},argTypes:{failure:{control:'select',options:['none','refresh-once','report-once','connection-once','launch-once','transfer-once'],description:'Однократная ошибка мок-операции; повтор проходит успешно.'},empty:{control:'boolean',description:'Исследование без наблюдений.'}},parameters:{layout:'fullscreen',docs:{description:{component:'React-композиция по Figma 175:614. Общий мок-слой, история переходов, участники, форма состава отчёта и печать. Состояния ошибок включаются через Controls.'}}}} satisfies Meta<typeof ResultsOverview>;
export default meta;
type Story=StoryObj<typeof meta>;
export const Default:Story={name:'Обзор результатов'};
export const RefreshFailure:Story={name:'Ошибка обновления и повтор',args:{failure:'refresh-once'}};
export const ReportFailure:Story={name:'Ошибка формирования отчёта',args:{failure:'report-once'}};
export const NoObservations:Story={name:'Нет наблюдений',args:{empty:true}};

export const ConnectionFailure:Story={args:{failure:'connection-once'}};
export const LaunchFailure:Story={args:{failure:'launch-once'}};
export const TransferFailure:Story={args:{failure:'transfer-once'}};
