import { chromium, expect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
const results=[];
await mkdir('.tmp/wire',{recursive:true});
try {
  for(const url of ['http://localhost:5173/?screen=results-overview#/report','http://localhost:6006/iframe.html?id=sandbox-results-overview--default&viewMode=story#/report']) {
    // The shared shell keeps its header fixed while only main content scrolls.
    for(const width of [1440,390]) {
      await page.setViewportSize({width,height:1000});
      await page.goto(url.replace('#/report','#/projects'));
      await expect(page.getByRole('heading',{level:1})).toBeVisible();
      await page.evaluate(()=>document.fonts.ready);
      const main=page.locator('main');
      const before=await main.locator(':scope > *').first().boundingBox();
      const initial=await main.evaluate(el=>({height:el.clientHeight,scrollHeight:el.scrollHeight}));
      await main.evaluate(el=>{const spacer=document.createElement('div');spacer.id='scrollbar-check';spacer.style.cssText='height:5000px;flex-shrink:0';el.append(spacer);});
      const overflowing=await main.locator(':scope > *').first().boundingBox();
      const scroll=await page.evaluate(()=>[document.querySelector('main'),document.scrollingElement].map(el=>({height:el.clientHeight,scrollHeight:el.scrollHeight,gutter:getComputedStyle(el).scrollbarGutter})));
      expect(scroll.some(el=>el.scrollHeight>el.height)).toBe(true);
      expect(Math.abs(before.x-overflowing.x)).toBeLessThan(.1);
      expect(Math.abs(before.width-overflowing.width)).toBeLessThan(.1);
      const header=page.locator('header').first();
      const headerBefore=await header.boundingBox();
      const sidebar=page.locator('aside').first();
      const sidebarBefore=width>700?await sidebar.boundingBox():null;
      await main.evaluate(el=>{el.scrollTop=500;});
      expect(await main.evaluate(el=>el.scrollTop)).toBe(500);
      expect(await header.boundingBox()).toEqual(headerBefore);
      if(sidebarBefore)expect(await sidebar.boundingBox()).toEqual(sidebarBefore);
      expect(await page.evaluate(()=>document.scrollingElement.scrollTop)).toBe(0);
      expect(await page.evaluate(()=>document.scrollingElement.scrollHeight<=innerHeight)).toBe(true);
      await main.evaluate(el=>{el.scrollTop=0;});
      await page.locator('#scrollbar-check').evaluate(el=>el.remove());
      results.push({url,width,scrollbarLayout:{initial,scroll,before,overflowing}});
    }
    // Cover both shell compositions and real long content, including a short laptop.
    for(const route of ['heatmap','overview']) {
      await page.setViewportSize({width:1440,height:600});
      await page.goto(url.replace('#/report',`#/${route}`));
      await expect(page.getByRole('heading',{level:1})).toBeVisible();
      const main=page.locator('main'),header=page.locator('header').first(),sidebar=page.locator('aside').first();
      const headerBefore=await header.boundingBox(),sidebarBefore=await sidebar.boundingBox();
      await main.evaluate(el=>{el.scrollTop=el.scrollHeight;});
      expect(await main.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
      expect(await header.boundingBox()).toEqual(headerBefore);
      expect(await sidebar.boundingBox()).toEqual(sidebarBefore);
      await sidebar.evaluate(el=>{el.scrollTop=el.scrollHeight;});
      expect(await sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
      expect(await page.evaluate(()=>document.scrollingElement.scrollHeight<=innerHeight)).toBe(true);
      results.push({url,route,fixedShell:true,independentMenuScroll:true});
    }
    await page.setViewportSize({width:1440,height:1000});
    await page.goto(url);
    await expect(page.locator('.euiModal')).toBeVisible();
    for(const width of [1440,390]) {
      await page.setViewportSize({width,height:1000});
      await page.evaluate(()=>{document.getAnimations().forEach(animation=>animation.finish());});
      const modal=page.locator('.euiModal');
      const button=modal.locator('.euiModal__closeIcon');
      const bounds=await modal.boundingBox(),close=await button.boundingBox();
      const gutter=width===390?16:24;
      expect(Math.abs(close.y-bounds.y-gutter)).toBeLessThanOrEqual(1.1);
      expect(Math.abs(bounds.x+bounds.width-close.x-close.width-gutter)).toBeLessThanOrEqual(1.1);
      const title=await modal.locator('#overview-dialog-title').boundingBox();
      expect(title.x+title.width).toBeLessThanOrEqual(close.x);
      results.push({url,width,gutter,closeSize:close.width});
    }
    await page.setViewportSize({width:1440,height:1000});
    await page.screenshot({path:`.tmp/wire/modal-alignment-${url.includes('6006')?'storybook':'app'}.png`});
    await page.locator('.euiModal__closeIcon').click();
    await expect(page.locator('.euiModal')).toHaveCount(0);
  }
  console.log(JSON.stringify(results));
  await writeFile('.tmp/wire/control-alignment.json',JSON.stringify(results,null,2));
} finally {await browser.close();}
