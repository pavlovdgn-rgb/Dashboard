import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
const api=process.env.LIVE_TEST_API;
if(!api)throw Error('Only use an isolated test API');
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
const errors=[];
context.on('page',page=>page.on('pageerror',e=>errors.push(e.message)));
await context.route('http://127.0.0.1:5174/**',async route=>{
 const response=await route.fetch({url:route.request().url().replace('http://127.0.0.1:5174',api)});await route.fulfill({response});
});
const get=async path=>(await fetch(api+path)).json();
const post=async(path,data)=>(await fetch(api+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})).json();
try{
 const page=await context.newPage();await page.goto('http://127.0.0.1:5173/#/studies');
 const create=page.getByRole('button',{name:'Создать исследование',exact:true});await expect(create).toBeVisible();assert.equal((await create.boundingBox()).height,56);
 await expect(page.getByRole('button',{name:'Обновить',exact:true})).toHaveCount(0);
 await create.click();const dialog=page.getByRole('dialog');await expect(dialog.getByRole('button',{name:'Создать',exact:true})).toBeDisabled();
 await dialog.getByLabel('Название исследования',{exact:true}).fill('Проверка фильтров');await dialog.getByLabel('Сценарий для участника (необязательно)',{exact:true}).fill('Найдите лид через фильтр канала.');
 await dialog.getByRole('button',{name:'Создать',exact:true}).click();await expect(page).toHaveURL(/study=study-/);
 const a=new URLSearchParams(page.url().split('?')[1]).get('study');assert.ok(a);
 await expect(page.getByRole('heading',{name:'Настройка исследования',exact:true})).toBeVisible();
 await expect(page.getByLabel('Задание',{exact:true})).toHaveValue('Найдите лид через фильтр канала.');
 await page.getByLabel('Задание',{exact:true}).fill('Откройте фильтр канала и выберите форму.');await page.getByRole('button',{name:'Сохранить сценарий',exact:true}).click();await expect(page.getByText('Сценарий сохранён',{exact:true})).toBeVisible();
 await page.getByRole('button',{name:'Проверка и запуск',exact:true}).first().click();await expect(page).toHaveURL(new RegExp('study='+a));
 const control=page.getByRole('switch',{name:'Сбор данных',exact:true});await expect(control).not.toBeChecked();await control.click();await expect(control).toBeChecked();
 const config=await get('/api/project/config?study='+a);assert.equal(config.enabled,true);assert.ok(config.url.includes('ux_study='+a));
 await post('/api/project/config?study='+a,{recordingMode:'screenshots'});
 const target=await context.newPage();await target.goto(config.url);await expect(target.getByRole('dialog',{name:'Задание исследования'})).toContainText('Откройте фильтр канала и выберите форму.');
 await expect.poll(async()=>(await get('/api/project?study='+a)).total.sessions,{timeout:15000}).toBe(1);
 const before=await get('/api/project?study='+a),session=before.sessions[0].id;
 await target.getByRole('button',{name:'Понятно, к заданию'}).click();
 await target.getByRole('button',{name:'Канал: Все',exact:true}).click();
 await expect.poll(async()=>(await get('/api/project?study='+a)).total.clicks).toBeGreaterThan(0);
 await expect.poll(async()=>(await get('/api/project/frames?study='+a+'&session='+session)).frames.length,{timeout:15000}).toBeGreaterThan(1);
 const b=await post('/api/project/studies',{studyTitle:'Второй сценарий',scenario:'Создайте лид.'});
 const second=await context.newPage();await second.goto(b.url);await expect(second.getByRole('dialog',{name:'Задание исследования'})).toContainText('Создайте лид.');
 assert.equal((await get('/api/project?study='+b.studyId)).total.sessions,0);
 await post('/api/project/config?study='+b.studyId,{enabled:true,collectClicks:false,recordingMode:'screenshots'});
 await expect.poll(async()=>(await get('/api/project?study='+b.studyId)).total.sessions).toBe(1);
 await second.getByRole('button',{name:'Понятно, к заданию'}).click();
 await second.getByRole('button',{name:'Канал: Все',exact:true}).click();assert.equal((await get('/api/project?study='+b.studyId)).total.clicks,0);
 assert.equal((await get('/api/project')).total.clicks,4,'Legacy events preserved');
 await page.goto('http://127.0.0.1:5173/#/studies');await expect(page.getByRole('table',{name:'Исследования'}).getByRole('row')).toHaveCount(4);
 await page.getByRole('table',{name:'Исследования'}).getByRole('button',{name:'Проверка фильтров',exact:true}).click();await expect(page).toHaveURL(new RegExp('study='+a));
 await page.getByRole('button',{name:'Тепловая карта',exact:true}).click();await expect(page.getByTestId('real-click-count')).toContainText('1 сессий');
 await page.getByRole('button',{name:'Сессии',exact:true}).click();await expect(page.getByRole('table',{name:'Сессии Lead Generation'}).getByRole('row')).toHaveCount(2);
 await page.getByRole('button',{name:session.slice(0,8),exact:true}).click();await expect(page.getByRole('heading',{name:'Скриншоты действий',exact:true})).toBeVisible();
 await page.screenshot({path:'.tmp/multi-study-replay.png'});
 await page.goto('http://127.0.0.1:5173/#/studies');await page.screenshot({path:'.tmp/multi-study-list.png'});
 // A paused study's queued video must not block uploading another study's recording.
 await post('/api/project/config?study='+a,{enabled:false});await post('/api/project/config?study='+b.studyId,{recordingMode:'video',allowVideo:true});
 await second.evaluate(async({a,b})=>{
   const q=await import('/src/ux-lab/videoQueue.ts');
   const bytes=new Uint8Array([0x1a,0x45,0xdf,0xa3,0x80,0x18,0x53,0x80,0x67,0xff,0x15,0x49,0xa9,0x66,0x87,0x2a,0xd7,0xb1,0x83,0x0f,0x42,0x40]);
   for(const [id,study]of [['queued-paused',a],['queued-active',b]]){
     const job={id,study,session:'video-isolation',startedAt:Date.now(),mime:'video/webm',chunks:0,duration:1,finished:false,interrupted:false};
     await q.beginVideo(job);await q.saveVideoChunk(job,new Blob([bytes],{type:'video/webm'}));await q.finishVideo(job);
   }
   await q.flushVideos();
 },{a,b:b.studyId});
 await expect.poll(async()=>(await get('/api/recordings?study='+b.studyId+'&session=video-isolation')).some(r=>r.status==='ready'),{timeout:15000}).toBe(true);
 assert.equal((await get('/api/recordings?study='+a+'&session=video-isolation')).length,0);
 await expect(second.getByRole('button',{name:'Начать запись теста',exact:true})).toBeEnabled({timeout:15000});
 assert.deepEqual(errors,[]);console.log('PASS study creation, scenario editing, scoped launch, two participant links, independent settings, click/frame isolation, sessions/heatmap/replay, preserved legacy data');
}finally{await browser.close();}
