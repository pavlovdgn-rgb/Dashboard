import {chromium,expect} from '@playwright/test';
import {mkdir} from 'node:fs/promises';

const base=process.env.UXLAB_TEST_URL||'http://127.0.0.1:5186';
if(!/^http:\/\/127\.0\.0\.1:\d+$/.test(base))throw Error('Use the isolated local preview only');
await mkdir('../.tmp/automatic-tasks',{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:960}});
const errors=[];context.on('page',page=>page.on('pageerror',e=>errors.push(e.message)));
const post=async(path,data)=>{const r=await context.request.post(base+path,{data});expect(r.ok(),await r.text()).toBe(true);return r.json();};
const get=async path=>{const r=await context.request.get(base+path);expect(r.ok()).toBe(true);return r.json();};
try{
 await post('/api/auth',{password:'test-password-cloud-123'});
 const seed=await post('/api/project/studies',{studyTitle:'Observed controls'});
 await post('/api/project/config?study='+seed.studyId,{enabled:true,mode:'free',collectClicks:false,recordingMode:'screenshots'});
 const catalogPage=await context.newPage();
 const policy=catalogPage.waitForResponse(r=>r.url().includes('/api/project/config?')&&r.ok());
 await catalogPage.goto(base+'/participant/leads-table?ux_study='+seed.studyId);
 await policy;
 const catalog=async()=> (await get('/api/project/criteria-catalog?study='+seed.studyId)).signals;
 await expect.poll(async()=> (await catalog()).some(s=>s.type==='screen'&&s.value==='leed-leads-table')).toBe(true);
 await expect(catalogPage.getByText('Действия и снимки интерфейса сохраняются автоматически. Значения полей скрыты.')).toHaveCount(0);
 await expect(catalogPage.getByRole('complementary',{name:'Запись теста'})).toHaveCount(0);
 await catalogPage.getByRole('button',{name:'Новый лид',exact:true}).click();
 await expect.poll(async()=> (await catalog()).some(s=>s.type==='element'&&s.label==='Кнопка «Новый лид»')).toBe(true);
 const target=(await catalog()).find(s=>s.type==='element'&&s.label==='Кнопка «Новый лид»');
 await catalogPage.goto(base+'/participant/settings/telephony?ux_study='+seed.studyId);
 await expect.poll(async()=> (await catalog()).some(s=>s.type==='screen'&&s.value==='leed-telephony-settings')).toBe(true);
 await catalogPage.close();
 const study=await post('/api/project/studies',{studyTitle:'Automatic completion'}),id=study.studyId;
 const task=(id,title,verification)=>({id,title,instruction:title,criterion:'custom',successDescription:'Цель достигнута',verification});
 const tasks=[task('screen','Откройте телефонию',{method:'automatic',type:'screen',value:'leed-telephony-settings',page:'leed-telephony-settings'}),
  task('element','Нажмите Новый лид',{method:'automatic',type:'element',value:target.value,page:target.page}),
  task('manual','Ручная проверка',{method:'manual'})];
 await post('/api/project/config?study='+id,{enabled:true,mode:'scenario',collectClicks:false,collectVisits:false,recordingMode:'screenshots',tasks});
 const page=await context.newPage();await page.goto(base+'/participant/leads-table?ux_study='+id);
 const dialog=page.getByRole('dialog',{name:'Задание исследования'});
 await expect(dialog).toContainText('Задание завершится автоматически');
 await expect(dialog.getByRole('button',{name:'Завершить задание'})).toHaveCount(0);
 await dialog.getByRole('button',{name:'Понятно, к заданию'}).click();
 const session=await page.evaluate(()=>window.__uxLabStatus.session);
 const run=async()=> (await get('/api/project?study='+id)).sessions.find(s=>s.id===session)?.task;
 await page.goto(base+'/participant/settings/telephony?ux_study='+id);
 await expect(dialog).toContainText('Задание 2 из 3');
 expect((await run()).tasks[0].status).toBe('succeeded');expect((await run()).finishedTasks).toBe(1);
 await page.goto(base+'/participant/leads-table?ux_study='+id);
 await expect(dialog).toContainText('Задание 2 из 3');
 await expect(dialog.getByRole('button',{name:'Завершить задание'})).toHaveCount(0);
 await page.screenshot({path:'../.tmp/automatic-tasks/automatic.png'});
 await dialog.getByRole('button',{name:'Понятно, к заданию'}).click();
 // Lose one response before processing, then allow the persisted event queue to retry.
 let offline=true;
 await page.route('**/api/project/task-events',async route=>{
  const body=route.request().postDataJSON();
  if(offline&&body.kind==='element_clicked'&&body.value===target.value){offline=false;return route.abort();}
  return route.continue();
 });
 await page.getByRole('button',{name:'Новый лид',exact:true}).click();
 await expect(dialog).toContainText('Задание 3 из 3',{timeout:15000});
 expect((await run()).succeededTasks).toBe(2);expect((await run()).finishedTasks).toBe(2);
 await expect(dialog.getByRole('button',{name:'Завершить задание'})).toBeVisible();
 await dialog.getByRole('button',{name:'Завершить задание'}).click();
 await expect(dialog).toContainText('Попытка завершена');
 expect((await run()).tasks[2].status).toBe('needs_review');
 await page.close();
 // A single automatic task must show the final confirmation without any finish click.
 const finalStudy=await post('/api/project/studies',{studyTitle:'Single automatic task'});
 await post('/api/project/config?study='+finalStudy.studyId,{enabled:true,mode:'scenario',collectClicks:false,recordingMode:'screenshots',tasks:[tasks[1]]});
 const last=await context.newPage();await last.goto(base+'/participant/leads-table?ux_study='+finalStudy.studyId);
 const finalDialog=last.getByRole('dialog');await expect(finalDialog).toContainText('Задание завершится автоматически');
 await finalDialog.getByRole('button',{name:'Понятно, к заданию'}).click();
 await last.getByRole('button',{name:'Новый лид',exact:true}).click();
 await expect(finalDialog).toContainText('Попытка завершена');
 await expect(finalDialog.getByRole('button',{name:'Завершить задание'})).toHaveCount(0);
 await last.screenshot({path:'../.tmp/automatic-tasks/complete.png'});
 await last.reload();await expect(finalDialog).toContainText('Попытка завершена');
 expect(errors).toEqual([]);
 console.log('PASS screen and real button completion, hidden manual finish, next task, final dialog, manual review, disabled click/visit collection, retry and reload');
}finally{await browser.close();}
