import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';

const browser=await chromium.launch({channel:'chrome',headless:true});
try {
 const page=await browser.newPage({viewport:{width:1600,height:1050}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const live=await(await fetch('http://127.0.0.1:5174/api/project?device=all')).json();
 let enabled=true,fail=false,release;const writes=[];
 await page.route('http://127.0.0.1:5174/api/project?*',route=>route.fulfill({json:{...live,project:{...live.project,enabled}}}));
 await page.route('http://127.0.0.1:5174/api/project/config',async route=>{
   if(route.request().method()!=='POST')return route.fulfill({json:{...live.project,enabled}});
   writes.push(route.request().postDataJSON());await new Promise(resolve=>release=resolve);
   if(fail)return route.fulfill({status:503,json:{error:'Test failure'}});
   enabled=route.request().postDataJSON().enabled;await route.fulfill({json:{...live.project,enabled}});
 });
 for(const screen of ['setup','launch']){
   await page.goto(`http://127.0.0.1:5173/#/${screen}`);
   const open=page.getByRole('button',{name:screen==='heatmap'?'Открыть тестовый интерфейс':'Открыть Lead Generation',exact:true});
   await expect(open).toBeVisible();assert.equal((await open.boundingBox()).height,56);
 }
 for(const screen of ['projects','studies','overview','signals','funnel','participants','report']){
   await page.goto(`http://127.0.0.1:5173/#/${screen}`);
   await expect(page.getByRole('button',{name:screen==='report'?'Сформировать отчёт':screen==='studies'?'Создать исследование':'Обновить',exact:true})).toBeVisible();
   await expect(page.getByRole('button',{name:/Открыть (Lead Generation|тестовый интерфейс)/})).toHaveCount(0);
 }
 await page.goto('http://127.0.0.1:5173/#/heatmap');
 await expect(page.getByRole('button',{name:'Открыть тестовый интерфейс',exact:true})).toHaveCount(0);
 const panel=page.getByRole('region',{name:'Параметры тепловой карты'});
 await expect(panel.getByRole('button',{name:'Размер окна',exact:true})).toBeVisible();
 const fieldBoxes=await Promise.all(['Сессия участника','Экран','Размер окна'].map(name=>panel.getByRole('button',{name,exact:true}).boundingBox()));
 assert.equal(fieldBoxes[0].y,fieldBoxes[1].y);assert.equal(fieldBoxes[1].y,fieldBoxes[2].y);
 const tabs=panel.getByRole('tablist'),status=panel.locator('[class*="filterStatus"]');
 const tb=await tabs.boundingBox(),sb=await status.boundingBox();assert.ok(sb.x>tb.x+tb.width);
 assert.ok(Math.abs(tb.y+tb.height/2-sb.y-sb.height/2)<2);
 await panel.getByRole('tab',{name:'Первый клик',exact:true}).click();await expect(panel.getByRole('tab',{name:'Первый клик',exact:true})).toHaveAttribute('aria-selected','true');
 await panel.getByRole('tab',{name:'Все клики',exact:true}).click();
 await panel.getByRole('button',{name:'Сессия участника',exact:true}).click();
 await page.getByRole('menuitemradio').filter({hasText:/[1-9]\d* кликов/}).first().click();await expect(page).toHaveURL(/session=/);
 await expect(page.getByRole('button',{name:'Скачать',exact:true})).toBeEnabled();
 const exports=[];
 await page.route('**/api/heatmap/export?**',route=>{exports.push(route.request().url());return route.fulfill({contentType:'image/png',body:Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+afoQAAAAASUVORK5CYII=','base64')});});
 const downloaded=page.waitForEvent('download');await page.getByRole('button',{name:'Скачать',exact:true}).click();await downloaded;assert.ok(exports[0].includes('format=png'));
 await page.getByRole('button',{name:'Варианты скачивания',exact:true}).click();await expect(page.getByRole('menuitem')).toHaveCount(2);assert.equal(exports.length,1);
 const zipped=page.waitForEvent('download');await page.getByRole('menuitem',{name:'Все экраны ZIP'}).click();await zipped;assert.ok(exports[1].includes('format=zip'));
 await page.screenshot({path:'.tmp/heatmap-panel-b.png'});
 await page.setViewportSize({width:760,height:1000});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.setViewportSize({width:1440,height:1000});await page.goto('http://127.0.0.1:5173/#/launch');
 const control=page.getByRole('switch',{name:'Сбор данных',exact:true});await expect(control).toBeChecked();
 await expect(control.locator('.euiSwitch__icons')).toBeHidden();
 await control.click();await expect(control).toBeDisabled();await expect.poll(()=>writes.length).toBe(1);assert.deepEqual(writes[0],{enabled:false});
 release();await expect(control).not.toBeChecked();await expect(page.getByText('Перед тестом включите переключатель', {exact:false})).toBeVisible();
 fail=true;await control.click();await expect.poll(()=>writes.length).toBe(2);release();
 await expect(page.getByText('Не удалось изменить сбор данных. Состояние сохранено. Повторите попытку.',{exact:true})).toBeVisible();await expect(control).not.toBeChecked();
 fail=false;await control.focus();await page.keyboard.press('Space');await expect.poll(()=>writes.length).toBe(3);release();await expect(control).toBeChecked();
 const copy=page.getByRole('button',{name:'Скопировать',exact:true}),open=page.getByRole('button',{name:'Открыть Lead Generation',exact:true});assert.equal((await copy.boundingBox()).height,(await open.boundingBox()).height);
 await page.screenshot({path:'.tmp/launch-large-switch.png',fullPage:true});assert.deepEqual(errors,[]);
 console.log('PASS filters, alignment, session scope, PNG/ZIP split action, 56px open actions, switch pending/success/error/keyboard, narrow layout');
} finally {await browser.close();}
