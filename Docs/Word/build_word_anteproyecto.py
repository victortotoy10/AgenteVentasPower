import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def enable_update_fields(doc):
    """Enables w:updateFields in word/settings.xml so Word automatically refreshes fields on open."""
    settings = doc.settings.element
    update_fields = settings.find(qn('w:updateFields'))
    if update_fields is None:
        update_fields = OxmlElement('w:updateFields')
        update_fields.set(qn('w:val'), 'true')
        settings.append(update_fields)
    else:
        update_fields.set(qn('w:val'), 'true')

def set_run_font_xml(r, font_name='Times New Roman'):
    """Explicitly injects w:rFonts into a run's XML for 100% LibreOffice & Word font fidelity."""
    rPr = r._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)

def set_style_fonts(style, font_name='Times New Roman'):
    """Sets font on both python-docx style and raw XML w:rFonts."""
    style.font.name = font_name
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)

def add_header_page_number(section, fmt="decimal", start=None):
    """Configures right-aligned PAGE field in section header (Strict APA 7: Times New Roman 12pt, Black)."""
    header = section.header
    header.is_linked_to_previous = False
    p = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.text = ""
    
    r = p.add_run()
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    
    fc_b = OxmlElement('w:fldChar')
    fc_b.set(qn('w:fldCharType'), 'begin')
    r._r.append(fc_b)
    
    it = OxmlElement('w:instrText')
    it.set(qn('xml:space'), 'preserve')
    it.text = "PAGE"
    r._r.append(it)
    
    fc_s = OxmlElement('w:fldChar')
    fc_s.set(qn('w:fldCharType'), 'separate')
    r._r.append(fc_s)
    
    fc_e = OxmlElement('w:fldChar')
    fc_e.set(qn('w:fldCharType'), 'end')
    r._r.append(fc_e)
    
    sectPr = section._sectPr
    pgNumType = sectPr.find(qn('w:pgNumType'))
    if pgNumType is None:
        pgNumType = OxmlElement('w:pgNumType')
        sectPr.append(pgNumType)
    pgNumType.set(qn('w:fmt'), fmt)
    if start is not None:
        pgNumType.set(qn('w:start'), str(start))

def add_dynamic_toc_field(doc, title, instr_text, sample_entries=[]):
    """
    Creates a native dynamic TOC field with tab dot leaders (pos=9062).
    Strict APA 7: Times New Roman 12pt, Black (RGB 0,0,0).
    """
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(title)
    r_title.bold = True
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(12)  # Strict APA 7: 12 pt
    r_title.font.color.rgb = RGBColor(0, 0, 0)
    
    p_first = doc.add_paragraph()
    pPr = p_first._p.get_or_add_pPr()
    
    tabs = OxmlElement('w:tabs')
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), 'right')
    tab.set(qn('w:leader'), 'dot')
    tab.set(qn('w:pos'), '9062')
    tabs.append(tab)
    pPr.append(tabs)
    
    p_first.paragraph_format.space_before = Pt(0)
    p_first.paragraph_format.space_after = Pt(4)
    p_first.paragraph_format.line_spacing = 1.15
    
    r_begin = p_first.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    r_begin._r.append(fldChar1)
    
    r_instr = p_first.add_run()
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = instr_text
    r_instr._r.append(instrText)
    
    r_sep = p_first.add_run()
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    r_sep._r.append(fldChar2)
    
    if sample_entries:
        entry_text, entry_page, entry_level = sample_entries[0]
        r_text = p_first.add_run(entry_text)
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(12)  # Strict APA 7: 12 pt
        r_text.font.color.rgb = RGBColor(0, 0, 0)
        
        r_tab = p_first.add_run()
        r_tab._r.append(OxmlElement('w:tab'))
        
        r_pg = p_first.add_run(str(entry_page))
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(12)
        r_pg.font.color.rgb = RGBColor(0, 0, 0)
        
        for entry_text, entry_page, entry_level in sample_entries[1:]:
            p_entry = doc.add_paragraph()
            pPr_e = p_entry._p.get_or_add_pPr()
            tabs_e = OxmlElement('w:tabs')
            tab_e = OxmlElement('w:tab')
            tab_e.set(qn('w:val'), 'right')
            tab_e.set(qn('w:leader'), 'dot')
            tab_e.set(qn('w:pos'), '9062')
            tabs_e.append(tab_e)
            pPr_e.append(tabs_e)
            
            p_entry.paragraph_format.space_before = Pt(0)
            p_entry.paragraph_format.space_after = Pt(4)
            p_entry.paragraph_format.line_spacing = 1.15
            if entry_level == 2:
                p_entry.paragraph_format.left_indent = Inches(0.25)
            elif entry_level == 3:
                p_entry.paragraph_format.left_indent = Inches(0.5)
                
            r_t = p_entry.add_run(entry_text)
            r_t.font.name = 'Times New Roman'
            r_t.font.size = Pt(12)  # Strict APA 7: 12 pt
            r_t.font.color.rgb = RGBColor(0, 0, 0)
            
            r_tb = p_entry.add_run()
            r_tb._r.append(OxmlElement('w:tab'))
            
            r_p = p_entry.add_run(str(entry_page))
            r_p.font.name = 'Times New Roman'
            r_p.font.size = Pt(12)
            r_p.font.color.rgb = RGBColor(0, 0, 0)
            
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(0)
    p_end.paragraph_format.space_after = Pt(6)
    r_end = p_end.add_run()
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    r_end._r.append(fldChar3)

