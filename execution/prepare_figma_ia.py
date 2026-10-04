"""Prepare deterministic editable Figma diagram payloads from approved IA files."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.tmp/figma-ia'
PAGE_ID = '8:2'

RENDERER = r'''
const page=await figma.getNodeByIdAsync(DATA.pageId);
await figma.setCurrentPageAsync(page);
if(page.children.some(n=>n.name===DATA.name)) throw new Error('Diagram exists; inspect before retry');
await figma.loadFontAsync({family:'Inter',style:'Regular'});
await figma.loadFontAsync({family:'Inter',style:'Medium'});
await figma.loadFontAsync({family:'Inter',style:'Semi Bold'});
const ids=[]; const track=n=>{ids.push(n.id); return n;};
const color=h=>({r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255});
const paint=h=>[{type:'SOLID',color:color(h)}];
const root=track(figma.createFrame()); root.name=DATA.name; page.appendChild(root);
root.x=DATA.x;root.y=DATA.y;root.resize(DATA.width,DATA.height);root.fills=paint('#F8FAFC');root.clipsContent=false;
function text(parent,value,x,y,w,size=16,style='Regular',ink='#334155'){
 const n=track(figma.createText());parent.appendChild(n);n.fontName={family:'Inter',style};n.fontSize=size;
 n.characters=value;n.fills=paint(ink);n.resize(w,1);n.textAutoResize='HEIGHT';n.x=x;n.y=y;return n;
}
text(root,DATA.kicker,64,42,DATA.width-128,16,'Medium','#64748B');
text(root,DATA.title,64,80,DATA.width-128,40,'Semi Bold','#0F172A');
text(root,DATA.subtitle,64,140,DATA.width-128,18);
const cards={};
for(const d of DATA.nodes){
 const card=track(figma.createAutoLayout('VERTICAL'));root.appendChild(card); card.name=d.id;
 card.resize(d.w||300,d.h||112);card.primaryAxisSizingMode='FIXED';card.counterAxisSizingMode='FIXED';
 card.paddingLeft=18;card.paddingRight=18;card.paddingTop=14;card.paddingBottom=14;card.itemSpacing=7;
 card.cornerRadius=12;card.fills=paint(d.fill||'#C8F7C5');card.strokes=paint(d.stroke||'#2E8B3E');card.strokeWeight=1;
 card.x=d.x;card.y=d.y;
 text(card,d.id+'  ['+(d.priority||'core')+']',0,0,(d.w||300)-36,17,'Semi Bold','#173A24');
 text(card,d.desc,0,0,(d.w||300)-36,14,'Regular','#334155');
 cards[d.id]=card;
}
function path(points,name,stroke='#64748B',dash=false,arrow=true){
 const minX=Math.min(...points.map(p=>p[0])),minY=Math.min(...points.map(p=>p[1]));
 let data=points.map((p,i)=>(i?'L':'M')+' '+(p[0]-minX)+' '+(p[1]-minY)).join(' ');
 if(arrow){const a=points[points.length-2],b=points[points.length-1],angle=Math.atan2(b[1]-a[1],b[0]-a[0]);
 const wing=s=>[b[0]-minX-9*Math.cos(angle+s),b[1]-minY-9*Math.sin(angle+s)];
 const w1=wing(.5),w2=wing(-.5);data+=' M '+w1.join(' ')+' L '+(b[0]-minX)+' '+(b[1]-minY)+' L '+w2.join(' ');}
 const n=track(figma.createVector());root.appendChild(n);n.name=name;n.vectorPaths=[{windingRule:'NONZERO',data}];
 n.fills=[];n.strokes=paint(stroke);n.strokeWeight=1.8;if(dash)n.dashPattern=[6,5];n.x=minX;n.y=minY;return n;
}
for(const e of DATA.edges){
 path(e.points,e.name,e.secondary?'#94A3B8':'#475569',e.secondary);
 if(e.number){
  const badge=track(figma.createAutoLayout('HORIZONTAL'));root.appendChild(badge);badge.name='Transition '+e.number;
  badge.paddingLeft=6;badge.paddingRight=6;badge.paddingTop=3;badge.paddingBottom=3;badge.cornerRadius=6;
  badge.fills=paint('#FFFFFF');badge.strokes=paint('#CBD5E1');badge.x=e.badge[0];badge.y=e.badge[1];
  text(badge,e.number,0,0,24,13,'Semi Bold','#334155');
 }
}
if(DATA.legend){
 const panel=track(figma.createAutoLayout('VERTICAL'));root.appendChild(panel);panel.name='Условия переходов';
 panel.resize(DATA.legendWidth||610,100);panel.primaryAxisSizingMode='AUTO';panel.counterAxisSizingMode='FIXED';
 panel.paddingLeft=24;panel.paddingRight=24;panel.paddingTop=24;panel.paddingBottom=24;panel.itemSpacing=16;
 panel.fills=paint('#FFFFFF');panel.cornerRadius=16;panel.x=DATA.legendX;panel.y=240;
 text(panel,'Переходы и условия',0,0,(DATA.legendWidth||610)-48,22,'Semi Bold','#0F172A');
 text(panel,DATA.legend,0,0,(DATA.legendWidth||610)-48,16);
}
for(const note of DATA.notes||[])text(root,note.text,note.x,note.y,note.w,note.size||16,'Regular');
const clipped=[];
for(const [name,card] of Object.entries(cards)){
 const bottom=Math.max(...card.children.map(n=>n.y+n.height));if(bottom>card.height-card.paddingBottom+1)clipped.push(name);
}
return {createdNodeIds:ids,frameId:root.id,name:root.name,nodeCount:DATA.nodes.length,edgeCount:DATA.edges.length,clippedCards:clipped};
'''


def flow_data(stem, title, subtitle, positions, width, height, x, legend_x):
    raw=(ROOT/f'ia/flows/{stem}.mmd').read_text(encoding='utf-8')
    names=dict(re.findall(r'^    (\w+)\["(\w+)"\]',raw,re.M))
    transitions=re.findall(r'^    (\w+) -->\|"(.*?)"\| (\w+)$',raw,re.M)
    nodes=[dict(id=name,desc=DESCRIPTIONS[name],x=positions[name][0],y=positions[name][1]) for name in names.values()]
    edges=[];legend=[];back=0
    for i,(a,label,b) in enumerate(transitions,1):
        a,b=names[a],names[b];ax,ay=positions[a];bx,by=positions[b];num=f'{i:02}'
        secondary=a==b or by<ay
        if stem=='results-analysis' and a=='ResultsOverview' and b=='Participants':
            pts=[[ax,ay+70],[25,ay+70],[25,by+56],[bx,by+56]];badge=[30,920]
        elif stem=='results-analysis' and a=='Heatmaps' and b=='ResultsOverview':
            pts=[[ax,ay+45],[50,ay+45],[50,by+40],[bx,by+40]];badge=[55,610]
        elif stem=='results-analysis' and a==b=='Report':
            yy=ay+(16 if i==18 else 68)
            pts=[[ax+300,yy],[ax+330,yy],[ax+330,yy+26],[ax+300,yy+26]];badge=[ax+334,yy-1]
        elif a==b:
            right=ax+345
            pts=[[ax+300,ay+28],[right,ay+28],[right,ay+84],[ax+300,ay+84]]
            badge=[right+6,ay+44]
        elif by>ay:
            mid=(ay+112+by)/2
            # Long bypass in launch flow avoids intermediate cards.
            if by-ay>260 and stem=='study-launch':
                pts=[[ax+300,ay+80],[870,ay+80],[870,by+56],[bx+300,by+56]];badge=[878,(ay+by)/2]
            else:
                offset=18*(i%3-1)
                pts=[[ax+150+offset,ay+112],[ax+150+offset,mid],[bx+150+offset,mid],[bx+150+offset,by]]
                badge=[(ax+bx)/2+160+offset,mid-27]
        else:
            back+=1
            if stem=='results-analysis' and a!='Heatmaps':
                rail=1160+back*35
                pts=[[ax+300,ay+75],[rail,ay+75],[rail,by+60],[bx+300,by+60]];badge=[rail+6,(ay+by)/2]
            else:
                rail=75+back*40
                pts=[[ax,ay+75],[rail,ay+75],[rail,by+60],[bx,by+60]];badge=[rail-35,(ay+by)/2]
        edges.append(dict(name=f'{num} {a} → {b} · {label}',points=pts,number=num,badge=badge,secondary=secondary))
        legend.append(f'{num}  {a} → {b}\n{label}')
    return dict(pageId=PAGE_ID,name=title,title=title,kicker='UX RESEARCH / USER FLOW / CORE',subtitle=subtitle,
                x=x,y=3900,width=width,height=height,nodes=nodes,edges=edges,legend='\n\n'.join(legend),legendX=legend_x,legendWidth=660,
                notes=[dict(x=64,y=height-160,w=width-128,text='Номера на стрелках соответствуют условиям справа. Пунктир — возврат или состояние текущего экрана.\nИсточник: ia/flows/'+stem+'.mmd. Подробные ограничения и открытые решения: ia/flows/README.md.')])


sitemap=(ROOT/'ia/sitemap.md').read_text(encoding='utf-8')
tree=re.search(r'```text\n(.*?)\n```',sitemap,re.S).group(1)
parsed=[]
for line in tree.splitlines():
    m=re.match(r'( *)(\w+) \[(\w+)\] — (.*)',line)
    parsed.append((len(m[1])//2,m[2],m[3],m[4]))
DESCRIPTIONS={name:desc for _,name,_,desc in parsed}


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    nodes=[];edges=[];parent=None;col=-1;row=0
    for depth,name,priority,desc in parsed:
        if depth==0: px,py=1010,230
        elif depth==1: col+=1;row=0;px,py=64+col*380,470;parent=name
        else: px,py=64+col*380,690+row*170;row+=1
        nodes.append(dict(id=name,priority=priority,desc=desc,x=px,y=py,w=320,h=136))
        if depth==1:
            edges.append(dict(name=f'Home → {name}',points=[[1170,366],[1170,415],[px+160,415],[px+160,470]]))
        elif depth==2:
            edges.append(dict(name=f'{parent} → {name}',points=[[px+160,606],[px-18,606],[px-18,py+68],[px,py+68]]))
    states=[];future=[]
    for line in sitemap.splitlines():
        m=re.match(r'\| (\w+) \[(core|v2|later)\] \| (\w+) \| (.*?) \|',line)
        if m:
            name,priority,owner,desc=m.groups()
            if priority=='core':states.append(f'{name} → {owner}\n{desc}')
            else:future.append((name,priority,owner,desc))
    notes=[dict(x=64,y=1940,w=2170,size=18,text='СТРУКТУРА, А НЕ ПОРЯДОК ПЕРЕХОДОВ • Home, Analysis, Participation и System — логические группы.\nResultsOverview — первый экран результатов. Heatmaps — подробный анализ по выбору. Все 25 узлов дерева — [core].'),
           dict(x=64,y=2050,w=2170,size=24,text='Состояния и режимы · принадлежат экранам, не создают новые разделы')]
    for i,entry in enumerate(states):
        notes.append(dict(x=64+(i%3)*750,y=2110+(i//3)*135,w=700,text=entry))
    notes.append(dict(x=64,y=2960,w=2100,size=22,text='Развитие · [v2] = кандидаты v1.1 PRD; [later] = бэклог'))
    for i,(name,priority,owner,desc) in enumerate(future):
        nodes.append(dict(id=name,priority=priority,desc=f'Владелец: {owner}. {desc}',x=64+(i%3)*750,y=3020+(i//3)*165,w=700,h=140,
                          fill='#FFF3B0' if priority=='v2' else '#E5E5E5',stroke='#B58900' if priority=='v2' else '#888888'))
    for note in notes: note['y']+=130
    for node in nodes[25:]: node['y']+=130
    data=[dict(pageId=PAGE_ID,name='01 · Sitemap',title='Sitemap · UX-Lab',kicker='ИНФОРМАЦИОННАЯ АРХИТЕКТУРА / V1.0',
               subtitle='25 узлов дерева • 17 состояний и режимов • 6 расширений • источник: ia/sitemap.md',x=160,y=160,width=2420,height=3530,nodes=nodes,edges=edges,notes=notes)]
    data.append(flow_data('study-launch','02 · Запуск исследования','Дизайнер / PM · от создания исследования до готовой ссылки',
                         {n:(390,240+i*210) for i,n in enumerate(['Login','Studies','StudySetup','Connection','Tasks','SuccessCriteria','Launch'])},1900,2200,160,1120))
    data.append(flow_data('participant-test','03 · Прохождение участником','Участник · приглашение без регистрации, задание или свободное изучение',
                         {n:(250,240+i*250) for i,n in enumerate(['ParticipantIntro','TaskBriefing','ParticipantSession','ParticipantFinish'])},1680,1660,2220,920))
    data.append(flow_data('results-analysis','04 · Анализ результатов','Сначала обзор сценариев и цифр, затем выбранный инструмент подробного анализа',
                         {'Studies':(450,240),'ResultsOverview':(450,460),'Heatmaps':(70,740),'Funnel':(450,740),'Signals':(830,740),'Participants':(450,1050),'ParticipantDetails':(450,1300),'Replay':(450,1550),'Report':(1410,740)},2520,2650,4060,1790))
    manifest=[]
    for index,item in enumerate(data,1):
        path=OUT/f'{index:02}.js'
        path.write_text('const DATA='+json.dumps(item,ensure_ascii=False)+';\n'+RENDERER,encoding='utf-8')
        manifest.append(dict(index=index,name=item['name'],nodes=len(item['nodes']),edges=len(item['edges']),path=str(path)))
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False))


if __name__=='__main__':main()
