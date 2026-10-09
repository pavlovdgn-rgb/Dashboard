export type ClickPoint={x:number;y:number;target:string;count:number;sessions:string[];element?:{label:string;rect:[number,number,number,number]}};
export type ClickGroup={layout:string;page:string;version:string;vw:number;vh:number;rw:number;rh:number;clicks:number;sessions:number;path?:string;aggregation?:string;backgroundResponsive?:boolean;context?:{signature:string;scrolls:number[][];snapshot?:string}};
export type ClickData={groups:ClickGroup[];total:{clicks:number;sessions:number};points:ClickPoint[];sessions:string[];availableSessions?:{id:string;startedAt:number;clicks:number}[]};
export type CollectorStatus={session?:string;pending:number;dropped?:number;error:string};
export const LOCAL_VERSION='nova-local-v1';
export const CLICK_API=location.origin;
export const pageLabels:Record<string,string>={product:'Карточка товара',cart:'Корзина',checkout:'Оформление заказа',success:'Заказ оформлен','leed-leads-table':'Таблица лидов','leed-leads-kanban':'Канбан лидов','leed-dashboard':'Дашборд','leed-lead-card':'Карточка лида','leed-chat-panel':'Чат','leed-user-roles-settings':'Роли и права','leed-telephony-settings':'Телефония'};
export const targetLabels:Record<string,string>={'add-to-cart':'Добавить в корзину','navigation':'Корзина / каталог','backpack':'Изображение товара','quantity-less':'Уменьшить количество','quantity-more':'Увеличить количество','checkout':'Оформить заказ','place-order':'Отправить заказ','return':'Вернуться в каталог',select:'Выпадающий список',input:'Поле ввода'};
declare global {
  interface Window {
    UXLabCollector?:{attach(config:{root:HTMLElement;study:string;version:string;endpoint:string;onStatus?:(status:CollectorStatus)=>void}):{flush:()=>Promise<void>;session:string;dispose:()=>void}};
  }
}

Object.assign(pageLabels,{"leed-leads-table": "Таблица лидов", "leed-leads-kanban": "Канбан лидов", "leed-dashboard": "Дашборд руководителя", "leed-lead-card": "Карточка лида", "leed-chat-panel": "Плавающее окно чата", "leed-chat-widget": "Чат-виджет сайта", "leed-call-log-modal": "Записать звонок", "leed-incoming-call-popup": "Входящий звонок", "leed-user-roles-settings": "Роли и права", "leed-auto-assignment-settings": "Автоназначение", "leed-telephony-settings": "Телефония", "leed-chat-widget-settings": "Настройки чат-виджета", "leed-access-denied": "Доступ ограничен", "leed-error-state": "Ошибка загрузки", "leed-not-found-404": "404 — лид не найден", "leed-empty-leads-table": "Таблица лидов — пусто", "leed-loading-state": "Таблица лидов — загрузка", "leed-empty-leads-kanban": "Канбан — пусто", "leed-empty-dashboard": "Дашборд — нет данных", "leed-loading-dashboard": "Дашборд — загрузка", "leed-empty-user-roles-settings": "Роли и права — пусто", "leed-loading-user-roles-settings": "Роли и права — загрузка", "leed-index": "Главная", "leed-showcase": "Обзор экранов"});
export const pagePaths:Record<string,string>={"leed-index": "/", "leed-showcase": "/showcase", "leed-leads-table": "/leads-table", "leed-leads-kanban": "/leads-kanban", "leed-dashboard": "/dashboard", "leed-lead-card": "/lead-card", "leed-chat-panel": "/chat-panel", "leed-chat-widget": "/chat-widget", "leed-call-log-modal": "/call-log-modal", "leed-incoming-call-popup": "/incoming-call-popup", "leed-user-roles-settings": "/settings/roles", "leed-auto-assignment-settings": "/settings/auto-assignment", "leed-telephony-settings": "/settings/telephony", "leed-chat-widget-settings": "/settings/chat-widget", "leed-access-denied": "/access-denied", "leed-error-state": "/error", "leed-not-found-404": "/not-found", "leed-empty-leads-table": "/leads-table/empty", "leed-loading-state": "/leads-table/loading", "leed-empty-leads-kanban": "/leads-kanban/empty", "leed-empty-dashboard": "/dashboard/empty", "leed-loading-dashboard": "/dashboard/loading", "leed-empty-user-roles-settings": "/settings/roles/empty", "leed-loading-user-roles-settings": "/settings/roles/loading"};

const mobileScreens:Record<string,{label:string;path:string}>={
  main:{label:'Главная',path:'/main'},events:{label:'Афиша',path:'/events'},filter:{label:'Фильтры',path:'/filter'},
  event:{label:'Событие',path:'/event'},sessions:{label:'Выбор даты',path:'/sessions'},
  seats:{label:'Выбор мест',path:'/seats'},'seats--confirm':{label:'Выбор тарифа',path:'/seats/confirm'},
  'seats--selected':{label:'Выбранные места',path:'/seats/selected'},
  'order-form':{label:'Оформление заказа',path:'/order-form'},'order-form--filled':{label:'Заполненный заказ',path:'/order-form/filled'},
  payment:{label:'Оплата',path:'/payment'},done:{label:'Оплата прошла',path:'/done'},
  profile:{label:'Профиль',path:'/profile'},'profile--data':{label:'Личные данные',path:'/profile/data'},
  tickets:{label:'Мои билеты',path:'/tickets'},refund:{label:'Возврат',path:'/refund'},
  'refund--done':{label:'Заявка на возврат',path:'/refund/done'},orders:{label:'История заказов',path:'/orders'},
  ticket:{label:'Билет',path:'/ticket'},'no-ticket':{label:'Нет билетов',path:'/no-ticket'},
  plan:{label:'План дня',path:'/plan'},'plan--add':{label:'Добавление мест',path:'/plan/add'},
  map:{label:'Карта',path:'/map'},'map--route':{label:'Маршрут',path:'/map/route'},
  story:{label:'История',path:'/story'},gallery:{label:'Галерея',path:'/gallery'},
  reviews:{label:'Отзывы',path:'/reviews'},review:{label:'Написать отзыв',path:'/review'},
  activity:{label:'Активность',path:'/activity'},person:{label:'Персона',path:'/person'},
  venue:{label:'Площадка',path:'/venue'},favourites:{label:'Избранное',path:'/favourites'}
};
for(const [key,value] of Object.entries(mobileScreens)){
  pageLabels[`bb-${key}`]=value.label;
  pagePaths[`bb-${key}`]=value.path;
}
