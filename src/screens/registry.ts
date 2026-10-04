/** Navigable product compositions. State variants share the same route and data. */
export const screenRegistry={
  projects:{title:'Все проекты',navigation:'Projects',presentation:'page'},
  studies:{title:'Исследования проекта',navigation:'Studies',presentation:'page'},
  setup:{title:'Настройка исследования',navigation:'Setup',presentation:'page'},
  task:{title:'Редактирование задания',navigation:'Setup',presentation:'page'},
  criteria:{title:'Критерий успеха',navigation:'Setup',presentation:'page'},
  launch:{title:'Проверка и запуск',navigation:'Launch',presentation:'page'},
  control:{title:'Результат контрольного прохождения',navigation:'Launch',presentation:'page'},
  heatmap:{title:'Тепловая карта кликов',navigation:'Heatmap',presentation:'page'},
  'heatmap-live':{title:'Тепловая карта · локальные клики',navigation:'Heatmap',presentation:'page'},
  funnel:{title:'Воронка прохождения',navigation:'Funnel',presentation:'page'},
  signals:{title:'Сигналы затруднений',navigation:'Signals',presentation:'page'},
  findings:{title:'Находки команды',navigation:'Signals',presentation:'page'},
  finding:{title:'Находка',navigation:'Signals',presentation:'page'},
  replay:{title:'Запись сессии',navigation:'Participants',presentation:'page'},
  participant:{title:'Участник',navigation:'Participants',presentation:'page'},
  session:{title:'Прохождение исследования',navigation:'Launch',presentation:'page'},
  login:{title:'Вход в UX-Lab',navigation:'Projects',presentation:'page'},
  overview:{title:'Обзор результатов',navigation:'Overview',presentation:'page'},
  participants:{title:'Участники исследования',navigation:'Participants',presentation:'dialog'},
  report:{title:'Отчёты',navigation:'PDF',presentation:'dialog'},
} as const;
export type ScreenId=keyof typeof screenRegistry;
export const navigationRoutes:Record<string,ScreenId>={Projects:'projects',Studies:'studies',Setup:'setup',Launch:'launch',Overview:'overview',Heatmap:'heatmap',Funnel:'funnel',Participants:'participants',Signals:'signals',PDF:'report'};
