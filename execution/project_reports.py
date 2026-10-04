"""Immutable project report snapshots and deterministic PDF export."""
import io
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

SECTIONS=['tasks','pages','sessions','funnel','signals','findings']
STATUS={'succeeded':'Выполнено','failed':'Не выполнено','pending':'Без итогового результата','not_started':'Не начато','unassessed':'Не оценивалось','needs_review':'Ожидает оценки','indeterminate':'Невозможно оценить'}

def options(data):
    if set(data)-{'device','title','sections'}:raise ValueError('Unknown report option')
    sections=data.get('sections',SECTIONS)
    if not isinstance(sections,list) or not sections or any(not isinstance(s,str) or s not in SECTIONS for s in sections) or len(set(sections))!=len(sections):raise ValueError('Choose report sections')
    title=data.get('title','')
    if not isinstance(title,str) or len(title)>160 or ('title' in data and not title.strip()):raise ValueError('Invalid report title')
    return {'title':title.strip(),'sections':sections}

def catalog(db,project):
    result=[]
    for row in db.execute('SELECT r.value FROM live_reports r JOIN live_studies s ON s.id=r.study WHERE s.project_id=? ORDER BY r.rowid DESC',(project,)):
        report=json.loads(row[0])
        result.append({key:report[key] for key in ('id','createdAt','device','project','total')}|{'title':report.get('title') or 'Отчёт · '+report['project']['studyTitle'],'sections':report.get('sections',SECTIONS)})
    return result

def read(db,project,report_id):
    row=db.execute('SELECT r.value FROM live_reports r JOIN live_studies s ON s.id=r.study WHERE s.project_id=? AND r.id=?',(project,report_id)).fetchone()
    if not row:raise ValueError('Report not found in project')
    return json.loads(row[0])

def task_list(session):
    run=session.get('task')
    if not run:return []
    return run.get('tasks',[{**run,'title':'Задание 1','taskId':'legacy-task','revision':'legacy'}])

def render_pdf(report,page_names):
    if not page_names:page_names=json.loads(Path(__file__).with_name('leed_page_labels.json').read_text(encoding='utf-8'))
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether
    if 'ReportRegular' not in pdfmetrics.getRegisteredFontNames():
        regular=next((p for p in [Path('C:/Windows/Fonts/arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists()),None)
        bold=next((p for p in [Path('C:/Windows/Fonts/arialbd.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')] if p.exists()),regular)
        if regular is None:raise ValueError('PDF font unavailable')
        pdfmetrics.registerFont(TTFont('ReportRegular',str(regular)));pdfmetrics.registerFont(TTFont('ReportBold',str(bold)))
    body=ParagraphStyle('Body',fontName='ReportRegular',fontSize=9,leading=13,textColor=colors.HexColor('#282b25'),spaceAfter=6,wordWrap='CJK')
    heading=ParagraphStyle('Heading',parent=body,fontName='ReportBold',fontSize=14,leading=19,spaceBefore=15,spaceAfter=9,keepWithNext=True)
    title_style=ParagraphStyle('Title',parent=heading,fontSize=20,leading=25)
    muted=ParagraphStyle('Muted',parent=body,fontSize=8,textColor=colors.HexColor('#696e62'))
    def p(value,style=body):return Paragraph(escape(str(value)).replace('\n','<br/>'),style)
    def date(value):return datetime.fromtimestamp(value/1000).strftime('%d.%m.%Y %H:%M') if value else '—'
    def page(key):return page_names.get(key,key)
    stream=io.BytesIO();doc=SimpleDocTemplate(stream,pagesize=(595.28,841.89),rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=42,title=report.get('title') or report['project']['studyTitle'],author='UX-Lab')
    flow=[p(report.get('title') or 'Отчёт · '+report['project']['studyTitle'],title_style),p(report['project']['title']+' · '+report['project']['studyTitle']),p('Сформирован '+date(report['createdAt'])+' · '+{'all':'Все размеры экрана','desktop':'От 768 px','mobile':'До 768 px'}[report['device']],muted),p(f"Сессии: {report['total']['sessions']} · Клики: {report['total']['clicks']} · Экраны: {report['total']['pages']}")]
    def table(headers,rows,widths):
        if not rows:flow.append(p('Нет данных в этой выборке.',muted));return
        data=[[p(h,muted) for h in headers]]+[[p(v) for v in row] for row in rows]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT',splitInRow=1)
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#f2f3ed')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),.4,colors.HexColor('#dddfd5')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));flow.append(t)
    sections=report.get('sections',SECTIONS)
    if 'tasks' in sections:
        flow.append(p('Выполнение заданий',heading));groups={}
        for s in report['sessions']:
            for task in task_list(s):groups.setdefault((task['taskId'],task.get('revision','legacy')),[]).append(task)
        flow.append(p('Доля успеха рассчитана среди всех сессий, получивших соответствующую версию задания. Ожидание оценки и незавершённые попытки не считаются неуспехом.',muted))
        table(['Задание и критерий','Успех','Остальные результаты'],[(items[0]['title']+'\n'+items[0]['scenario']+'\nКритерий: '+items[0]['criterionLabel'],f"{sum(t['status']=='succeeded' for t in items)} из {len(items)} ({round(100*sum(t['status']=='succeeded' for t in items)/len(items))}%)",'\n'.join(STATUS[k]+': '+str(v) for k,v in Counter(t['status'] for t in items if t['status']!='succeeded').items()) or 'Все выполнены') for items in groups.values()],[230,85,200])
    if 'pages' in sections:
        flow.append(p('Экраны',heading));table(['Экран','Сессии','Клики'],[(page(r['id']),r['sessions'],r['clicks']) for r in report['pages']],[315,100,100])
    if 'sessions' in sections:
        flow.append(p('Сессии',heading));table(['Сессия / последнее действие','Клики','Результаты заданий'],[(s['id']+'\n'+date(s['lastAt']),s['clicks'],'\n'.join(t['title']+': '+STATUS.get(t['status'],t['status']) for t in task_list(s)) or 'Не оценивалось') for s in report['sessions']],[225,55,235])
    if 'funnel' in sections:
        flow.append(p('Воронка переходов',heading));table(['Шаг','Дошли, сессий'],[(str(i+1)+'. '+page(r['page']),r['sessions']) for i,r in enumerate(report['funnel'])],[395,120])
    if 'signals' in sections:
        flow.append(p('Сигналы затруднений',heading));flow.append(p('Повторные клики - повод изучить контекст, а не доказательство проблемы.',muted));table(['Экран / действие','Сессия / время'],[(page(r['page'])+'\n'+r['label'],r['session']+'\n'+date(r['timestamp'])) for r in report['signals']],[265,250])
    if 'findings' in sections:
        flow.append(p('Находки',heading))
        if not report['findings']:flow.append(p('Находок пока нет.',muted))
        for finding in report['findings']:flow.extend([p(finding['title'],heading),p(finding.get('observation',''))])
    flow.extend([Spacer(1,16),p('Отчёт фиксирует данные на момент формирования. Сессия соответствует вкладке браузера, а не уникальному человеку.',muted)])
    def footer(canvas,document):
        canvas.setFont('ReportRegular',8);canvas.setFillColor(colors.HexColor('#696e62'));canvas.drawString(40,24,'UX-Lab');canvas.drawRightString(555,24,str(document.page))
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)
    return stream.getvalue()
