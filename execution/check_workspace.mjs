import {chromium,expect} from '@playwright/test';
import {mkdir,writeFile} from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1600,height:1100},reducedMotion:'reduce'});
const page=await context.newPage();const errors=[],results=[];
page.on('pageerror',e=>errors.push(e.message));
const root=process.argv.includes('--storybook')?'http://localhost:6006/iframe.html?id=sandbox-results-overview--default&viewMode=story':'http://localhost:5173/?screen=results-overview';
await mkdir('.tmp/wire/full',{recursive:true});
const go=async hash=>{await page.goto(`${root}#/${hash}`);await expect(page.locator('main')).toBeVisible();};
const click=async name=>page.getByRole('button',{name,exact:true}).click();
try {
  await go('projects');await page.evaluate(()=>localStorage.removeItem('ux-lab-workspace-v1'));await page.reload();
  for(const route of ['projects','studies','setup','launch','heatmap','funnel','signals','findings','participant','replay']) {
    await go(route);await expect(page.getByRole('heading',{level:1})).toBeVisible();await page.screenshot({path:`.tmp/wire/full/${route}.png`});results.push(`Route ${route} renders`);
  }
  await go('heatmap?scenario=catalog');await click('Выбрать область: Добавить в корзину');await click('Открыть 7 участников');
  await expect(page.locator('.euiModal')).toContainText('7 участников начали');await page.keyboard.press('Escape');
  results.push('Heatmap selection opens scoped participants');
  await go('replay?scenario=checkout&participant=014&time=138');
  await click('Воспроизвести');await expect.poll(async()=>Number(await page.getByRole('slider',{name:'Позиция записи'}).inputValue())).toBeGreaterThan(138);await click('Пауза');
  await page.getByRole('button',{name:/Сохранить наблюдение ·/}).click();
  const drawer=page.locator('.euiFlyout');await drawer.getByLabel('Название *',{exact:true}).fill('Проверка сквозного сценария');await drawer.getByLabel('Что наблюдали *',{exact:true}).fill('Участник повторил действие после паузы.');await drawer.getByRole('button',{name:'Сохранить находку',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Проверка сквозного сценария'})).toBeVisible();await expect(page.getByText('014 · попытка 1', {exact:false})).toBeVisible();
  await page.reload();await expect(page.getByRole('heading',{name:'Проверка сквозного сценария'})).toBeVisible();results.push('Playback advances; finding saves evidence and survives reload');
  await go('report');const modal=page.locator('.euiModal');await modal.getByRole('checkbox',{name:'Находки и выводы команды'}).check();await modal.getByRole('button',{name:'Сформировать отчёт',exact:true}).click();await expect(modal.getByRole('heading',{name:'Проверка сквозного сценария'})).toBeVisible();results.push('Saved finding is included in report snapshot');
  await go('projects');await click('Создать проект');let dialog=page.locator('.euiModal');await dialog.getByLabel('Название *',{exact:true}).fill('Сквозная проверка');await dialog.getByRole('button',{name:'Создать',exact:true}).click();await expect(page).toHaveURL(/studies/);
  await click('Создать исследование');dialog=page.locator('.euiModal');await dialog.getByLabel('Название *',{exact:true}).fill('Проверка нового исследования');await dialog.getByRole('button',{name:'Создать',exact:true}).click();await expect(page).toHaveURL(/setup/);
  await page.getByLabel('Ссылка на тестируемый интерфейс *',{exact:true}).fill('https://prototype.example.test/catalog');await click('Сохранить черновик');await expect(page.getByRole('status').first()).toHaveText('Изменения сохранены');await click('Добавить сценарий');await expect(page).toHaveURL(/task/);
  await click('Выбрать задание из списка');await page.locator('.euiModal').getByRole('button',{name:'Использовать задание',exact:true}).first().click();await click('Сохранить задание');await expect(page.getByRole('status').first()).toHaveText('Изменения сохранены');await click('К настройке');await click('Проверить подключение');await expect(page.getByRole('status').filter({hasText:'Демонстрационные события получены'})).toBeVisible();await click('К проверке и запуску');await expect(page).toHaveURL(/launch/);await click('Контрольное прохождение');
  await page.getByRole('checkbox',{name:'Я согласен участвовать'}).check();await click('Начать исследование');await click('Приступить к заданию');await click('Добавить в корзину');await page.getByRole('radio',{name:'Выполнил задание',exact:true}).check();await click('Далее');await expect(page.getByRole('heading',{name:'Спасибо за участие!'})).toBeVisible();await click('Посмотреть проверку');await expect(page.getByRole('heading',{name:'Проверка пройдена'})).toBeVisible();await click('К запуску');await click('Запустить исследование');await expect(page.getByRole('heading',{name:'Без панели участника',exact:true})).toBeVisible();
  results.push('Create project/study/task → save → connection check → control → launch');
  const links=await page.locator('p').allTextContents();const clean=links.find(t=>t.startsWith('http')&&t.includes('clean=true'));const guided=links.find(t=>t.startsWith('http')&&t.includes('clean=false'));expect(clean).toBeTruthy();expect(guided).toBeTruthy();
  const invited=await context.newPage();invited.on('pageerror',e=>errors.push(e.message));await invited.goto(clean);await expect(invited.getByRole('heading',{name:'Городской рюкзак'})).toBeVisible();await expect(invited.getByText('Действия и ввод записываются')).toHaveCount(0);await invited.getByRole('button',{name:'Добавить в корзину',exact:true}).click();await invited.close();
  await click('Открыть обзор результатов');await expect(page.getByRole('table',{name:'Сценарии исследования'})).toContainText('1 / 1');results.push('Clean link has no participant panel; demo events reach dashboard across tabs');
  const guest=await context.newPage();await guest.goto(guided);await guest.getByRole('checkbox',{name:'Я согласен участвовать'}).check();await guest.getByRole('button',{name:'Начать исследование',exact:true}).click();await guest.getByRole('button',{name:'Приступить к заданию',exact:true}).click();await expect(guest.getByRole('button',{name:'Далее',exact:true})).toBeDisabled();await guest.getByRole('button',{name:'Добавить в корзину',exact:true}).click();await guest.getByRole('radio',{name:'Выполнил задание',exact:true}).check();await guest.getByRole('button',{name:'Далее',exact:true}).click();await expect(guest.getByRole('heading',{name:'Спасибо за участие!'})).toBeVisible();await guest.close();await expect(page.getByRole('table',{name:'Сценарии исследования'})).toContainText('2 / 2');results.push('Guided link requires result choice; control attempts excluded, real demo sessions counted');
  await go('launch');await click('Завершить сбор');await page.goto(clean);await expect(page.getByRole('heading',{name:'Ссылка недоступна'})).toBeVisible();results.push('Finished study invalidates participant links');
  if(errors.length)throw Error(errors.join('\n'));
}catch(e){errors.push(e.message);await page.screenshot({path:'.tmp/wire/full/failure.png'});process.exitCode=1;}
finally {await writeFile('.tmp/wire/full/audit.json',JSON.stringify({results,errors},null,2));console.log(JSON.stringify({results,errors}));await browser.close();}
