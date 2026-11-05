import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, HRFlowable
)

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page numbers and standard GxP header/footer.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0f2942"))
        
        # Header (pages > 1 or all pages)
        doc_ref = getattr(self, "_doc_ref", "PHARMANOVA GxP DOCUMENTATION")
        doc_title = getattr(self, "_doc_title", "SYSTÈME QUALITÉ PHARMACEUTIQUE")
        
        # Header top line
        self.setStrokeColor(colors.HexColor("#0f2942"))
        self.setLineWidth(1)
        self.line(40, 802, 555, 802)
        
        self.drawString(40, 808, f"PHARMANOVA SA | {doc_ref}")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4b5563"))
        self.drawRightString(555, 808, f"Réf: {doc_title[:45]}")
        
        # Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(40, 45, 555, 45)
        
        self.setFont("Helvetica", 7)
        self.drawString(40, 34, "CONFIDENTIEL - Ce document est la propriété exclusive de PharmaNova SA. Reproduction et diffusion interdites sans accord écrit.")
        self.setFont("Helvetica-Bold", 8)
        self.drawRightString(555, 34, f"Page {self._pageNumber} / {page_count}")
        self.restoreState()

def create_pharma_doc(filepath, doc_ref="DOC-GxP", doc_title="Document"):
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )
    
    # Attach doc info to canvas maker
    class CustomCanvas(NumberedCanvas):
        def __init__(self, *args, **kwargs):
            self._doc_ref = doc_ref
            self._doc_title = doc_title
            super(CustomCanvas, self).__init__(*args, **kwargs)
            
    return doc, CustomCanvas

def get_pharma_styles():
    styles = getSampleStyleSheet()
    
    # Custom colors
    PRIMARY = colors.HexColor("#0f2942")     # Deep Pharma Navy
    SECONDARY = colors.HexColor("#0284c7")   # Medical Blue
    ACCENT = colors.HexColor("#0d9488")      # Clinical Teal
    TEXT = colors.HexColor("#1e293b")        # Dark Slate
    MUTED = colors.HexColor("#64748b")       # Cool Gray
    
    styles.add(ParagraphStyle(
        name='PharmaDocTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceAfter=12
    ))
    
    styles.add(ParagraphStyle(
        name='PharmaDocSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceAfter=15
    ))

    styles.add(ParagraphStyle(
        name='PharmaH1',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='PharmaH2',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='PharmaBody',
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=TEXT,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='PharmaBodyBold',
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=TEXT,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='PharmaSmall',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=MUTED
    ))

    styles.add(ParagraphStyle(
        name='PharmaTableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=TEXT
    ))

    styles.add(ParagraphStyle(
        name='PharmaTableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    ))

    styles.add(ParagraphStyle(
        name='PharmaCallout',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=PRIMARY
    ))

    return styles

def build_approval_block(styles, author, reviewer, approver, doc_id, rev_date):
    data = [
        [
            Paragraph("<b>ÉTABLI PAR</b>", styles['PharmaSmall']),
            Paragraph("<b>VÉRIFIÉ PAR</b>", styles['PharmaSmall']),
            Paragraph("<b>APPROUVÉ PAR (QP / Directoire)</b>", styles['PharmaSmall']),
        ],
        [
            Paragraph(f"<b>Nom :</b> {author['name']}<br/><b>Titre :</b> {author['title']}<br/><b>Date :</b> {rev_date}", styles['PharmaTableCell']),
            Paragraph(f"<b>Nom :</b> {reviewer['name']}<br/><b>Titre :</b> {reviewer['title']}<br/><b>Date :</b> {rev_date}", styles['PharmaTableCell']),
            Paragraph(f"<b>Nom :</b> {approver['name']}<br/><b>Titre :</b> {approver['title']}<br/><b>Date :</b> {rev_date}", styles['PharmaTableCell']),
        ],
        [
            Paragraph("<b>Signature :</b> <i>[Signé électroniquement via DocuSign GxP 21 CFR Part 11]</i>", styles['PharmaSmall']),
            Paragraph("<b>Signature :</b> <i>[Signé électroniquement via DocuSign GxP 21 CFR Part 11]</i>", styles['PharmaSmall']),
            Paragraph("<b>Signature :</b> <i>[Signé électroniquement via DocuSign GxP 21 CFR Part 11]</i>", styles['PharmaSmall']),
        ]
    ]
    t = Table(data, colWidths=[170, 170, 175])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t

def build_metadata_box(styles, meta_pairs):
    data = []
    row = []
    for i, (k, v) in enumerate(meta_pairs):
        p_k = Paragraph(f"<b>{k} :</b>", styles['PharmaTableCell'])
        p_v = Paragraph(str(v), styles['PharmaTableCell'])
        row.extend([p_k, p_v])
        if len(row) == 4:
            data.append(row)
            row = []
    if row:
        while len(row) < 4:
            row.append(Paragraph("", styles['PharmaTableCell']))
        data.append(row)
    t = Table(data, colWidths=[100, 155, 100, 160])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t
