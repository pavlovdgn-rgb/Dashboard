import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
  for(const viewport of [{width:1600,height:1000},{width:1024,height:600},{width:390,height:844}]) {
    const page=await browser.newPage({viewport});
    await page.goto('http://127.0.0.1:5173/#/funnel');
    const anchor=page.getByRole('button',{name:'Шаг 1',exact:true});
    await anchor.click();
    const menu=page.getByRole('menu',{name:'Шаг 1'});
    await expect(menu.getByRole('menuitemradio').first()).toBeVisible();
    await expect.poll(async()=>{const r=await menu.boundingBox();return !!r&&r.x>=0&&r.y>=0&&r.x+r.width<=viewport.width&&r.y+r.height<=viewport.height;}).toBe(true);
    const a=await anchor.boundingBox(),m=await menu.boundingBox();
    assert.ok(Math.abs(Math.min(a.width,viewport.width-32)-m.width)<=12,`Menu matches available field width at ${viewport.width}: ${a.width}/${m.width}`);
    assert.ok(m.height<=Math.min(320,viewport.height*.4)+1,'Long menu is bounded');
    // Keyboard navigation must scroll the menu to the last option, not lose it off screen.
    const items=menu.getByRole('menuitemradio'),last=items.last();
    await items.first().focus();
    await page.keyboard.press('ArrowUp');
    await expect(last).toBeFocused();
    await expect(last).toBeInViewport();
    const label=await last.innerText();
    await page.keyboard.press('Enter');
    await expect(menu).toHaveCount(0);
    await expect(anchor).toContainText(label);
    await anchor.click();await expect(last).toBeFocused();await page.keyboard.press('Escape');
    await expect(anchor).toHaveAttribute('aria-expanded','false');
    await page.close();
  }
  console.log('PASS dropdown viewport bounds, width, scroll, keyboard selection and Escape at 3 sizes');
}finally {await browser.close();}
