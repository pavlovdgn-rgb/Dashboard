import { chromium, expect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';

const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1600,height:1000}});
const results=[],errors=[];
page.on('pageerror',error=>errors.push(error.message));
const modal=page.locator('[role="dialog"][aria-labelledby="overview-dialog-title"]');
const root='http://localhost:5173/?screen=results-overview';
const openStory=async story=>{await page.goto(`http://localhost:6006/iframe.html?id=sandbox-results-overview--${story}&viewMode=story`);await expect(page.getByRole('heading',{name:'Обзор результатов',exact:true})).toBeVisible();};
await mkdir('.tmp/wire',{recursive:true});
try {
  await page.goto(root);
  const scenarios=page.getByRole('table',{name:'Сценарии исследования'});
  await expect(scenarios.locator('tbody tr')).toHaveCount(3);
  for(const [index,fraction] of ['14 / 18','12 / 17','10 / 15'].entries())await expect(scenarios.locator('tbody tr').nth(index)).toContainText(fraction);
  await scenarios.locator('tbody tr').nth(2).getByRole('radio').check();
  await page.getByRole('region',{name:'Анализ сценария'}).getByRole('button',{name:'Участники',exact:true}).click();
  await expect(page).toHaveURL(/#\/participants\?.*scenario=checkout/);
  await expect(modal).toContainText('16 участников начали');
  await expect(page.locator('aside button[aria-current="page"]')).toHaveText('Участники');
  await modal.getByRole('textbox',{name:'Поиск по ID'}).fill('018');
  await expect(modal.getByRole('table').locator('tbody tr')).toHaveCount(1);
  await page.goBack();await expect(modal).toHaveCount(0);
  await expect(page.getByRole('region',{name:'Анализ сценария'}).getByRole('heading')).toHaveText('Оформить заказ');
  await page.goForward();await expect(modal.getByRole('textbox',{name:'Поиск по ID'})).toHaveValue('018');
  await modal.getByRole('textbox',{name:'Поиск по ID'}).fill('x'.repeat(300));
  await expect(modal.getByRole('heading',{name:'Ничего не найдено'})).toBeVisible();
  await modal.getByRole('button',{name:'Сбросить фильтры'}).click();
  await expect(modal.getByRole('table').locator('tbody tr')).toHaveCount(4);
  await page.keyboard.press('Escape');
  results.push('History/back/forward preserves selected scenario and participant filters; long no-match input and reset');

  await page.getByRole('button',{name:'Посмотреть участников',exact:true}).click();
  await expect(modal).toContainText('2 участников начали');
  await expect(modal.getByRole('table').locator('tbody tr')).toHaveCount(2);
  await modal.getByRole('button',{name:'Все участники',exact:true}).click();
  await expect(modal).toContainText('20 участников начали');
  await page.keyboard.press('Escape');
  results.push('One mock source: 20 unique participants, 2 incomplete, scoped checkout contains 16');

  await page.locator('main').getByRole('button',{name:'Отчёт PDF',exact:true}).click();
  await modal.getByRole('checkbox',{name:'Сводка по сценариям'}).uncheck();
  await modal.getByRole('checkbox',{name:'Участники',exact:true}).uncheck();
  await modal.getByRole('button',{name:'Сформировать отчёт',exact:true}).click();
  await expect(modal.getByRole('alert')).toContainText('Выберите хотя бы один раздел');
  await expect(modal.locator('fieldset')).toHaveAttribute('aria-invalid','true');
  await modal.getByRole('checkbox',{name:'Сводка по сценариям'}).check();
  await modal.getByRole('button',{name:'Сформировать отчёт',exact:true}).click();
  await expect(modal.getByRole('button',{name:'Формируем отчёт',exact:true})).toBeDisabled();
  await expect(modal.getByRole('status')).toContainText('Отчёт сформирован');
  await expect(page).toHaveURL(/report=/);
  await expect(modal.getByRole('table')).toHaveCount(1);
  await page.evaluate(()=>{window.print=()=>{window.__printCalled=true;};});
  await modal.getByRole('button',{name:'Печать / сохранить PDF'}).click();
  expect(await page.evaluate(()=>window.__printCalled)).toBe(true);
  await page.screenshot({path:'.tmp/wire/report-ready.png'});
  await page.keyboard.press('Escape');
  await page.locator('main').getByRole('button',{name:'Отчёт PDF',exact:true}).click();
  await expect(modal).toContainText('Сформированные отчёты · 1');
  await page.keyboard.press('Escape');
  results.push('Report form validates zero sections, prevents duplicate submit, saves shared snapshot and invokes print');

  await page.getByRole('button',{name:'Устройство',exact:true}).click();
  await page.getByRole('menuitemradio',{name:'Мобильное',exact:true}).click();
  await expect(scenarios).toContainText('Сценарии не найдены');
  await page.locator('main').getByRole('button',{name:'Отчёт PDF',exact:true}).click();
  await expect(modal.getByRole('button',{name:'Сформировать отчёт',exact:true})).toBeDisabled();
  await page.keyboard.press('Escape');
  await page.getByRole('button',{name:'Сбросить фильтры',exact:true}).click();
  await expect(scenarios.locator('tbody tr')).toHaveCount(3);
  results.push('Zero-observation device filter blocks empty reports; reset restores data');

  await openStory('refresh-failure');
  await page.getByRole('button',{name:'Обновить результаты',exact:true}).click();
  await expect(page.locator('main [role="alert"]')).toContainText('Не удалось обновить результаты');
  await expect(page.getByRole('table',{name:'Сценарии исследования'}).locator('tbody tr')).toHaveCount(3);
  await page.getByRole('button',{name:'Повторить обновление'}).click();
  await expect(page.getByRole('status').filter({hasText:'Результаты обновлены'})).toBeVisible();
  await expect(page.locator('main [role="alert"]')).toHaveCount(0);
  results.push('Refresh error retains previous data; retry succeeds');

  await openStory('report-failure');
  await page.locator('main').getByRole('button',{name:'Отчёт PDF',exact:true}).click();
  await modal.getByRole('button',{name:'Сформировать отчёт',exact:true}).click();
  await expect(modal.getByRole('alert')).toContainText('Не удалось сформировать отчёт');
  await expect(modal.getByRole('checkbox',{name:'Сводка по сценариям'})).toBeChecked();
  await modal.getByRole('button',{name:'Сформировать отчёт',exact:true}).click();
  await expect(modal.getByRole('status')).toContainText('Отчёт сформирован');
  await page.emulateMedia({media:'print'});
  await page.pdf({path:'.tmp/wire/demo-report.pdf',format:'A4',printBackground:true});
  await page.emulateMedia({media:'screen'});
  results.push('Report failure preserves form choices and succeeds on retry; printable PDF generated');

  await openStory('no-observations');
  await expect(page.getByRole('table',{name:'Сценарии исследования'})).toContainText('Пока нет результатов');
  await expect(page.getByRole('progressbar',{name:'Полнота данных'})).toHaveCount(0);
  await page.goto(`${root}#/participants?device=desktop&scenario=checkout`);
  await expect(modal).toContainText('16 участников начали');
  await page.goto(`${root}#/toString?device=wrong&scenario=missing`);
  await expect(page.getByRole('heading',{name:'Обзор результатов',exact:true})).toBeVisible();
  await expect(modal).toHaveCount(0);
  await page.setViewportSize({width:390,height:844});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  results.push('Empty study, valid deep link, invalid route normalization and mobile layout');
  if(errors.length)throw new Error(errors.join('\n'));
} catch(error) {errors.push(error.message);process.exitCode=1;}
finally {await writeFile('.tmp/wire/audit.json',JSON.stringify({results,errors},null,2));console.log(JSON.stringify({results,errors}));await browser.close();}
