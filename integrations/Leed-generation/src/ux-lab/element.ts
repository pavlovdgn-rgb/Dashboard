import { hash } from './view'

// Only reviewed interface labels. Never derive names from customer records or field values.
const labels=new Set(['Новый лид','Найти лида','Сбросить всё','Сбросить фильтры','Сохранить','Отмена','Закрыть',
  'Создать','Создать лид','Добавить','Удалить','Лиды','Канбан','Дашборд','Настройки','Генератор лидов',
  'Поиск','Имя','Телефон','Email','Компания','Комментарий','Отправить','Назад','Применить',
  'Канал','Имя и компания','Скор','Статус','Последний контакт','Ответственный'])
export type ElementInfo={label:string;rect:[number,number,number,number]}
export function describeElement(target:Element) {
  const element=target.closest('button,a,input,select,textarea,[role="button"],tr,[role="row"],[data-track="lead-row"]')||target
  const isRow=element.matches('tr,[role="row"],[data-track="lead-row"]')
  const type=isRow?'Строка таблицы':element.matches('input[type="checkbox"],[role="checkbox"]')?'Флажок':element.matches('input,textarea')?'Поле':element.matches('select,[aria-haspopup]')?'Список':element.matches('button,[role="button"]')?'Кнопка':element.matches('a')?'Ссылка':element.textContent?.trim()?'Область без названия':'Пустая область'
  const candidates=[element.getAttribute('aria-label'),element.getAttribute('placeholder'),element.getAttribute('title'),element.textContent?.trim()]
  let name=candidates.find(value=>value&&labels.has(value))||''
  // Filter labels contain changing choices (including people's names): retain only the static heading.
  for(const prefix of ['Канал','Менеджер','Период'])if(candidates.some(value=>value?.startsWith(prefix+':')))name=prefix
  const label=name?`${type} «${name}»`:type
  const r=element.getBoundingClientRect(),x=Math.max(0,r.left),y=Math.max(0,r.top)
  const rect:ElementInfo['rect']=[x/innerWidth,y/innerHeight,Math.max(0,Math.min(innerWidth,r.right)-x)/innerWidth,Math.max(0,Math.min(innerHeight,r.bottom)-y)/innerHeight]
  // A structural path distinguishes repeated unnamed elements without collecting their contents.
  const path:string[]=[];let node:Element|null=element
  while(node&&node!==document.body){path.push(`${node.tagName}:${[...(node.parentElement?.children||[])].indexOf(node)}`);node=node.parentElement}
  return {target:`element-${hash(label+'|'+path.join('/'))}`,info:{label,rect},element}
}
