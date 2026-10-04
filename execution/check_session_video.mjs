import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const api=process.env.LIVE_TEST_API;if(!api)throw Error('Isolated API is required');
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
  const context=await browser.newContext({viewport:{width:1440,height:900}}),errors=[];
  let uploadsOffline=false;
  await context.route('http://127.0.0.1:5174/**',async route=>{if(uploadsOffline&&route.request().url().includes('/api/recordings/chunk'))return route.fulfill({status:503,json:{error:'Verification outage'}});await route.fulfill({response:await route.fetch({url:route.request().url().replace('http://127.0.0.1:5174',api)})});});
  const target=await context.newPage();target.on('pageerror',e=>errors.push(e.message));
  // Supply only a synthetic moving canvas as capture input. No real screen or microphone permission.
  await target.addInitScript(()=>{
    let calls=0;
    Object.defineProperty(navigator.mediaDevices,'getDisplayMedia',{value:async()=>{
      window.__captureCalls=++calls;
      if(calls===1)throw new DOMException('Denied for verification','NotAllowedError');
      const canvas=document.createElement('canvas');canvas.width=640;canvas.height=360;const ctx=canvas.getContext('2d');let frame=0;
      const timer=setInterval(()=>{ctx.fillStyle='#eceedc';ctx.fillRect(0,0,640,360);ctx.fillStyle='#616f30';ctx.fillRect((frame++*4)%560,80,80,80);ctx.font='30px sans-serif';ctx.fillText('Video pipeline verification',20,260)},50);
      const stream=canvas.captureStream(15);stream.getTracks()[0].addEventListener('ended',()=>clearInterval(timer));return stream;
    }});
  });
  await target.goto('http://127.0.0.1:5175/leads-table?ux_study=leed-local');
  await target.waitForFunction(()=>Boolean(window.__uxLabStatus?.session));
  const session=await target.evaluate(()=>window.__uxLabStatus.session);
  const start=target.getByRole('button',{name:'Начать запись теста',exact:true});
  await start.click();await expect(target.getByRole('status').filter({hasText:'разрешение не выдано'})).toBeVisible();
  assert.equal((await(await fetch(api+`/api/recordings?session=${session}`)).json()).length,0);
  await start.click();await expect(target.getByRole('button',{name:'Завершить запись',exact:true})).toBeVisible();
  uploadsOffline=true;
  await target.waitForTimeout(2400);await target.mouse.click(600,750);
  await target.waitForTimeout(2200);await target.getByRole('button',{name:'Завершить запись',exact:true}).click();
  await expect(target.getByRole('button',{name:'Повторить отправку',exact:true})).toBeVisible();
  uploadsOffline=false; // The queue must resume automatically without another capture permission.
  await expect.poll(async()=>{const list=await(await fetch(api+`/api/recordings?session=${session}`)).json();return list[0]?.status},{timeout:20000}).toBe('ready');
  const record=(await(await fetch(api+`/api/recordings?session=${session}`)).json())[0];
  assert.ok(record.duration>=4&&record.chunks>=2);
  const dashboard=await context.newPage();dashboard.on('pageerror',e=>errors.push(e.message));
  await dashboard.goto(`http://127.0.0.1:5173/#/participant?participant=${session}`);
  const video=dashboard.getByLabel('Видео прохождения теста');
  await expect.poll(()=>video.evaluate(el=>el.readyState)).toBeGreaterThanOrEqual(1);
  assert.ok(Number.isFinite(await video.evaluate(el=>el.duration)),'Finite WebM duration');
  await dashboard.getByRole('button',{name:'Воспроизвести',exact:true}).click();
  await expect.poll(()=>video.evaluate(el=>el.currentTime)).toBeGreaterThan(.2);
  await dashboard.getByRole('button',{name:'Пауза',exact:true}).click();
  assert.equal(await video.evaluate(el=>el.paused),true);
  await dashboard.getByRole('slider',{name:'Временная шкала записи'}).fill('3');
  await expect.poll(()=>video.evaluate(el=>el.currentTime)).toBeCloseTo(3,1);
  await dashboard.getByRole('button',{name:'Скорость видео',exact:true}).click();
  await dashboard.getByRole('menuitemradio',{name:'2×',exact:true}).click();
  assert.equal(await video.evaluate(el=>el.playbackRate),2);
  await dashboard.getByRole('button',{name:/Перейти к событию/}).first().click();
  assert.ok((await video.evaluate(el=>el.currentTime))<3);
  await fs.mkdir('.tmp/video',{recursive:true});await dashboard.screenshot({path:'.tmp/video/player.png',fullPage:true});
  const response=await fetch(api+`/api/recordings/media?id=${record.id}`,{headers:{Range:'bytes=0-15'}});assert.equal(response.status,206);
  const bytes=Buffer.from(await(await fetch(api+`/api/recordings/media?id=${record.id}`)).arrayBuffer());await fs.writeFile('.tmp/video/verification.webm',bytes);
  // A reload ends the stream; the next load recovers the last durable chunks, labelled partial.
  await expect(start).toBeEnabled();await start.click();
  await expect(target.getByRole('button',{name:'Завершить запись',exact:true})).toBeVisible();
  await target.waitForTimeout(2400);
  target.on('dialog',dialog=>void dialog.accept());await target.reload();
  await expect.poll(async()=>{const list=await(await fetch(api+`/api/recordings?session=${session}`)).json();return list.filter(item=>item.status==='ready').length},{timeout:20000}).toBe(2);
  const recovered=(await(await fetch(api+`/api/recordings?session=${session}`)).json())[1];assert.equal(recovered.interrupted,1);
  await expect(start).toBeEnabled();await start.click();
  // The init-script denial fixture resets after reload; acknowledge that first request.
  await expect(target.getByRole('status').filter({hasText:'разрешение не выдано'})).toBeVisible();
  await start.click();
  await expect(target.getByRole('button',{name:'Завершить запись',exact:true})).toBeVisible();
  await target.waitForTimeout(2400);
  await fetch(api+'/api/project/config',{method:'POST',body:JSON.stringify({allowVideo:false})});
  await expect(target.getByRole('button',{name:'Завершить запись',exact:true})).toHaveCount(0);
  await expect(start).toBeDisabled();
  await expect.poll(async()=>{const list=await(await fetch(api+`/api/recordings?session=${session}`)).json();return list.filter(item=>item.status==='ready').length},{timeout:20000}).toBe(3);
  assert.deepEqual(errors,[]);console.log('PASS denied permission, MediaRecorder encoding, offline retry, reload recovery, finite duration, play/pause, seek, speed, event markers and HTTP ranges');
}finally {await browser.close();}
