import {chromium,expect} from '@playwright/test';
import {mkdir,stat} from 'node:fs/promises';
import path from 'node:path';

const base=process.env.UXLAB_TEST_URL||'http://127.0.0.1:5184';
const output=path.resolve('../.tmp/vercel-browser');await mkdir(output,{recursive:true});
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:960},acceptDownloads:true});
// Match Vercel's public-path rewrite form, including the appended query metadata.
await context.route('**/api/**',route=>{
  const url=new URL(route.request().url());url.searchParams.set('__path',url.pathname);
  return route.continue({url:url.toString()});
});
const errors=[],failed=[];
context.on('page',page=>{
  page.on('pageerror',error=>errors.push(error.message));
  page.on('request',request=>{if(/127\.0\.0\.1:517[3-7]|localhost:517[3-7]/.test(request.url()))failed.push(request.url());});
});
try{
  const page=await context.newPage();await page.goto(base);
  await page.getByLabel('Пароль',{exact:true}).fill('test-password-cloud-123');
  await page.getByRole('button',{name:'Войти',exact:true}).click();
  await expect(page.getByText('Облачное рабочее пространство',{exact:true})).toBeVisible();
  await context.request.get(base+'/api/project');
  const participant=await context.newPage();
  await participant.addInitScript(()=>{
    // Test video uses a generated canvas; it never captures the user's screen.
    Object.defineProperty(navigator.mediaDevices,'getDisplayMedia',{value:async()=>{
      const canvas=document.createElement('canvas');canvas.width=640;canvas.height=360;
      const ctx=canvas.getContext('2d');let tick=0;
      const timer=setInterval(()=>{ctx.fillStyle=`hsl(${tick++*13%360} 70% 50%)`;ctx.fillRect(0,0,640,360);ctx.fillStyle='white';ctx.fillRect(tick*11%600,80,40,80);},60);
      const stream=canvas.captureStream(15);stream.getVideoTracks()[0].addEventListener('ended',()=>clearInterval(timer));return stream;
    }});
  });
  await participant.goto(base+'/participant/leads-table?ux_study=leed-local');
  await participant.waitForFunction(()=>Boolean(window.__uxLabStatus?.session),null,{timeout:20000});
  await expect(participant.getByText('Иванов Пётр',{exact:false}).first()).toBeVisible({timeout:20000});
  await expect.poll(async()=>{const response=await context.request.get(base+'/api/project');return (await response.json()).total.sessions;}).toBeGreaterThan(0);
  await participant.mouse.click(960,320);
  await participant.mouse.click(1100,460);
  await expect.poll(async()=>{const response=await context.request.get(base+'/api/heatmap?study=leed-local');return (await response.json()).total.clicks;},{timeout:20000}).toBeGreaterThan(0);
  await page.goto(base+'/#/heatmap?device=all');
  const map=page.getByTestId('captured-heatmap');
  await expect(map).toHaveAttribute('data-background','saved',{timeout:25000});
  await page.screenshot({path:path.join(output,'heatmap.png'),fullPage:true});
  const downloaded=page.waitForEvent('download',{timeout:60000});
  await page.getByRole('button',{name:'Скачать',exact:true}).click();
  const png=await downloaded;await png.saveAs(path.join(output,'export.png'));
  expect((await stat(path.join(output,'export.png'))).size).toBeGreaterThan(10000);
  await page.getByRole('button',{name:'Варианты скачивания'}).click();
  const zipPromise=page.waitForEvent('download',{timeout:60000});
  await page.getByRole('menuitem').filter({hasText:'Все экраны'}).click();
  await (await zipPromise).saveAs(path.join(output,'heatmaps.zip'));
  expect((await stat(path.join(output,'heatmaps.zip'))).size).toBeGreaterThan(10000);
  await page.goto(base+'/#/launch');
  await expect(page.getByRole('heading',{name:'Ссылка для участника'})).toBeVisible();
  await expect(page.getByRole('textbox',{name:'Ссылка для участника'})).toHaveValue(new RegExp('^'+base.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'/participant/'));
  await participant.getByRole('button',{name:'Начать запись теста',exact:true}).click();
  await expect(participant.getByText('Идёт запись · 0:03',{exact:true})).toBeVisible({timeout:15000});
  await participant.getByRole('button',{name:'Завершить запись',exact:true}).click();
  await expect(participant.getByRole('link',{name:'Посмотреть запись'})).toBeVisible({timeout:30000});
  const videoLink=await participant.getByRole('link',{name:'Посмотреть запись'}).getAttribute('href');
  await page.goto(base+videoLink);
  const video=page.getByLabel('Видео прохождения теста',{exact:true});
  await expect.poll(()=>video.evaluate(element=>element.readyState),{timeout:20000}).toBeGreaterThanOrEqual(1);
  const duration=await video.evaluate(element=>element.duration);expect(duration).toBeGreaterThan(2);expect(Number.isFinite(duration)).toBe(true);
  await video.evaluate(async element=>{element.currentTime=1;await element.play();});
  await expect.poll(()=>video.evaluate(element=>element.currentTime)).toBeGreaterThan(1);
  const videoDownload=page.waitForEvent('download',{timeout:30000});
  await page.getByRole('link',{name:/Скачать.*(видео|запись|WebM)/i}).click();
  await (await videoDownload).saveAs(path.join(output,'recording.webm'));
  expect(failed).toEqual([]);expect(errors).toEqual([]);
  console.log(JSON.stringify({login:true,participant:true,clicks:true,snapshots:true,png:true,zip:true,publicParticipantLink:true,videoRecording:true,videoPlayback:true,videoDownload:true,oldLocalRequests:failed,browserErrors:errors,output}));
}catch(error){console.error(JSON.stringify({browserErrors:errors,oldLocalRequests:failed}));throw error;}
finally{await browser.close();}