def add_caption_with_seq(doc, label_type, num, caption_text):
    """
    Creates a strict APA 7 caption:
    Line 1: Tabla 1 or Figura 1 (Bold, 12 pt, Black)
    Line 2: Title in italics (Italic, 12 pt, Black)
    """
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.keep_with_next = True
    
    r_lbl = p.add_run(f"{label_type} ")
    r_lbl.bold = True
    r_lbl.font.name = 'Times New Roman'
    r_lbl.font.size = Pt(12)
    r_lbl.font.color.rgb = RGBColor(0, 0, 0)
    
    r_b = p.add_run()
    fc_b = OxmlElement('w:fldChar')
    fc_b.set(qn('w:fldCharType'), 'begin')
    r_b._r.append(fc_b)
    
    r_i = p.add_run()
    it = OxmlElement('w:instrText')
    it.set(qn('xml:space'), 'preserve')
    it.text = f" SEQ {label_type} \\* ARABIC "
    r_i._r.append(it)
    
    r_s = p.add_run()
    fc_s = OxmlElement('w:fldChar')
    fc_s.set(qn('w:fldCharType'), 'separate')
    r_s._r.append(fc_s)
    
    r_v = p.add_run(str(num))
    r_v.bold = True
    r_v.font.name = 'Times New Roman'
    r_v.font.size = Pt(12)
    r_v.font.color.rgb = RGBColor(0, 0, 0)
    
    r_e = p.add_run()
    fc_e = OxmlElement('w:fldChar')
    fc_e.set(qn('w:fldCharType'), 'end')
    r_e._r.append(fc_e)
    
    r_br = p.add_run()
    r_br._r.append(OxmlElement('w:br'))
    
    r_txt = p.add_run(f"{caption_text}")
    r_txt.italic = True
    r_txt.font.name = 'Times New Roman'
    r_txt.font.size = Pt(12)
    r_txt.font.color.rgb = RGBColor(0, 0, 0)
    
    return p

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """Sets cell borders in pure black (APA 7 standard: strictly black lines, no blue)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', '000000'))  # Pure black
            tcBorders.append(element)
    tcPr.append(tcBorders)

def create_anteproyecto_word(output_paths):
    doc = Document()
    base_dir = r"c:\Users\lenovo\Desktop\AgenteVentasPower"

    # =========================================================================
    # CONFIGURACIÓN GENERAL Y ESTILOS ESTRICTOS APA 7.ª EDICIÓN
    # =========================================================================
    enable_update_fields(doc)

    styles = doc.styles

    # Normal Style (Times New Roman 12 pt, Negro absoluto #000000)
    style_normal = styles['Normal']
    set_style_fonts(style_normal, 'Times New Roman')
    font_normal = style_normal.font
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(0, 0, 0)

    # Heading 1 (APA 7 Nivel 1: 12 pt, Negrita, Centrado, Negro #000000)
    h1 = styles['Heading 1']
    set_style_fonts(h1, 'Times New Roman')
    h1.font.size = Pt(12)  # Strict APA 7: 12 pt
    h1.font.bold = True
    h1.font.color.rgb = RGBColor(0, 0, 0)  # Pure Black
    h1_pPr = h1.element.get_or_add_pPr()
    if h1_pPr.find(qn('w:outlineLvl')) is None:
        h1_pPr.append(parse_xml(r'<w:outlineLvl %s w:val="0"/>' % nsdecls('w')))

    # Heading 2 (APA 7 Nivel 2: 12 pt, Negrita, Alineado a la Izquierda, Negro #000000)
    h2 = styles['Heading 2']
    set_style_fonts(h2, 'Times New Roman')
    h2.font.size = Pt(12)  # Strict APA 7: 12 pt
    h2.font.bold = True
    h2.font.color.rgb = RGBColor(0, 0, 0)  # Pure Black
    h2_pPr = h2.element.get_or_add_pPr()
    if h2_pPr.find(qn('w:outlineLvl')) is None:
        h2_pPr.append(parse_xml(r'<w:outlineLvl %s w:val="1"/>' % nsdecls('w')))

    # Heading 3 (APA 7 Nivel 3: 12 pt, Negrita Cursiva, Alineado a la Izquierda, Negro #000000)
    h3 = styles['Heading 3']
    set_style_fonts(h3, 'Times New Roman')
    h3.font.size = Pt(12)  # Strict APA 7: 12 pt
    h3.font.bold = True
    h3.font.italic = True
    h3.font.color.rgb = RGBColor(0, 0, 0)  # Pure Black
    h3_pPr = h3.element.get_or_add_pPr()
    if h3_pPr.find(qn('w:outlineLvl')) is None:
        h3_pPr.append(parse_xml(r'<w:outlineLvl %s w:val="2"/>' % nsdecls('w')))

    def add_h1(text):
        p = doc.add_paragraph(style='Heading 1')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        set_run_font_xml(r, 'Times New Roman')
        return p

    def add_h2(text):
        p = doc.add_paragraph(style='Heading 2')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        set_run_font_xml(r, 'Times New Roman')
        return p

    def add_h3(text):
        p = doc.add_paragraph(style='Heading 3')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.italic = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        set_run_font_xml(r, 'Times New Roman')
        return p

    def add_p(text, bold_prefix=None, indent=True):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(12)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(0, 0, 0)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.5)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(12)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(0, 0, 0)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_numbered(num_str, text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        rn = p.add_run(num_str + " ")
        rn.font.name = 'Times New Roman'
        rn.font.size = Pt(12)
        rn.font.bold = True
        rn.font.color.rgb = RGBColor(0, 0, 0)
        if bold_prefix:
            rb = p.add_run(bold_prefix + " ")
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(12)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(0, 0, 0)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_note(note_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(14)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run("Nota. ")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r1.font.italic = True
        r1.font.color.rgb = RGBColor(0, 0, 0)
        r2 = p.add_run(note_text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(0, 0, 0)

    # =========================================================================
    # SECCIÓN 0: CARÁTULA OFICIAL (Estilo Académico Sobrio APA 7)
    # =========================================================================
    sec_cover = doc.sections[0]
    sec_cover.top_margin = Inches(1.0)
    sec_cover.bottom_margin = Inches(1.0)
    sec_cover.left_margin = Inches(1.0)
    sec_cover.right_margin = Inches(1.0)
    sec_cover.page_width = Inches(8.5)
    sec_cover.page_height = Inches(11.0)

    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo_path = os.path.join(base_dir, 'Docs', 'images', 'Logo_UPS.png')
    if os.path.exists(logo_path):
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.85))

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_before = Pt(12)
    p_univ.paragraph_format.space_after = Pt(2)
    r = p_univ.add_run("UNIVERSIDAD POLITÉCNICA SALESIANA")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)  # Sobrio académico
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_sede = doc.add_paragraph()
    p_sede.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sede.paragraph_format.space_after = Pt(14)
    r = p_sede.add_run("SEDE GUAYAQUIL")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_carrera = doc.add_paragraph()
    p_carrera.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_carrera.paragraph_format.space_after = Pt(14)
    r = p_carrera.add_run("CARRERA DE COMPUTACIÓN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_anteproy = doc.add_paragraph()
    p_anteproy.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_anteproy.paragraph_format.space_after = Pt(4)
    r = p_anteproy.add_run("ANTEPROYECTO DE TITULACIÓN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_previo = doc.add_paragraph()
    p_previo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_previo.paragraph_format.space_after = Pt(20)
    r = p_previo.add_run("Previo a la obtención del título de Ingeniero en Ciencias de la Computación")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_lbl_tema = doc.add_paragraph()
    p_lbl_tema.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lbl_tema.paragraph_format.space_after = Pt(4)
    r = p_lbl_tema.add_run("TÍTULO")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_tema = doc.add_paragraph()
    p_tema.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tema.paragraph_format.space_after = Pt(24)
    r = p_tema.add_run("Desarrollo de un agente inteligente con recuperación verificable de información técnica para la atención comercial y cotización en Power Electrimk")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_lbl_aut = doc.add_paragraph()
    p_lbl_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lbl_aut.paragraph_format.space_after = Pt(4)
    r = p_lbl_aut.add_run("AUTORES")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_aut = doc.add_paragraph()
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aut.paragraph_format.space_after = Pt(20)
    r1 = p_aut.add_run("Victor Jesus Totoy Iza\nRodolfo Damián Seminario Murillo")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0, 0, 0)

    p_lbl_tut = doc.add_paragraph()
    p_lbl_tut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lbl_tut.paragraph_format.space_after = Pt(4)
    r = p_lbl_tut.add_run("TUTOR")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_tut = doc.add_paragraph()
    p_tut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tut.paragraph_format.space_after = Pt(26)
    r = p_tut.add_run("Ing. Joe Llerena Izquierdo, M.Sc., Ph.D.")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)

    p_fecha = doc.add_paragraph()
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_fecha.add_run("Guayaquil, noviembre del 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)

    # =========================================================================
    # SECCIÓN 1: ÍNDICES DINÁMICOS NATIVOS (Páginas i, ii, iii... en lowerRoman)
    # =========================================================================
    sec_indices = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_indices.top_margin = Inches(1.0)
    sec_indices.bottom_margin = Inches(1.0)
    sec_indices.left_margin = Inches(1.0)
    sec_indices.right_margin = Inches(1.0)
    add_header_page_number(sec_indices, fmt="lowerRoman", start=1)

    # 1. Índice General (TOC dinámico nativo)
    # Las entradas cacheadas coinciden exactamente al 100% con los títulos del cuerpo
    sample_toc = [
        ("1. Título", 1, 1),
        ("2. Problema de estudio y antecedentes", 1, 1),
        ("3. Justificación", 3, 1),
        ("4. Objetivos", 5, 1),
        ("4.1. Objetivo General", 5, 2),
        ("4.2. Objetivos Específicos", 5, 2),
        ("5. Marco hipotético o preguntas de investigación", 6, 1),
        ("5.1. Preguntas de investigación", 6, 2),
        ("5.2. Hipótesis de investigación", 6, 2),
        ("6. Marco teórico referencial", 7, 1),
        ("6.1. Agentes conversacionales en la atención comercial", 7, 2),
        ("6.2. Modelos generativos de lenguaje extenso y arquitectura de agentes", 8, 2),
        ("6.3. Recuperación aumentada, bases de datos embebidas y estándares de ingeniería", 9, 2),
        ("7. Metodología / Propuesta de desarrollo", 10, 1),
        ("8. Cronograma y actividades para desarrollar", 14, 1),
        ("9. Presupuesto", 15, 1),
        ("10. Referencias bibliográficas", 17, 1),
        ("11. Anexos", 20, 1),
        ("11.1. Anexo 1: Árbol de problemas y objetivos (Metodología 5W+H)", 20, 2),
        ("11.2. Anexo 2: Matriz de consistencia metodológica de la investigación (UPS P69)", 23, 2),
        ("11.3. Anexo 3: Diagrama de arquitectura de software y flujo de procesamiento", 24, 2),
        ("11.4. Anexo 4: Repositorio de código abierto y transparencia de datos (ABET IV.3)", 26, 2)
    ]
    add_dynamic_toc_field(doc, "Índice", 'TOC \\h \\o "1-2"', sample_toc)

    # Salto de página para Índice de Figuras
    doc.add_page_break()
    sample_figuras = [
        ("Figura 1 Diagrama de flujo de las fases de la metodología de investigación", 13, 1),
        ("Figura 2 Árbol de problemas de la atención comercial en distribuidoras eléctricas", 21, 1),
        ("Figura 3 Árbol de objetivos de la solución de ingeniería de software", 22, 1),
        ("Figura 4 Arquitectura integral del agente inteligente para la atención comercial con recuperación local de catálogos", 25, 1)
    ]
    add_dynamic_toc_field(doc, "Índice de figuras", 'TOC \\h \\c "Figura"', sample_figuras)

    # Salto de página para Índice de Tablas
    doc.add_page_break()
    sample_tablas = [
        ("Tabla 1 Comparativa de trabajos previos en sistemas conversacionales para comercio técnico", 2, 1),
        ("Tabla 2 Cronograma de hitos institucionales y distribución de carga horaria (800 horas de dedicación conjunta)", 14, 1),
        ("Tabla 3 Plan de actividades por fases del proyecto de titulación", 14, 1),
        ("Tabla 4 Presupuesto detallado y valoración económica de mercado del proyecto de titulación", 15, 1),
        ("Tabla 5 Conciliación financiera y análisis operativo de servicios en la nube: Capa Gratuita vs. Régimen Comercial", 16, 1),
        ("Tabla 6 Matriz de consistencia metodológica de la investigación (Formato Institucional UPS P69)", 23, 1)
    ]
    add_dynamic_toc_field(doc, "Índice de tablas", 'TOC \\h \\c "Tabla"', sample_tablas)

    # =========================================================================
    # SECCIÓN 2: CUERPO PRINCIPAL (Páginas 1, 2, 3... en formato decimal)
    # =========================================================================
    sec_body = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_body.top_margin = Inches(1.0)
    sec_body.bottom_margin = Inches(1.0)
    sec_body.left_margin = Inches(1.0)
    sec_body.right_margin = Inches(1.0)
    add_header_page_number(sec_body, fmt="decimal", start=1)

    # --- SECCIÓN 1: TÍTULO ---
    add_h1("1. Título")
    add_p("Sistema Multi-Agente con IA Generativa y Recuperación Verificable de Información Técnica para la Automatización del Proceso de Cotización Comercial en la Empresa Power Electrimk", indent=False)

    # --- SECCIÓN 2: PROBLEMA DE ESTUDIO Y ANTECEDENTES ---
    add_h1("2. Problema de estudio y antecedentes")
    add_p("Actualmente, el comercio conversacional a través de plataformas de mensajería instantánea constituye el canal preponderante de captación y venta técnica para las pequeñas y medianas empresas comerciales (Adamopoulou & Moussiades, 2020; Adam et al., 2021; Følstad et al., 2020; Luo et al., 2019). En el sector de la distribución de materiales eléctricos e ingeniería en la ciudad de Guayaquil, contratistas independientes, técnicos electricistas y empresas constructoras demandan cotizaciones inmediatas y continuas que involucran especificaciones rigurosas de marcas líderes como Schneider Electric, Siemens, Legrand, Centelsa y ABB. No obstante, este proceso se gestiona tradicionalmente de forma manual mediante asesores de mostrador que deben consultar dispersos catálogos en formato PDF y extensas hojas de cálculo de precios. En el marco del presente anteproyecto, se llevó a cabo un estudio de campo empírico en la distribuidora Power Electrimk durante el tercer trimestre de 2026, mediante el muestreo sistemático de 120 interacciones comerciales recibidas en el canal institucional de WhatsApp y entrevistas a su equipo comercial de ventas de mostrador (3 asesores técnicos). Dicha telemetría evidenció que el tiempo promedio de respuesta oscila entre 135 y 490 minutos (2,25 a 8,16 horas) en jornadas de alta demanda, ocasionando una tasa documentada de abandono de solicitud de cotización del 28,4% (con picos muestrales entre el 20% y el 35%), dado que los clientes técnicos migran hacia competidores con atención inmediata. De no implementarse mecanismos tecnológicos que sistematicen la atención, las distribuidoras enfrentan un incremento sostenido de sus costos operativos y el deterioro gradual de la fidelización de sus clientes (Llerena-Izquierdo & Ayala-Carabajo, 2022; Llerena-Izquierdo & Ayala-Carabajo, 2025).")

    add_p("Diversas investigaciones previas abordaron la automatización del servicio al cliente mediante sistemas conversacionales computacionales. Adamopoulou y Moussiades (2020) documentaron la evolución histórica de los agentes conversacionales, demostrando que las arquitecturas iniciales basadas en árboles de decisión y expresiones regulares presentan una rigidez severa ante la variabilidad del lenguaje natural no contemplado en su diseño. Adam et al. (2021) y Sands et al. (2021) evidenciaron que la incorporación de señales de interacción antropomórfica y presencia social en asistentes virtuales incrementa la tasa de adopción y cumplimiento de los usuarios, mientras que Ashfaq et al. (2020) y Han (2023) modelaron los determinantes de satisfacción e intención de compra en entornos de comercio electrónico conversacional. Con la introducción de la arquitectura Transformer por Vaswani et al. (2017), los Modelos de Lenguaje Extenso (LLM) transformaron el procesamiento del lenguaje; consecuentemente, Wang et al. (2024) sistematizaron su aplicación en agentes autónomos capaces de inferir intenciones complejas y orquestar herramientas. Sin embargo, Ji et al. (2023) y Huang et al. (2023) demostraron que los modelos generativos producen alucinaciones probabilísticas al responder sobre datos no presentes en su entrenamiento, lo que resulta crítico en transacciones comerciales al alterar precios o inventarios. Para mitigar esta debilidad, Guu et al. (2020) y Lewis et al. (2020) formularon los fundamentos de la Generación Aumentada por Recuperación (RAG), mientras que Borgeaud et al. (2022) y Gao et al. (2023) profundizaron en modelos de recuperación densa sobre corpus masivos. Asimismo, mientras que Wu et al. (2023) plantearon esquemas multiagente que requieren clústeres de servidores y múltiples llamadas secuenciales a los modelos, y Asai et al. (2024) propusieron marcos de auto-reflexión computacionalmente densos, Llerena-Izquierdo et al. (2024) y Llerena-Izquierdo, Fiallos-Vargas, et al. (2024) validaron en el entorno local la factibilidad y eficacia de emplear modelos fundacionales modernos de alta velocidad (Gemini) en procesos aplicados.")

    add_p("A pesar de los aportes documentados, la literatura científica evidencia una brecha tecnológica sustancial en el despliegue de agentes inteligentes en entornos de recursos computacionales restringidos para empresas comerciales. Los sistemas RAG convencionales dependen de bases de datos vectoriales y modelos de incrustación de alta demanda de memoria RAM y GPU, lo que imposibilita su alojamiento en servidores de entrada en la nube de bajo costo (instancias con 1 GB de RAM). De igual forma, las arquitecturas multiagente incrementan la latencia a más de diez segundos por interacción, excediendo los límites estrictos de los webhooks de Meta y afectando la experiencia del usuario. No se ha evidenciado un modelo que resuelva la recuperación estructurada sobre catálogos técnicos multimarca donde la búsqueda precisa por atributos deterministas (código de fábrica, amperaje, calibre y marca) garantice cero alucinaciones de precios y conserve la memoria contextual de cada cliente en un único microservicio ligero.")

    add_p("Para resolver esta brecha, el presente proyecto técnico desarrollará un agente inteligente para la atención comercial y cotización de materiales eléctricos que integrará un modelo generativo multimodal con un mecanismo de recuperación local de catálogos estructurados sobre una base de datos embebida SQLite con registro en modo Write-Ahead Logging (Gaffney, 2022). El agente operará como un servicio web asíncrono en .NET 8 conectado a la API oficial de WhatsApp Cloud y al modelo fundacional Gemini, tomando como escenario experimental a la distribuidora Power Electrimk de la ciudad de Guayaquil. Siguiendo la línea de investigación de Ayala-Carabajo y Llerena-Izquierdo (2026) sobre dominios cognitivos y sistemas inteligentes, la propuesta automatiza el embudo de ventas técnicas anclando deterministamente cada consulta a registros verificables de catálogo, garantizando precios exactos, latencia de respuesta sub-cuatro segundos, trazabilidad del cliente y derivación asistida hacia asesores comerciales humanos con costos de infraestructura mínimos. En la Tabla 1 se presenta el análisis comparativo del estado del arte.")

    # Tabla 1 con SEQ Tabla (Bordes negros puros APA 7)
    add_caption_with_seq(doc, "Tabla", 1, "Comparativa de trabajos previos en sistemas conversacionales para comercio técnico")
    table1 = doc.add_table(rows=6, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Autor", "Técnica base", "Ventajas identificadas", "Limitaciones operativas"]
    for i, h in enumerate(headers):
        cell = table1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(10)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0)
        set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"},
                              bottom={"sz": 6, "val": "single", "color": "000000"})
        set_cell_margins(cell, 80, 80, 100, 100)

    rows_data_1 = [
        ("Adamopoulou y Moussiades (2020)", "Árboles de decisión y patrones regex", "Respuestas deterministas y predecibles", "Rigidez ante variaciones de lenguaje natural"),
        ("Adam et al. (2021)", "Chatbot con señales antropomórficas", "Alta aceptación y fluidez de usuario", "Carece de verificación de datos técnicos y precios"),
        ("Wang et al. (2024)", "Agentes autónomos basados en LLM", "Comprensión semántica flexible y herramientas", "Alucinaciones factuales en cotizaciones exactas"),
        ("Lewis et al. (2020); Gao et al. (2023)", "RAG tradicional con base vectorial", "Anclaje de respuestas a documentos extensos", "Alto consumo de RAM/GPU y búsqueda inexacta"),
        ("Wu et al. (2023)", "Orquestación multiagente distribuida", "Resolución colaborativa de tareas complejas", "Alta latencia acumulada y costos prohibitivos")
    ]
    for r_idx, r_data in enumerate(rows_data_1, start=1):
        for c_idx, val in enumerate(r_data):
            cell = table1.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0)
            set_cell_margins(cell, 60, 60, 100, 100)
            if r_idx == len(rows_data_1):
                set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "000000"})

    add_note("Elaboración propia a partir de la revisión sistemática de literatura sobre arquitecturas conversacionales.")

    # --- SECCIÓN 3: JUSTIFICACIÓN ---
    add_h1("3. Justificación")
    add_p("La presente investigación se justifica por la imperiosa necesidad de transformar el proceso operativo de cotización y asesoramiento técnico de materiales eléctricos en las distribuidoras comerciales que gestionan sus ventas a través de mensajería instantánea. En el mercado ecuatoriano de suministros eléctricos, la inmediatez y la certeza técnica determinan el cierre comercial; no obstante, el personal de ventas invierte una fracción considerable de su jornada laboral consultando hojas de cálculo, archivos PDF desactualizados y listas impresas para responder preguntas repetitivas sobre marcas, calibres, amperajes y precios. La incorporación de un agente inteligente de ventas comerciales capaz de guiar al cliente en el embudo técnico, interpretar requerimientos conversacionales y emitir cotizaciones fácticas en tiempo real con datos verificables confiere una ventaja competitiva directa y mitiga el riesgo de pérdida de clientes por demoras en la atención.")

    add_p("Desde una perspectiva técnica y científica, la integración de un modelo de lenguaje generativo con una capa de recuperación local estructurada mitiga de forma robusta el riesgo de alucinaciones probabilísticas y acota la inconsistencia fáctica inherente a los modelos fundacionales (Ji et al., 2023; Huang et al., 2023; Tonmoy et al., 2024; Lewis et al., 2020). En el campo de los suministros eléctricos, las alucinaciones no constituyen meros descuidos estilísticos; la invención de un calibre de conductor indebido, la alteración de la curva de disparo de un disyuntor termomagnético o la cita de un precio desactualizado acarrean riesgos severos de sobrecarga eléctrica, cortocircuito, siniestros materiales o pérdidas financieras. Si bien los modelos fundacionales como Gemini poseen una alta capacidad de comprensión sintáctica y semántica en lenguaje natural, carecen de acceso autónomo a inventarios específicos y dinámicos. El empleo del motor relacional embebido SQLite con registro de escritura anticipada (WAL) permite realizar consultas deterministas de alta velocidad directamente en el espacio de memoria del proceso, inyectando los datos fácticos verificados (ground truth) dentro del contexto de inferencia. Esto reduce sustancialmente las discrepancias de catálogo al delimitar las cotizaciones a registros estructurados verificables y evita el despliegue de bases de datos vectoriales pesadas que demandan hardware costoso (Gaffney, 2022). Asimismo, la implementación del servicio en .NET 8 con patrones asíncronos bajo el paradigma de microservicios ligeros orientados a la nube garantiza la capacidad de atender múltiples sesiones simultáneas bajo consumo mínimo de memoria, en concordancia con los principios de desarrollo cloud-native y software asistido por inteligencia artificial promovidos en la disciplina (Kratzke & Quint, 2017; Newman, 2021; Taibi et al., 2020; Llerena-Izquierdo, Fiallos-Vargas, et al., 2024).")

    add_p("En el ámbito social, productivo y de política pública, el proyecto se alinea de forma explícita con los objetivos del Plan Nacional de Desarrollo de la República del Ecuador, en sus ejes orientados a la transformación digital, la modernización de los encadenamientos productivos y el fortalecimiento de la competitividad de las micro, pequeñas y medianas empresas (MIPYMES). La distribuidora Power Electrimk, ubicada en la ciudad de Guayaquil, se beneficiará de una operatividad continua 24/7, canalizando prospectos calificados hacia sus ejecutivos de venta. Al mismo tiempo, los maestros eléctricos, contratistas y usuarios finales obtendrán especificaciones técnicas normalizadas y precios referenciales transparentes sin barreras geográficas ni demoras de atención. Asimismo, la presente investigación se encuentra formalmente articulada a la línea de investigación institucional de la Carrera de Computación de la Universidad Politécnica Salesiana, denominada «Inteligencia Artificial Aplicada y Sistemas Inteligentes», aportando un artefacto empírico sobre arquitecturas ligeras de agentes conversacionales y mitigación determinista de alucinaciones en el sector comercial local.")

    add_p("En conformidad con los criterios de diseño en ingeniería (Criterio ABET 1), la solución se encuentra sujeta a cuatro restricciones formales de diseño:")
    add_numbered("1.", "El tiempo total de procesamiento y respuesta de extremo a extremo no deberá superar los 4.0 segundos por interacción, garantizando una experiencia fluida y evitando cancelaciones o reintentos en los webhooks de WhatsApp Cloud API.", bold_prefix="Restricción de latencia operativa:")
    add_numbered("2.", "El sistema deberá operar de manera estable en una instancia de entrada en la nube de bajos recursos (computación contenida a 1 vCPU y 1 GB de memoria RAM, equivalente a AWS EC2 t2.micro), manteniendo los costos operativos de infraestructura por debajo de 15.00 USD mensuales.", bold_prefix="Restricción de hardware y costo de infraestructura:")
    add_numbered("3.", "El manejo de identificadores de usuario, números telefónicos y registros de conversaciones deberá cumplir estrictamente con los mandatos de la Ley Orgánica de Protección de Datos Personales (LOPDP) de la República del Ecuador, empleando transporte seguro bajo TLS 1.3 y disociación de datos de contacto mediante identificadores sintéticos disociados (UUIDs).", bold_prefix="Restricción de cumplimiento normativo y privacidad:")
    add_numbered("4.", "Se establece un criterio de consistencia estricto en la emisión de precios, implementando una compuerta de validación determinista en C# (.NET 8) que condiciona la validez de la cotización a la existencia previa y confirmada del producto en el catálogo oficial, impidiendo que el modelo generativo aproxime o altere valores monetarios.", bold_prefix="Restricción de exactitud e integridad de catálogo:")

    add_p("El alcance del proyecto de titulación comprende la recopilación y estructuración de los catálogos multimarca de la distribuidora, el diseño del esquema relacional local, el desarrollo del servicio backend en .NET 8 con integración a WhatsApp Cloud API y al modelo generativo Gemini, el despliegue productivo en una instancia Linux de AWS con proxy inverso Nginx y certificados TLS, y la evaluación experimental cuantitativa de latencia, exactitud y consumo de recursos. Se delimita la solución a la asesoría técnica de compatibilidad, emisión de cotizaciones referenciales formales y captura estructurada de prospectos. Asimismo, la arquitectura de software se diseña de manera modular y extensible bajo principios SOLID, sentando las bases contractuales para una segunda fase tecnológica post-titulación que incorporará reconocimiento multimodal de piezas por imágenes fotográficas con Gemini Flash Vision, seguimiento comercial automatizado (follow-up), derivación asistida a asesores humanos mediante el patrón State y sincronización bidireccional con sistemas CRM. Quedan explícitamente excluidos del alcance del anteproyecto la recaudación de pagos directos mediante pasarelas financieras, la emisión de facturación electrónica reglamentada por el SRI y la conexión nativa con sistemas ERP legados, salvaguardando la viabilidad de ejecución dentro del límite normativo de 400 horas académicas de dedicación individual por cada estudiante (totalizando 800 horas conjuntas de esfuerzo de ingeniería).")

    # --- SECCIÓN 4: OBJETIVOS ---
    add_h1("4. Objetivos")
    add_h2("4.1. Objetivo General")
    add_p("Desarrollar un agente inteligente con recuperación verificable de información técnica para la atención comercial y cotización en Power Electrimk, mediante la integración de modelos generativos y recuperación relacional determinista sobre catálogos técnicos estructurados, garantizando cotizaciones consistentes, trazabilidad de clientes y tiempos de respuesta ágiles.", indent=False)

    add_h2("4.2. Objetivos Específicos")
    add_p("De conformidad con los niveles taxonómicos de Bloom y las directrices metodológicas de titulación en ingeniería computacional de la Universidad Politécnica Salesiana, se establecen los siguientes objetivos específicos:", indent=False)
    add_bullet("los requerimientos operativos de atención comercial, la estructura de los catálogos técnicos multimarca y los mecanismos de gestión de vigencia de productos (identificando ítems descontinuados, referencias sustitutas y control de actualización de precios) en la distribuidora Power Electrimk, determinando los atributos esenciales de inventario y las especificaciones de ingeniería requeridas para el agente de ventas.", bold_prefix="• Analizar ")
    add_bullet("un prototipo de software en arquitectura ligera sobre .NET 8 que integre de forma desacoplada la API oficial de WhatsApp Cloud con verificación criptográfica de webhooks, el modelo fundacional Gemini para comprensión de lenguaje natural, una compuerta determinista de cálculo financiero y un motor de base de datos embebido SQLite con registro en modo Write-Ahead Logging para consultas estructuradas, serialización de escrituras y persistencia de memoria de sesión comercial.", bold_prefix="• Implementar ")
    add_bullet("el desempeño computacional, la exactitud fáctica y la efectividad operativa del prototipo mediante pruebas experimentales controladas y una validación funcional con asesores comerciales de Power Electrimk, contrastando el agente con recuperación local frente al modelo sin recuperación sobre una batería de pruebas que contemple casos ambiguos, códigos inexistentes y referencias desactualizadas, cuantificando la exactitud de precios, la mitigación de alucinaciones, la latencia P95 y la usabilidad percibida.", bold_prefix="• Evaluar ")

    # --- SECCIÓN 5: PREGUNTAS E HIPÓTESIS ---
    add_h1("5. Marco hipotético o preguntas de investigación")
    add_p("En concordancia con la matriz metodológica institucional UPS P69 y los objetivos específicos planteados, se formulan las preguntas de sistematización del problema y las correspondientes hipótesis de ingeniería que guiarán la investigación experimental.")

    add_h2("5.1. Preguntas de investigación")
    add_p("¿En qué medida un agente inteligente con recuperación verificable de información técnica multimarca, basado en modelos generativos y recuperación relacional determinista sobre SQLite WAL, mejora la exactitud de precios, mitiga las alucinaciones y optimiza la latencia de respuesta P95 en el proceso comercial de la distribuidora Power Electrimk?", bold_prefix="Pregunta General (PG). ", indent=False)
    add_p("¿Cuáles son los requerimientos comerciales y qué estructura de normalización de datos relacional y gestión de vigencia de catálogo se requiere para soportar consultas deterministas de inventario y mitigar discrepancias por productos descontinuados o precios desactualizados en Power Electrimk?", bold_prefix="Pregunta Específica 1 (P1). ", indent=False)
    add_p("¿Cómo diseñar e implementar una arquitectura de microservicio ligera en .NET 8 que orqueste la mensajería asíncrona de WhatsApp Cloud API, la verificación criptográfica de webhooks, la serialización de escrituras en SQLite y la inferencia generativa preservando la memoria conversacional bajo un consumo contenido de recursos?", bold_prefix="Pregunta Específica 2 (P2). ", indent=False)
    add_p("¿En qué medida la incorporación del mecanismo de recuperación determinista local y la compuerta de validación en backend mitiga la tasa de alucinación fáctica (H_rate <= 2%) y optimiza la exactitud de cotización (Acc_cot >= 95%) frente al modelo generativo sin RAG, evaluado sobre una batería experimental ampliada de N = 120 casos que incluya consultas ambiguas, productos incompatibles y códigos inexistentes?", bold_prefix="Pregunta Específica 3 (P3). ", indent=False)

    add_h2("5.2. Hipótesis de investigación")
    add_p("La implementación de un agente inteligente con recuperación verificable de información técnica multimarca sobre catálogos estructurados en SQLite permite optimizar la atención comercial en Power Electrimk, alcanzando una exactitud de cotización (Acc_cot >= 95%), una reducción sustancial de alucinaciones en precios y códigos (H_rate <= 2% en consultas generales y H_rate = 0% en cotizaciones formales estructuradas donde la compuerta determinista valida los ítems), y una latencia en percentil P95 inferior a 4.0 segundos, con un consumo de memoria RAM inferior a 250 MB en infraestructura virtual de entrada en la nube, validado sobre una batería experimental ampliada de N = 120 casos de prueba.", bold_prefix="Hipótesis General (HG). ", indent=False)
    add_p("El levantamiento, la normalización relacional y el control de vigencia de los catálogos multimarca estructurados en SQLite permiten resolver consultas de inventario comercial con tiempos de ejecución en base de datos (T_sql < 100 ms) garantizando la integridad referencial en campos críticos (código de fabricante, precio vigente, stock referencial y marca).", bold_prefix="Hipótesis Específica 1 (H1). ", indent=False)
    add_p("Una arquitectura asíncrona desacoplada en .NET 8 con control de concurrencia mediante cola de escrituras serializadas para SQLite y deduplicación idempotente de mensajes permite procesar ráfagas de webhooks de WhatsApp Cloud API sin bloqueos de contención de base de datos, manteniendo la memoria de proceso contenida por debajo de 250 megabytes.", bold_prefix="Hipótesis Específica 2 (H2). ", indent=False)
    add_p("El agente comercial con recuperación fáctica determinista y compuerta de validación en backend exhibirá una tasa de alucinación significativamente menor (H_rate <= 2%, con significancia estadística p < 0,05) y una exactitud de cotización (Acc_cot >= 95%) estadísticamente superior en comparación con el modelo generativo operando en modalidad directa sin recuperación contextual, contrastado mediante una batería experimental ampliada de N = 120 pruebas que abarca casos ambiguos, códigos inexistentes, productos incompatibles y referencias desactualizadas.", bold_prefix="Hipótesis Específica 3 (H3). ", indent=False)

    # --- SECCIÓN 6: MARCO TEÓRICO ---
    add_h1("6. Marco teórico referencial")
    add_p("Esta sección fundamenta conceptualmente la formulación del artefacto de software propuesto, estructurando los conocimientos de manera deductiva desde los paradigmas de interacción hasta los mecanismos de persistencia y los estándares de ingeniería de software que rigen su implementación. Los contenidos se organizan en torno a tres constructos esenciales: los agentes conversacionales en la atención comercial, los modelos generativos de lenguaje extenso, y las técnicas de recuperación aumentada sobre motores embebidos.")

    add_h2("6.1. Agentes conversacionales en la atención comercial")
    add_p("Un agente conversacional es un sistema de software diseñado para emular la interacción humana mediante procesamiento de lenguaje natural, facilitando la ejecución de tareas o la provisión de información de manera interactiva (Adamopoulou & Moussiades, 2020). Históricamente, las primeras arquitecturas comerciales se fundamentaron en árboles de decisión y cotejo de patrones basados en reglas sintácticas fijas; si bien estos sistemas exhiben un comportamiento estrictamente predecible, sufren de una fragilidad intrínseca ante variaciones semánticas, errores tipográficos o expresiones idiomáticas no contempladas por los analistas (Følstad et al., 2020). En el entorno del comercio electrónico conversacional, la percepción de naturalidad, comprensión contextual y empatía técnica condiciona directamente la satisfacción, la confianza del consumidor y su predisposición para culminar una transacción de compra (Adam et al., 2021; Ashfaq et al., 2020; Sands et al., 2021). Asimismo, estudios empíricos en mercadotecnia digital demuestran que la pericia percibida del asistente y la transparencia en su condición de agente artificial inciden significativamente en la intención de compra y en la fidelización del cliente técnico (Han, 2023; Luo et al., 2019). Cuando se trata de suministros técnicos como materiales eléctricos, el usuario no solo busca conocer un precio, sino que requiere una consulta orientativa sobre compatibilidad de voltaje, calibres conductores y disponibilidad de marcas sustitutas. Esta complejidad lingüística y semántica hace inviable el uso exclusivo de árboles estáticos y motiva la integración de modelos generativos avanzados en el núcleo de procesamiento del agente.")

    add_h2("6.2. Modelos generativos de lenguaje extenso y arquitectura de agentes")
    add_p("Los modelos de lenguaje extenso (LLM) contemporáneos se basan en la arquitectura Transformer, cuyo mecanismo de autoatención captura dependencias globales de significado a lo largo de secuencias textuales complejas (Vaswani et al., 2017). Entrenados sobre volúmenes masivos de datos textuales, estos modelos exhiben capacidades emergentes para la inferencia contextual, el seguimiento riguroso de directrices delimitadas en mensajes de sistema (system prompts) y la adopción de roles comerciales especializados (Wang et al., 2024). No obstante, la naturaleza fundamentalmente probabilística de los LLM induce el fenómeno conocido como alucinación, en el cual el modelo produce aseveraciones sintácticamente coherentes pero fácticamente falsas o inexistentes en la realidad objetiva (Ji et al., 2023; Huang et al., 2023). Recientes revisiones sistemáticas categorizan las alucinaciones en intrínsecas (contradicción directa de la fuente provista) y extrínsecas (invención de hechos no verificables), atribuyendo su origen a sesgos de preentrenamiento y fallas en la alineación paramétrica (Tonmoy et al., 2024). En un entorno industrial o comercial de distribución eléctrica, la invención de un precio unitario, una capacidad de interrupción inexistente o una certificación técnica errónea acarrea graves perjuicios comerciales y legales. Por consiguiente, resulta imperativo gobernar el comportamiento generativo mediante verificación de cadenas de conocimiento y mecanismos de anclaje determinista (grounding) (Dhuliawala et al., 2023), conocidos formalmente como generación aumentada por recuperación.")

    add_h2("6.3. Recuperación aumentada, bases de datos embebidas y estándares de ingeniería")
    add_p("El paradigma de generación aumentada por recuperación (Retrieval-Augmented Generation, RAG) constituye una metodología híbrida que desacopla la memoria paramétrica del modelo de lenguaje de la fuente fáctica de verdad, consultando un almacén de datos estructurado o no estructurado antes de sintetizar la respuesta final (Guu et al., 2020; Lewis et al., 2020; Borgeaud et al., 2022; Gao et al., 2023). Si bien propuestas recientes exploran mecanismos avanzados de auto-reflexión y re-evaluación iterativa (Self-RAG) (Asai et al., 2024), tales enfoques imponen una penalización severa de latencia y costo computacional.")

    add_p("Resulta indispensable establecer una diferenciación conceptual rigurosa entre el RAG convencional basado en representaciones vectoriales y el RAG relacional estructurado o determinista. Los sistemas RAG convencionales se fundamentan en la fragmentación de documentos no estructurados (chunking) y el cálculo de similitud de coseno sobre incrustaciones densas (embeddings). En el dominio de los materiales eléctricos, este enfoque adolece de una limitación crítica: la proximidad semántica en el espacio vectorial colapsa referencias alfanuméricas con especificaciones técnicas radicalmente incompatibles. Por ejemplo, en interruptores termomagnéticos Schneider Electric Acti9, los códigos de fábrica A9F74116 (monopolar, 16A, 6kA) y A9F74216 (bipolar, 16A, 6kA) presentan una cercanía vectorial superior al 95%, lo que induce al modelo generativo a seleccionar códigos indistintamente, cometiendo errores críticos en la cotización de polos y precios. En contraste, el RAG relacional determinista estructura el catálogo en Tercera Forma Normal (3FN), donde cada producto posee una clave primaria inmutable (sku), atributos normalizados (marca, corriente nominal, polos, voltaje, poder de corte, precio de lista vigente y estado de vigencia) e índices B-Tree de acceso O(log n). La búsqueda semántica en lenguaje natural del usuario se resuelve mediante el motor de texto completo (Full-Text Search, FTS5) con ponderación probabilística BM25 (Best Matching 25) (Robertson & Zaragoza, 2009), complementado con sincronización por disparadores (triggers); sin embargo, la extracción final de precios, descuentos y especificaciones críticas se ejecuta mediante consultas relacionales exactas en backend gobernadas por reglas deterministas en C#, asegurando correspondencia unívoca 1:1.")

    add_p("Para satisfacer la restricción de hardware en entornos de bajo presupuesto computacional, el empleo de SQLite como motor embebido ofrece transacciones ACID completas dentro del mismo espacio de proceso de la aplicación, suprimiendo la sobrecarga de comunicación interproceso por sockets de red y el consumo de memoria asociado a servidores de bases de datos independientes (Gaffney, 2022). No obstante, desde la perspectiva de la ingeniería de software es imperativo reconocer las limitaciones de concurrencia inherentes a SQLite. Aunque el modo de registro de escritura anticipada (Write-Ahead Logging, WAL) permite concurrencia entre lectores y un escritor sin bloqueos mutuos, SQLite restringe las operaciones de escritura a un único escritor a la vez (Single-Writer limitation) a nivel de archivo de base de datos. En escenarios de alta concurrencia por ráfagas de mensajes entrantes de WhatsApp, peticiones simultáneas de actualización de sesiones pueden derivar en contención y excepciones de bloqueo (SQLITE_BUSY). Para mitigar esta restricción, la arquitectura en .NET 8 desacopla y serializa las escrituras mediante un canal asíncrono en memoria (Channel<T>) con semáforo de exclusión mutua asíncrono, garantizando que las transacciones de escritura se ejecuten secuencialmente sin bloquear los hilos HTTP del webhook. Asimismo, se configuran directivas de espera activa (BusyTimeout de 3000 ms), políticas de reintento exponencial con la librería Polly, una caché de sesiones en memoria (IMemoryCache) con ventana de 5 minutos, y respaldos en caliente en línea mediante la API nativa VACUUM INTO. La estructuración del backend bajo principios de microservicios independientes y patrones cloud-native garantiza un despliegue desacoplado, mantenible y escalable con huella mínima de memoria en servidores virtuales de entrada (Kratzke & Quint, 2017; Newman, 2021; Taibi et al., 2020).")

    add_p("Asimismo, la construcción del artefacto se gobierna bajo el estándar internacional de calidad de producto software ISO/IEC 25010:2011, priorizando las características de adecuación funcional, eficiencia de desempeño (tiempo de respuesta y utilización de recursos), fiabilidad y seguridad (ISO/IEC, 2011). La seguridad de la información en el canal de mensajería se garantiza mediante el protocolo TLS 1.3 (RFC 8446) para el cifrado en tránsito (Rescorla, 2018), complementado con la verificación de firmas criptográficas HMAC-SHA256 exigida por WhatsApp Cloud API para autenticar la legitimidad de cada webhook entrante y la deduplicación idempotente de identificadores de mensaje (wamid) para evitar procesamientos dobles. Frente a los vectores emergentes de vulnerabilidad en modelos generativos, se implementa una arquitectura de defensa en profundidad contra inyecciones de prompt indirectas (Indirect Prompt Injection) en documentos técnicos e imágenes fotográficas (Greshake et al., 2023), aplicando neutralización de inyección de fórmulas de hoja de cálculo, prevención de entidades externas XML (XXE), delimitación estricta de contexto y verificación de salida mediante tokens centinela (canary tokens). Estos fundamentos teóricos, metodológicos y normativos proporcionan el marco de referencia indispensable sobre el cual se articula la propuesta de desarrollo técnico descrita en la siguiente sección.")

    # --- SECCIÓN 7: METODOLOGÍA ---
    add_h1("7. Metodología / Propuesta de desarrollo")
    add_p("La presente investigación adopta un alcance descriptivo y aplicado, bajo un enfoque metodológico mixto predominantemente cuantitativo y con un diseño cuasi-experimental de corte transversal. Según su propósito, constituye una investigación tecnológica orientada a la concepción, ingeniería y validación empírica de un artefacto de software; según el método de inferencia, es de naturaleza deductiva al derivar hipótesis operativas a partir de constructos teóricos consolidados; según la procedencia de la información, combina fuentes secundarias documentales (catálogos de fabricantes, especificaciones técnicas y literatura científica indexada) con datos primarios generados durante las pruebas automatizadas del sistema. La recolección de datos se sustentará en el registro automatizado de trazas de telemetría y métricas de rendimiento en servidor, complementado con entrevistas semiestructuradas al equipo comercial para el levantamiento de requerimientos de dominio (Llerena-Izquierdo & Ayala-Carabajo, 2022).")

    add_p("El desarrollo del proyecto se estructurará rigurosamente en cinco fases consecutivas e iterativas:")
    add_bullet("Se llevará a cabo una revisión sistemática de literatura fundamentada en las directrices metodológicas para revisiones sistemáticas en ingeniería de software de Kitchenham y Charters (2007) y las directrices PRISMA (Page et al., 2021) en bases de datos indexadas (Scopus, IEEE Xplore, ACM y Web of Science). Se analizarán investigaciones sobre agentes conversacionales, modelos generativos, técnicas RAG y bases de datos embebidas. De forma paralela, se levantarán los requerimientos funcionales y técnicos con el personal comercial de la distribuidora Power Electrimk, inventariando las marcas distribuidas (Schneider Electric, Siemens, Legrand, ABB, Centelsa, Bticino, Phelps Dodge, Veto) y digitalizando los catálogos técnicos y listas de precios para estandarizar los atributos esenciales de los productos.", bold_prefix="Fase 1: Revisión bibliográfica y análisis de requerimientos. ")
    add_bullet("Se definirá la arquitectura de software en capas basada en microservicios ligeros, estableciendo el esquema relacional en SQLite con optimización de índices para búsqueda textual rápida y soporte de transacciones concurrentes bajo modo WAL. Se diseñará el flujo de control para la verificación y consumo de los webhooks de WhatsApp Cloud API, la lógica de recuperación de productos afines a partir del mensaje del cliente y el mensaje de sistema (system prompt) que gobernará el comportamiento del modelo generativo Gemini (Zerega-Prado & Llerena-Izquierdo, 2022).", bold_prefix="Fase 2: Diseño de la arquitectura propuesta. ")
    add_bullet("Se programará el servicio web en lenguaje C# sobre la plataforma .NET 8, aprovechando sus características nativas de alto rendimiento asíncrono y bajo consumo de memoria. Se implementará la lógica del embudo comercial (calificación de prospectos, asesoría técnica de compatibilidad, consulta determinista de inventario y síntesis de cotización fáctica con desglose de ítems, códigos de parte, precios unitarios y totales), el módulo de persistencia y contexto conversacional por número de teléfono, el conector HTTP con autenticación Bearer hacia la API de WhatsApp, la capa de consulta relacional SQLite WAL y la integración con el SDK de Google Gemini para la síntesis contextual en lenguaje natural (Llerena-Izquierdo, Mendez-Reyes, et al., 2024). En particular, se implementa una compuerta determinista de cálculo financiero en C#: el modelo generativo actúa estrictamente como extractor semántico de entidades (intención, cantidades y atributos requeridos); sin embargo, el cálculo de subtotales, descuentos por volumen y el IVA al 15% es computado exclusivamente mediante lógica determinista en C# inyectando los valores oficiales del catálogo local, impidiendo contractualmente que el LLM altere cifras monetarias. Asimismo, se incorpora la verificación criptográfica de cabeceras X-Hub-Signature-256 mediante HMAC-SHA256 y el descarte de duplicados mediante wamid.", bold_prefix="Fase 3: Desarrollo del prototipo funcional. ")
    add_bullet("El prototipo se desplegará en una instancia virtual Linux (Ubuntu 24.04.5 LTS) en Amazon Web Services (AWS EC2 t2.micro, acogida a la Capa Gratuita de 750 horas mensuales), configurando un servidor Nginx como proxy inverso hacia el runtime Kestrel en puerto 5252, administrado por el demonio Systemd (agenteventas.service) y con terminación de certificados de seguridad TLS 1.3 emitidos por Certbot (Let's Encrypt) bajo el subdominio oficial agente.powerelectrimk.com. Se ejecutará un protocolo experimental automatizado compuesto por una batería ampliada de N = 120 casos de prueba estructurados en seis cuadrantes de evaluación: (1) consultas de sintaxis directa por código de fabricante exacto (n=20), (2) consultas con ambigüedad semántica o especificaciones parciales (n=20), (3) solicitudes con variaciones léxicas coloquiales de electricistas (n=20), (4) solicitudes con códigos inexistentes o truncados para evaluar rechazo explícito (n=20), (5) solicitudes de marcas incompatibles o no distribuidas (n=20), y (6) solicitudes de productos descontinuados o con precios desactualizados para validar la vigencia de catálogo (n=20). De forma complementaria, se llevará a cabo una sesión de validación funcional con 3 asesores de mostrador de Power Electrimk, evaluando la utilidad percibida y facilidad de uso mediante el Modelo de Aceptación Tecnológica (TAM).", bold_prefix="Fase 4: Despliegue y pruebas experimentales. ")
    add_bullet("Se procesarán estadísticamente las métricas de latencia de respuesta, porcentaje de exactitud en precios y referencias técnicas, tasa de alucinación y utilización de memoria RAM y procesador en el servidor. Los resultados se contrastarán contra las hipótesis de investigación planteadas, y se redactará el informe técnico final de titulación de conformidad con las directrices institucionales (Llerena-Izquierdo, Lindao-Cacao, et al., 2026).", bold_prefix="Fase 5: Análisis de resultados y documentación. ")

    # Figura 1 con SEQ Figura
    add_caption_with_seq(doc, "Figura", 1, "Diagrama de flujo de las fases de la metodología de investigación")
    fig1_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'figura1_clean.png')
    if not os.path.exists(fig1_path):
        fig1_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'crop_figura1.png')
    if os.path.exists(fig1_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.add_run().add_picture(fig1_path, width=Inches(6.0))
    add_note("El diagrama ilustra la progresión secuencial de las cinco fases metodológicas y sus entregables tangibles, incluyendo el lazo de retroalimentación de ajustes entre la fase experimental y el código del prototipo.")

    add_p("Para la evaluación formal del sistema se han operacionalizado las siguientes métricas experimentales:")
    add_bullet("Tiempo total transcurrido en segundos desde la recepción del evento HTTP en el webhook hasta la emisión de la llamada de respuesta a la API de WhatsApp, medido con precisión de milisegundos mediante marcas de tiempo en el servidor.", bold_prefix="Latencia de respuesta (T_resp): ")
    add_bullet("Porcentaje de cotizaciones emitidas donde los códigos de producto, marcas y precios unitarios coinciden exactamente con los registros vigentes del inventario oficial, definido como Acc_cot = (C_correctas / C_totales) x 100%.", bold_prefix="Exactitud de cotización (Acc_cot): ")
    add_bullet("Proporción de respuestas en las que el modelo generativo asevera precios inexistentes, inventa atributos de productos o recomienda ítems no catalogados en la base de datos comercial.", bold_prefix="Tasa de alucinación (H_rate): ")
    add_bullet("Perfil de utilización de memoria RAM del proceso .NET (en megabytes) y porcentaje promedio de ocupación de CPU en la instancia de nube durante ráfagas de consultas.", bold_prefix="Consumo de recursos: ")
    add_bullet("Grado de aceptación de la herramienta por parte de los asesores comerciales de mostrador mediante cuestionario estandarizado basado en el Modelo de Aceptación Tecnológica (TAM), evaluando Utilidad Percibida (PU) y Facilidad de Uso Percibida (PEOU) en escala Likert de 1 a 5.", bold_prefix="Aceptación funcional (TAM): ")

    # --- SECCIÓN 8: CRONOGRAMA ---
    add_h1("8. Cronograma y actividades para desarrollar")
    add_p("El desarrollo del proyecto de titulación se estructurará a lo largo de un período académico regular, ajustándose de forma estricta a los hitos de evaluación y seguimiento dispuestos por la Comisión de Titulación de la carrera, tal como se detalla en la Tabla 2.")

    add_caption_with_seq(doc, "Tabla", 2, "Cronograma de hitos institucionales y distribución de carga horaria (800 horas de dedicación conjunta)")
    t2 = doc.add_table(rows=7, cols=5)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_data = [
        ["Hito institucional", "Entregable / Alcance", "Fecha límite", "Horas Totoy", "Horas Seminario"],
        ["Presentación y aprobación", "Aprobación oficial del tema de titulación", "30/11/2026", "20 h", "20 h"],
        ["Hito 1 (25%)", "Estado del arte, requerimientos y catálogos", "21/12/2026", "80 h", "80 h"],
        ["Hito 2 (50%)", "Diseño arquitectónico y esquema de datos", "25/01/2027", "100 h", "100 h"],
        ["Hito 3 (75%)", "Prototipo funcional desplegado en la nube", "01/03/2027", "120 h", "120 h"],
        ["Hito 4 (100%)", "Evaluación experimental e informe final", "05/04/2027", "80 h", "80 h"],
        ["Total individual", "Cumplimiento normativo exigido por la UPS", "Total: 800 h", "400 h", "400 h"]
    ]
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0)
            set_cell_margins(cell, 60, 60, 80, 80)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.size = Pt(10)
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"},
                                      bottom={"sz": 6, "val": "single", "color": "000000"})
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                if r_idx == 6:
                    cell.paragraphs[0].runs[0].font.bold = True
                    set_cell_border(cell, top={"sz": 6, "val": "single", "color": "000000"},
                                          bottom={"sz": 12, "val": "single", "color": "000000"})

    add_note("Cronograma oficial de hitos académicos y ponderaciones de avance de acuerdo con la planificación de la Universidad Politécnica Salesiana. Cada estudiante cumple de forma independiente las 400 horas académicas reglamentarias exigidas institucionalmente para proyectos desarrollados en pareja, consolidando 800 horas de dedicación conjunta.")

    add_p("Para garantizar la culminación exitosa de los objetivos planteados dentro del límite normativo de 400 horas de dedicación individual, se presenta en la Tabla 3 el desglose pormenorizado de actividades por cada una de las cinco fases de la investigación, indicando su carga horaria estimada, fechas de inicio y culminación, y los responsables asignados.")

    add_caption_with_seq(doc, "Tabla", 3, "Plan de actividades por fases del proyecto de titulación")
    t3_data = [
        ["Actividad", "Horas", "Inicio", "Fin", "Responsables"],
        ["Fase 1: Revisión bibliográfica y análisis de requerimientos", "", "", "", ""],
        ["Revisión sistemática de literatura científica (Kitchenham / PRISMA)", "80", "01/12/2026", "12/12/2026", "Autores"],
        ["Levantamiento de requerimientos y digitalización de catálogos", "60", "14/12/2026", "21/12/2026", "Autores / Tutor"],
        ["Fase 2: Diseño de la arquitectura propuesta", "", "", "", ""],
        ["Diseño arquitectónico y modelado relacional SQLite WAL", "80", "22/12/2026", "11/01/2027", "Autores"],
        ["Estructuración de índices y normalización multimarca", "60", "12/01/2027", "25/01/2027", "Autores"],
        ["Fase 3: Desarrollo del prototipo funcional", "", "", "", ""],
        ["Implementación del backend .NET 8, serialización y compuerta", "120", "26/01/2027", "12/02/2027", "Autores"],
        ["Integración con API Gemini y WhatsApp Cloud API", "80", "15/02/2027", "01/03/2027", "Autores"],
        ["Fase 4: Despliegue y pruebas experimentales", "", "", "", ""],
        ["Despliegue en AWS con Nginx TLS y batería de pruebas (N=120)", "120", "02/03/2027", "19/03/2027", "Autores"],
        ["Fase 5: Análisis de resultados y documentación", "", "", "", ""],
        ["Análisis estadístico de telemetría, validación TAM y redacción", "120", "20/03/2027", "05/04/2027", "Autores / Tutor"],
        ["Horas de contingencia técnica y ajustes experimentales", "80", "06/04/2027", "15/04/2027", "Autores"]
    ]
    t3 = doc.add_table(rows=len(t3_data), cols=5)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t3_data):
        for c_idx, val in enumerate(row):
            cell = t3.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0)
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.size = Pt(10)
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"},
                                      bottom={"sz": 6, "val": "single", "color": "000000"})
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                if "Fase" in val and c_idx == 0:
                    cell.paragraphs[0].runs[0].font.bold = True
                    cell.paragraphs[0].runs[0].font.italic = True
                elif r_idx == len(t3_data) - 1:
                    set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "000000"})

    add_note("Distribución del esfuerzo de ingeniería en 720 horas de ejecución técnica y 80 horas de contingencia para imprevistos o ajustes experimentales, completando las 800 horas conjuntas reglamentarias (400 horas por estudiante).")

    # --- SECCIÓN 9: PRESUPUESTO ---
    add_h1("9. Presupuesto")
    add_p("El presupuesto estimado para la ejecución integral del proyecto de titulación considera tanto la valoración formal del esfuerzo de ingeniería de software (mano de obra de los tesistas), como el dimensionamiento técnico de la infraestructura computacional en la nube, conectividad, licencias de consumo y suministros requeridos para el ciclo de vida del software. En la Tabla 4 se expone la valoración económica formal de mercado del proyecto, cuantificada conforme a precios estándar de la industria del software.")

    add_caption_with_seq(doc, "Tabla", 4, "Presupuesto detallado y valoración económica de mercado del proyecto de titulación")
    t4_data = [
        ["Categoría / Rubro", "Descripción y dedicación del recurso", "Valor de mercado (USD)"],
        ["1. Mano de obra de ingeniería y desarrollo (Tesistas)", "", ""],
        ["Victor Jesús Totoy Iza", "Arquitectura backend (.NET 8), webhooks, SQLite y despliegue (400 h a $10.00/h)", "4000.00"],
        ["Rodolfo Damián Seminario Murillo", "Estructuración de catálogos, integración Gemini y evaluación (400 h a $10.00/h)", "4000.00"],
        ["Subtotal Mano de obra de ingeniería", "Valoración económica del esfuerzo conjunto de 800 horas", "8000.00"],
        ["2. Infraestructura tecnológica, servicios y suministros directos", "", ""],
        ["Servidor en la nube (AWS EC2)", "Instancia virtual Linux (t2.micro) durante 6 meses de proyecto", "60.00"],
        ["Nombre de dominio y gestión TLS", "Dominio powerelectrimk.com y gestión de DNS Cloudflare (1 año)", "15.00"],
        ["Consumo de inferencia API Gemini", "Cuota de tokens para pruebas de integración y validación (N=120)", "40.00"],
        ["Línea telefónica comercial", "Tarjeta SIM y recargas para WhatsApp Business API", "25.00"],
        ["Servicio de acceso a Internet", "Conectividad fija de banda ancha durante 6 meses ($30.00/mes)", "180.00"],
        ["Impresión y encuadernación", "Empastado y documentación física institucional de titulación", "70.00"],
        ["Fondo de contingencia", "Margen para imprevistos operativos y pruebas adicionales (10%)", "40.00"],
        ["Valor total estimado de mercado del proyecto", "Suma ponderada de mano de obra y recursos tecnológicos", "8430.00"]
    ]
    t4 = doc.add_table(rows=len(t4_data), cols=3)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t4_data):
        for c_idx, val in enumerate(row):
            cell = t4.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0)
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.size = Pt(10)
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"},
                                      bottom={"sz": 6, "val": "single", "color": "000000"})
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                if "Mano de obra" in val or "Infraestructura" in val:
                    cell.paragraphs[0].runs[0].font.bold = True
                elif r_idx == len(t4_data) - 1:
                    cell.paragraphs[0].runs[0].font.bold = True
                    set_cell_border(cell, top={"sz": 6, "val": "single", "color": "000000"},
                                          bottom={"sz": 12, "val": "single", "color": "000000"})

    add_note("Valores expresados en dólares de los Estados Unidos de América (USD), calculados a tarifas vigentes a noviembre de 2026. La tarifa horaria de 10.00 USD/h se fundamenta en los valores referenciales de mercado para desarrolladores de software junior en Ecuador. Los costos directos de suministros (195.00 USD) y la mano de obra de investigación (8000.00 USD) son asumidos íntegramente por los autores.")

    add_p("Como se expone en la Tabla 4, el valor económico total de mercado del proyecto asciende a 8430.00 USD. De este monto, el 94.9% (8000.00 USD) corresponde a la mano de obra de ingeniería aportada por los tesistas (Victor Jesús Totoy Iza y Rodolfo Damián Seminario Murillo), cuantificada en 800 horas de dedicación conjunta (400 horas individuales exigidas por el reglamento de titulación de la UPS) a una tarifa estandarizada de 10.00 USD por hora, representando la inversión de capital humano inherente a la formación en ingeniería en computación.")

    add_p("Por otra parte, desde la perspectiva operativa y financiera de la puesta en marcha, el proyecto exhibe una ventaja competitiva excepcional gracias al aprovechamiento estratégico de las capas gratuitas (Free Tiers) ofrecidas por los principales proveedores tecnológicos de nube e inteligencia artificial. Durante la etapa de investigación, desarrollo y validación experimental, los costos computacionales de la nube y de la API de inferencia se reducen de forma efectiva a 0.00 USD. En la Tabla 5 se presenta la conciliación financiera detallada entre los costos estimados de mercado, la cobertura por capas gratuitas y el desembolso efectivo real asumido por los tesistas.")

    add_caption_with_seq(doc, "Tabla", 5, "Conciliación financiera y análisis operativo de servicios en la nube: Capa Gratuita vs. Régimen Comercial")
    t5_data = [
        ["Proveedor / Servicio", "Condición de gratuidad / Cobertura en tesis", "Régimen Comercial (Pay-as-you-go)", "Costo efectivo en tesis (USD)"],
        ["Google Gemini API (Google AI Studio)", "Free Tier (hasta 15 RPM, 1M TPM y 1500 solicitudes/día gratuitas para Gemini Flash).", "Entrada: $0.075 / 1M tokens. Salida: $0.30 / 1M tokens (aprox. $2.50/mes por 1000 chats/día).", "0.00"],
        ["Amazon Web Services (AWS EC2 t2.micro)", "AWS Free Tier (750 horas/mes gratuitas durante 12 meses; 30 GB SSD EBS gp3).", "On-Demand: $0.0116/h (aprox. $8.35/mes) + $2.40/mes almacenamiento EBS gp3.", "0.00"],
        ["Meta Cloud API (WhatsApp Business)", "1000 conversaciones de servicio al cliente al mes gratuitas iniciadas por usuario.", "Tarifa variable por categoría de conversación ($0.008 a $0.035 USD/chat tras superar 1000).", "0.00"],
        ["Let's Encrypt / Certbot (Certificado TLS 1.3)", "Certificados SSL/TLS automatizados de renovación continua (100% de gratuidad permanente).", "Certificados comerciales corporativos con validación de organización ($15.00 a $60.00/año).", "0.00"],
        ["Dominio powerelectrimk.com", "Infraestructura preexistente y financiada por la distribuidora Power Electrimk.", "Renovación anual de dominio comercial en registrador acreditado ($15.00/año).", "0.00"],
        ["Suministros físicos y documentación", "No aplica gratuidad (material de oficina, resmas, encuadernación institucional).", "Costo directo de papelería e impresiones de control normativo.", "195.00"],
        ["Desembolso efectivo real de los estudiantes en fase de titulación", "Financiamiento directo exclusivo de suministros no cubiertos por gratuidad", "Total asumido íntegramente por los autores", "195.00"]
    ]
    t5 = doc.add_table(rows=len(t5_data), cols=4)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(t5_data):
        for c_idx, val in enumerate(row):
            cell = t5.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0)
            set_cell_margins(cell, 50, 50, 70, 70)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.size = Pt(10)
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"},
                                      bottom={"sz": 6, "val": "single", "color": "000000"})
            else:
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                if r_idx == len(t5_data) - 1:
                    cell.paragraphs[0].runs[0].font.bold = True
                    set_cell_border(cell, top={"sz": 6, "val": "single", "color": "000000"},
                                          bottom={"sz": 12, "val": "single", "color": "000000"})

    add_note("Datos recopilados de la documentación técnica y tablas de facturación de Google AI Studio, Amazon Web Services Free Tier y Meta for Developers (noviembre 2026). El desembolso efectivo real asumido por los tesistas se limita estrictamente a suministros de oficina e impresiones (195.00 USD), ratificando la plena factibilidad presupuestaria de la investigación.")

    add_p("Este análisis evidencia que la combinación de un motor embebido SQLite (modo WAL sin costo de licenciamiento) con la Capa Gratuita de Google AI Studio y el AWS Free Tier minimiza el riesgo de inversión para la distribuidora Power Electrimk, requiriendo un desembolso directo de únicamente 195.00 USD durante los meses de ejecución del proyecto de titulación. Si la distribuidora decidiera extender la solución a un volumen comercial masivo superando los límites de la capa gratuita, el esquema de cobro por consumo de Gemini Flash garantiza que el costo mensual de inferencia por cada 1 000 cotizaciones atendidas no excederá los 3.00 USD, lo cual consolida la sostenibilidad económica y el retorno de inversión del sistema frente a plataformas propietarias de alto costo recurrente.")

    # --- SECCIÓN 10: REFERENCIAS BIBLIOGRÁFICAS ---
    doc.add_page_break()
    add_h1("10. Referencias bibliográficas")
    referencias = [
        "Adam, M., Wessel, M., & Benlian, A. (2021). AI-based chatbots in customer service and their effects on user compliance. Electronic Markets, 31(2), 427–445. https://doi.org/10.1007/s12525-020-00414-7",
        "Adamopoulou, E., & Moussiades, L. (2020). Chatbots: History, technology, and applications. Machine Learning with Applications, 2, 100006. https://doi.org/10.1016/j.mlwa.2020.100006",
        "Asai, A., Sewon, M., Jiang, Z., Chen, X., Zettlemoyer, L., Yih, W.-T., & Hajishirzi, H. (2024). Self-RAG: Learning to retrieve, generate, and critique through self-reflection. The Twelfth International Conference on Learning Representations (ICLR 2024). https://openreview.net/forum?id=e7ItjTETbW",
        "Ashfaq, M., Yun, J., Yu, S., & Loureiro, S. M. C. (2020). I, Chatbot: Modeling the determinants of users' satisfaction and continuance intention of AI-powered service agents. Telematics and Informatics, 54, 101473. https://doi.org/10.1016/j.tele.2020.101473",
        "Ayala-Carabajo, R., & Llerena-Izquierdo, J. (2026). Comparative Experimental Studies on Superior Cognitive Domains: AI Versus Humans. Technologies, 14(1), 55. https://doi.org/10.3390/technologies14010055",
        "Borgeaud, S., Mensch, A., Hoffmann, J., Cai, T., Rutherford, E., Millican, K., van den Driessche, G., Lespiau, J.-B., Damoc, B., Clark, A., de Las Casas, D., Guy, A., Menick, J., Ring, R., Hennigan, T., Huang, S., Maggiore, L., Jones, C., Cassirer, A., … Sifre, L. (2022). Improving language models by retrieving from trillions of tokens. Proceedings of the 39th International Conference on Machine Learning, 2206–2240. https://proceedings.mlr.press/v162/borgeaud22a.html",
        "Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., & Weston, J. (2023). Chain-of-Verification Reduces Hallucination in Large Language Models. arXiv Preprint arXiv:2309.11495. https://arxiv.org/abs/2309.11495",
        "Følstad, A., Araujo, T., & Brandtzæg, P. B. (2020). What makes users trust a chatbot for customer service? An exploratory study. The 4th International Workshop on Chatbot Research and Design (CONVERSATIONS 2020), 12604, 3–18. https://doi.org/10.1007/978-3-030-68288-0_1",
        "Gaffney, K. (2022). SQLite: Past, Present, and Future. Proceedings of the 2022 International Conference on Management of Data (SIGMOD '22), 2465–2467. https://doi.org/10.1145/3514221.3524075",
        "Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., & Wang, H. (2023). Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv Preprint arXiv:2312.10997. https://doi.org/10.48550/arXiv.2312.10997",
        "Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. Proceedings of the 16th ACM Workshop on Artificial Intelligence and Security (AISEC '23), 79–90. https://doi.org/10.1145/3605764.3623982",
        "Guu, K., Lee, K., Tung, Z., Pasupat, P., & Chang, M.-W. (2020). REALM: Retrieval-Augmented Language Model Pre-Training. Proceedings of the 37th International Conference on Machine Learning (ICML 2020), 119, 3929–3938. https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html",
        "Han, M. C. (2023). The effect of conversational AI chatbot's perceived competence, empathy, and conversational quality on customer satisfaction and purchase intention. Journal of Global Fashion Marketing, 14(4), 391–406. https://doi.org/10.1088/20932685.2023.2209772",
        "Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., & Liu, T. (2023). A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. arXiv Preprint arXiv:2311.05232. https://doi.org/10.48550/arXiv.2311.05232",
        "ISO/IEC. (2011). Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models (Standard ISO/IEC 25010:2011). International Organization for Standardization. https://www.iso.org/standard/35733.html",
        "Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Yan, S., Ishii, E., Bang, Y. J., Madotto, A., & Fung, P. (2023). Survey of Hallucination in Natural Language Generation. ACM Computing Surveys, 55(12), 248:1-248:38. https://doi.org/10.1145/3571730",
        "Kitchenham, B., & Charters, S. (2007). Guidelines for performing Systematic Literature Reviews in Software Engineering (Technical Report EBSE-2007-01). Keele University and Durham University Joint Report.",
        "Kratzke, N., & Quint, P.-C. (2017). Understanding cloud-native applications after 10 years of cloud computing - A systematic mapping study. Journal of Systems and Software, 126, 1–16. https://doi.org/10.1016/j.jss.2017.01.001",
        "Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-T., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 9459–9474. https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html",
        "Llerena-Izquierdo, J., & Ayala-Carabajo, R. (2022). Desarrollo de competencia investigativa de estudiantes universitarios de ingeniería en proceso de titulación: propuesta metodológica y experiencia. Memoria Investigaciones en Ingeniería, 23, 50–62. https://doi.org/10.36561/ING.23.5",
        "Llerena-Izquierdo, J., & Ayala-Carabajo, R. (2025). Guía práctica para redactar y publicar manuscritos científicos. Ediciones Abya-Yala. https://doi.org/10.17163/abyaups.134",
        "Llerena-Izquierdo, J., Fiallos-Vargas, I., Portugal-Gorozabel, J., & Veloz-Arce, A. (2024). Towards an experience in AI-driven development for programming applied to multimedia using Tabnine. 2024 IEEE URUCON, 1–5. https://doi.org/10.1109/URUCON63440.2024.10850207",
        "Llerena-Izquierdo, J., Lindao-Cacao, K., Espinoza-Rosero, Gloria, & Carrera-Jimenez, J. (2026). Towards a Management Model for the Final Year Project in Computer Engineering in the Field of Research. En M. V. Garcia, J.-P. Reyes, C. Nuñez, & C. Gordón-Gallegos (Eds.), Proceedings of the International Conference on Computer Science, Electronics and Industrial Engineering (CSEI 2024) (pp. 37–49). Springer Nature Switzerland. https://doi.org/10.1007/978-3-031-98890-5_3",
        "Llerena-Izquierdo, J., Mendez-Reyes, J., Ayala-Carabajo, R., & Andrade-Martinez, C. (2024). Innovations in Introductory Programming Education: The Role of AI with Google Colab and Gemini. Education Sciences, 14(12), 1330. https://doi.org/10.3390/educsci14121330",
        "Luo, X., Tong, S., Fang, Z., & Qu, Z. (2019). Frontiers: Machines vs. Humans: The Impact of Artificial Intelligence Chatbot Disclosure on Customer Purchases. Marketing Science, 38(6), 937–947. https://doi.org/10.1287/mksc.2019.1192",
        "Newman, S. (2021). Building Microservices: Designing Fine-Grained Systems (2nd ed.). O'Reilly Media.",
        "Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., Shamseer, L., Tetzlaff, J. M., Akl, E. A., Brennan, S. E., Chou, R., Glanville, J., Grimshaw, J. M., Hróbjartsson, A., Lalu, M. M., Li, T., Loder, E. W., Mayo-Wilson, E., McDonald, S., … Moher, D. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ, 372, n71. https://doi.org/10.1136/bmj.n71",
        "Rescorla, E. (2018). The Transport Layer Security (TLS) Protocol Version 1.3 (RFC 8446). Internet Engineering Task Force. https://doi.org/10.17487/RFC8446",
        "Robertson, S., & Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval, 3(4), 333–389. https://doi.org/10.1561/1500000019",
        "Sands, S., Ferraro, C., Campbell, C., & Tsao, H.-Y. (2021). Managing the human-chatbot divide: How the presence of white space influences consumer engagement with conversational agents. Journal of Business Research, 122, 638–647. https://doi.org/10.1016/j.jbusres.2020.09.065",
        "Taibi, D., Lenarduzzi, V., & Pahl, C. (2020). Processes, Motivations, and Issues for Migrating to Microservices Architectures: An Empirical Investigation. IEEE Cloud Computing, 4(5), 22–32. https://doi.org/10.1109/MCC.2017.4250931",
        "Tonmoy, S. M. T. I., Zaman, S. M., Jain, V., Rani, A., Rawte, V., Chadha, A., & Das, A. (2024). A Comprehensive Survey of Hallucination in Large Language Models. arXiv Preprint arXiv:2402.04944. https://doi.org/10.48550/arXiv.2402.04944",
        "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is All you Need. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 5998–6008. https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html",
        "Wang, L., Ma, C., Feng, X., Zhang, Z., Yang, H., Chen, J., Tang, J., Chen, X., Lin, Y., Zhao, W. X., Wei, Z., & Wen, J.-R. (2024). A survey on large language model based autonomous agents. Frontiers of Computer Science, 18(6), 186345. https://doi.org/10.1007/s11704-024-40231-1",
        "Wu, Q., Bansal, G., Zhang, J., Wu, Y., Zhang, S., Erkens, E., Kiciman, E., Wang, H., Liang, Q., & Wang, C. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework. arXiv Preprint arXiv:2308.08155. https://doi.org/10.48550/arXiv.2308.08155",
        "Zerega-Prado, J., & Llerena-Izquierdo, J. (2022). Arquitectura de consolidación de la información para seguros de la salud mediante Big Data. Memoria Investigaciones en Ingeniería, 23, 18–31. https://doi.org/10.36561/ING.23.3"
    ]
    for ref in referencias:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.left_indent = Inches(0.5)
        p_ref.paragraph_format.first_line_indent = Inches(-0.5)
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p_ref.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0, 0, 0)

    # --- SECCIÓN 11: ANEXOS ---
    doc.add_page_break()
    add_h1("11. Anexos")

    add_h2("11.1. Anexo 1: Árbol de problemas y objetivos (Metodología 5W+H)")
    add_p("De acuerdo con la guía metodológica de formulación de proyectos 5W+H de la Universidad Politécnica Salesiana, se presentan en la Figura 2 y la Figura 3 las representaciones causales del problema central y su transformación propositiva hacia los medios y fines de la solución técnica.")

    add_caption_with_seq(doc, "Figura", 2, "Árbol de problemas de la atención comercial en distribuidoras eléctricas")
    fig2_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'figura2_clean.png')
    if not os.path.exists(fig2_path):
        fig2_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'crop_figura2.png')
    if os.path.exists(fig2_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.add_run().add_picture(fig2_path, width=Inches(6.0))
    add_note("Estructura causal del problema identificada a través de la metodología 5W+H en la distribuidora Power Electrimk.")

    add_caption_with_seq(doc, "Figura", 3, "Árbol de objetivos de la solución de ingeniería de software")
    fig3_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'figura3_clean.png')
    if not os.path.exists(fig3_path):
        fig3_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'crop_figura3.png')
    if os.path.exists(fig3_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.add_run().add_picture(fig3_path, width=Inches(6.0))
    add_note("Transformación de medios y fines orientada a la ingeniería de software y la validación experimental.")

    # =========================================================================
    # SECCIÓN 3: ANEXO 2 EN FORMATO HORIZONTAL (LANDSCAPE)
    # =========================================================================
    sec_matrix = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_matrix.orientation = WD_ORIENT.LANDSCAPE
    sec_matrix.page_width = Inches(11.0)
    sec_matrix.page_height = Inches(8.5)
    sec_matrix.top_margin = Inches(0.8)
    sec_matrix.bottom_margin = Inches(0.8)
    sec_matrix.left_margin = Inches(0.8)
    sec_matrix.right_margin = Inches(0.8)
    add_header_page_number(sec_matrix, fmt="decimal")

    add_h2("11.2. Anexo 2: Matriz de consistencia metodológica de la investigación (UPS P69)")
    add_p("En la Tabla 6 se detalla la Matriz de Consistencia Metodológica elaborada bajo el formato normativo institucional UPS P69, evidenciando la coherencia entre problemas, objetivos, hipótesis, variables e indicadores.")

    add_caption_with_seq(doc, "Tabla", 6, "Matriz de consistencia metodológica de la investigación (Formato Institucional UPS P69)")
    t6 = doc.add_table(rows=5, cols=6)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    t6_headers = ["Problema", "Objetivos", "Hipótesis", "Variables y Dimensiones", "Indicadores Prioritarios", "Técnicas e Instrumentos"]
    for i, h in enumerate(t6_headers):
        cell = t6.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0)
        set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"},
                              bottom={"sz": 6, "val": "single", "color": "000000"})
        set_cell_margins(cell, 40, 40, 50, 50)

    t6_rows = [
        [
            "Problema General (PG):\n¿En qué medida un agente inteligente con recuperación verificable de información técnica multimarca, basado en modelos generativos y recuperación relacional determinista sobre SQLite WAL, mejora la exactitud de precios, mitiga las alucinaciones y optimiza la latencia P95 en Power Electrimk?",
            "Objetivo General (OG):\nDesarrollar un agente inteligente con recuperación verificable de información técnica para la atención comercial y cotización en Power Electrimk, mediante modelos generativos y recuperación relacional determinista sobre catálogos estructurados.",
            "Hipótesis General (HG):\nEl agente con recuperación local sobre SQLite permite alcanzar Acc_cot >= 95%, mitigación de alucinaciones en cotizaciones (H_rate <= 2%), latencia en P95 T_resp < 4.0 s y consumo de RAM < 250 MB en la nube, validado sobre N=120 casos.",
            "Variable Independiente (VI):\nModalidad de interacción conversacional con recuperación determinista local sobre catálogo estructurado y compuerta financiera en backend.",
            "- Exactitud cotización (Acc_cot >= 95%)\n- Tasa alucinación (H_rate <= 2%)\n- Latencia P95 (T_resp < 4.0 s)\n- Consumo RAM (< 250 MB)\n- Aceptación asesores (TAM >= 4.0/5.0)",
            "Técnicas:\n- Telemetría automatizada en AWS.\n- Pruebas sintéticas de carga.\n- Evaluación de usabilidad TAM.\nInstrumentos:\n- Scripts k6 / wrk.\n- Logs estructurados.\n- Cuestionario estandarizado TAM."
        ],
        [
            "Sistematización P1:\n¿Cuáles son los requerimientos técnicos y comerciales, y qué estructura relacional multimarca y control de vigencia se requiere en Power Electrimk?",
            "Objetivo Específico 1 (O1):\nAnalizar los requerimientos operativos de cotización, la estructura de catálogos multimarca y la gestión de vigencia de productos en Power Electrimk, fijando especificaciones de diseño.",
            "Hipótesis Específica 1 (H1):\nLa normalización relacional y el control de vigencia en SQLite permiten resolver consultas de inventario en T_sql < 100 ms con 100% de integridad en datos vigentes.",
            "Variable Dependiente 1 (VD1):\nDimensión Estructura e Integridad de Catálogo:\nConsistencia y celeridad de consulta de inventario técnico y control de obsolescencia.",
            "- Tiempo ejecución SQL (T_sql < 100 ms)\n- Tasa de recuperación SKU (100%)\n- Integridad atributos (código, precio, marca)\n- Detección productos descontinuados",
            "Técnicas:\n- Revisión bibliográfica.\n- Entrevistas comerciales.\nInstrumentos:\n- Guía de entrevista semiestructurada.\n- Matriz de extracción y vigencia."
        ],
        [
            "Sistematización P2:\n¿Cómo diseñar una arquitectura ligera en .NET 8 que integre WhatsApp, Gemini y SQLite preservando la memoria conversacional y mitigando la contención de escritura?",
            "Objetivo Específico 2 (O2):\nImplementar un prototipo de microservicio en .NET 8 con persistencia SQLite WAL, serialización asíncrona de escrituras, verificación HMAC-SHA256, deduplicación y WhatsApp Cloud API.",
            "Hipótesis Específica 2 (H2):\nLa arquitectura asíncrona en .NET 8 con cola de serialización procesa webhooks concurrentes sin bloqueos de contención y con memoria de proceso < 250 MB.",
            "Variable Dependiente 2 (VD2):\nDimensión Eficiencia de Recursos:\nHuella computacional, seguridad de webhooks y concurrencia del servicio backend.",
            "- Utilización memoria RAM (< 250 MB)\n- Concurrencia de sesiones\n- Ocupación CPU AWS (< 30%)\n- Cero bloqueos (SQLITE_BUSY)",
            "Técnicas:\n- Inspección y perfilado de memoria.\n- Monitoreo runtime en Kestrel.\nInstrumentos:\n- dotnet-counters y dotnet-dump.\n- Métricas CloudWatch en AWS."
        ],
        [
            "Sistematización P3:\n¿En qué medida la recuperación determinista mitiga la alucinación, mejora la exactitud y reduce la latencia P95 frente al modelo sin RAG en pruebas adversariales y con usuarios?",
            "Objetivo Específico 3 (O3):\nEvaluar el prototipo mediante pruebas experimentales comparativas (N=120) y validación funcional con asesores comerciales de Power Electrimk.",
            "Hipótesis Específica 3 (H3):\nEl agente con recuperación local y compuerta en backend logra H_rate <= 2%, Acc_cot >= 95% y T_resp, P95 < 4.0 s con significancia (p < 0,05), obteniendo alta aceptación funcional en el equipo de ventas.",
            "Variable Dependiente 3 (VD3):\nDimensión Exactitud Fáctica y Rendimiento:\nCerteza técnica, inmutabilidad de precios y celeridad de respuesta de cotización.",
            "- Exactitud cotización (Acc_cot >= 95%)\n- Tasa alucinación fáctica (H_rate <= 2%)\n- Latencia P95 (T_resp, P95 < 4.0 s)\n- Valor p significancia (p < 0,05)\n- Puntuación usabilidad TAM (>= 4.0/5.0)",
            "Técnicas:\n- Ensayo experimental controlado.\n- Prueba t-Student / Wilcoxon.\n- Validación funcional con usuarios.\nInstrumentos:\n- Batería N=120 casos (6 cuadrantes).\n- Matriz de cotejo de precios.\n- Cuestionario TAM."
        ]
    ]
    for r_idx, row in enumerate(t6_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = t6.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0, 0, 0)
            set_cell_margins(cell, 30, 30, 40, 40)
            if r_idx == 4:
                set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "000000"})

    add_note("Matriz adaptada de la plantilla oficial de consistencia de la investigación UPS Sede Guayaquil (P69).")

    # =========================================================================
    # SECCIÓN 4: ANEXOS 3 Y 4 EN FORMATO VERTICAL (PORTRAIT)
    # =========================================================================
    sec_annex_portrait = doc.add_section(WD_SECTION.NEW_PAGE)
    sec_annex_portrait.orientation = WD_ORIENT.PORTRAIT
    sec_annex_portrait.page_width = Inches(8.5)
    sec_annex_portrait.page_height = Inches(11.0)
    sec_annex_portrait.top_margin = Inches(1.0)
    sec_annex_portrait.bottom_margin = Inches(1.0)
    sec_annex_portrait.left_margin = Inches(1.0)
    sec_annex_portrait.right_margin = Inches(1.0)
    add_header_page_number(sec_annex_portrait, fmt="decimal")

    add_h2("11.3. Anexo 3: Diagrama de arquitectura de software y flujo de procesamiento")
    add_p("En la Figura 4 se ilustra la arquitectura de componentes y el flujo secuencial de procesamiento de mensajes del agente inteligente, detallando la interacción entre los servicios externos de mensajería e inferencia y la infraestructura de cómputo local en la nube. La arquitectura incorpora cuatro salvaguardas críticas de ingeniería de software:")
    add_bullet("Middleware en .NET 8 que valida la firma X-Hub-Signature-256 mediante HMAC-SHA256 antes de enrutar el payload, y verifica el identificador único del mensaje (wamid) contra una tabla de deduplicación en SQLite con caché en memoria (TTL de 5 minutos) para descartar reintentos duplicados de WhatsApp.", bold_prefix="Autenticación criptográfica e idempotencia: ")
    add_bullet("Canal asíncrono en memoria (Channel<T>) con semáforo de exclusión mutua (SemaphoreSlim) para serializar todas las transacciones de escritura (persistencia de sesión y trazas), garantizando cero excepciones de contención (SQLITE_BUSY) ante ráfagas concurrentes.", bold_prefix="Mitigación de contención en SQLite (Single-Writer): ")
    add_bullet("El modelo generativo actúa estrictamente como extractor semántico de requerimientos; los cálculos de precios unitarios, descuentos comerciales y del IVA al 15% son ejecutados exclusivamente por código determinista en C#, inyectando una cotización inmutable que el LLM no puede alterar.", bold_prefix="Compuerta determinista de cálculo financiero: ")
    add_bullet("Procesamiento en memoria RAM de documentos de requerimientos (.xlsx, .csv, .pdf) con neutralización de inyección de fórmulas y prevención de entidades externas XML (XXE).", bold_prefix="Inspección segura en memoria (Zero Disk): ")

    add_caption_with_seq(doc, "Figura", 4, "Arquitectura integral del agente inteligente para la atención comercial con recuperación local de catálogos")
    fig4_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'figura4_clean.png')
    if not os.path.exists(fig4_path):
        fig4_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'crop_figura4_updated.png')
    if not os.path.exists(fig4_path):
        fig4_path = os.path.join(base_dir, 'Docs', 'images', 'extracted', 'crop_figura4.png')
    if os.path.exists(fig4_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.add_run().add_picture(fig4_path, width=Inches(6.2))
    add_note("Diagrama arquitectónico del flujo de ejecución desacoplado entre el webhook de mensajería, el backend en .NET 8, el almacenamiento local embebido y el servicio de inferencia en la nube.")

    add_h2("11.4. Anexo 4: Repositorio de código abierto y transparencia de datos (ABET IV.3)")
    add_p("En estricto cumplimiento con el criterio de evaluación ABET IV.3 (Ética, Impacto y Reproducibilidad en Ingeniería), se formaliza el compromiso de acceso abierto a los artefactos de investigación:")
    add_bullet("Todo el código fuente del microservicio backend, los scripts de migración y estructuración de catálogos y las herramientas de benchmarking automatizado serán gestionados y publicados en el repositorio institucional público de GitHub: https://github.com/vtotoy/agente-ventas-power", bold_prefix="1. Repositorio de código fuente: ")
    add_bullet("El software se distribuye bajo los términos de la licencia de código abierto MIT License, permitiendo la auditoría por pares, su reutilización académica y la transferencia tecnológica sin fines de lucro hacia otras micro y pequeñas empresas ecuatorianas.", bold_prefix="2. Licenciamiento de software: ")
    add_bullet("Los conjuntos de datos de prueba, trazas de telemetría y transcripciones experimentales publicadas en el repositorio se someterán a un protocolo riguroso de anonimización irreversible. Los números telefónicos y nombres de personas naturales son sustituidos por identificadores sintéticos disociados (UUIDs), garantizando el pleno acatamiento de la Ley Orgánica de Protección de Datos Personales del Ecuador.", bold_prefix="3. Gobernanza y anonimización de datos (LOPDP): ")
    add_bullet("El repositorio incluye las directrices técnicas, el archivo Dockerfile de compilación multicapa y los procedimientos documentados paso a paso para desplegar el entorno de evaluación sobre cualquier distribución Linux con el runtime de .NET 8 y SQLite preinstalados.", bold_prefix="4. Guía de reproducibilidad computacional: ")

    # =========================================================================
    # POST-PROCESAMIENTO GLOBAL APA 7: ENFORCEMENT ESTRICTO DE FUENTES
    # Recorre TODOS los párrafos, tablas, celdas y encabezados para garantizar
    # que el 100% de los runs tengan 'Times New Roman' en XML w:rFonts y color #000000.
    # =========================================================================
    for p in doc.paragraphs:
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.color.rgb = RGBColor(0, 0, 0)
            set_run_font_xml(r, 'Times New Roman')

    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.name = 'Times New Roman'
                        r.font.color.rgb = RGBColor(0, 0, 0)
                        set_run_font_xml(r, 'Times New Roman')

    for s in doc.sections:
        for h_p in s.header.paragraphs:
            for r in h_p.runs:
                r.font.name = 'Times New Roman'
                r.font.color.rgb = RGBColor(0, 0, 0)
                set_run_font_xml(r, 'Times New Roman')
        for f_p in s.footer.paragraphs:
            for r in f_p.runs:
                r.font.name = 'Times New Roman'
                r.font.color.rgb = RGBColor(0, 0, 0)
                set_run_font_xml(r, 'Times New Roman')

    for path in output_paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        doc.save(path)
        print(f"Document successfully saved to: {path}")

if __name__ == "__main__":
    base = r"c:\Users\lenovo\Desktop\AgenteVentasPower"
    paths = [
        os.path.join(base, "Docs", "Word", "Anteproyecto_PowerElectrimk.docx"),
    ]
    create_anteproyecto_word(paths)
