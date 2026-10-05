import { useState } from 'react'
import styles from './Showcase.module.css'
import { SEMANTIC_COLORS as PALETTE, TYPE_ROWS } from './foundationData'
import {
  Avatar,
  Breadcrumb,
  Button,
  Card,
  Checkbox,
  Dropdown,
  FunnelBar,
  Header,
  IconButton,
  Input,
  KanbanCard,
  MessageBubble,
  MetricCard,
  NavListItem,
  Pagination,
  Radio,
  Select,
  Sidebar,
  StatusBadge,
  Table,
  TableCell,
  Tabs,
  TextButton,
  TimelineItem,
  Toast,
  Toggle,
  Tooltip,
} from './components'

function CheckmarkIcon() {
  return (
    <svg viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M3 8L6.5 11.5L13 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function CloseIcon() {
  return (
    <svg viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M4 4L12 12M12 4L4 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

function ArrowIcon({ direction = 'left' }: { direction?: 'left' | 'right' }) {
  const d = direction === 'left' ? 'M7.5 3L3.5 7L7.5 11' : 'M3.5 3L7.5 7L3.5 11'
  return (
    <svg viewBox="0 0 11 14" fill="none" aria-hidden="true">
      <path d={d} stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export default function Showcase() {
  const [checked, setChecked] = useState(true)
  const [radioSelected, setRadioSelected] = useState('a')
  const [toggleOn, setToggleOn] = useState(true)
  const [inputValue, setInputValue] = useState('')
  const [textareaValue, setTextareaValue] = useState('Например: обсудили условия поставки')
  const [selectValue, setSelectValue] = useState('Все')
  const [activeTab, setActiveTab] = useState('Список')

  return (
    <div className={styles.page}>
      <h1 className={`ds-desktop-header-1-semibold ${styles.pageTitle}`}>Design System — React база</h1>

      {/* ==== Палитра ==== */}
      <section className={styles.section}>
        <h2 className="ds-desktop-header-2-medium">Палитра — semantic-цвета</h2>
        <div className={styles.swatchGrid}>
          {PALETTE.map((c) => (
            <div className={styles.swatch} key={c.name}>
              <div className={styles.swatchColor} style={{ background: `var(${c.varName})` }} />
              <span className={styles.swatchName}>
                {c.name}
                <br />
                {c.varName}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* ==== Типографика ==== */}
      <section className={styles.section}>
        <h2 className="ds-desktop-header-2-medium">Шкала текста</h2>
        <div>
          {TYPE_ROWS.map((t) => (
            <div className={styles.typeRow} key={t.className}>
              <span className={styles.typeRowLabel}>{t.label}</span>
              <span className={t.className}>Пример текста Aa Яя 123</span>
            </div>
          ))}
        </div>
      </section>

      {/* ==== Действия ==== */}
      <section className={styles.section}>
        <h2 className="ds-desktop-header-2-medium">Действия</h2>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Button — Style × Size × State</span>
          <div className={styles.row}>
            <Button variant="primary" size="m">Primary M</Button>
            <Button variant="primary" size="s">Primary S</Button>
            <Button variant="secondary" size="m">Secondary M</Button>
            <Button variant="tertiary" size="m">Tertiary M</Button>
            <Button variant="primary" size="m" leftIcon={<CheckmarkIcon />}>С иконкой</Button>
            <Button variant="primary" size="m" loading>Loading</Button>
            <Button variant="primary" size="m" disabled>Disabled</Button>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Text Button</span>
          <div className={styles.row}>
            <TextButton>Сбросить всё</TextButton>
            <TextButton rightIcon={<ArrowIcon direction="right" />}>Открыть карточку лида</TextButton>
            <TextButton disabled>Disabled</TextButton>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Icon Button</span>
          <div className={styles.row}>
            <IconButton icon={<CloseIcon />} aria-label="Закрыть" />
            <IconButton icon={<CloseIcon />} aria-label="Закрыть" disabled />
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Avatar — Size Sm|Md</span>
          <div className={styles.row}>
            <Avatar size="sm" initials="МК" />
            <Avatar size="md" initials="МК" />
          </div>
        </div>
      </section>

      {/* ==== Ввод ==== */}
      <section className={styles.section}>
        <h2 className="ds-desktop-header-2-medium">Ввод</h2>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Input — Type=Text|Textarea, State</span>
          <div className={styles.row}>
            <div className={styles.narrow}>
              <Input label="Название поля" value={inputValue} onChange={setInputValue} placeholder="Введите значение" />
            </div>
            <div className={styles.narrow}>
              <Input label="Комментарий" type="textarea" value={textareaValue} onChange={setTextareaValue} />
            </div>
            <div className={styles.narrow}>
              <Input label="С ошибкой" value="" onChange={() => {}} error showHint hint="Обязательное поле" />
            </div>
            <div className={styles.narrow}>
              <Input label="Disabled" value="Недоступно" onChange={() => {}} disabled />
            </div>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Checkbox / Radio / Toggle</span>
          <div className={styles.row}>
            <Checkbox checked={checked} onChange={setChecked} label="Игорь Петров" />
            <Checkbox checked={false} onChange={() => {}} label="Disabled" disabled />
            <Radio selected={radioSelected === 'a'} onChange={() => setRadioSelected('a')} label="Входящий" name="dir" />
            <Radio selected={radioSelected === 'b'} onChange={() => setRadioSelected('b')} label="Исходящий" name="dir" />
            <Toggle on={toggleOn} onChange={setToggleOn} aria-label="Включить автоназначение" />
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Dropdown</span>
          <div className={styles.row}>
            <Dropdown label="Канал: Все" options={['Все', 'Форма', 'Звонок', 'Чат']} />
            <Dropdown label="Недоступно" disabled />
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Select</span>
          <div className={styles.row}>
            <div className={styles.narrow}>
              <Select value={selectValue} onChange={setSelectValue} options={['Все', 'Форма', 'Звонок', 'Чат']} />
            </div>
            <div className={styles.narrow}>
              <Select value="Ошибка" onChange={() => {}} options={['Ошибка']} error />
            </div>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Tooltip</span>
          <div className={styles.row}>
            <Tooltip content="Подсказка сверху" position="top">
              <Button variant="secondary" size="s">Наведи (top)</Button>
            </Tooltip>
            <Tooltip content="Подсказка снизу" position="bottom">
              <Button variant="secondary" size="s">Наведи (bottom)</Button>
            </Tooltip>
          </div>
        </div>
      </section>

      {/* ==== Фидбэк ==== */}
      <section className={styles.section}>
        <h2 className="ds-desktop-header-2-medium">Фидбэк</h2>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Status Badge — Success|Error|Warning|Neutral</span>
          <div className={styles.row}>
            <StatusBadge status="success">Квалифицирован</StatusBadge>
            <StatusBadge status="error">Просрочен</StatusBadge>
            <StatusBadge status="warning">В работе</StatusBadge>
            <StatusBadge status="neutral">Новый</StatusBadge>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Toast — Success|Error|Warning|Info</span>
          <div className={styles.row}>
            <Toast status="success">Провайдер подключён</Toast>
            <Toast status="error">Не удалось сохранить</Toast>
            <Toast status="warning">Проверьте данные</Toast>
            <Toast status="info">Изменения сохранены автоматически</Toast>
          </div>
        </div>
      </section>

      {/* ==== Навигация ==== */}
      <section className={styles.section}>
        <h2 className="ds-desktop-header-2-medium">Навигация</h2>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Tabs — один инстанс = один таб</span>
          <div className={styles.row}>
            <Tabs active={activeTab === 'Список'} onClick={() => setActiveTab('Список')}>Список</Tabs>
            <Tabs active={activeTab === 'Канбан'} onClick={() => setActiveTab('Канбан')}>Канбан</Tabs>
            <Tabs disabled>Disabled</Tabs>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Breadcrumb</span>
          <div className={styles.row}>
            <Breadcrumb>Настройки</Breadcrumb>
            <span>/</span>
            <Breadcrumb current>Роли и права</Breadcrumb>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Pagination</span>
          <div className={styles.row}>
            <Pagination icon={<ArrowIcon direction="left" />} />
            <Pagination active>1</Pagination>
            <Pagination>2</Pagination>
            <Pagination>3</Pagination>
            <Pagination disabled>4</Pagination>
            <Pagination icon={<ArrowIcon direction="right" />} />
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>NavListItem — State × Pinned</span>
          <div className={styles.narrow} style={{ background: 'var(--color-bg-surface-primary)', padding: 'var(--space-sm)', borderRadius: 'var(--radius-sm)' }}>
            <NavListItem active>Лиды</NavListItem>
            <NavListItem pinned>Канбан</NavListItem>
            <NavListItem>Дашборд</NavListItem>
            <NavListItem>Настройки</NavListItem>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Header</span>
          <Header title="Генератор лидов" userName="Марина Кузнецова" avatar={<Avatar size="md" initials="МК" />} />
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Sidebar + Header — композиция шелла (наведи курсор на рельс, чтобы раскрыть список)</span>
          <div className={styles.shellRow}>
            <Sidebar />
            <div className={styles.shellBody}>
              <Header title="Генератор лидов" userName="Марина Кузнецова" avatar={<Avatar size="md" initials="МК" />} />
            </div>
          </div>
        </div>
      </section>

      {/* ==== Данные ==== */}
      <section className={styles.section}>
        <h2 className="ds-desktop-header-2-medium">Данные</h2>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Table Cell + Table</span>
          <Table
            density="default"
            columns={[
              { key: 'name', label: 'Имя и компания', width: 'fill' },
              { key: 'score', label: 'Скор', width: 90 },
              { key: 'status', label: 'Статус', width: 160 },
            ]}
            rows={[
              { name: 'Иванов Пётр, Ленинградский зоопарк', score: '82', status: <StatusBadge status="neutral">Новый</StatusBadge> },
              { name: 'Соколова Анна, Музей петербургского авангарда', score: '65', status: <StatusBadge status="warning">В работе</StatusBadge> },
              { name: 'Кузнецова Мария, ГМИИ им. А.С. Пушкина', score: '45', status: <StatusBadge status="error">Перезвонить</StatusBadge> },
            ]}
          />
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Table Cell — типы отдельно</span>
          <div className={styles.row}>
            <TableCell type="header">Заголовок</TableCell>
            <TableCell type="text">Текстовая ячейка</TableCell>
            <TableCell type="status">
              <StatusBadge status="success">Активно</StatusBadge>
            </TableCell>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>KanbanCard — Overdue No|Yes</span>
          <div className={styles.row}>
            <KanbanCard channel="Форма" nameCompany="Иванов Пётр, Ленинградский зоопарк" score={82} timeText="12 мин назад" managerName="Игорь Петров" managerInitials="ИП" />
            <KanbanCard channel="Чат" nameCompany="Дмитриев Олег, Петропавловская крепость" score={91} timeText="40 мин назад" />
            <KanbanCard channel="Форма" nameCompany="Кузнецова Мария, ГМИИ им. А.С. Пушкина" score={45} timeText="1 день назад — Просрочен" managerName="Игорь Петров" managerInitials="ИП" overdue />
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>TimelineItem — Call|Form|Chat</span>
          <div className={styles.column}>
            <TimelineItem type="call" title="Звонок исходящий" meta="1 день назад — Игорь Петров" quote="Просила перезвонить после обеда" />
            <TimelineItem type="form" title="Заявка с сайта" meta="3 дня назад" quote="Интересует установка 50 билетных систем" />
            <TimelineItem type="chat" title="Обращение через чат-виджет сайта" meta="Сегодня, 14:02" quote="Спрашивают об интеграции системы контроля доступа" />
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>MessageBubble — Client|Manager</span>
          <div className={styles.column}>
            <MessageBubble sender="client" meta="Клиент, 14:02" message="Здравствуйте! Подскажите про интеграцию" />
            <MessageBubble sender="manager" meta="Менеджер (Игорь Петров), 14:05" message="Добрый день! Да, есть такая возможность" />
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>FunnelBar — Tone Neutral|Negative</span>
          <div className={styles.column} style={{ width: '100%' }}>
            <FunnelBar label="Новый" value={42} percent={100} />
            <FunnelBar label="В работе" value={35} percent={83} />
            <FunnelBar label="Перезвонить" value={18} percent={43} />
            <FunnelBar label="Не подходит" value={8} percent={19} tone="negative" />
          </div>
        </div>
      </section>

      {/* ==== Контейнеры ==== */}
      <section className={styles.section}>
        <h2 className="ds-desktop-header-2-medium">Контейнеры</h2>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>Card — Padding × Border</span>
          <div className={styles.row}>
            <Card padding="default" border>
              <span className="ds-desktop-main-medium">Card title</span>
              <span className="ds-desktop-main-regular">Card body content goes here.</span>
            </Card>
            <Card padding="compact">
              <span className="ds-desktop-main-medium">Compact, no border</span>
            </Card>
          </div>
        </div>

        <div className={styles.componentBlock}>
          <span className={styles.componentBlockTitle}>MetricCard — Trend Neutral|Positive|Negative</span>
          <div className={styles.row}>
            <MetricCard label="Время первого ответа" value="4 мин" caption="цель &lt; 5 мин" trend="positive" />
            <MetricCard label="Просроченные лиды" value="3" caption="требуют внимания" trend="negative" />
            <MetricCard label="Лидов за период" value="127" caption="всего за месяц" trend="neutral" />
          </div>
        </div>
      </section>
    </div>
  )
}
