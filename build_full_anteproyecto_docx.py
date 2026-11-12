import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def create_anteproyecto_docx(output_path):
    doc = Document()

    # --- Configuración de Márgenes (APA 7: 2.54 cm / 1 pulgada) ---
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)

    # --- Estilo Base Normal ---
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(30, 30, 30)

    # --- Funciones Auxiliares ---
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
                element.set(qn('w:color'), edge_data.get('color', 'auto'))
                tcBorders.append(element)
        tcPr.append(tcBorders)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 51, 102)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = RGBColor(60, 60, 60)
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
            rb.font.size = Pt(11)
            rb.font.bold = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.5)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(11)
            rb.font.bold = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        return p

    def add_caption(fig_table_label, title_text):
        p1 = doc.add_paragraph()
        p1.paragraph_format.space_before = Pt(12)
        p1.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.line_spacing = 1.0
        p1.paragraph_format.keep_with_next = True
        r1 = p1.add_run(fig_table_label)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10)
        r1.font.bold = True

        p2 = doc.add_paragraph()
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(6)
        p2.paragraph_format.line_spacing = 1.0
        p2.paragraph_format.keep_with_next = True
        r2 = p2.add_run(title_text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        r2.font.italic = True

    def add_note(note_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run("Nota. ")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(9.5)
        r1.font.italic = True
        r2 = p.add_run(note_text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(9.5)

    # =========================================================================
    # CARÁTULA OFICIAL
    # =========================================================================
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo_path = r'C:\Users\lenovo\Desktop\AgenteVentasPower\Docs\images\Logo_UPS.png'
    if os.path.exists(logo_path):
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.8))

    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_univ.paragraph_format.space_before = Pt(12)
    p_univ.paragraph_format.space_after = Pt(2)
    r = p_univ.add_run("UNIVERSIDAD POLITÉCNICA SALESIANA")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 51, 102)

    p_sede = doc.add_paragraph()
    p_sede.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sede.paragraph_format.space_after = Pt(18)
    r = p_sede.add_run("SEDE GUAYAQUIL")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    p_carrera = doc.add_paragraph()
    p_carrera.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_carrera.paragraph_format.space_after = Pt(18)
    r = p_carrera.add_run("CARRERA DE COMPUTACIÓN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    p_anteproy = doc.add_paragraph()
    p_anteproy.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_anteproy.paragraph_format.space_after = Pt(4)
    r = p_anteproy.add_run("ANTEPROYECTO DE TITULACIÓN")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    p_previo = doc.add_paragraph()
    p_previo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_previo.paragraph_format.space_after = Pt(24)
    r = p_previo.add_run("Previo a la obtención del título de Ingeniero en Ciencias de la Computación")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.italic = True

    p_lbl_tema = doc.add_paragraph()
    p_lbl_tema.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lbl_tema.paragraph_format.space_after = Pt(4)
    r = p_lbl_tema.add_run("TÍTULO")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.bold = True

    p_tema = doc.add_paragraph()
    p_tema.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tema.paragraph_format.space_after = Pt(26)
    r = p_tema.add_run("Desarrollo de un agente inteligente para la atención comercial y cotización de materiales eléctricos en Guayaquil")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_lbl_aut = doc.add_paragraph()
    p_lbl_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lbl_aut.paragraph_format.space_after = Pt(4)
    r = p_lbl_aut.add_run("AUTORES")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.bold = True

    p_aut = doc.add_paragraph()
    p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aut.paragraph_format.space_after = Pt(24)
    r1 = p_aut.add_run("Victor Jesus Totoy Iza\nRodolfo Damián Seminario Murillo")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11.5)
    r1.font.bold = True

    p_lbl_tut = doc.add_paragraph()
    p_lbl_tut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lbl_tut.paragraph_format.space_after = Pt(4)
    r = p_lbl_tut.add_run("TUTOR")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)
    r.font.bold = True

    p_tut = doc.add_paragraph()
    p_tut.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tut.paragraph_format.space_after = Pt(30)
    r = p_tut.add_run("Ing. Joe Llerena Izquierdo, M.Sc., Ph.D.")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)
    r.font.bold = True

    p_fecha = doc.add_paragraph()
    p_fecha.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_fecha.add_run("Guayaquil, noviembre del 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # ÍNDICE GENERAL (TABLA DE CONTENIDOS)
    # =========================================================================
    add_h1("Índice General")
    indices = [
        ("1. Tema del Trabajo de Titulación", "3"),
        ("2. Antecedentes", "3"),
        ("3. Justificación", "5"),
        ("4. Objetivos", "7"),
        ("    4.1. Objetivo General", "7"),
        ("    4.2. Objetivos Específicos", "7"),
        ("5. Marco hipotético o preguntas de investigación", "8"),
        ("    5.1. Preguntas de investigación", "8"),
        ("    5.2. Hipótesis de investigación", "8"),
        ("6. Marco teórico referencial", "9"),
        ("    6.1. Agentes conversacionales en la atención comercial", "9"),
        ("    6.2. Modelos generativos de lenguaje extenso y arquitectura de agentes", "10"),
        ("    6.3. Recuperación aumentada, bases de datos embebidas y estándares de ingeniería", "11"),
        ("7. Metodología / Propuesta de desarrollo", "12"),
        ("8. Cronograma de actividades", "15"),
        ("9. Proyectos de investigación vinculados", "17"),
        ("10. Presupuesto del Proyecto de Titulación", "18"),
        ("11. Referencias bibliográficas", "21"),
        ("12. Anexos", "25"),
        ("    12.1. Anexo 1: Árbol de problemas y objetivos (Metodología 5W+H)", "25"),
        ("    12.2. Anexo 2: Matriz de consistencia metodológica de la investigación (UPS P69)", "27"),
        ("    12.3. Anexo 3: Diagrama de arquitectura de software y flujo de procesamiento", "29"),
        ("    12.4. Anexo 4: Repositorio de código abierto y transparencia de datos (ABET IV.3)", "30")
    ]
    for item, page in indices:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(item)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        # Tab dots
        dots = " ." * int((65 - len(item)) / 2)
        r_dots = p.add_run(dots + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(9)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)
        r2 = p.add_run(page)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10.5)
        r2.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # SECCIÓN 1: TEMA
    # =========================================================================
    add_h1("1. Tema del Trabajo de Titulación")
    add_p("Desarrollo de un agente inteligente para la atención comercial y cotización de materiales eléctricos en Guayaquil", indent=False)

    # =========================================================================
    # SECCIÓN 2: ANTECEDENTES
    # =========================================================================
    add_h1("2. Antecedentes")
    add_p("Actualmente, el comercio conversacional a través de plataformas de mensajería instantánea constituye el canal preponderante de captación y venta técnica para las pequeñas y medianas empresas comerciales (Adamopoulou & Moussiades, 2020; Adam et al., 2021; Følstad et al., 2020; Luo et al., 2019). En el sector de la distribución de materiales eléctricos e ingeniería en la ciudad de Guayaquil, contratistas independientes, técnicos electricistas y empresas constructoras demandan cotizaciones inmediatas y continuas que involucran especificaciones rigurosas de marcas líderes como Schneider Electric, Siemens, Legrand, Centelsa y ABB. No obstante, este proceso se gestiona tradicionalmente de forma manual mediante asesores de mostrador que deben consultar dispersos catálogos en formato PDF y extensas hojas de cálculo de precios. Esta modalidad ocasiona tiempos de espera para el cliente que oscilan entre 2 y 8 horas hábiles, lo cual provoca una pérdida directa de oportunidades comerciales estimada entre el 20% y el 35% de las solicitudes recibidas, dado que los compradores migran rápidamente hacia competidores con mayor celeridad de respuesta. De no implementarse mecanismos tecnológicos que sistematicen la atención, las distribuidoras enfrentan un incremento sostenido de sus costos operativos y el deterioro gradual de la fidelización de sus clientes (Llerena-Izquierdo & Ayala-Carabajo, 2022; Llerena-Izquierdo & Ayala-Carabajo, 2025).")

    add_p("Diversas investigaciones previas abordaron la automatización del servicio al cliente mediante sistemas conversacionales computacionales. Adamopoulou y Moussiades (2020) documentaron la evolución histórica de los agentes conversacionales, demostrando que las arquitecturas iniciales basadas en árboles de decisión y expresiones regulares presentan una rigidez severa ante la variabilidad del lenguaje natural no contemplado en su diseño. Adam et al. (2021) y Sands et al. (2021) evidenciaron que la incorporación de señales de interacción antropomórfica y presencia social en asistentes virtuales incrementa la tasa de adopción y cumplimiento de los usuarios, mientras que Ashfaq et al. (2020) y Han (2023) modelaron los determinantes de satisfacción e intención de compra en entornos de comercio electrónico conversacional. Con la introducción de la arquitectura Transformer por Vaswani et al. (2017), los Modelos de Lenguaje Extenso (LLM) transformaron el procesamiento del lenguaje; consecuentemente, Wang et al. (2024) sistematizaron su aplicación en agentes autónomos capaces de inferir intenciones complejas y orquestar herramientas. Sin embargo, Ji et al. (2023) y Huang et al. (2023) demostraron que los modelos generativos producen alucinaciones probabilísticas al responder sobre datos no presentes en su entrenamiento, lo que resulta crítico en transacciones comerciales al alterar precios o inventarios. Para mitigar esta debilidad, Guu et al. (2020) y Lewis et al. (2020) formularon los fundamentos de la Generación Aumentada por Recuperación (RAG), mientras que Borgeaud et al. (2022) y Gao et al. (2023) profundizaron en modelos de recuperación densa sobre corpus masivos. Asimismo, mientras que Wu et al. (2023) plantearon esquemas multiagente que requieren clústeres de servidores y múltiples llamadas secuenciales a los modelos, y Asai et al. (2024) propusieron marcos de auto-reflexión computacionalmente densos, Llerena-Izquierdo et al. (2024) y Llerena-Izquierdo, Fiallos-Vargas, et al. (2024) validaron en el entorno local la factibilidad y eficacia de emplear modelos fundacionales modernos de alta velocidad (Gemini) en procesos aplicados.")

    add_p("A pesar de los aportes documentados, la literatura científica evidencia una brecha tecnológica sustancial en el despliegue de agentes inteligentes en entornos de recursos computacionales restringidos para empresas comerciales. Los sistemas RAG convencionales dependen de bases de datos vectoriales y modelos de incrustación de alta demanda de memoria RAM y GPU, lo que imposibilita su alojamiento en servidores de entrada en la nube de bajo costo (instancias con 1 GB de RAM). De igual forma, las arquitecturas multiagente incrementan la latencia a más de diez segundos por interacción, excediendo los límites estrictos de los webhooks de Meta y afectando la experiencia del usuario. No se ha evidenciado un modelo que resuelva la recuperación estructurada sobre catálogos técnicos multimarca donde la búsqueda precisa por atributos deterministas (código de fábrica, amperaje, calibre y marca) garantice cero alucinaciones de precios y conserve la memoria contextual de cada cliente en un único microservicio ligero.")

    add_p("Para resolver esta brecha, el presente proyecto técnico desarrollará un agente inteligente para la atención comercial y cotización de materiales eléctricos que integrará un modelo generativo multimodal con un mecanismo de recuperación local de catálogos estructurados sobre una base de datos embebida SQLite con registro en modo Write-Ahead Logging (Gaffney, 2022). El agente operará como un servicio web asíncrono en .NET 8 conectado a la API oficial de WhatsApp Cloud y al modelo fundacional Gemini, tomando como escenario experimental a la distribuidora Power Electrimk de la ciudad de Guayaquil. Siguiendo la línea de investigación de Ayala-Carabajo y Llerena-Izquierdo (2026) sobre dominios cognitivos y sistemas inteligentes, la propuesta automatiza el embudo de ventas técnicas anclando deterministamente cada consulta a registros verificables de catálogo, garantizando precios exactos, latencia de respuesta sub-cuatro segundos, trazabilidad del cliente y derivación asistida hacia asesores comerciales humanos con costos de infraestructura mínimos. En la Tabla 1 se presenta el análisis comparativo del estado del arte.")

    # Tabla 1: Trabajos previos
    add_caption("Tabla 1", "Comparativa de trabajos previos en sistemas conversacionales para comercio técnico")
    table1 = doc.add_table(rows=6, cols=4)
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Autor", "Técnica base", "Ventajas identificadas", "Limitaciones operativas"]
    for i, h in enumerate(headers):
        cell = table1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_border(cell, top={"sz": 12, "val": "single", "color": "003366"},
                              bottom={"sz": 8, "val": "single", "color": "003366"})
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
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            set_cell_margins(cell, 60, 60, 100, 100)
            if r_idx == len(rows_data_1):
                set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "003366"})

    add_note("Elaboración propia a partir de la revisión sistemática de literatura sobre arquitecturas conversacionales.")

    # =========================================================================
    # SECCIÓN 3: JUSTIFICACIÓN
    # =========================================================================
    add_h1("3. Justificación")
    add_p("La presente investigación se justifica por la imperiosa necesidad de transformar el proceso operativo de cotización y asesoramiento técnico de materiales eléctricos en las distribuidoras comerciales que gestionan sus ventas a través de mensajería instantánea. En el mercado ecuatoriano de suministros eléctricos, la inmediatez y la certeza técnica determinan el cierre comercial; no obstante, el personal de ventas invierte una fracción considerable de su jornada laboral consultando hojas de cálculo, archivos PDF desactualizados y listas impresas para responder preguntas repetitivas sobre marcas, calibres, amperajes y precios. La incorporación de un agente inteligente de ventas comerciales capaz de guiar al cliente en el embudo técnico, interpretar requerimientos conversacionales y emitir cotizaciones fácticas en tiempo real con datos verificables confiere una ventaja competitiva directa y mitiga el riesgo de pérdida de clientes por demoras en la atención.")

    add_p("Desde una perspectiva técnica y científica, la integración de un modelo de lenguaje generativo con una capa de recuperación local estructurada resuelve de manera determinante el fenómeno de las alucinaciones probabilísticas y la inconsistencia fáctica en modelos fundacionales (Ji et al., 2023; Huang et al., 2023; Tonmoy et al., 2024; Lewis et al., 2020). En el campo de los suministros eléctricos, las alucinaciones no constituyen meros descuidos estilísticos; la invención de un calibre de conductor indebido, la alteración de la curva de disparo de un disyuntor termomagnético o la cita de un precio desactualizado acarrean riesgos severos de sobrecarga eléctrica, cortocircuito, siniestros materiales o pérdidas financieras. Si bien los modelos fundacionales como Gemini poseen una alta capacidad de comprensión sintáctica y semántica en lenguaje natural, carecen de acceso autónomo a inventarios específicos y dinámicos. El empleo del motor relacional embebido SQLite con registro de escritura anticipada (WAL) permite realizar consultas deterministas de alta velocidad directamente en el espacio de memoria del proceso, inyectando los datos fácticos verificados (ground truth) dentro del contexto de inferencia. Esto erradica las discrepancias de catálogo y evita el despliegue de bases de datos vectoriales pesadas que demandan hardware costoso (Gaffney, 2022). Asimismo, la implementación del servicio en .NET 8 con patrones asíncronos bajo el paradigma de microservicios ligeros orientados a la nube garantiza la capacidad de atender múltiples sesiones simultáneas bajo consumo mínimo de memoria, en concordancia con los principios de desarrollo cloud-native y software asistido por inteligencia artificial promovidos en la disciplina (Kratzke & Quint, 2017; Newman, 2021; Taibi et al., 2020; Llerena-Izquierdo, Fiallos-Vargas, et al., 2024).")

    add_p("En el ámbito social, productivo y de política pública, el proyecto se alinea de forma explícita con los objetivos del Plan Nacional de Desarrollo de la República del Ecuador, en sus ejes orientados a la transformación digital, la modernización de los encadenamientos productivos y el fortalecimiento de la competitividad de las micro, pequeñas y medianas empresas (MIPYMES). La distribuidora Power Electrimk, ubicada en la ciudad de Guayaquil, se beneficiará de una operatividad continua 24/7, canalizando prospectos calificados hacia sus ejecutivos de venta. Al mismo tiempo, los maestros eléctricos, contratistas y usuarios finales obtendrán especificaciones técnicas normalizadas y precios referenciales transparentes sin barreras geográficas ni demoras de atención.")

    add_p("En conformidad con los criterios de diseño en ingeniería (Criterio ABET 1), la solución se encuentra sujeta a cuatro restricciones formales de diseño:")
    add_bullet("El tiempo total de procesamiento y respuesta de extremo a extremo no deberá superar los 4.0 segundos por interacción, garantizando una experiencia fluida y evitando cancelaciones o reintentos en los webhooks de WhatsApp Cloud API.", bold_prefix="1. Restricción de latencia operativa: ")
    add_bullet("El sistema deberá operar de manera estable en una instancia de entrada en la nube de bajos recursos (computación contenida a 1 vCPU y 1 GB de memoria RAM, equivalente a AWS EC2 t2.micro), manteniendo los costos operativos de infraestructura por debajo de 15.00 USD mensuales.", bold_prefix="2. Restricción de hardware y costo de infraestructura: ")
    add_bullet("El manejo de identificadores de usuario, números telefónicos y registros de conversaciones deberá cumplir estrictamente con los mandatos de la Ley Orgánica de Protección de Datos Personales (LOPDP) de la República del Ecuador, empleando transporte seguro bajo TLS 1.3 y disociación de datos de contacto mediante identificadores sintéticos disociados (UUIDs).", bold_prefix="3. Restricción de cumplimiento normativo y privacidad: ")
    add_bullet("Se impone una tolerancia de error nula (0%), supeditando cualquier emisión de cotización a la coincidencia determinista con los registros oficiales de la base de datos local.", bold_prefix="4. Restricción de exactitud e integridad de catálogo: ")

    add_p("El alcance del proyecto de titulación comprende la recopilación y estructuración de los catálogos multimarca de la distribuidora, el diseño del esquema relacional local, el desarrollo del servicio backend en .NET 8 con integración a WhatsApp Cloud API y al modelo generativo Gemini, el despliegue productivo en una instancia Linux de AWS con proxy inverso Nginx y certificados TLS, y la evaluación experimental cuantitativa de latencia, exactitud y consumo de recursos. Se delimita la solución a la asesoría técnica de compatibilidad, emisión de cotizaciones referenciales formales y captura estructurada de prospectos. Asimismo, la arquitectura de software se diseña de manera modular y extensible bajo principios SOLID, sentando las bases contractuales para una segunda fase tecnológica post-titulación que incorporará reconocimiento multimodal de piezas por imágenes fotográficas con Gemini Flash Vision, seguimiento comercial automatizado (follow-up), derivación asistida a asesores humanos mediante el patrón State y sincronización bidireccional con sistemas CRM. Quedan explícitamente excluidos del alcance del anteproyecto la recaudación de pagos directos mediante pasarelas financieras, la emisión de facturación electrónica reglamentada por el SRI y la conexión nativa con sistemas ERP legados, salvaguardando la viabilidad de ejecución dentro del límite de 400 horas académicas.")

    # =========================================================================
    # SECCIÓN 4: OBJETIVOS
    # =========================================================================
    add_h1("4. Objetivos")
    add_h2("4.1. Objetivo General")
    add_p("Desarrollar un agente inteligente para la atención comercial y cotización de materiales eléctricos en Guayaquil, mediante la integración de modelos generativos y recuperación relacional determinista sobre catálogos técnicos para garantizar cotizaciones fácticas en la distribuidora Power Electrimk.", indent=False)

    add_h2("4.2. Objetivos Específicos")
    add_p("De conformidad con los niveles taxonómicos de Bloom y las directrices metodológicas de titulación en ingeniería computacional de la Universidad Politécnica Salesiana, se establecen los siguientes objetivos específicos:", indent=False)
    add_bullet("los requerimientos operativos de atención comercial y la estructura de los catálogos técnicos multimarca en la distribuidora Power Electrimk, determinando los atributos esenciales de inventario y las especificaciones de ingeniería requeridas para el agente de ventas.", bold_prefix="• Analizar ")
    add_bullet("un prototipo de software en arquitectura ligera sobre .NET 8 que integre de forma desacoplada la API oficial de WhatsApp Cloud, el modelo fundacional Gemini y un motor de base de datos embebido SQLite con registro en modo Write-Ahead Logging para consultas deterministas y persistencia de memoria de sesión comercial.", bold_prefix="• Implementar ")
    add_bullet("el desempeño computacional y la efectividad operativa del prototipo mediante pruebas experimentales controladas que contrasten el agente con recuperación local frente al modelo sin recuperación, cuantificando la exactitud de precios y referencias técnicas, la tasa de mitigación de alucinaciones, la latencia en percentil P95 y el consumo de recursos en la nube.", bold_prefix="• Evaluar ")

    # =========================================================================
    # SECCIÓN 5: PREGUNTAS E HIPÓTESIS
    # =========================================================================
    add_h1("5. Marco hipotético o preguntas de investigación")
    add_p("En concordancia con la matriz metodológica institucional UPS P69 y los objetivos específicos planteados, se formulan las preguntas de sistematización del problema y las correspondientes hipótesis de ingeniería que guiarán la investigación experimental.")

    add_h2("5.1. Preguntas de investigación")
    add_p("¿En qué medida un agente inteligente para la atención comercial y cotización de materiales eléctricos en Guayaquil, basado en modelos generativos y recuperación relacional determinista, mejora la exactitud de precios, la latencia de respuesta y la eficiencia de recursos computacionales en el proceso de ventas de la distribuidora Power Electrimk?", bold_prefix="Pregunta General (PG). ", indent=False)
    add_p("¿Cuáles son los requerimientos comerciales y qué estructura de normalización de datos en catálogos técnicos multimarca se requiere para soportar consultas deterministas de inventario y cotización en la distribuidora Power Electrimk?", bold_prefix="Pregunta Específica 1 (P1). ", indent=False)
    add_p("¿Cómo diseñar e implementar una arquitectura de microservicio ligera en .NET 8 que orqueste la mensajería asíncrona de WhatsApp Cloud API, la inferencia generativa de Gemini y la recuperación local en SQLite preservando la memoria conversacional comercial bajo un consumo contenido de recursos?", bold_prefix="Pregunta Específica 2 (P2). ", indent=False)
    add_p("¿En qué medida la incorporación del mecanismo de recuperación determinista local mitiga la tasa de alucinación, optimiza la exactitud fáctica de cotizaciones y reduce la latencia en percentil P95 frente al modelo generativo operando de manera aislada sin recuperación contextual?", bold_prefix="Pregunta Específica 3 (P3). ", indent=False)

    add_h2("5.2. Hipótesis de investigación")
    add_p("La implementación de un agente inteligente para la atención comercial y cotización de materiales eléctricos en Guayaquil con recuperación fáctica local sobre catálogos estructurados en SQLite permite optimizar el embudo de ventas técnicas en Power Electrimk, alcanzando una exactitud de precios y referencias técnicas superior al 95%, una tasa de alucinación fáctica nula (0%), y una latencia en percentil P95 inferior a 4.0 segundos, con un perfil de consumo de memoria RAM inferior a 250 MB en infraestructura virtual de entrada en la nube.", bold_prefix="Hipótesis General (HG). ", indent=False)
    add_p("El levantamiento y la normalización relacional de los atributos esenciales del catálogo multimarca estructurado en SQLite permiten resolver consultas de inventario comercial con tiempos de ejecución en base de datos (T_sql) inferiores a 100 milisegundos con 100% de integridad en campos críticos (código de fábrica, precio y marca).", bold_prefix="Hipótesis Específica 1 (H1). ", indent=False)
    add_p("Una arquitectura asíncrona desacoplada en .NET 8 con persistencia de sesiones comerciales permite procesar las ráfagas de webhooks entrantes de WhatsApp Cloud API sin bloqueos de concurrencia, manteniendo la utilización de memoria del proceso por debajo de 250 megabytes.", bold_prefix="Hipótesis Específica 2 (H2). ", indent=False)
    add_p("El agente comercial con recuperación fáctica determinista exhibirá una tasa de alucinación significativamente menor (H_rate = 0%, p < 0,05) y una exactitud de cotización (Acc_cot >= 95%) estadísticamente superior en comparación con el modelo generativo operando en modalidad directa sin recuperación contextual.", bold_prefix="Hipótesis Específica 3 (H3). ", indent=False)

    # =========================================================================
    # SECCIÓN 6: MARCO TEÓRICO
    # =========================================================================
    add_h1("6. Marco teórico referencial")
    add_p("Esta sección fundamenta conceptualmente la formulación del artefacto de software propuesto, estructurando los conocimientos de manera deductiva desde los paradigmas de interacción hasta los mecanismos de persistencia y los estándares de ingeniería de software que rigen su implementación. Los contenidos se organizan en torno a tres constructos esenciales: los agentes conversacionales en la atención comercial, los modelos generativos de lenguaje extenso, y las técnicas de recuperación aumentada sobre motores embebidos.")

    add_h2("6.1. Agentes conversacionales en la atención comercial")
    add_p("Un agente conversacional es un sistema de software diseñado para emular la interacción humana mediante procesamiento de lenguaje natural, facilitando la ejecución de tareas o la provisión de información de manera interactiva (Adamopoulou & Moussiades, 2020). Históricamente, las primeras arquitecturas comerciales se fundamentaron en árboles de decisión y cotejo de patrones basados en reglas sintácticas fijas; si bien estos sistemas exhiben un comportamiento estrictamente predecible, sufren de una fragilidad intrínseca ante variaciones semánticas, errores tipográficos o expresiones idiomáticas no contempladas por los analistas (Følstad et al., 2020). En el entorno del comercio electrónico conversacional, la percepción de naturalidad, comprensión contextual y empatía técnica condiciona directamente la satisfacción, la confianza del consumidor y su predisposición para culminar una transacción de compra (Adam et al., 2021; Ashfaq et al., 2020; Sands et al., 2021). Asimismo, estudios empíricos en mercadotecnia digital demuestran que la pericia percibida del asistente y la transparencia en su condición de agente artificial inciden significativamente en la intención de compra y en la fidelización del cliente técnico (Han, 2023; Luo et al., 2019). Cuando se trata de suministros técnicos como materiales eléctricos, el usuario no solo busca conocer un precio, sino que requiere una consulta orientativa sobre compatibilidad de voltaje, calibres conductores y disponibilidad de marcas sustitutas. Esta complejidad lingüística y semántica hace inviable el uso exclusivo de árboles estáticos y motiva la integración de modelos generativos avanzados en el núcleo de procesamiento del agente.")

    add_h2("6.2. Modelos generativos de lenguaje extenso y arquitectura de agentes")
    add_p("Los modelos de lenguaje extenso (LLM) contemporáneos se basan en la arquitectura Transformer, cuyo mecanismo de autoatención captura dependencias globales de significado a lo largo de secuencias textuales complejas (Vaswani et al., 2017). Entrenados sobre volúmenes masivos de datos textuales, estos modelos exhiben capacidades emergentes para la inferencia contextual, el seguimiento riguroso de directrices delimitadas en mensajes de sistema (system prompts) y la adopción de roles comerciales especializados (Wang et al., 2024). No obstante, la naturaleza fundamentalmente probabilística de los LLM induce el fenómeno conocido como alucinación, en el cual el modelo produce aseveraciones sintácticamente coherentes pero fácticamente falsas o inexistentes en la realidad objetiva (Ji et al., 2023; Huang et al., 2023). Recientes revisiones sistemáticas categorizan las alucinaciones en intrínsecas (contradicción directa de la fuente provista) y extrínsecas (invención de hechos no verificables), atribuyendo su origen a sesgos de preentrenamiento y fallas en la alineación paramétrica (Tonmoy et al., 2024). En un entorno industrial o comercial de distribución eléctrica, la invención de un precio unitario, una capacidad de interrupción inexistente o una certificación técnica errónea acarrea graves perjuicios comerciales y legales. Por consiguiente, resulta imperativo gobernar el comportamiento generativo mediante verificación de cadenas de conocimiento y mecanismos de anclaje determinista (grounding) (Dhuliawala et al., 2023), conocidos formalmente como generación aumentada por recuperación.")

    add_h2("6.3. Recuperación aumentada, bases de datos embebidas y estándares de ingeniería")
    add_p("El paradigma de generación aumentada por recuperación (Retrieval-Augmented Generation, RAG) constituye una metodología híbrida que desacopla la memoria paramétrica del modelo de lenguaje de la fuente fáctica de verdad, consultando un almacén de datos estructurado o no estructurado antes de sintetizar la respuesta final (Guu et al., 2020; Lewis et al., 2020; Borgeaud et al., 2022; Gao et al., 2023). Si bien propuestas recientes exploran mecanismos avanzados de auto-reflexión y re-evaluación iterativa (Self-RAG) (Asai et al., 2024), tales enfoques imponen una penalización severa de latencia y costo computacional. En el contexto de catálogos de materiales eléctricos, donde las entidades poseen atributos inequívocos como código de parte, amperaje, marca y precio de lista, la recuperación basada en esquemas relacionales e índices lexicográficos presenta mayor precisión y predictibilidad que las representaciones vectoriales densas, evitando discrepancias de redondeo y falsos positivos semánticos.")

    add_p("Para satisfacer la restricción de hardware en entornos de bajo presupuesto computacional, el empleo de SQLite como motor embebido ofrece transacciones ACID completas dentro del mismo espacio de proceso de la aplicación, suprimiendo la sobrecarga de comunicación interproceso por sockets de red y el consumo de memoria asociado a servicios de bases de datos independientes (Gaffney, 2022). Al habilitar el modo de registro de escritura anticipada (Write-Ahead Logging, WAL), el motor soporta lecturas simultáneas altamente concurrentes sin bloquear las escrituras de actualización de catálogo o registro de sesiones. Asimismo, la estructuración del backend bajo principios de microservicios independientes y patrones cloud-native garantiza un despliegue desacoplado, mantenible y escalable con huella mínima de memoria en servidores virtuales de entrada (Kratzke & Quint, 2017; Newman, 2021; Taibi et al., 2020).")

    add_p("Asimismo, la construcción del artefacto se gobierna bajo el estándar internacional de calidad de producto software ISO/IEC 25010:2011, priorizando las características de adecuación funcional, eficiencia de desempeño (tiempo de respuesta y utilización de recursos), fiabilidad y seguridad (ISO/IEC, 2011). La seguridad de la información en el canal de mensajería se garantiza mediante el protocolo TLS 1.3 (RFC 8446) para el cifrado en tránsito (Rescorla, 2018), complementado con la verificación de firmas criptográficas HMAC-SHA256 exigida por WhatsApp Cloud API para autenticar la legitimidad de cada webhook entrante. Estos fundamentos teóricos, metodológicos y normativos proporcionan el marco de referencia indispensable sobre el cual se articula la propuesta de desarrollo técnico descrita en la siguiente sección.")

    # =========================================================================
    # SECCIÓN 7: METODOLOGÍA
    # =========================================================================
    add_h1("7. Metodología / Propuesta de desarrollo")
    add_p("La presente investigación adopta un alcance descriptivo y aplicado, bajo un enfoque metodológico mixto predominantemente cuantitativo y con un diseño cuasi-experimental de corte transversal. Según su propósito, constituye una investigación tecnológica orientada a la concepción, ingeniería y validación empírica de un artefacto de software; según el método de inferencia, es de naturaleza deductiva al derivar hipótesis operativas a partir de constructos teóricos consolidados; según la procedencia de la información, combina fuentes secundarias documentales (catálogos de fabricantes, especificaciones técnicas y literatura científica indexada) con datos primarios generados durante las pruebas automatizadas del sistema. La recolección de datos se sustentará en el registro automatizado de trazas de telemetría y métricas de rendimiento en servidor, complementado con entrevistas semiestructuradas al equipo comercial para el levantamiento de requerimientos de dominio (Llerena-Izquierdo & Ayala-Carabajo, 2022).")

    add_p("El desarrollo del proyecto se estructurará rigurosamente en cinco fases consecutivas e iterativas:")
    add_bullet("Se llevará a cabo una revisión bibliográfica exhaustiva fundamentada en directrices metodológicas para ingeniería de software y la recopilación de literatura científica reciente en bases de datos indexadas (Scopus, IEEE Xplore, ACM y Web of Science). Se analizarán investigaciones sobre agentes conversacionales, modelos de lenguaje extenso y técnicas de recuperación aumentada (RAG). De forma paralela, se levantarán los requerimientos funcionales y técnicos con el personal comercial de la distribuidora Power Electrimk, inventariando las marcas distribuidas (e.g., Bticino, Schneider Electric, Phelps Dodge, Centelsa, Legrand, Siemens, ABB, Veto) y digitalizando los catálogos técnicos y listas de precios para estandarizar los atributos esenciales de los productos.", bold_prefix="Fase 1: Revisión bibliográfica y análisis de requerimientos. ")
    add_bullet("Se definirá la arquitectura de software en capas basada en microservicios ligeros, estableciendo el esquema relacional en SQLite con optimización de índices para búsqueda textual rápida y soporte de transacciones concurrentes bajo modo WAL. Se diseñará el flujo de control para la verificación y consumo de los webhooks de WhatsApp Cloud API, la lógica de recuperación de productos afines a partir del mensaje del cliente y el mensaje de sistema (system prompt) que gobernará el comportamiento del modelo generativo Gemini (Zerega-Prado & Llerena-Izquierdo, 2022).", bold_prefix="Fase 2: Diseño de la arquitectura propuesta. ")
    add_bullet("Se programará el servicio web en lenguaje C# sobre la plataforma .NET 8, aprovechando sus características nativas de alto rendimiento asíncrono y bajo consumo de memoria. Se implementará la lógica del embudo comercial (calificación de prospectos, asesoría técnica de compatibilidad, consulta determinista de inventario y síntesis de cotización fáctica con desglose de ítems, códigos de parte, precios unitarios y totales), el módulo de persistencia y contexto conversacional por número de teléfono, el conector HTTP con autenticación Bearer hacia la API de WhatsApp, la capa de consulta relacional SQLite WAL y la integración con el SDK de Google Gemini para la síntesis contextual en lenguaje natural (Llerena-Izquierdo, Mendez-Reyes, et al., 2024). La arquitectura se estructurará mediante interfaces desacopladas que habilitan contractualmente la integración de visión multimodal para reconocimiento de imágenes de piezas eléctricas, pase asistido a asesor humano mediante máquina de estados, seguimiento automatizado de cotizaciones y sincronización con plataformas CRM en fases operativas posteriores.", bold_prefix="Fase 3: Desarrollo del prototipo funcional. ")
    add_bullet("El prototipo se desplegará en una instancia virtual Linux (Ubuntu 24.04.5 LTS) en Amazon Web Services (AWS EC2 t2.micro, acogida a la Capa Gratuita de 750 horas mensuales), configurando un servidor Nginx como proxy inverso hacia el runtime Kestrel en puerto 5252, administrado por el demonio Systemd (agenteventas.service) y con terminación de certificados de seguridad TLS 1.3 emitidos por Certbot (Let's Encrypt) bajo el subdominio oficial agente.powerelectrimk.com. Se ejecutará un protocolo experimental automatizado compuesto por una batería de N = 50 casos de prueba estructurados (búsquedas por código exacto, por especificación técnica, por categoría y solicitudes multimarca), comparando el desempeño del agente con recuperación local determinista frente al modelo generativo sin recuperación para cuantificar la tasa de eliminación de alucinaciones en precios y referencias de catálogo.", bold_prefix="Fase 4: Despliegue y pruebas experimentales. ")
    add_bullet("Se procesarán estadísticamente las métricas de latencia de respuesta, porcentaje de exactitud en precios y referencias técnicas, tasa de alucinación y utilización de memoria RAM y procesador en el servidor. Los resultados se contrastarán contra las hipótesis de investigación planteadas, y se redactará el informe técnico final de titulación de conformidad con las directrices institucionales (Llerena-Izquierdo, Lindao-Cacao, et al., 2026).", bold_prefix="Fase 5: Análisis de resultados y documentación. ")

    # Figura 1: Metodología
    add_caption("Figura 1", "Diagrama de flujo de las fases de la metodología de investigación")
    fig1_path = r'C:\Users\lenovo\Desktop\AgenteVentasPower\Docs\images\extracted\crop_figura1.png'
    if os.path.exists(fig1_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.add_run().add_picture(fig1_path, width=Inches(4.5))
    add_note("El diagrama ilustra la progresión secuencial de las cinco fases metodológicas y sus entregables tangibles, incluyendo el lazo de retroalimentación de ajustes entre la fase experimental y el código del prototipo.")

    add_p("Para la evaluación formal del sistema se han operacionalizado las siguientes métricas experimentales:")
    add_bullet("Tiempo total transcurrido en segundos desde la recepción del evento HTTP en el webhook hasta la emisión de la llamada de respuesta a la API de WhatsApp, medido con precisión de milisegundos mediante marcas de tiempo en el servidor.", bold_prefix="Latencia de respuesta (T_resp): ")
    add_bullet("Porcentaje de cotizaciones emitidas donde los códigos de producto, marcas y precios unitarios coinciden exactamente con los registros vigentes del inventario oficial, definido como Acc_cot = (C_correctas / C_totales) x 100%.", bold_prefix="Exactitud de cotización (Acc_cot): ")
    add_bullet("Proporción de respuestas en las que el modelo generativo asevera precios inexistentes, inventa atributos de productos o recomienda ítems no catalogados en la base de datos comercial.", bold_prefix="Tasa de alucinación (H_rate): ")
    add_bullet("Perfil de utilización de memoria RAM del proceso .NET (en megabytes) y porcentaje promedio de ocupación de CPU en la instancia de nube durante ráfagas de consultas.", bold_prefix="Consumo de recursos: ")

    # =========================================================================
    # SECCIÓN 8: CRONOGRAMA
    # =========================================================================
    add_h1("8. Cronograma de actividades")
    add_p("El desarrollo del proyecto de titulación se estructurará a lo largo de un período académico regular, ajustándose de forma estricta a los hitos de evaluación y seguimiento dispuestos por la Comisión de Titulación de la carrera, tal como se detalla en la Tabla 2.")

    add_caption("Tabla 2", "Cronograma de hitos del programa de titulación")
    t2 = doc.add_table(rows=6, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_data = [
        ["Hito institucional", "Entregable / Alcance", "Fecha límite"],
        ["Presentación y aprobación", "Aprobación oficial del tema de titulación", "30/11/2026"],
        ["Hito 1 (25%)", "Estado del arte, requerimientos y catálogos", "21/12/2026"],
        ["Hito 2 (50%)", "Diseño arquitectónico y esquema de datos", "25/01/2027"],
        ["Hito 3 (75%)", "Prototipo funcional desplegado en la nube", "01/03/2027"],
        ["Hito 4 (100%)", "Evaluación experimental e informe final", "05/04/2027"]
    ]
    for r_idx, row in enumerate(t2_data):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 60, 60, 100, 100)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "003366"},
                                      bottom={"sz": 8, "val": "single", "color": "003366"})
            elif r_idx == 5:
                set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "003366"})

    add_note("Cronograma oficial de hitos académicos y ponderaciones de avance de acuerdo con la planificación de la Universidad Politécnica Salesiana.")

    add_p("Para garantizar la culminación exitosa de los objetivos planteados dentro del límite normativo de 400 horas de dedicación estudiantil, se presenta en la Tabla 3 el desglose pormenorizado de actividades por cada una de las cinco fases de la investigación, indicando su carga horaria estimada, fechas de inicio y culminación, y los responsables asignados.")

    add_caption("Tabla 3", "Plan de actividades por fases del proyecto de titulación")
    t3 = doc.add_table(rows=14, cols=5)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_data = [
        ["Actividad", "Horas", "Inicio", "Fin", "Responsables"],
        ["Fase 1: Revisión bibliográfica y análisis de requerimientos", "", "", "", ""],
        ["Revisión sistemática de literatura científica", "40", "01/12/2026", "12/12/2026", "Autores"],
        ["Levantamiento de requerimientos y digitalización", "30", "14/12/2026", "21/12/2026", "Autores / Tutor"],
        ["Fase 2: Diseño de la arquitectura propuesta", "", "", "", ""],
        ["Diseño arquitectónico y modelado relacional SQLite", "40", "22/12/2026", "11/01/2027", "Autores"],
        ["Estructuración de índices y normalización multimarca", "30", "12/01/2027", "25/01/2027", "Autores"],
        ["Fase 3: Desarrollo del prototipo funcional", "", "", "", ""],
        ["Implementación del backend .NET 8 y memoria de sesión", "60", "26/01/2027", "12/02/2027", "Autores"],
        ["Integración con API Gemini y WhatsApp Cloud API", "40", "15/02/2027", "01/03/2027", "Autores"],
        ["Fase 4: Despliegue y pruebas experimentales", "", "", "", ""],
        ["Despliegue en AWS con Nginx TLS y batería de pruebas", "60", "02/03/2027", "19/03/2027", "Autores"],
        ["Fase 5: Análisis de resultados y documentación", "", "", "", ""],
        ["Análisis estadístico de telemetría y redacción del informe", "60", "20/03/2027", "05/04/2027", "Autores / Tutor"],
    ]
    for r_idx, row in enumerate(t3_data):
        for c_idx, val in enumerate(row):
            cell = t3.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "003366"},
                                      bottom={"sz": 8, "val": "single", "color": "003366"})
            elif "Fase" in val and c_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.italic = True
            elif r_idx == 13:
                set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "003366"})

    add_note("Distribución del esfuerzo de ingeniería en 360 horas de ejecución técnica y 40 horas de contingencia para imprevistos o ajustes experimentales, completando las 400 horas reglamentarias.")

    # =========================================================================
    # SECCIÓN 9: PROYECTOS VINCULADOS
    # =========================================================================
    add_h1("9. Proyectos de investigación vinculados")
    add_p("El presente trabajo de titulación, desarrollado por los estudiantes Victor Jesus Totoy Iza y Rodolfo Damián Seminario Murillo, se ejecuta bajo la dirección y tutoría del docente investigador Ing. Joe Llerena Izquierdo, M.Sc., Ph.D., y se encuentra formalmente articulado a las actividades científicas del Grupo de Investigación en Enseñanza-Aprendizaje de las Ciencias para la Ingeniería (GIEACI) de la Universidad Politécnica Salesiana, Sede Guayaquil.")

    add_p("Específicamente, los postulantes solicitan su adhesión formal al proyecto de investigación institucional titulado:", indent=False)
    p_adh = doc.add_paragraph()
    p_adh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_adh = p_adh.add_run("«Percepciones y dilemas éticos de estudiantes de Ingeniería frente al uso de IA generativa en el aprendizaje»")
    r_adh.font.bold = True
    r_adh.font.name = 'Times New Roman'
    r_adh.font.color.rgb = RGBColor(0, 51, 102)

    add_p("el cual se inscribe en la línea de investigación institucional de la carrera de Computación denominada: Integración de Tecnologías Emergentes en la Educación en Ingeniería y Sistemas Inteligentes.", indent=False)
    add_p("La vinculación con dicho proyecto de investigación se fundamenta en que el desarrollo del agente conversacional no solo aborda la dimensión técnica del software y la ingeniería de datos sobre SQLite, sino que aporta evidencia empírica directa sobre los dilemas de confiabilidad, sesgo y ética algorítmica derivados del uso de modelos generativos fundacionales en entornos de interacción humana real (Llerena-Izquierdo, Mendez-Reyes, et al., 2024; Ayala-Carabajo & Llerena-Izquierdo, 2026). Los hallazgos sobre alucinaciones de precios, gobernanza de datos personales bajo la LOPDP ecuatoriana y patrones de interacción en mensajería instantánea enriquecerán las publicaciones y análisis del grupo GIEACI respecto a la adopción responsable de la inteligencia artificial.")

    # =========================================================================
    # SECCIÓN 10: PRESUPUESTO
    # =========================================================================
    add_h1("10. Presupuesto del Proyecto de Titulación")
    add_p("El presupuesto estimado para la ejecución integral del proyecto de titulación considera tanto la valoración formal del esfuerzo de ingeniería de software (mano de obra de los tesistas), como el dimensionamiento técnico de la infraestructura computacional en la nube, conectividad, licencias de consumo y suministros requeridos para el ciclo de vida del software. En la Tabla 4 se expone la valoración económica formal del proyecto, cuantificada conforme a precios de mercado y aranceles profesionales de desarrollo.")

    add_caption("Tabla 4", "Presupuesto detallado y valoración económica del proyecto de titulación")
    t4 = doc.add_table(rows=13, cols=3)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4_data = [
        ["Categoría / Rubro", "Descripción y dedicación del recurso", "Costo (USD)"],
        ["1. Mano de obra de ingeniería y desarrollo (Tesistas)", "", ""],
        ["Victor Jesús Totoy Iza", "Arquitectura backend (.NET 8), webhooks y despliegue (200 h a $10.00/h)", "2000.00"],
        ["Rodolfo Damián Seminario Murillo", "Esquema relacional SQLite, orquestación Gemini y pruebas (200 h a $10.00/h)", "2000.00"],
        ["Subtotal Mano de obra de ingeniería", "", "4000.00"],
        ["2. Infraestructura tecnológica, servicios y suministros directos", "", ""],
        ["Servidor en la nube (AWS EC2)", "Instancia virtual Linux (t2.micro) durante 6 meses de proyecto", "60.00"],
        ["Nombre de dominio y gestión TLS", "Dominio powerelectrimk.com y gestión de DNS Cloudflare (1 año)", "15.00"],
        ["Consumo de inferencia API Gemini", "Cuota de tokens para pruebas de integración y validación (N=50)", "40.00"],
        ["Línea telefónica comercial", "Tarjeta SIM y recargas para WhatsApp Business API", "25.00"],
        ["Servicio de acceso a Internet", "Conectividad fija de banda ancha durante 6 meses ($30.00/mes)", "180.00"],
        ["Impresión y encuadernación", "Empastado y documentación física institucional de titulación", "70.00"],
        ["Fondo de contingencia", "Margen para imprevistos operativos y pruebas adicionales (10%)", "40.00"]
    ]
    for r_idx, row in enumerate(t4_data):
        for c_idx, val in enumerate(row):
            cell = t4.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "003366"},
                                      bottom={"sz": 8, "val": "single", "color": "003366"})
            elif "Mano de obra" in val or "Infraestructura" in val:
                cell.paragraphs[0].runs[0].font.bold = True
            elif r_idx == 12:
                set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "003366"})

    # Fila de Total
    row_tot = t4.add_row()
    row_tot.cells[0].text = "Total general valorado del proyecto"
    row_tot.cells[0].paragraphs[0].runs[0].font.bold = True
    row_tot.cells[2].text = "4430.00"
    row_tot.cells[2].paragraphs[0].runs[0].font.bold = True
    set_cell_border(row_tot.cells[0], top={"sz": 8, "val": "single", "color": "003366"}, bottom={"sz": 12, "val": "single", "color": "003366"})
    set_cell_border(row_tot.cells[1], top={"sz": 8, "val": "single", "color": "003366"}, bottom={"sz": 12, "val": "single", "color": "003366"})
    set_cell_border(row_tot.cells[2], top={"sz": 8, "val": "single", "color": "003366"}, bottom={"sz": 12, "val": "single", "color": "003366"})

    add_note("Valores expresados en dólares de los Estados Unidos de América (USD). La tarifa horaria de 10.00 USD/h se fundamenta en los valores referenciales de mercado para desarrolladores de software junior en Ecuador. Los costos directos de infraestructura y servicios (430.00 USD) y la mano de obra de investigación (4000.00 USD) son asumidos íntegramente por los autores.")

    add_p("Como se expone en la Tabla 4, el costo consolidado del proyecto asciende a 4430.00 USD. De este valor, el 90.3% (4000.00 USD) corresponde a la mano de obra de ingeniería aportada por los tesistas (Victor Jesús Totoy Iza y Rodolfo Damián Seminario Murillo), cuantificada en 400 horas de dedicación conjunta (200 horas individuales) a una tarifa estandarizada de 10.00 USD por hora, representando la inversión de capital humano inherente a la formación en ingeniería en computación.")

    add_p("Por otra parte, desde la perspectiva operativa y financiera de la puesta en marcha, el proyecto exhibe una ventaja competitiva excepcional gracias al aprovechamiento estratégico de las capas gratuitas (Free Tiers) ofrecidas por los principales proveedores tecnológicos de nube e inteligencia artificial. Durante la etapa de investigación, desarrollo y validación experimental, los costos computacionales de la nube y de la API de inferencia se reducen de forma efectiva a 0.00 USD. En la Tabla 5 se presenta el análisis comparativo entre los límites operativos de la Capa Gratuita y la estructura tarifaria de pago (Pay-as-you-go) para cuando la empresa distribuidora Power Electrimk decida escalar la solución a régimen comercial masivo.")

    add_caption("Tabla 5", "Análisis operativo de servicios de nube: Capa Gratuita vs. Régimen Comercial de Pago")
    t5 = doc.add_table(rows=7, cols=4)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_data = [
        ["Proveedor / Servicio", "Capa Gratuita (Free Tier)", "Régimen Comercial (Pay-as-you-go)", "Gasto Fase Tesis"],
        ["Google Gemini API (Google AI Studio)", "15 RPM, 1 000 000 TPM y hasta 1 500 solicitudes/día gratuitas (Flash).", "Entrada: $0.075 / 1M tokens. Salida: $0.30 / 1M tokens (aprox. $2.50/mes por 1 000 chats/día).", "0.00"],
        ["Amazon Web Services (AWS EC2 t2.micro)", "750 horas/mes gratuitas durante 12 meses; 30 GB almacenamiento SSD EBS gp3.", "On-Demand: $0.0116/h (aprox. $8.35/mes) + $2.40/mes almacenamiento EBS gp3.", "0.00"],
        ["Meta Cloud API (WhatsApp Business)", "1 000 conversaciones de servicio al cliente al mes gratuitas iniciadas por usuario.", "Tarifa variable por categoría de conversación ($0.008 a $0.035 USD/chat tras superar 1 000).", "0.00"],
        ["Let's Encrypt / Certbot (Certificado TLS 1.3)", "Certificados criptográficos SSL/TLS automatizados de renovación continua (100% gratis).", "Certificados comerciales corporativos con validación de organización ($15.00 a $60.00/año).", "0.00"],
        ["Dominio y DNS (Cloudflare / Namecheap)", "DNS seguro gratuito en Cloudflare; registro de dominio de pago.", "Renovación anual de dominio comercial powerelectrimk.com a precio de mercado.", "15.00"],
        ["Conectividad fija (Proveedor local)", "No aplica capa gratuita comercial.", "Tarifa residencial/comercial mensual de banda ancha simétrica ($30.00/mes x 6 meses).", "180.00"]
    ]
    for r_idx, row in enumerate(t5_data):
        for c_idx, val in enumerate(row):
            cell = t5.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 50, 50, 70, 70)
            if r_idx == 0:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_border(cell, top={"sz": 12, "val": "single", "color": "003366"},
                                      bottom={"sz": 8, "val": "single", "color": "003366"})
            elif r_idx == 6:
                set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "003366"})

    row_t5_tot = t5.add_row()
    row_t5_tot.cells[0].text = "Desembolso directo real de infraestructura en fase de investigación"
    row_t5_tot.cells[0].paragraphs[0].runs[0].font.bold = True
    row_t5_tot.cells[3].text = "195.00"
    row_t5_tot.cells[3].paragraphs[0].runs[0].font.bold = True
    set_cell_border(row_t5_tot.cells[0], top={"sz": 8, "val": "single", "color": "003366"}, bottom={"sz": 12, "val": "single", "color": "003366"})
    set_cell_border(row_t5_tot.cells[1], top={"sz": 8, "val": "single", "color": "003366"}, bottom={"sz": 12, "val": "single", "color": "003366"})
    set_cell_border(row_t5_tot.cells[2], top={"sz": 8, "val": "single", "color": "003366"}, bottom={"sz": 12, "val": "single", "color": "003366"})
    set_cell_border(row_t5_tot.cells[3], top={"sz": 8, "val": "single", "color": "003366"}, bottom={"sz": 12, "val": "single", "color": "003366"})

    add_note("Datos oficiales recopilados de la documentación técnica y tablas de facturación de Google Cloud / Google AI Studio (2026), Amazon Web Services Free Tier y Meta for Developers. El gasto real de 195.00 USD demuestra la alta viabilidad financiera del proyecto para su validación en la distribuidora Power Electrimk.")

    add_p("Este análisis evidencia que la combinación de un motor embebido SQLite (modo WAL sin costo de licenciamiento) con la Capa Gratuita de Google AI Studio y el AWS Free Tier minimiza el riesgo de inversión para la distribuidora Power Electrimk, requiriendo un desembolso directo de únicamente 195.00 USD durante los seis meses de ejecución del proyecto de titulación. Si la distribuidora decidiera extender la solución a un volumen comercial de alta demanda superando los límites de la capa gratuita, el esquema de cobro por consumo de Gemini Flash garantiza que el costo mensual de inferencia por cada 1 000 cotizaciones atendidas no excederá los 3.00 USD, lo cual consolida la sostenibilidad económica y el retorno de inversión del sistema frente a plataformas propietarias de alto costo recurrente.")

    # =========================================================================
    # SECCIÓN 11: REFERENCIAS BIBLIOGRÁFICAS
    # =========================================================================
    doc.add_page_break()
    add_h1("11. Referencias bibliográficas")
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
        "Guu, K., Lee, K., Tung, Z., Pasupat, P., & Chang, M.-W. (2020). REALM: Retrieval-Augmented Language Model Pre-Training. Proceedings of the 37th International Conference on Machine Learning (ICML 2020), 119, 3929–3938. https://proceedings.mlr.press/v119/guu20a.html",
        "Han, M. C. (2023). The effect of conversational AI chatbot's perceived competence, empathy, and conversational quality on customer satisfaction and purchase intention. Journal of Global Fashion Marketing, 14(4), 391–406. https://doi.org/10.1088/20932685.2023.2209772",
        "Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., & Liu, T. (2023). A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions. arXiv Preprint arXiv:2311.05232. https://doi.org/10.48550/arXiv.2311.05232",
        "ISO/IEC. (2011). Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models (Standard ISO/IEC 25010:2011). International Organization for Standardization. https://www.iso.org/standard/35733.html",
        "Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Yan, S., Ishii, E., Bang, Y. J., Madotto, A., & Fung, P. (2023). Survey of Hallucination in Natural Language Generation. ACM Computing Surveys, 55(12), 248:1-248:38. https://doi.org/10.1145/3571730",
        "Kratzke, N., & Quint, P.-C. (2017). Understanding cloud-native applications after 10 years of cloud computing - A systematic mapping study. Journal of Systems and Software, 126, 1–16. https://doi.org/10.1016/j.jss.2017.01.001",
        "Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W.-T., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 9459–9474. https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html",
        "Llerena-Izquierdo, J., & Ayala-Carabajo, R. (2022). Desarrollo de competencia investigativa de estudiantes universitarios de ingeniería en proceso de titulación: propuesta metodológica y experiencia. Memoria Investigaciones en Ingeniería, 23, 50–62. https://doi.org/10.36561/ING.23.5",
        "Llerena-Izquierdo, J., & Ayala-Carabajo, R. (2025). Guía práctica para redactar y publicar manuscritos científicos. Ediciones Abya-Yala. https://doi.org/10.17163/abyaups.134",
        "Llerena-Izquierdo, J., Fiallos-Vargas, I., Portugal-Gorozabel, J., & Veloz-Arce, A. (2024). Towards an experience in AI-driven development for programming applied to multimedia using Tabnine. 2024 IEEE URUCON, 1–5. https://doi.org/10.1109/URUCON63440.2024.10850207",
        "Llerena-Izquierdo, J., Lindao-Cacao, K., Espinoza-Rosero, Gloria, & Carrera-Jimenez, J. (2026). Towards a Management Model for the Final Year Project in Computer Engineering in the Field of Research. En M. V. Garcia, J.-P. Reyes, C. Nuñez, & C. Gordón-Gallegos (Eds.), Proceedings of the International Conference on Computer Science, Electronics and Industrial Engineering (CSEI 2024) (pp. 37–49). Springer Nature Switzerland. https://doi.org/10.1007/978-3-031-98890-5_3",
        "Llerena-Izquierdo, J., Mendez-Reyes, J., Ayala-Carabajo, R., & Andrade-Martinez, C. (2024). Innovations in Introductory Programming Education: The Role of AI with Google Colab and Gemini. Education Sciences, 14(12), 1330. https://doi.org/10.3390/educsci14121330",
        "Luo, X., Tong, S., Fang, Z., & Qu, Z. (2019). Frontiers: Machines vs. Humans: The Impact of Artificial Intelligence Chatbot Disclosure on Customer Purchases. Marketing Science, 38(6), 937–947. https://doi.org/10.1287/mksc.2019.1192",
        "Newman, S. (2021). Building Microservices: Designing Fine-Grained Systems (2nd ed.). O'Reilly Media.",
        "Rescorla, E. (2018). The Transport Layer Security (TLS) Protocol Version 1.3 (RFC 8446). Internet Engineering Task Force. https://doi.org/10.17487/RFC8446",
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

    # =========================================================================
    # SECCIÓN 12: ANEXOS
    # =========================================================================
    doc.add_page_break()
    add_h1("12. Anexos")

    add_h2("12.1. Anexo 1: Árbol de problemas y objetivos (Metodología 5W+H)")
    add_p("De acuerdo con la guía metodológica de formulación de proyectos 5W+H de la Universidad Politécnica Salesiana, se presentan en la Figura 2 y la Figura 3 las representaciones causales del problema central y su transformación propositiva hacia los medios y fines de la solución técnica.")

    add_caption("Figura 2", "Árbol de problemas de la atención comercial en distribuidoras eléctricas")
    fig2_path = r'C:\Users\lenovo\Desktop\AgenteVentasPower\Docs\images\extracted\crop_figura2.png'
    if os.path.exists(fig2_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.add_run().add_picture(fig2_path, width=Inches(6.2))
    add_note("Estructura causal del problema identificada a través de la metodología 5W+H en la distribuidora Power Electrimk.")

    add_caption("Figura 3", "Árbol de objetivos de la solución de ingeniería de software")
    fig3_path = r'C:\Users\lenovo\Desktop\AgenteVentasPower\Docs\images\extracted\crop_figura3.png'
    if os.path.exists(fig3_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.add_run().add_picture(fig3_path, width=Inches(6.2))
    add_note("Transformación de medios y fines orientada a la ingeniería de software y la validación experimental.")

    doc.add_page_break()
    add_h2("12.2. Anexo 2: Matriz de consistencia metodológica de la investigación (UPS P69)")
    add_p("En la Tabla 6 se detalla la Matriz de Consistencia Metodológica elaborada bajo el formato normativo institucional UPS P69, evidenciando la coherencia entre problemas, objetivos, hipótesis, variables e indicadores.")

    add_caption("Tabla 6", "Matriz de consistencia metodológica de la investigación (Formato Institucional UPS P69)")
    t6 = doc.add_table(rows=5, cols=6)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    t6_headers = ["Problema", "Objetivos", "Hipótesis", "Variables y Dimensiones", "Indicadores Prioritarios", "Técnicas e Instrumentos"]
    for i, h in enumerate(t6_headers):
        cell = t6.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        set_cell_border(cell, top={"sz": 12, "val": "single", "color": "003366"},
                              bottom={"sz": 8, "val": "single", "color": "003366"})
        set_cell_margins(cell, 40, 40, 50, 50)

    t6_rows = [
        [
            "Problema General (PG):\n¿En qué medida un agente inteligente para la atención comercial y cotización de materiales eléctricos en Guayaquil, basado en modelos generativos y recuperación relacional determinista, mejora la exactitud de precios, la latencia P95 y la eficiencia de recursos en Power Electrimk?",
            "Objetivo General (OG):\nDesarrollar un agente inteligente para la atención comercial y cotización de materiales eléctricos en Guayaquil, mediante la integración de modelos generativos y recuperación relacional determinista para garantizar cotizaciones fácticas en Power Electrimk.",
            "Hipótesis General (HG):\nEl agente con recuperación local sobre SQLite permite alcanzar una exactitud en cotización >= 95%, tasa de alucinación nula (0%), latencia en P95 < 4.0 s y consumo de RAM < 250 MB en la nube.",
            "Variable Independiente (VI):\nModalidad de interacción comercial con recuperación determinista local sobre catálogo relacional estructurado.",
            "- Exactitud cotización (Acc_cot >= 95%)\n- Tasa alucinación (H_rate = 0%)\n- Latencia P95 (T_resp < 4.0 s)\n- Consumo RAM (< 250 MB)",
            "Técnicas:\n- Telemetría automatizada en AWS EC2.\n- Benchmarking sintético.\nInstrumentos:\n- Scripts k6 / wrk.\n- Logs estructurados."
        ],
        [
            "Sistematización P1:\n¿Cuáles son los requerimientos técnicos y comerciales, y qué estructura relacional multimarca se requiere en Power Electrimk?",
            "Objetivo Específico 1 (O1):\nAnalizar los requerimientos operativos de cotización y la estructura de catálogos multimarca en Power Electrimk, fijando especificaciones de diseño.",
            "Hipótesis Específica 1 (H1):\nLa estructuración relacional normalizada en SQLite permite resolver consultas de inventario en T_sql < 100 ms con 100% de integridad.",
            "Variable Dependiente 1 (VD1):\nDimensión Estructura e Integridad:\nConsistencia y celeridad de consulta de inventario técnico.",
            "- Tiempo consulta SQL (T_sql < 100 ms)\n- Tasa de recuperación SKU (100%)\n- Integridad atributos (100%)",
            "Técnicas:\n- Revisión bibliográfica.\n- Entrevistas comerciales.\nInstrumentos:\n- Guía de entrevista.\n- Matriz de extracción."
        ],
        [
            "Sistematización P2:\n¿Cómo diseñar una arquitectura ligera en .NET 8 que integre WhatsApp, Gemini y SQLite preservando la memoria conversacional?",
            "Objetivo Específico 2 (O2):\nImplementar un prototipo de microservicio en .NET 8 con persistencia SQLite WAL, orquestación Gemini y WhatsApp Cloud API.",
            "Hipótesis Específica 2 (H2):\nLa arquitectura asíncrona en .NET 8 procesa webhooks concurrentes sin bloqueos y con memoria de proceso < 250 MB.",
            "Variable Dependiente 2 (VD2):\nDimensión Eficiencia de Recursos:\nHuella computacional y concurrencia del servicio backend.",
            "- Utilización memoria RAM (< 250 MB)\n- Concurrencia de sesiones\n- Ocupación CPU AWS (< 30%)",
            "Técnicas:\n- Perfilado de memoria runtime.\n- Monitoreo Kestrel.\nInstrumentos:\n- dotnet-counters / dump.\n- Métricas CloudWatch."
        ],
        [
            "Sistematización P3:\n¿En qué medida la recuperación determinista mitiga la alucinación, mejora la exactitud y reduce la latencia P95 frente al modelo sin RAG?",
            "Objetivo Específico 3 (O3):\nEvaluar el prototipo mediante pruebas experimentales comparativas cuantificando exactitud, tasa de alucinación y latencia P95.",
            "Hipótesis Específica 3 (H3):\nEl agente con recuperación local logra H_rate = 0%, Acc_cot >= 95% y T_resp, P95 < 4.0 s con significancia (p < 0,05).",
            "Variable Dependiente 3 (VD3):\nDimensión Exactitud Fáctica y Rendimiento:\nCerteza técnica y celeridad de respuesta de cotización.",
            "- Exactitud cotización (Acc_cot >= 95%)\n- Tasa alucinación (H_rate = 0%)\n- Latencia P95 (< 4.0 s)\n- Valor p (< 0,05)",
            "Técnicas:\n- Ensayo experimental controlado.\n- Prueba t-Student / Wilcoxon.\nInstrumentos:\n- Batería N=50 casos estructurados.\n- Matriz de cotejo fáctico."
        ]
    ]
    for r_idx, row in enumerate(t6_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = t6.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8)
            set_cell_margins(cell, 30, 30, 40, 40)
            if r_idx == 4:
                set_cell_border(cell, bottom={"sz": 12, "val": "single", "color": "003366"})

    add_note("Matriz adaptada de la plantilla oficial de consistencia de la investigación UPS Sede Guayaquil (P69).")

    doc.add_page_break()
    add_h2("12.3. Anexo 3: Diagrama de arquitectura de software y flujo de procesamiento")
    add_p("En la Figura 4 se ilustra la arquitectura de componentes y el flujo secuencial de procesamiento de mensajes del agente inteligente, detallando la interacción entre los servicios externos de mensajería e inferencia y la infraestructura de cómputo local en la nube.")

    add_caption("Figura 4", "Arquitectura integral del agente inteligente para la atención comercial con recuperación local de catálogos")
    fig4_path = r'C:\Users\lenovo\Desktop\AgenteVentasPower\Docs\images\extracted\crop_figura4.png'
    if os.path.exists(fig4_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.add_run().add_picture(fig4_path, width=Inches(5.0))
    add_note("Diagrama arquitectónico del flujo de ejecución desacoplado entre el webhook de mensajería, el backend en .NET 8, el almacenamiento local embebido y el servicio de inferencia en la nube.")

    add_h2("12.4. Anexo 4: Repositorio de código abierto y transparencia de datos (ABET IV.3)")
    add_p("En estricto cumplimiento con el criterio de evaluación ABET IV.3 (Ética, Impacto y Reproducibilidad en Ingeniería), se formaliza el compromiso de acceso abierto a los artefactos de investigación:")
    add_bullet("Todo el código fuente del microservicio backend, los scripts de migración y estructuración de catálogos y las herramientas de benchmarking automatizado serán gestionados y publicados en el repositorio institucional público de GitHub: https://github.com/vtotoy/agente-ventas-power", bold_prefix="1. Repositorio de código fuente: ")
    add_bullet("El software se distribuye bajo los términos de la licencia de código abierto MIT License, permitiendo la auditoría por pares, su reutilización académica y la transferencia tecnológica sin fines de lucro hacia otras micro y pequeñas empresas ecuatorianas.", bold_prefix="2. Licenciamiento de software: ")
    add_bullet("Los conjuntos de datos de prueba, trazas de telemetría y transcripciones experimentales publicadas en el repositorio se someterán a un protocolo riguroso de anonimización irreversible. Los números telefónicos y nombres de personas naturales son sustituidos por identificadores sintéticos disociados (UUIDs), garantizando el pleno acatamiento de la Ley Orgánica de Protección de Datos Personales del Ecuador.", bold_prefix="3. Gobernanza y anonimización de datos (LOPDP): ")
    add_bullet("El repositorio incluye las directrices técnicas, el archivo Dockerfile de compilación multicapa y los procedimientos documentados paso a paso para desplegar el entorno de evaluación sobre cualquier distribución Linux con el runtime de .NET 8 y SQLite preinstalados.", bold_prefix="4. Guía de reproducibilidad computacional: ")

    doc.save(output_path)
    print(f"Document saved successfully to {output_path}")

if __name__ == "__main__":
    out_file = r"C:\Users\lenovo\Desktop\AgenteVentasPower\AnteproyectoTotoyDamian.docx"
    create_anteproyecto_docx(out_file)

