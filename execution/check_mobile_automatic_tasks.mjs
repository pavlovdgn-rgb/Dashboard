/** Real mobile UI + isolated cloud handler. Never writes to a production study. */
import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
const api=process.env.MOBILE_TEST_API,app=process.env.MOBILE_TEST_APP;
if(!api?.startsWith('http://127.0.0.1:')||!app?.startsWith('http://127.0.0.1:'))throw Error('Explicit isolated local servers required');
const folder=new URL('../.tmp/mobile-automatic/',import.meta.url);await mkdir(folder,{recursive:true});
const auth=await fetch(api+'/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:'test-password-cloud-123'})});
assert.equal(auth.status,200);const cookie=auth.headers.get('set-cookie').split(';')[0];
async function request(path,data){const response=await fetch(api+path,{headers:{Cookie:cookie,'Content-Type':'application/json'},...(data===undefined?{}:{method:'POST',body:JSON.stringify(data)})});assert.ok(response.ok,await response.clone().text());return response.json();}
const browser=await chromium.launch({channel:'chrome',headless:true});const errors=[];
try{
 const dashboard=await browser.newContext({viewport:{width:1440,height:1100}});
 await dashboard.addCookies([{name:'uxlab_session',value:cookie.slice(cookie.indexOf('=')+1),url:api}]);
 const editor=await dashboard.newPage();editor.on('pageerror',error=>errors.push(error.message));
 const created=await request('/api/project/studies',{studyTitle:'Six automatic mobile tasks'}),study=created.studyId;
 await editor.goto(api+'/#/setup?study='+study);
 await editor.getByRole('button',{name:'Загрузить 6 заданий для повторного теста',exact:true}).click();
 await editor.getByRole('button',{name:'Загрузить задания',exact:true}).click();
 await expect(editor.getByLabel('Название задания',{exact:true})).toHaveCount(6);
 await editor.getByRole('button',{name:'Сохранить сценарий',exact:true}).click();
 await expect(editor.getByText('Сценарий сохранён',{exact:true})).toBeVisible();
 let config=await request('/api/project/config?study='+study,{enabled:true,collectClicks:true,collectVisits:true});
 assert.equal(config.tasks.length,6);assert.ok(config.tasks.every(task=>task.verification.method==='automatic'));
 assert.deepEqual(config.tasks[2].verification,{method:'automatic',type:'screen',value:'bb-done',page:'bb-done'});
 await editor.screenshot({path:new URL('configured.png',folder).pathname});
 const mobile=await browser.newContext({viewport:{width:393,height:852},isMobile:true,hasTouch:true});
 let blockWrites=false,holdSlowTraffic=false,holdSuccess=false;
 let releaseSlowTraffic,releaseSuccess;
 const slowGate=new Promise(resolve=>{releaseSlowTraffic=resolve;}),successGate=new Promise(resolve=>{releaseSuccess=resolve;});
 const heldTraffic=new Set();let releasedTraffic=0;
 const studyBridge=async route=>{
  const req=route.request(),url=new URL(req.url());
  const cors={'access-control-allow-origin':app,'access-control-allow-headers':'Content-Type,X-UXLab-Participant','access-control-allow-methods':'GET,POST,OPTIONS'};
  if(req.method()==='OPTIONS')return route.fulfill({status:204,headers:cors});
  if(blockWrites&&url.pathname==='/api/project/task-events')return route.abort('failed');
  const data=req.method()==='POST'?req.postDataJSON():null;
  const success=url.pathname==='/api/project/task-events'&&data?.kind==='prototype_event'&&data.value==='nearby_activity_opened';
  if(holdSuccess&&success)await successGate;
  const response=await fetch(api+url.pathname+url.search,{method:req.method(),headers:{Origin:'https://biletberu-mobile.vercel.app','Content-Type':req.headers()['content-type']||'application/json','X-UXLab-Participant':req.headers()['x-uxlab-participant']||''},...(req.method()==='POST'?{body:req.postDataBuffer()}: {})});
  if(!response.ok)console.log('Test bridge response',url.pathname,response.status,await response.clone().text());
  const slowKind=url.pathname==='/api/project/config'?'config':url.pathname==='/api/project/visit'?'visit':url.pathname.startsWith('/api/heatmap/')?'heatmap':data?.kind==='screen_visited'||data?.kind==='element_clicked'?'catalog':null;
  if(holdSlowTraffic&&slowKind){heldTraffic.add(slowKind);await slowGate;releasedTraffic++;}
  await route.fulfill({status:response.status,headers:{...cors,'content-type':response.headers.get('content-type')||'application/json'},body:Buffer.from(await response.arrayBuffer())});
 };
 await mobile.route('https://dashboard-woad-one-64.vercel.app/**',studyBridge);
 await mobile.addInitScript(()=>{
  window.__paymentSignalScreens=[];
  addEventListener('ux-success-signal',event=>{if(event.detail?.value==='two_theatre_tickets_purchased')window.__paymentSignalScreens.push({path:location.pathname,successVisible:document.body.innerText.includes('Оплата прошла успешно!')});});
  if(!localStorage.getItem('mobile-test-seeded')){localStorage.setItem('mobile-test-seeded','1');localStorage.setItem('bilet-beru-demo-v3',JSON.stringify({cart:{eventId:'weekend',seats:[{id:'16-16',row:16,place:16,category:4},{id:'16-17',row:16,place:17,category:4}]}}));}
 });
 const page=await mobile.newPage();page.on('pageerror',error=>errors.push(error.message));
 function participantLink(cfg){const original=new URL(cfg.url),url=new URL('/app/main',app),fragment=new URLSearchParams(original.hash.slice(1));url.search=original.search;fragment.set('ux_api','https://dashboard-woad-one-64.vercel.app');url.hash=fragment.toString();return url.href;}
 await page.goto(participantLink(config));
 console.log('Study link shape',await page.evaluate(()=>({queryKeys:[...new URLSearchParams(location.search).keys()],hashKeys:[...new URLSearchParams(location.hash.slice(1)).keys()],storedLink:!!sessionStorage.getItem('uxlab-biletberu-link-v1')})));
 const modal=page.getByRole('dialog',{name:'Задание исследования',exact:true});
 const current=async n=>{
  await expect(page.locator('.uxlab-study-count')).toHaveText(`${n}/6`,{timeout:20000});
  await expect(page.locator('.uxlab-study-goal')).toHaveText(config.tasks[n-1].title);
  await expect(modal).not.toBeVisible();
  const goal=await page.locator('.uxlab-study-goal').evaluate(el=>({height:el.clientHeight,content:el.scrollHeight}));
  assert.ok(goal.content<=goal.height+1,'Short task must fit without opening details');
 };
 const close=async()=>{await modal.getByRole('button',{name:'К приложению',exact:true}).click();};
 const nav=async path=>page.evaluate(path=>{history.pushState({},'',path);dispatchEvent(new PopStateEvent('popstate'));},'/app'+path);
 const run=async()=>{const summary=await request('/api/project?study='+study);return summary.sessions.find(session=>session.task)?.task;};
 await current(1);assert.equal(await page.locator('.uxlab-study').evaluate(el=>el.getBoundingClientRect().height),40);
 await page.setViewportSize({width:320,height:800});await current(1);
 assert.equal(await page.locator('.uxlab-study').evaluate(el=>el.getBoundingClientRect().height),40);
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.screenshot({path:new URL('inline-320.png',folder).pathname});
 await page.setViewportSize({width:393,height:852});
 await page.locator('.uxlab-study-open').click();await expect(modal).toBeVisible();
 await expect(modal.locator('.uxlab-study-title')).toHaveText(config.tasks[0].title);
 await expect(page.locator('.uxlab-study-caption')).toHaveCount(0);
 await expect(modal).not.toContainText(config.studyTitle);
 await page.screenshot({path:new URL('details.png',folder).pathname});await close();
 holdSlowTraffic=true;holdSuccess=true;
 await page.evaluate(()=>document.getElementById('root').dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:1,clientY:1})));
 await expect.poll(()=>heldTraffic.has('catalog')).toBe(true);
 await nav('/activity?id=nook');await expect.poll(async()=> (await run())?.succeededTasks).toBe(0);
 await page.evaluate(()=>dispatchEvent(new Event('online')));
 await expect.poll(()=>heldTraffic.has('config')&&heldTraffic.has('heatmap')).toBe(true);
 await nav('/activity?id=nook&event=weekend');
 await expect(page.locator('.uxlab-study-goal')).toHaveText('✓ Выполнено · сохраняем…',{timeout:1000});
 await expect(page.locator('.uxlab-study-skip')).toBeDisabled();
 assert.equal(await page.locator('.uxlab-study').evaluate(el=>el.getBoundingClientRect().height),40);
 await expect(modal).not.toBeVisible();await page.screenshot({path:new URL('success-saving.png',folder).pathname});
 const transitionStarted=Date.now();holdSuccess=false;releaseSuccess();await current(2);
 const transitionMs=Date.now()-transitionStarted;assert.ok(transitionMs<1000,`Success must not wait for analytics or policy polling (${transitionMs}ms)`);
 await page.getByRole('button',{name:'В избранное',exact:true}).click();await current(3);
 assert.equal(releasedTraffic,0,'Both successes must bypass the held background responses');
 const heldKinds=[...heldTraffic];holdSlowTraffic=false;releaseSlowTraffic();
 await expect.poll(()=>releasedTraffic).toBeGreaterThan(0);
 await expect(page.locator('.uxlab-study-count')).toHaveText('3/6');
 await nav('/payment?demo=1');assert.equal((await run()).succeededTasks,2,'Opening payment is not success');
 await page.getByText('Банковская карта',{exact:true}).click();await page.getByRole('button',{name:'К оплате',exact:true}).click();
 await expect(page.getByText('Банк отклонил платёж. Попробуйте ещё раз или оплатите через СБП',{exact:true}).first()).toBeVisible();
 assert.equal((await run()).succeededTasks,2,'A declined payment is not success');
 assert.deepEqual(await page.evaluate(()=>window.__paymentSignalScreens),[]);
 await page.getByText('СБП (Оплата по QR-коду)',{exact:true}).click();await page.getByRole('button',{name:'К оплате',exact:true}).click();await current(4);
 await expect(page.getByText('Оплата прошла успешно!',{exact:true})).toBeVisible();
 const paymentSignals=await page.evaluate(()=>window.__paymentSignalScreens);
 assert.ok(paymentSignals.length>0&&paymentSignals.every(signal=>signal.path==='/app/done'&&signal.successVisible));
 await nav('/favourites');await current(5);
 await nav('/plan');await current(6);
 await page.screenshot({path:new URL('inline-393.png',folder).pathname});
 await nav('/activity?id=nook&event=weekend');await page.getByRole('button',{name:'Добавить в план дня',exact:true}).click();
 await expect(modal.locator('.uxlab-study-title')).toHaveText('Спасибо за участие!',{timeout:20000});
 await expect(modal).toContainText('Выполнено 6 из 6');assert.equal((await run()).succeededTasks,6);
 await page.screenshot({path:new URL('complete.png',folder).pathname});await close();await expect(page.locator('.uxlab-study')).toHaveCount(0);
 await mobile.close();

 // All visual Done variants share the same completion point; no ticket/home tap is needed.
 const paidStudy=await request('/api/project/studies',{studyTitle:'Payment success screen variants'});
 const paidTask=(({revision,...task})=>task)(config.tasks[2]);
 const paidConfig=await request('/api/project/config?study='+paidStudy.studyId,{enabled:true,mode:'scenario',tasks:[paidTask],collectClicks:false,collectVisits:false});
 for(const variant of ['plain','plan-prompt','existing-plan']){
  const context=await browser.newContext({viewport:{width:393,height:852}});
  await context.route('https://dashboard-woad-one-64.vercel.app/**',studyBridge);
  await context.addInitScript(variant=>localStorage.setItem('bilet-beru-demo-v3',JSON.stringify({
   tickets:[0,1].map(index=>({id:'paid-'+index,orderId:'paid-order',eventId:'weekend',seatId:'16-'+index,row:'16',place:String(index+1),zone:'Партер',price:1000,tariff:'Базовый',owner:'Тест',code:'test'})),
   plans:variant==='existing-plan'?{'2026-04-25':['nook']}:{},planPromptEnabled:variant!=='plain'
  })),variant);
  const screen=await context.newPage();screen.on('pageerror',error=>errors.push(error.message));
  const link=new URL(participantLink(paidConfig));link.pathname='/app/done';await screen.goto(link.href);
  await expect(screen.getByText('Оплата прошла успешно!',{exact:true})).toBeVisible();
  await expect(screen.getByRole('button',{name:'Посмотреть билеты',exact:true})).toBeVisible();
  await expect(screen.getByRole('button',{name:'Вернуться на главную',exact:true})).toBeVisible();
  if(variant==='plan-prompt')await expect(screen.getByText('Спланируем 25 апреля?',{exact:true})).toBeVisible();
  if(variant==='existing-plan')await expect(screen.getByRole('button',{name:/1 место уже в плане/})).toBeVisible();
  await expect(screen.getByRole('dialog',{name:'Задание исследования',exact:true})).toContainText('Выполнено 1 из 1',{timeout:20000});
  await screen.screenshot({path:new URL('payment-'+variant+'.png',folder).pathname});
  await context.close();
 }

 // Retry a skip after a transport failure and reload; it must advance exactly once.
 const skipStudy=await request('/api/project/studies',{studyTitle:'Skip retry'});
 const tasks=config.tasks.slice(0,2).map(({revision,...task})=>task);const skipConfig=await request('/api/project/config?study='+skipStudy.studyId,{enabled:true,mode:'scenario',tasks,collectClicks:false,collectVisits:false});
 const retry=await browser.newContext({viewport:{width:393,height:852}});
 await retry.route('https://dashboard-woad-one-64.vercel.app/**',async route=>{
  const req=route.request(),url=new URL(req.url());const headers={'access-control-allow-origin':app,'access-control-allow-headers':'Content-Type,X-UXLab-Participant','access-control-allow-methods':'GET,POST,OPTIONS'};
  if(req.method()==='OPTIONS')return route.fulfill({status:204,headers});
  if(blockWrites&&url.pathname==='/api/project/task-events')return route.abort();
  const response=await fetch(api+url.pathname+url.search,{method:req.method(),headers:{Origin:'https://biletberu-mobile.vercel.app','Content-Type':'application/json','X-UXLab-Participant':req.headers()['x-uxlab-participant']||''},...(req.method()==='POST'?{body:req.postDataBuffer()}: {})});
  await route.fulfill({status:response.status,headers:{...headers,'content-type':'application/json'},body:Buffer.from(await response.arrayBuffer())});
 });
 const other=await retry.newPage();other.on('pageerror',error=>errors.push(error.message));await other.goto(participantLink(skipConfig));
 const retryModal=other.getByRole('dialog',{name:'Задание исследования',exact:true});
 await expect(other.locator('.uxlab-study-goal')).toHaveText(tasks[0].title);await expect(retryModal).not.toBeVisible();
 await expect(other.locator('.uxlab-study-skip')).toBeEnabled();blockWrites=true;
 await other.locator('.uxlab-study-skip').click();await expect(other.locator('.uxlab-study-skip')).toHaveText('Сохраняем…');
 await other.reload();await expect(other.locator('.uxlab-study-skip')).toBeDisabled();blockWrites=false;
 await expect(other.locator('.uxlab-study-goal')).toHaveText(tasks[1].title,{timeout:20000});await expect(retryModal).not.toBeVisible();await other.locator('.uxlab-study-skip').click();
 await expect(retryModal).toContainText('Пропущено 2',{timeout:20000});
 const skipped=(await request('/api/project?study='+skipStudy.studyId)).sessions[0].task;
 assert.equal(skipped.succeededTasks,0);assert.ok(skipped.tasks.every(task=>task.status==='skipped'));
 await other.screenshot({path:new URL('skipped.png',folder).pathname});
 await retry.close();

 // A real success must survive an offline reload without satisfying the next
 // task, even when both tasks deliberately use the same automatic criterion.
 const offlineStudy=await request('/api/project/studies',{studyTitle:'Automatic success retry'});
 const repeated=tasks.map((task,index)=>({...task,id:'repeat-'+index,verification:tasks[0].verification}));
 const offlineConfig=await request('/api/project/config?study='+offlineStudy.studyId,{enabled:true,mode:'scenario',tasks:repeated,collectClicks:false,collectVisits:false});
 const offline=await browser.newContext({viewport:{width:393,height:852}});await offline.route('https://dashboard-woad-one-64.vercel.app/**',studyBridge);
 const replay=await offline.newPage();replay.on('pageerror',error=>errors.push(error.message));
 await replay.goto(participantLink(offlineConfig));await expect(replay.locator('.uxlab-study-skip')).toBeEnabled();
 blockWrites=true;
 await replay.evaluate(()=>{history.pushState({},'','/app/activity?id=nook&event=weekend');dispatchEvent(new PopStateEvent('popstate'));});
 await expect(replay.locator('.uxlab-study-goal')).toHaveText('✓ Действие выполнено · повторяем сохранение…');
 await replay.reload();await expect(replay.locator('.uxlab-study-skip')).toBeDisabled();blockWrites=false;
 await expect(replay.locator('.uxlab-study-count')).toHaveText('2/2',{timeout:20000});
 await expect(replay.locator('.uxlab-study-goal')).toHaveText(repeated[1].title);
 const recovered=(await request('/api/project?study='+offlineStudy.studyId)).sessions[0].task;
 assert.equal(recovered.succeededTasks,1);assert.equal(recovered.activeTaskId,repeated[1].id);
 await replay.locator('.uxlab-study-skip').click();
 await expect(replay.getByRole('dialog',{name:'Задание исследования',exact:true})).toContainText('Выполнено 1 из 2 · Пропущено 1');
 await offline.close();
 assert.deepEqual(errors,[]);await writeFile(new URL('result.json',folder),JSON.stringify({sixAutomaticTasks:true,purchaseOnSuccessScreen:true,paymentSuccessVariants:3,declinedPaymentRejected:true,nearbyContextChecked:true,skipRetryAndReload:true,automaticSuccessRetryAndReload:true,panelHeight:40,detailsOnlyOnTap:true,inlineSkip:true,noResearchCaption:true,immediateSuccessFeedback:true,priorityTransitionMs:transitionMs,bypassedSlowResponses:heldKinds},null,2));
 console.log('PASS priority task transitions and instant feedback, blocked analytics/config/catalog responses, all six tasks, payment variants, offline success and skip retries after reload.');
}finally{await browser.close();}
