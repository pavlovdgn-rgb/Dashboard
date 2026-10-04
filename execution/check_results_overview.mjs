import { chromium, expect } from '@playwright/test';
import { writeFile } from 'node:fs/promises';

const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1920,height:1080}});
const errors=[],results=[];
page.on('pageerror',error=>errors.push(error.message));
try {
  await page.goto('http://localhost:5173/?screen=results-overview');
  await expect(page.getByRole('heading',{name:'Обзор результатов',exact:true})).toBeVisible();
  await page.evaluate(()=>document.fonts.ready);
  const table=page.getByRole('table',{name:'Сценарии исследования',exact:true});
  await expect(table.locator('tbody tr')).toHaveCount(3);
  await expect(table.getByRole('radio',{checked:true})).toHaveCount(0);
  expect((await page.locator('aside').boundingBox()).width).toBe(320);
  await expect(page.getByRole('progressbar',{name:'Полнота данных'})).toHaveAttribute('value','90');
  await page.screenshot({path:'.tmp/storybook/results-overview-desktop.png'});
  results.push('1920px: source layout, three scenarios, 90% coverage, no initial selection');
  await expect(table.getByRole('columnheader')).toHaveCount(5);
  await expect(table.getByRole('button')).toHaveCount(0);
  await table.locator('tbody tr').nth(2).locator('td').nth(1).click();
  await expect(table.getByRole('radio',{checked:true})).toHaveCount(1);
  const analysis=page.getByRole('region',{name:'Анализ сценария'});
  await expect(analysis.getByRole('heading')).toHaveText('Оформить заказ');
  await expect(analysis).toContainText('16 участников начали · 15 попыток оценены');
  await page.keyboard.press('ArrowUp');
  await expect(table.locator('tbody tr').nth(1).getByRole('radio')).toBeChecked();
  await expect(analysis.getByRole('heading')).toHaveText('Изменить количество товара');
  results.push('Scenario selection updates the analysis context');
  await page.getByRole('button',{name:'Устройство',exact:true}).click();
  await page.getByRole('menuitemradio',{name:'Мобильное',exact:true}).click();
  await expect(table).toContainText('Сценарии не найдены');
  await expect(analysis.getByRole('heading')).toHaveText('Выберите сценарий в списке выше');
  await page.getByRole('button',{name:'Сбросить фильтры',exact:true}).click();
  await expect(table.locator('tbody tr')).toHaveCount(3);
  results.push('Mobile empty state and filter reset');
  await page.getByRole('button',{name:'Посмотреть участников',exact:true}).click();
  const dialog=page.locator('[role="dialog"][aria-labelledby="overview-dialog-title"]');
  await expect(dialog).toBeVisible();
  await expect(dialog.getByRole('table').locator('tbody tr')).toHaveCount(2);
  await page.keyboard.press('Escape');
  await expect(dialog).toHaveCount(0);
  results.push('Incomplete-data drilldown opens two demo participants and closes with Escape');
  await page.getByRole('button',{name:'Обновить результаты',exact:true}).click();
  await expect(page.locator('main [role="status"]').first()).toContainText(/обновлено \d{2}:\d{2}/);
  await page.locator('main').getByRole('button',{name:'Отчёт PDF',exact:true}).click();
  await dialog.getByRole('button',{name:'Сформировать отчёт',exact:true}).click();
  await expect(dialog.getByRole('table',{name:'Сценарии исследования'}).locator('tbody tr')).toHaveCount(3);
  await expect(dialog.getByRole('button',{name:'Печать / сохранить PDF'})).toBeVisible();
  await dialog.getByRole('button',{name:'Вернуться к результатам'}).click();
  results.push('Refresh and PDF preview');
  await page.locator('aside').getByRole('button',{name:'Настройка исследования',exact:true}).click();
  await expect(dialog).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('aside').getByRole('button',{name:'Обзор результатов',exact:true})).toHaveAttribute('aria-current','page');
  results.push('Returning from navigation restores the active section');
  for(const width of [1440,390]){
    await page.setViewportSize({width,height:900});
    await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
    await page.screenshot({path:`.tmp/storybook/results-overview-${width}.png`,fullPage:true});
  }
  results.push('1440px and 390px: no page overflow; table scroll stays inside its surface');
  await page.goto('http://localhost:6006/iframe.html?id=sandbox-results-overview--default&viewMode=story');
  await expect(page.getByRole('heading',{name:'Обзор результатов',exact:true})).toBeVisible();
  results.push('Storybook entry loads');
  for(const id of ['136-715','135-1062']){
    await page.goto(`http://localhost:6006/iframe.html?id=ds-${id}--default&viewMode=story`);
    const sample=page.locator(`[data-component-id="${id.replace('-',':')}"]`).first();
    await expect(sample.locator('tbody tr').first().locator('td')).toHaveCount(5);
    await expect(sample.locator('tbody').getByRole('button')).toHaveCount(0);
  }
  results.push('Storybook ScenarioTable and ScenarioRow both have five cells and no action buttons; keyboard selection works');
  if(errors.length)throw new Error(errors.join('\n'));
}catch(error){errors.push(error.message);process.exitCode=1;}
finally{await writeFile('.tmp/storybook/results-overview-audit.json',JSON.stringify({results,errors},null,2));console.log(JSON.stringify({results,errors}));await browser.close();}
