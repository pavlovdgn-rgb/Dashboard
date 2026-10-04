import { daysAgo, hoursAgo, minutesAgo } from './format'
import type { Lead } from './types'

export const MANAGERS: string[] = ['Игорь Петров', 'Анна Смирнова', 'Дмитрий Волков']

export function initials(name: string): string {
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
}

/**
 * Единый мок-слой лидов — читают и меняют LeadsTable/LeadsKanban/LeadCard/ChatPanel/Dashboard(бейдж просрочки).
 * Реалистичные, но мок: lastContactAt/createdAt — реальные timestamp'ы, а не прибитый текст «N назад» (форматируется на лету, см. format.ts).
 */
export function createInitialLeads(): Lead[] {
  return [
    {
      id: 'lead-1',
      channel: 'form',
      name: 'Иванов Пётр',
      company: 'Ленинградский зоопарк',
      phone: '+7 911 222-10-30',
      email: 'p.ivanov@spbzoo.ru',
      source: 'Форма, сайт spbzoo.ru',
      score: 82,
      status: 'new',
      owner: 'Игорь Петров',
      overdue: false,
      createdAt: minutesAgo(12),
      lastContactAt: minutesAgo(12),
      timeline: [
        { id: 'tl-1-1', type: 'form', title: 'Заявка с сайта', quote: 'Интересует система контроля доступа для двух входов', at: minutesAgo(12) },
      ],
      messages: [],
    },
    {
      id: 'lead-2',
      channel: 'chat',
      name: 'Дмитриев Олег',
      company: 'Петропавловская крепость',
      phone: '+7 981 222-33-44',
      email: null,
      source: 'Чат-виджет сайта',
      score: 91,
      status: 'new',
      owner: null,
      overdue: false,
      createdAt: minutesAgo(40),
      lastContactAt: minutesAgo(40),
      timeline: [
        { id: 'tl-2-1', type: 'chat', title: 'Обращение через чат-виджет сайта', quote: 'Спрашивают об интеграции системы контроля доступа с билетной кассой', at: minutesAgo(40) },
      ],
      messages: [
        { id: 'msg-2-1', sender: 'client', authorLabel: 'Клиент', message: 'Здравствуйте! Подскажите, есть ли возможность предоставить КП на\nустановку 50ти ваших систем на наш объект?', at: minutesAgo(38) },
        { id: 'msg-2-2', sender: 'manager', authorLabel: 'Менеджер (Игорь Петров)', message: 'Добрый день, Олег! Да, есть такая возможность, посчитаю\nточную стоимость с доставкой', at: minutesAgo(35) },
        { id: 'msg-2-3', sender: 'client', authorLabel: 'Клиент', message: 'Отлично, буду ждать расчёт', at: minutesAgo(34) },
      ],
    },
    {
      id: 'lead-3',
      channel: 'call',
      name: 'Соколова Анна',
      company: 'Музей петербургского авангарда',
      phone: '+7 921 333-44-55',
      email: 'a.sokolova@avangard-museum.ru',
      source: 'Входящий звонок',
      score: 65,
      status: 'in_progress',
      owner: 'Игорь Петров',
      overdue: false,
      createdAt: hoursAgo(3),
      lastContactAt: hoursAgo(3),
      timeline: [{ id: 'tl-3-1', type: 'call', title: 'Звонок входящий', quote: 'Уточняли стоимость обслуживания', at: hoursAgo(3) }],
      messages: [],
    },
    {
      id: 'lead-4',
      channel: 'form',
      name: 'Екатерина Иванова',
      company: '«ГМИИ им. А.С. Пушкина»',
      phone: '+7 916 407-52-18',
      email: 'e.ivanova@pushkinmuseum.art',
      source: 'Форма, сайт pushkinmuseum.art',
      score: 45,
      status: 'callback',
      owner: 'Игорь Петров',
      overdue: true,
      createdAt: daysAgo(4),
      lastContactAt: daysAgo(1),
      timeline: [
        { id: 'tl-4-1', type: 'call', title: 'Звонок исходящий (ручной лог)', quote: 'Просила перезвонить после обеда', at: daysAgo(1) },
        { id: 'tl-4-2', type: 'call', title: 'Звонок исходящий', quote: 'Нет ответа', at: daysAgo(2) },
        { id: 'tl-4-3', type: 'form', title: 'Заявка с сайта', quote: 'Интересует установка 50 билетных систем с последующим обучением персонала', at: daysAgo(4) },
      ],
      messages: [],
    },
    {
      id: 'lead-5',
      channel: 'form',
      name: 'Кузнецова Мария',
      company: 'Мариинский театр',
      phone: '+7 911 555-77-88',
      email: 'm.kuznetsova@mariinsky.ru',
      source: 'Форма, сайт mariinsky.ru',
      score: 58,
      status: 'callback',
      owner: 'Игорь Петров',
      overdue: true,
      createdAt: daysAgo(3),
      lastContactAt: daysAgo(2),
      timeline: [{ id: 'tl-5-1', type: 'form', title: 'Заявка с сайта', quote: 'Нужна система контроля доступа на служебные входы', at: daysAgo(3) }],
      messages: [],
    },
    {
      id: 'lead-6',
      channel: 'call',
      name: 'Волков Сергей',
      company: 'Большой концертный зал «Октябрьский»',
      phone: '+7 921 555-12-34',
      email: 'volkov@bkz-oktyabrsky.ru',
      source: 'Входящий звонок',
      score: 78,
      status: 'qualified',
      owner: 'Игорь Петров',
      overdue: false,
      createdAt: daysAgo(2),
      lastContactAt: daysAgo(2),
      timeline: [{ id: 'tl-6-1', type: 'call', title: 'Звонок входящий', quote: 'Договорились о демонстрации на объекте', at: daysAgo(2) }],
      messages: [],
    },
    {
      id: 'lead-7',
      channel: 'form',
      name: 'Смирнов Игорь',
      company: 'Большой концертный зал «Октябрьский»',
      phone: '+7 911 888-99-00',
      email: null,
      source: 'Форма, сайт bkz-oktyabrsky.ru',
      score: 22,
      status: 'rejected',
      owner: 'Игорь Петров',
      overdue: false,
      createdAt: daysAgo(5),
      lastContactAt: daysAgo(5),
      timeline: [{ id: 'tl-7-1', type: 'form', title: 'Заявка с сайта', quote: 'Уточнял цены «для сравнения», бюджета нет', at: daysAgo(5) }],
      messages: [],
    },
  ]
}
