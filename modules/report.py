import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

BLACK = HexColor("#0A0A0A")
WHITE = HexColor("#FFFFFF")
ACCENT = HexColor("#C8FF00")
DARK_GRAY = HexColor("#1A1A1A")
MID_GRAY = HexColor("#333333")
LIGHT_GRAY = HexColor("#F5F5F5")
TEXT_GRAY = HexColor("#555555")

def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='ReportTitle', fontName='Helvetica-Bold', fontSize=28, textColor=WHITE, spaceAfter=8, leading=32))
    styles.add(ParagraphStyle(name='SubTitle', fontName='Helvetica-Bold', fontSize=11, textColor=MID_GRAY, spaceBefore=10, spaceAfter=4))
    styles.add(ParagraphStyle(name='BodyText21', fontName='Helvetica', fontSize=10, textColor=TEXT_GRAY, leading=16, spaceAfter=6))
    styles.add(ParagraphStyle(name='BulletItem', fontName='Helvetica', fontSize=10, textColor=TEXT_GRAY, leading=15, leftIndent=15, spaceAfter=4))
    styles.add(ParagraphStyle(name='FooterText', fontName='Helvetica', fontSize=8, textColor=HexColor("#999999"), alignment=TA_CENTER))
    return styles

def add_header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(ACCENT)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#CCCCCC"))
    canvas.rect(0, 0, w, 28, fill=1, stroke=0)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#888888"))
    canvas.drawString(2*cm, 10, "21STUDIO — AI Sales Intelligence Agent")
    canvas.drawRightString(w - 2*cm, 10, f"Pag. {doc.page}  |  Confidenziale")
    canvas.restoreState()

def _section_header(title, styles, width):
    t = Table([[Paragraph(title, ParagraphStyle(name=f'SH_{title}', fontName='Helvetica-Bold', fontSize=13, textColor=BLACK))]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#F0F0F0")),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 2, HexColor("#C8FF00")),
    ]))
    return t

