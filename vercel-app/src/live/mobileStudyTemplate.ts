import type {StudyTaskDefinition} from './types';

/** A fresh task list for a new iteration; existing session snapshots stay unchanged. */
export function mobileStudyTemplate():StudyTaskDefinition[]{
 const tasks:Array<[string,string,string,'event'|'screen',string]>=[
  ['Найти активности рядом с событием','Вы собираетесь на событие. Найдите интересное место рядом с ним и откройте его описание.','Открыто описание активности рядом с выбранным событием.','event','nearby_activity_opened'],
  ['Добавить активность в избранное','Сохраните понравившуюся активность в избранное, чтобы вернуться к ней позже.','Активность появилась в избранном.','event','activity_favourited'],
  ['Купить 2 билета на спектакль','Выберите спектакль и оформите два билета на один показ. Оплата в прототипе тестовая.','Успешно оформлен заказ на спектакль ровно с двумя билетами.','event','two_theatre_tickets_purchased'],
  ['Найти раздел «Избранное»','Найдите раздел с сохранёнными вами местами и событиями.','Открыт раздел «Избранное».','screen','bb-favourites'],
  ['Найти функцию «Куда пойдём?»','Найдите возможность спланировать, куда пойти в день мероприятия.','Открыт раздел «Куда пойдём?», включая состояние без билетов.','event','planning_opened'],
  ['Построить план из избранного','Добавьте сохранённое в избранном место в план дня.','В план дня добавлено место, которое есть в избранном.','event','favourite_added_to_plan'],
 ];
 return tasks.map(([title,instruction,successDescription,type,value])=>({id:crypto.randomUUID(),title,instruction,successDescription,criterion:'custom',verification:{method:'automatic',type,value,page:type==='screen'?value:''}}));
}
