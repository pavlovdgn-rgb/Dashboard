import { chromium, expect } from '@playwright/test';
import { readFile,writeFile,mkdir } from 'node:fs/promises';
const base='http://127.0.0.1:6006';
const catalog=JSON.parse(await readFile('src/components/catalog.json','utf8'));
const expected=JSON.parse(await readFile('src/storybook/story-index.json','utf8'));
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1050}});
const errors=[],checks=[];let current='';
page.on('pageerror',error=>errors.push({current,message:error.message}));
page.on('console',message=>{if(message.type()==='error')errors.push({current,message:message.text(),location:message.location()});});
const visit=async id=>{current=id;await page.goto(`${base}/iframe.html?id=${id}&viewMode=story`);await page.locator('#storybook-root').waitFor();};
await mkdir('.tmp/storybook',{recursive:true});
try {
  const index=await (await page.request.get(base+'/index.json')).json();
  for(const entry of expected){
    for(const suffix of ['default','all-variants','docs'])if(!index.entries[`${entry.id}--${suffix}`])throw new Error(`Missing ${entry.id}--${suffix}`);
    for(const variant of entry.variants)if(!index.entries[variant.id])throw new Error(`Missing variant ${variant.id}`);
    const text=await readFile(entry.file,'utf8');
    const source=catalog.find(e=>e.id===entry.catalogId);
    for(const key of Object.keys(source.properties))if(!text.includes(JSON.stringify(key)))throw new Error(`Missing control ${entry.id}:${key}`);
  }
  checks.push(`Index: ${expected.length} components, ${expected.reduce((n,e)=>n+e.variants.length,0)} variants, autodocs and matrices`);
  await visit('ds-125-450--default');
  const button=page.getByRole('button',{name:'Сохранить исследование',exact:true});await expect(button).toBeVisible();
  const before=await button.evaluate(el=>getComputedStyle(el).backgroundColor);await button.hover();await page.waitForTimeout(200);
  const after=await button.evaluate(el=>getComputedStyle(el).backgroundColor);if(before===after)throw new Error('Native hover has no visual feedback');
  if(await button.evaluate(el=>getComputedStyle(el).transitionDuration)==='0s')throw new Error('Missing motion');
  checks.push('Native button hover and motion');

  await visit('sandboxes--form');
  await page.getByRole('button',{name:'Сохранить',exact:true}).click();await expect(page.getByRole('alert')).toHaveText('Укажите название исследования.');
  await page.getByRole('textbox',{name:'Название исследования'}).fill('Покупка рюкзака');
  await page.getByRole('combobox',{name:'Режим исследования'}).selectOption('Свободное изучение');
  await page.getByRole('button',{name:'Сохранить',exact:true}).click();await expect(page.getByRole('status')).toContainText('Покупка рюкзака');
  await page.getByRole('button',{name:'Отмена',exact:true}).click();await expect(page.getByRole('textbox',{name:'Название исследования'})).toHaveValue('');
  checks.push('Form: validation, select, save and reset');

  await visit('sandboxes--dialog');
  await page.getByRole('button',{name:'Открыть окно'}).click();await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByRole('textbox',{name:'Название исследования'}).fill('Проверка каталога');
  await page.getByRole('button',{name:'Сохранить',exact:true}).click();await expect(page.getByRole('dialog')).toHaveCount(0);await expect(page.getByRole('status')).toContainText('Проверка каталога');
  await page.getByRole('button',{name:'Открыть окно'}).click();await page.keyboard.press('Escape');await expect(page.getByRole('dialog')).toHaveCount(0);
  checks.push('Dialog: composition, save, close and Escape');

  await visit('sandboxes--navigation');await page.getByRole('tab',{name:'Находки · 2'}).click();await expect(page.getByRole('tabpanel')).toContainText('Находки команды');
  await page.getByRole('button',{name:'Участники',exact:true}).click();await expect(page.locator('p[role="status"]')).toContainText('Participants');
  await expect(page.getByRole('tab',{name:'Находки · 2'})).toHaveAttribute('aria-selected','true');
  await expect(page.getByRole('tab',{name:'Сигналы',exact:true})).toHaveAttribute('aria-selected','false');
  await expect(page.getByRole('button',{name:'Участники',exact:true})).toHaveAttribute('aria-current','page');
  checks.push('Navigation: linked sidebar and tabs');
  await page.screenshot({path:'.tmp/storybook/navigation.png',fullPage:true});

  await visit('sandboxes--data-feedback');await page.getByRole('button',{name:'Открыть запись',exact:true}).first().click();await expect(page.getByText('Запись 014 · попытка 1',{exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Следующая страница',exact:true}).click();await expect(page.getByRole('navigation',{name:'Страницы таблицы'})).toContainText('2 из 4');
  await page.getByRole('button',{name:'Как считаются результаты?'}).hover();await expect(page.getByRole('tooltip')).toBeVisible();
  checks.push('Data: recording feedback, table pages and tooltip');

  for(const kind of ['primitive','semantic','typography']){await visit(`foundation--${kind}`);await expect(page.locator('[data-foundation]')).toBeVisible();const count=await page.locator(kind==='typography'?'[data-text-style]':'[data-token]').count();const expectedCount=kind==='typography'?29:new Set([...(await readFile(`src/tokens/${kind==='primitive'?'primitives':'semantics'}.css`,'utf8')).matchAll(/(--[\w-]+)\s*:/g)].map(m=>m[1])).size;if(count!==expectedCount)throw new Error(`Incomplete ${kind}: ${count}/${expectedCount}`);checks.push(`Foundation ${kind}: ${count}`);}
  await visit('foundation-icons--library');await expect(page.getByRole('heading',{name:'Иконки исходной дизайн-системы'})).toBeVisible();if(await page.locator('svg path').count()<300)throw new Error('Icons did not render');
  await expect(page.getByRole('img',{name:'UX-Lab'})).toHaveJSProperty('naturalWidth',24);
  checks.push('Original library icons and local Figma logo');
  await page.screenshot({path:'.tmp/storybook/icons.png'});

  await visit('ds-125-450--all-variants');await expect(page.locator('[data-matrix-count]')).toHaveAttribute('data-matrix-count','18');await expect(page.locator('[data-component-id="125:450"]')).toHaveCount(18);
  checks.push('AllVariants: all 18 product button instances present');

  current='autodocs';await page.goto(`${base}/?path=/docs/ds-125-450--docs`);const frame=page.frameLocator('#storybook-preview-iframe');
  await expect(frame.getByRole('heading',{name:/ProductButton/}).first()).toBeVisible({timeout:30000});
  await expect(frame.getByText('Kind',{exact:true}).first()).toBeVisible();
  await frame.getByText('Show code',{exact:true}).first().click();await expect(frame.getByRole('button',{name:'Copy code',exact:true}).first()).toBeVisible();
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);
  await frame.getByRole('button',{name:'Copy code',exact:true}).first().click();
  const snippet=await page.evaluate(()=>navigator.clipboard.readText());if(!snippet.includes('ProductButton')||!snippet.includes('Сохранить исследование'))throw new Error('Copy code did not copy the actual component and args');
  await frame.locator('select').first().selectOption('Disabled');await expect(frame.getByRole('button',{name:'Сохранить исследование',exact:true}).first()).toBeDisabled();
  await page.screenshot({path:'.tmp/storybook/docs.png',fullPage:true});checks.push('Autodocs: property controls and Show code / Copy');

  if(process.argv.includes('--all'))for(const [n,entry] of expected.entries()){
    const from=process.argv.find(arg=>arg.startsWith('--from='))?.slice(7);if(from&&n<expected.findIndex(item=>item.catalogId===from))continue;
    await visit(`${entry.id}--default`);await expect(page.locator(`[data-component-id="${entry.catalogId}"]`)).toBeVisible({timeout:15000});
    if(n%25===0)console.log(`Rendered ${n+1}/${expected.length}`);
  }
  if(process.argv.includes('--all'))checks.push(process.argv.some(arg=>arg.startsWith('--from='))?'Rendered requested tail of isolated default stories':`Rendered ${expected.length} isolated default stories`);
  if(errors.length)throw new Error(`${errors.length} browser errors`);
} catch(error){errors.push({current,message:error.message});process.exitCode=1;}
finally{await writeFile('.tmp/storybook/audit.json',JSON.stringify({checks,errors},null,2));console.log(JSON.stringify({checks,errors}));await browser.close();}