def generate_pdf(analysis, output_path=None):
    if not output_path:
        company = analysis.get("company_name", "report").replace(" ", "_").lower()
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        output_path = f"report_{company}_{ts}.pdf"

    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2.5*cm, bottomMargin=2*cm)
    styles = build_styles()
    story = []
    w = A4[0] - 4*cm

    # COVER
    cover_table = Table([[Paragraph("SALES INTELLIGENCE<br/>REPORT", styles['ReportTitle'])]], colWidths=[w])
    cover_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLACK),('TOPPADDING',(0,0),(-1,-1),30),('BOTTOMPADDING',(0,0),(-1,-1),30),('LEFTPADDING',(0,0),(-1,-1),20)]))
    story.append(cover_table)
    story.append(Spacer(1, 12))

    meta = [["Azienda analizzata", analysis.get("company_name","—")],["Data report", datetime.now().strftime("%d %B %Y")],["Generato da","21STUDIO AI Sales Intelligence Agent"]]
    meta_table = Table(meta, colWidths=[w*0.35, w*0.65])
    meta_table.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),LIGHT_GRAY),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTNAME',(1,0),(1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),10),('TEXTCOLOR',(0,0),(-1,-1),MID_GRAY),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),12),('GRID',(0,0),(-1,-1),0.5,HexColor("#DDDDDD"))]))
    story.append(meta_table)
    story.append(PageBreak())

    # EXECUTIVE SUMMARY
    story.append(_section_header("Executive Summary", styles, w))
    story.append(Paragraph(analysis.get("executive_summary",""), styles['BodyText21']))
    story.append(Spacer(1,10))

    # BUSINESS OVERVIEW
    story.append(_section_header("Business Overview", styles, w))
    story.append(Paragraph(f"<b>Panoramica:</b> {analysis.get('business_overview','')}", styles['BodyText21']))
    story.append(Spacer(1,6))
    story.append(Paragraph(f"<b>Target Market:</b> {analysis.get('target_market','')}", styles['BodyText21']))
    story.append(Spacer(1,6))
    story.append(Paragraph(f"<b>Value Proposition:</b> {analysis.get('value_proposition','')}", styles['BodyText21']))
    story.append(Spacer(1,10))

    # COMPETITOR ANALYSIS
    story.append(_section_header("Analisi Competitor", styles, w))
    for comp in analysis.get("competitor_analysis",[]):
        story.append(Paragraph(f"<b>{comp.get('name','')}</b> — {comp.get('url','')}", styles['SubTitle']))
        story.append(Paragraph(f"<b>Punti di forza:</b> {comp.get('strengths','')}", styles['BulletItem']))
        story.append(Paragraph(f"<b>Debolezze:</b> {comp.get('weaknesses','')}", styles['BulletItem']))
        story.append(Paragraph(f"<b>Segnali di prezzo:</b> {comp.get('pricing_signals','')}", styles['BulletItem']))
        story.append(Spacer(1,8))

    # GAP ANALYSIS
    story.append(PageBreak())
    story.append(_section_header("Gap Analysis", styles, w))
    for i, gap in enumerate(analysis.get("gap_analysis",[]), 1):
        story.append(Paragraph(f"<b>{i}.</b> {gap}", styles['BulletItem']))
    story.append(Spacer(1,10))

    # REVIEW INSIGHTS
    story.append(_section_header("Insight dalle Recensioni", styles, w))
    story.append(Paragraph(analysis.get("review_insights",""), styles['BodyText21']))
    story.append(Spacer(1,10))

    # GROWTH OPPORTUNITIES
    story.append(_section_header("Opportunita di Crescita", styles, w))
    for opp in analysis.get("growth_opportunities",[]):
        if isinstance(opp, dict):
            story.append(Paragraph(f"<b>{opp.get('title','')}</b>", styles['SubTitle']))
            story.append(Paragraph(opp.get('description',''), styles['BulletItem']))
        else:
            story.append(Paragraph(f"• {opp}", styles['BulletItem']))
    story.append(Spacer(1,10))

    # RECOMMENDATIONS — celle come Paragraph per il word wrap corretto
    story.append(PageBreak())
    story.append(_section_header("Raccomandazioni Prioritizzate", styles, w))
    recs = analysis.get("recommendations",[])
    if recs:
        h_style = ParagraphStyle('RH', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)
        c_style = ParagraphStyle('RC', fontName='Helvetica', fontSize=9, textColor=TEXT_GRAY, leading=14)
        t_style = ParagraphStyle('RT', fontName='Helvetica-Bold', fontSize=9, textColor=MID_GRAY, leading=14)
        n_style = ParagraphStyle('RN', fontName='Helvetica-Bold', fontSize=11, textColor=ACCENT, alignment=TA_CENTER)

        rec_data = [[Paragraph("#",h_style), Paragraph("Titolo",h_style), Paragraph("Azione",h_style), Paragraph("Impatto Atteso",h_style)]]
        for rec in recs:
            rec_data.append([
                Paragraph(str(rec.get("priority","")), n_style),
                Paragraph(rec.get("title",""), t_style),
                Paragraph(rec.get("action",""), c_style),
                Paragraph(rec.get("expected_impact",""), c_style),
            ])
        rec_table = Table(rec_data, colWidths=[w*0.06, w*0.20, w*0.44, w*0.30])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),BLACK),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT_GRAY]),
            ('GRID',(0,0),(-1,-1),0.3,HexColor("#DDDDDD")),
            ('TOPPADDING',(0,0),(-1,-1),8),
            ('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('LEFTPADDING',(0,0),(-1,-1),8),
            ('RIGHTPADDING',(0,0),(-1,-1),8),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(rec_table)

    story.append(Spacer(1,30))
    story.append(HRFlowable(width=w, thickness=1, color=HexColor("#DDDDDD")))
    story.append(Spacer(1,8))
    story.append(Paragraph("Report generato automaticamente da <b>21STUDIO AI Sales Intelligence Agent</b> — 21studio.io", styles['FooterText']))

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"[report] PDF saved: {output_path}")
    return output_path
