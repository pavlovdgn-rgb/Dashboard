import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const api=process.env.LIVE_TEST_API;if(!api)throw Error('Disposable API required');
const dir='.tmp/criteria-journey';await fs.mkdir(dir,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1100}});
await context.tracing.start({screenshots:true,snapshots:true});
const errors=[],serverErrors=[],checks=[],sessions=[];
context.on('page',p=>{p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=500)serverErrors.push(`${r.status()} ${r.url()}`)})});
await context.route('http://127.0.0.1:5174/**',async r=>{const response=await r.fetch({url:r.request().url().replace('http://127.0.0.1:5174',api)});await r.fulfill({response})});
const get=async path=>(await fetch(api+path)).json();
const post=async(path,data)=>{const r=await fetch(api+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});assert.ok(r.ok,await r.clone().text());return r.json()};
const mark=text=>{checks.push(text);console.log('PASS '+text)};
const chat=async page=>{await page.getByRole('button',{name:'Чаты',exact:true}).click();await page.getByRole('button',{name:/Дмитриев Олег/}).click()};
const message=async page=>{await page.getByPlaceholder('Написать сообщение...').fill('Тестовое сообщение');await page.getByRole('button',{name:'Отправить',exact:true}).click()};
let dash;
try{
 // Establish the event using a real chat action in a separate calibration study.
 const calibration=await post('/api/project/studies',{studyTitle:'Калибровка событий'});
 await post('/api/project/config?study='+calibration.studyId,{mode:'free',enabled:true,recordingMode:'screenshots'});
 const calibrationPage=await context.newPage();await calibrationPage.goto(calibration.url);await chat(calibrationPage);await message(calibrationPage);
 await expect.poll(async()=> (await get('/api/project/criteria-catalog?study='+calibration.studyId)).signals.some(s=>s.value==='chat_message_sent')).toBe(true);
 await calibrationPage.close();mark('Событие отправки получено после настоящего действия в прототипе');
 const config=await post('/api/project/studies',{studyTitle:'E2E · ручная и автоматическая оценка'}),id=config.studyId;
 dash=await context.newPage();await dash.goto('http://127.0.0.1:5173/#/setup?study='+id);
 await dash.getByRole('button',{name:'По сценарию',exact:true}).click();
 const first=dash.getByRole('region',{name:'Задание 1',exact:true});
 await first.getByLabel('Название задания',{exact:true}).fill('Найти чат');
 await first.getByLabel('Задание',{exact:true}).fill('Откройте чат с Олегом Дмитриевым.');
 await first.getByLabel('Что считать успехом',{exact:true}).fill('Открыт диалог с Олегом Дмитриевым');
 await first.getByRole('button',{name:'Как проверять результат',exact:true}).click();await dash.getByRole('menuitemradio',{name:'Вручную по записи сессии',exact:true}).click();
 await expect(dash.getByRole('menuitemradio',{name:'Вручную по записи сессии',exact:true})).toHaveCount(0);
 await dash.getByRole('button',{name:'Добавить задание',exact:true}).click();
 const second=dash.getByRole('region',{name:'Задание 2',exact:true});
 await second.getByLabel('Название задания',{exact:true}).fill('Написать сообщение');
 await second.getByLabel('Задание',{exact:true}).fill('Отправьте сообщение в открытый чат.');
 await second.getByLabel('Что считать успехом',{exact:true}).fill('Сообщение отправлено в чат');
 await second.getByRole('button',{name:'Как проверять результат',exact:true}).click();await dash.getByRole('menuitemradio',{name:'Автоматически',exact:true}).click();
 await second.getByLabel('Или укажите имя своего события',{exact:true}).fill('not_connected');await expect(dash.getByRole('button',{name:'Сохранить сценарий'})).toBeDisabled();
 await second.getByRole('button',{name:'Записанное событие',exact:true}).click();await dash.getByRole('menuitemradio',{name:'Отправлено сообщение в чат',exact:true}).click();
 await dash.getByRole('button',{name:'Сохранить сценарий'}).click();await expect(dash.getByText('Сценарий сохранён',{exact:true})).toBeVisible();
 await dash.reload();await expect(first.getByLabel('Что считать успехом',{exact:true})).toHaveValue('Открыт диалог с Олегом Дмитриевым');await expect(second.getByLabel('Или укажите имя своего события',{exact:true})).toHaveValue('chat_message_sent');
 await second.scrollIntoViewIfNeeded();await dash.screenshot({path:dir+'/settings.png'});
 const saved=await get('/api/project/config?study='+id);assert.deepEqual(saved.tasks.map(t=>t.verification.method),['manual','automatic']);
 await post('/api/project/config?study='+id,{enabled:true,recordingMode:'screenshots'});
 mark('Два задания, свои описания и способы проверки созданы через интерфейс и сохранены после перезагрузки');
 const summary=()=>get('/api/project?study='+id);
 const run=async sid=>(await summary()).sessions.find(s=>s.id===sid)?.task;
 async function participant(name,openChat,send,abandon=false){
   const page=await context.newPage();await page.goto(config.url);const dialog=page.getByRole('dialog',{name:'Задание исследования'});
   await expect(dialog).toContainText('Задание 1 из 2');const sid=await page.evaluate(()=>window.__uxLabStatus.session);sessions.push({name,id:sid});
   await dialog.getByRole('button',{name:'Понятно, к заданию'}).click();
   if(abandon){await page.close();return sid}
   if(openChat)await chat(page);
   assert.equal((await run(sid)).tasks[0].status,'pending','Manual result requires researcher review');
   await page.getByRole('button',{name:'Посмотреть задание'}).click();await dialog.getByRole('button',{name:'Завершить задание'}).click();
   await expect(dialog).toContainText('Задание 2 из 2');assert.deepEqual((await run(sid)).tasks.map(t=>t.status),['needs_review','pending']);
   await dialog.getByRole('button',{name:'Понятно, к заданию'}).click();
   if(!openChat)await chat(page);
   assert.equal((await run(sid)).tasks[1].status,'pending','Opening chat cannot complete sending task');
   await page.getByPlaceholder('Написать сообщение...').fill('   ');await expect(page.getByRole('button',{name:'Отправить',exact:true})).toBeDisabled();
   if(send){await message(page);await expect.poll(async()=> (await run(sid)).tasks[1].status).toBe('succeeded')}
   if(send)await expect(dialog).toContainText('Попытка завершена');else {await page.getByRole('button',{name:'Посмотреть задание'}).click();await expect(dialog.getByRole('button',{name:'Завершить задание'})).toBeVisible()}
   await expect.poll(async()=> (await summary()).sessions.find(s=>s.id===sid)?.frames||0).toBeGreaterThan(0);
   await page.close();return sid;
 }
 const success=await participant('Оба выполнены',true,true);
 const failed=await participant('Оба не выполнены',false,false);
 const unknown=await participant('Ручной результат невозможно оценить',false,false);
 const awaiting=await participant('Ожидает ручной оценки',true,false);
 const abandoned=await participant('Прервана до завершения первого задания',false,false,true);
 mark('5 сессий: успех, неуспех, недостаточно данных, ожидание оценки и прерванная попытка');
 async function assess(sid,label){
   await dash.getByRole('button',{name:'Сессии',exact:true}).click();await dash.getByRole('button',{name:sid.slice(0,8),exact:true}).click();
   const table=dash.getByRole('table',{name:'Задания сессии'});await expect(table).toContainText('Открыт диалог с Олегом Дмитриевым');await expect(table).toContainText('Сообщение отправлено в чат');await expect(table).toContainText('Ручная оценка');await expect(table).toContainText('Автоматически');
   await expect(dash.getByRole('heading',{name:'Скриншоты действий',exact:true})).toBeVisible();
   await table.getByRole('button',{name:'Оценка исследователя'}).click();await dash.getByRole('menuitemradio',{name:label,exact:true}).click();
   await expect(table.getByRole('row').nth(1).getByText(label,{exact:true}).first()).toBeVisible();
 }
 await assess(success,'Выполнено');await assess(failed,'Не выполнено');await assess(unknown,'Невозможно оценить');
 await dash.reload();await expect(dash.getByRole('table',{name:'Задания сессии'})).toContainText('Невозможно оценить');
 mark('Ручные оценки выставлены через историю сессий; критерии, способ оценки и запись доступны');
 const expected={ [success]:['succeeded','succeeded'],[failed]:['failed','pending'],[unknown]:['indeterminate','pending'],[awaiting]:['needs_review','pending'],[abandoned]:['pending','not_started']};
 const data=await summary();assert.equal(data.sessions.length,5);
 for(const row of data.sessions){assert.deepEqual(row.task.tasks.map(t=>t.status),expected[row.id]);assert.equal(row.task.tasks.length,2);assert.ok(row.task.tasks[0].startedAt);assert.ok(row.visits>0);if(row.id!==abandoned){assert.ok(row.frames>0);assert.ok(row.clicks>0);assert.ok(row.task.tasks[0].finishedAt);assert.equal(Boolean(row.task.tasks[1].finishedAt),row.id===success)}}
 await dash.getByRole('button',{name:'Обзор результатов',exact:true}).click();const results=dash.getByRole('table',{name:'Результаты заданий'});
 await expect(results.getByText('1 из 5 сессий',{exact:true})).toHaveCount(2);
 for(const bar of await results.getByRole('progressbar').all())await expect(bar).toHaveAttribute('aria-valuetext','20% (1 из 5)');
 const manualRow=results.getByRole('row').filter({hasText:'Найти чат'}),autoRow=results.getByRole('row').filter({hasText:'Написать сообщение'});
 for(const text of ['Не выполнено: 1','Без итога: 1','Ожидает оценки: 1','Невозможно оценить: 1'])await expect(manualRow).toContainText(text);
 await expect(autoRow).toContainText('Без итога: 3');await expect(autoRow).toContainText('Не начато: 1');
 await results.scrollIntoViewIfNeeded();await dash.screenshot({path:dir+'/overview.png'});
 mark('Обзор: по каждому заданию 1/5 = 20%, остальные статусы посчитаны отдельно');
 await dash.getByRole('button',{name:'Сессии',exact:true}).click();const list=dash.getByRole('table',{name:'Сессии Lead Generation'});
 await expect(list.getByRole('row').filter({hasText:success.slice(0,8)})).toContainText('2 из 2 заданий');
 // Review the discoverability of outstanding manual work, not only the database status.
 await expect(list.getByRole('row').filter({hasText:awaiting.slice(0,8)})).toContainText('Ожидает оценки: 1');
 await expect(list.getByRole('row').filter({hasText:unknown.slice(0,8)})).toContainText('Невозможно оценить: 1');
 await expect(list.getByRole('row').filter({hasText:abandoned.slice(0,8)})).toContainText('Не завершено: 2');
 mark('Список сессий показывает ожидание оценки, невозможность оценки и незавершённые задания');
 await dash.screenshot({path:dir+'/sessions.png'});
 await dash.getByRole('button',{name:success.slice(0,8),exact:true}).click();await dash.getByRole('table',{name:'Задания сессии'}).scrollIntoViewIfNeeded();await dash.screenshot({path:dir+'/session-success.png'});
 await dash.getByRole('button',{name:'Отчёты',exact:true}).click();await dash.getByRole('button',{name:'Создать отчёт',exact:true}).click();await dash.getByRole('button',{name:'Сформировать PDF',exact:true}).click();await expect(dash.getByRole('button',{name:'Скачать PDF',exact:true})).toBeVisible();
 const report=(await summary()).reports[0];assert.equal(report.sessions.length,5);for(const row of report.sessions)assert.deepEqual(row.task.tasks.map(t=>t.status),expected[row.id]);
 mark('Сохранённый отчёт содержит те же 5 сессий и результаты обоих заданий');
 assert.deepEqual(errors,[]);assert.deepEqual(serverErrors,[]);
 await fs.writeFile(dir+'/result.json',JSON.stringify({checks,sessions,totals:data.total,statuses:expected,errors,serverErrors},null,2));
}catch(e){if(dash)await dash.screenshot({path:dir+'/failure.png'}).catch(()=>{});throw e}
finally{await context.tracing.stop({path:dir+'/trace.zip'});await browser.close()}
