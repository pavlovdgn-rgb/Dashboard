import { chromium } from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1600,height:1100}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
const url='http://127.0.0.1:5174/api/heatmap?study=leed-local&aggregation=page';
const labels={'leed-leads-table':'Таблица лидов','leed-leads-kanban':'Канбан лидов','leed-dashboard':'Дашборд'};
try {
  const data=await(await fetch(url)).json();
  assert.equal(data.groups.length,new Set(data.groups.map(g=>`${g.page}:${g.vw}:${g.vh}`)).size,'one map per screen/viewport');
  assert.equal(data.groups.reduce((n,g)=>n+g.clicks,0),data.total.clicks);
  await page.goto('http://127.0.0.1:5173/?screen=results-overview#/heatmap-live?link=leed-local');
  const screenSelect=page.getByRole('button',{name:'Экран',exact:true});
  await screenSelect.hover();await page.waitForTimeout(250);
  const fieldStyle=await screenSelect.evaluate(el=>{
    const probe=document.createElement('span');probe.style.background='var(--accent-soft)';el.parentElement.append(probe);
    const expected=getComputedStyle(probe).backgroundColor;probe.remove();
    return {width:el.getBoundingClientRect().width,background:getComputedStyle(el).backgroundColor,expected};
  });
  assert.ok(fieldStyle.width<=480,'screen selector must be compact');
  assert.equal(fieldStyle.background,fieldStyle.expected,'hover must be light green');
  await fs.mkdir('.tmp/heatmap',{recursive:true});
  for(const group of data.groups) {
    const detail=await(await fetch(url+'&group='+group.layout)).json();
    assert.ok(detail.points.reduce((n,p)=>n+p.count,0)>=group.clicks);
    await page.getByRole('button',{name:'Экран',exact:true}).click();
    await page.getByRole('menuitemradio',{name:new RegExp(labels[group.page])}).click();
    await page.waitForFunction(n=>parseInt(document.querySelector('[data-testid="real-click-count"]')?.textContent||'0')>=n,group.clicks);
    const iframe=page.frameLocator('[data-testid="captured-heatmap"] iframe');
    await iframe.getByPlaceholder('Найти лида').waitFor();
    await page.waitForTimeout(1000);
    const count=await page.getByTestId('captured-click-layer').evaluate(canvas=>{
      const pixels=canvas.getContext('2d').getImageData(0,0,canvas.width,canvas.height).data;
      let count=0;for(let i=3;i<pixels.length;i+=4)if(pixels[i])count++;return count;
    });
    assert.ok(count>100,'visible density is drawn above the interface');
    await page.getByTestId('captured-heatmap').screenshot({path:`.tmp/heatmap/density-${group.page}.png`});
  }
  const density=await page.evaluate(async()=>{
    const {drawHeatmap}=await import('/src/heatmap/drawHeatmap.ts');
    const canvas=document.createElement('canvas');document.querySelector('[data-testid="captured-heatmap"]').append(canvas);
    drawHeatmap(canvas,[{x:.2,y:.5,count:1,target:'a',sessions:[]},{x:.8,y:.5,count:20,target:'b',sessions:[]}],500,200);
    const ctx=canvas.getContext('2d');const result={low:[...ctx.getImageData(100,100,1,1).data],high:[...ctx.getImageData(400,100,1,1).data]};canvas.remove();return result;
  });
  assert.ok(density.high[3]>density.low[3],'20 clicks must be more intense than one click');
  assert.notDeepEqual(density.low.slice(0,3),density.high.slice(0,3),'density changes heat colour');
  await page.getByRole('button',{name:'Скрыть слой кликов',exact:true}).click();
  assert.equal(await page.getByTestId('captured-click-layer').evaluate(c=>[...c.getContext('2d').getImageData(0,0,c.width,c.height).data].some((v,i)=>i%4===3&&v)),false);
  assert.equal(errors.length,0,errors.join('\n'));
  console.log(JSON.stringify({total:data.total,groups:data.groups.map(g=>({page:g.page,clicks:g.clicks})),fieldStyle,density,errors},null,2));
}finally{await browser.close();}
