import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

// Read-only real-data check, then isolated browser responses; never writes the project database.
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  const live=await (await fetch('http://127.0.0.1:5174/api/project?device=all')).json();
  await page.goto('http://127.0.0.1:5173/#/overview');
  await expect(page.getByRole('heading',{name:'Активность по экранам'})).toBeVisible();
  await expect(page.getByRole('table',{name:'Экраны проекта'}).getByRole('progressbar')).toHaveCount(0);
  await page.screenshot({path:'.tmp/metric-overview-live.png',fullPage:true});
  const ids=['leed-dashboard','leed-leads-table','leed-leads-kanban'];
  let fixture={...live,total:{...live.total,clicks:257},pages:ids.map((id,i)=>({id,clicks:[148,91,18][i],sessions:[3,12,2][i],visits:[4,15,4][i]})),signals:[
    {id:'one',page:ids[0],session:'a',timestamp:1,label:'Повторные клики',target:'Кнопка'},
    {id:'repeat-same-session',page:ids[0],session:'a',timestamp:2,label:'Повторные клики',target:'Кнопка'},
    {id:'two',page:ids[0],session:'b',timestamp:3,label:'Повторные клики',target:'Кнопка'},
    ...Array.from({length:6},(_,i)=>({id:`table-${i}`,page:ids[1],session:`s${i}`,timestamp:i+10,label:'Повторные клики',target:'Кнопка'}))
  ],funnel:[{page:ids[1],sessions:10,sessionIds:['a','b']},{page:ids[2],sessions:7,sessionIds:['a']},{page:ids[0],sessions:4,sessionIds:['a']}]};
  const requests=[];
  await page.route('http://127.0.0.1:5174/api/project?*',async route=>{requests.push(route.request().url());await route.fulfill({json:fixture});});
  await page.reload();
  const overview=page.getByRole('table',{name:'Экраны проекта'});
  await expect(overview.getByRole('progressbar')).toHaveCount(0);
  await expect(overview).toContainText('148');
  await overview.locator('tbody tr').first().locator('td').nth(1).click();
  await expect(page).toHaveURL(/heatmap.*page/);
  await page.goto('http://127.0.0.1:5173/#/signals');
  await page.getByRole('button',{name:'По страницам',exact:true}).click();
  const signals=page.getByRole('table',{name:'Сигналы по страницам'});
  await expect(signals).toContainText('2 из 3');await expect(signals).toContainText('67%');
  await expect(signals).toContainText('6 из 12');await expect(signals).toContainText('50%');
  await expect(signals).toContainText('0 из 2');await expect(signals).toContainText('0%');
  await page.screenshot({path:'.tmp/metric-signals.png',fullPage:true});
  await signals.locator('tbody tr').first().locator('td').nth(1).click();
  await expect(page).toHaveURL(/participants.*ids/);
  await page.goto('http://127.0.0.1:5173/#/funnel');
  const funnel=page.getByRole('table',{name:'Воронка переходов'});
  await expect(funnel).toContainText('100%');await expect(funnel).toContainText('70%');await expect(funnel).toContainText('40%');
  await expect(funnel.locator('tbody tr').nth(1).locator('td').nth(3)).toHaveText('−3');
  await page.screenshot({path:'.tmp/metric-funnel.png',fullPage:true});
  fixture={...fixture,total:{...fixture.total,clicks:0},pages:fixture.pages.map(p=>({...p,clicks:0})),signals:[],funnel:fixture.funnel.map(step=>({...step,sessions:0,sessionIds:[]}))};
  await page.reload();await expect(page.getByText('Нет данных: первый шаг пока не посетила ни одна сессия.')).toBeVisible();
  for(const bar of await page.getByRole('progressbar').all())await expect(bar).toHaveAttribute('aria-valuetext','Нет данных');
  await expect(page.getByRole('button',{name:'Посмотреть',exact:true}).first()).toBeDisabled();
  await page.goto('http://127.0.0.1:5173/#/overview?device=mobile');
  await expect(page.getByRole('table',{name:'Экраны проекта'}).getByRole('progressbar')).toHaveCount(0);
  assert.ok(requests.some(url=>url.includes('device=mobile')));
  await page.goto('http://127.0.0.1:5173/#/signals');await page.getByRole('button',{name:'По страницам',exact:true}).click();
  await expect(page.getByRole('table',{name:'Сигналы по страницам'}).locator('tbody tr')).toHaveCount(3);
  await expect(page.getByRole('progressbar').first()).toHaveAttribute('aria-valuetext','0% (0 из 3)');
  await page.setViewportSize({width:760,height:900});
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);assert.equal(overflow,false);
  assert.deepEqual(errors,[]);
  fs.writeFileSync('.tmp/metric-bars-check.json',JSON.stringify({passed:true,checks:['real data','exact ratios','unique affected sessions','zero signals','zero denominators','funnel loss','row navigation','device scope','narrow layout','no runtime errors']},null,2));
  console.log('PASS metric bars: live data, ratios, deduplication, empty/zero states, navigation, device scope, narrow layout');
} finally {await browser.close();}
