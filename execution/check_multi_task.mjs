import {seedChatSignal,chooseChatCriterion} from './criteria_browser_helpers.mjs';
﻿import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
const api=process.env.LIVE_TEST_API;if(!api)throw Error('Isolated API required');
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1100}});
const errors=[];context.on('page',p=>p.on('pageerror',e=>errors.push(e.message)));
await context.route('http://127.0.0.1:5174/**',async r=>{const response=await r.fetch({url:r.request().url().replace('http://127.0.0.1:5174',api)});await r.fulfill({response});});
const get=async path=>(await fetch(api+path)).json();
const post=async(path,data)=>{const r=await fetch(api+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});assert.ok(r.ok,await r.clone().text());return r.json();};
try{
 await seedChatSignal(post);
 const config=await post('/api/project/studies',{studyTitle:'Два задания',scenario:'Отправьте первое сообщение.'}),id=config.studyId;
 const dash=await context.newPage();await dash.goto('http://127.0.0.1:5173/#/setup?study='+id);
 let first=dash.getByRole('region',{name:'Задание 1',exact:true});
 await first.getByLabel('Название задания',{exact:true}).fill('Первое сообщение');await chooseChatCriterion(dash,first);
 await dash.getByRole('button',{name:'Добавить задание'}).click();const second=dash.getByRole('region',{name:'Задание 2',exact:true});
 await second.getByLabel('Название задания',{exact:true}).fill('Второе сообщение');await second.getByLabel('Задание',{exact:true}).fill('Отправьте ещё одно сообщение.');await chooseChatCriterion(dash,second);
 await first.getByRole('button',{name:'Переместить задание 1 вниз'}).click();await expect(first.getByLabel('Название задания',{exact:true})).toHaveValue('Второе сообщение');await first.getByRole('button',{name:'Переместить задание 1 вниз'}).click();
 await dash.getByRole('button',{name:'Добавить задание'}).click();await dash.getByRole('button',{name:'Удалить задание 3'}).click();
 await dash.getByRole('button',{name:'Сохранить сценарий'}).click();await expect(dash.getByText('Сценарий сохранён',{exact:true})).toBeVisible();
 const saved=await get('/api/project/config?study='+id);assert.equal(saved.tasks.length,2);assert.equal(saved.tasks[0].title,'Первое сообщение');assert.notEqual(saved.tasks[0].id,saved.tasks[1].id);
 await post('/api/project/config?study='+id,{enabled:true,recordingMode:'screenshots'});
 await dash.screenshot({path:'.tmp/multi-task-editor.png'});
 const participant=await context.newPage();await participant.goto(config.url);const modal=participant.getByRole('dialog',{name:'Задание исследования'});
 await expect(modal).toContainText('Задание 1 из 2');await expect(modal.getByRole('button',{name:'Завершить задание'})).toBeVisible();await modal.getByRole('button',{name:'Понятно, к заданию'}).click();
 const session=await participant.evaluate(()=>window.__uxLabStatus.session);
 const run=async sid=>(await get('/api/project?study='+id)).sessions.find(s=>s.id===sid)?.task;
 await participant.getByRole('button',{name:'Чаты',exact:true}).click();await participant.getByRole('button',{name:/Дмитриев Олег/}).click();await participant.getByPlaceholder('Написать сообщение...').fill('Первое');await participant.getByRole('button',{name:'Отправить',exact:true}).click();
 await expect.poll(async()=>(await run(session))?.succeededTasks).toBe(1);
 await participant.getByRole('button',{name:'Посмотреть задание'}).click();await modal.getByRole('button',{name:'Завершить задание'}).click();await expect(modal).toContainText('Задание 2 из 2');assert.equal((await run(session)).tasks[1].status,'pending');
 await participant.reload();await expect(modal).toContainText('Задание 2 из 2');await expect(modal.getByRole('button',{name:'Завершить задание'})).toBeVisible();await modal.getByRole('button',{name:'Понятно, к заданию'}).click();
 await participant.getByRole('button',{name:'Чаты',exact:true}).click();await participant.getByRole('button',{name:/Дмитриев Олег/}).click();await participant.getByPlaceholder('Написать сообщение...').fill('Второе');await participant.getByRole('button',{name:'Отправить',exact:true}).click();await expect.poll(async()=>(await run(session))?.succeededTasks).toBe(2);
 await participant.getByRole('button',{name:'Посмотреть задание'}).click();await modal.getByRole('button',{name:'Завершить задание'}).click();await expect(modal).toContainText('Попытка завершена');
 const failed=await context.newPage();await failed.goto(config.url);await expect(failed.getByRole('button',{name:'Завершить задание'})).toBeVisible();await failed.getByRole('button',{name:'Завершить задание'}).click();await expect(failed.getByRole('dialog')).toContainText('Задание 2 из 2');await failed.getByRole('button',{name:'Завершить задание'}).click();await expect(failed.getByRole('dialog')).toContainText('Попытка завершена');
 const pending=await context.newPage();await pending.goto(config.url);await expect(pending.getByRole('button',{name:'Завершить задание'})).toBeVisible();await pending.close();
 // Fourth session received the same tasks without automatic verification. It belongs in the denominator.
 await post('/api/project/config?study='+id,{tasks:saved.tasks.map(({revision,verification,successDescription,...t})=>({...t,criterion:'none'}))});
 const unassessed=await context.newPage();await unassessed.goto(config.url);await expect(unassessed.getByRole('button',{name:'Завершить задание'})).toBeVisible();await unassessed.getByRole('button',{name:'Завершить задание'}).click();await expect(unassessed.getByRole('dialog')).toContainText('Задание 2 из 2');await unassessed.getByRole('button',{name:'Завершить задание'}).click();await expect(unassessed.getByRole('dialog')).toContainText('Попытка завершена');
 await post('/api/project/config?study='+id,{tasks:saved.tasks.map(({revision,...task})=>task)});
 await dash.getByRole('button',{name:'Обзор результатов',exact:true}).click();const results=dash.getByRole('table',{name:'Результаты заданий'});await expect(results.getByText('1 из 4 сессий',{exact:true})).toHaveCount(2);await expect(results.getByRole('progressbar').first()).toHaveAttribute('aria-valuetext','25% (1 из 4)');await expect(results).toContainText('Не оценивалось: 1');await expect(results).toContainText('Не начато: 1');await dash.screenshot({path:'.tmp/multi-task-overview.png'});
 await dash.getByRole('button',{name:'Сессии',exact:true}).click();await expect(dash.getByText('2 из 2 заданий',{exact:true})).toBeVisible();await dash.getByRole('button',{name:session.slice(0,8),exact:true}).click();await expect(dash.getByRole('table',{name:'Задания сессии'}).getByText('Выполнено',{exact:true})).toHaveCount(2);await dash.screenshot({path:'.tmp/multi-task-session.png'});
 const picker=dash.getByRole('button',{name:'Выбрать исследование',exact:true});await picker.click();const menu=dash.getByRole('menu',{name:'Исследования проекта'});await expect(menu).toBeVisible();const anchor=await picker.boundingBox(),popup=await menu.boundingBox();assert.ok(popup.y>=anchor.y+anchor.height-1,'Menu opens below its trigger');assert.ok(Math.abs(popup.x-anchor.x)<20,'Menu aligns to the trigger');const all=dash.getByRole('menuitem',{name:'Все исследования проекта'});await all.hover();assert.equal(await all.locator('.euiContextMenuItem__text').evaluate(n=>getComputedStyle(n).textDecorationLine),'none');await dash.screenshot({path:'.tmp/study-picker-below.png'});await dash.keyboard.press('Escape');
 // Seeded legacy funnel has non-completing sessions and exposes their actual last action.
 await post('/api/project/config',{funnel:['leed-dashboard','leed-leads-table']});await dash.goto('http://127.0.0.1:5173/#/funnel');await expect(dash.getByRole('heading',{name:'Последнее действие у не дошедших'})).toBeVisible();const last=dash.getByRole('table',{name:'Последние действия перед шагом 2'});await expect(last).toBeVisible();await dash.screenshot({path:'.tmp/funnel-last-actions.png'});await last.getByRole('button').first().click();await expect(dash).toHaveURL(/participants.*ids/);
 assert.deepEqual(errors,[]);console.log('PASS list editing/order/delete, sequential real actions, reload, per-task 1/4=25%, session 2/2, unassessed/unfinished, dropdown below/hover, last actions and navigation');
}finally{await browser.close();}

