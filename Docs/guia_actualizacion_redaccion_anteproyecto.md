# Guía y Pautas de Redacción Técnica para el Anteproyecto de Titulación
## Actualización Integral del Artefacto de Software: Agente de Ventas Power ElectriMK

---

### 1. Resumen de Novedades Técnicas Incorporadas al Anteproyecto

Durante la evolución e ingeniería del artefacto de software se han consolidado cinco pilares de alta relevancia metodológica y académica que enriquecen directamente el documento de anteproyecto en formato LaTeX (normativa UPS Sede Guayaquil, APA 7ma Edición):

| Dimensión Técnica | Estado Previo | Estado Actual Consolidado | Ubicación en LaTeX |
| :--- | :--- | :--- | :--- |
| **Amplitud del Catálogo** | 16 productos de prueba iniciales | **613 referencias industriales completas** (Schneider Electric y Siemens) en 6 líneas. | `07_metodologia.tex` (Fase 1) |
| **Motor de Búsqueda RAG** | Búsqueda SQL simple por igualdad | **Híbrido FTS5 (BM25) con auto-reparación** y fallback tolerante a fallos. | `06_marco_teorico.tex`, `07_metodologia.tex` |
| **Ciberseguridad y Resiliencia** | Protección básica perimetral | **Defensa en Profundidad (Zero Disk)**: mitigación de inyecciones visuales e indirectas en Excel/PDF, Canary Tokens y Circuit Breaker. | `06_marco_teorico.tex`, `07_metodologia.tex` |
| **Política Comercial Multimarca** | Mención aleatoria de marcas | **"Solución primero, marca bajo demanda"** (Regla del Espejo, cero fatiga de decisión). | `07_metodologia.tex` (Fase 2 y 3) |
| **Cero Alucinación Económica** | Prohibición general en prompt | **Derivación formal a la Ing. Kely Pacalla** para validación de stock y proforma oficial. | `07_metodologia.tex`, `12_anexos.tex` |

---

### 2. Justificación Académica y Teórica para el Tribunal

#### 2.1. Búsqueda Léxica FTS5 y Algoritmo BM25 vs. Embeddings Densos
* **Argumento Académico:** En catálogos técnicos donde códigos como `LC1D25M7` o `3RT2026-1AP00` se diferencian por un solo carácter (tensión de bobina o amperaje), los modelos de embeddings densos cometen **falsos positivos semánticos** al mezclar bobinas de 110V y 220V debido a su proximidad vectorial.
* La búsqueda de texto completo con **FTS5 y ponderación BM25** *(Robertson & Zaragoza, 2009)* garantiza que el término técnico y sus parámetros electrotécnicos coincidan con exactitud matemática, sin requerir GPUs ni clústeres de bases vectoriales pesadas que romperían el límite de 1 GB de RAM en la nube gratuita de AWS (t2.micro).
* **Resiliencia Operativa:** Se incorporó una rutina de **auto-reparación en tiempo de ejecución** (`INSERT INTO Products_FTS(Products_FTS) VALUES('rebuild')`) que solventa desincronizaciones de índice de manera transparente para el usuario final.

#### 2.2. Seguridad en Modelos de Lenguaje (Directrices OWASP LLM 2025)
* **Vulnerabilidad Abordada:** Ataques de *Prompt Injection* indirecto a través de archivos de proyecto (listas de materiales en Excel, hojas CSV o planos en PDF) y fotografías de placas de motores donde actores maliciosos intentan forzar descuentos, extraer el prompt del sistema o alterar directivas.
* **Solución de Ingeniería:** 
  1. Procesamiento 100% en memoria RAM (Zero Disk Storage), evitando persistencia de malware en el servidor.
  2. Sanitización contra *Formula Injection* (anteposición de apóstrofe en celdas con `=`, `+`, `-`, `@`).
  3. Prohibición estricta de DTD para inmunidad contra ataques *XXE* (`XmlReaderSettings.DtdProcessing = Prohibit`).
  4. Generación de *Canary Tokens* criptográficos efímeros en cada turno para auditar fugas de instrucciones confidenciales en la respuesta de salida.

#### 2.3. Psicología Comercial y Manejo Multimarca Inteligente
* **El Problema del Spam de Fabricantes:** Cuando una empresa maneja más de 20 marcas (Schneider, Siemens, ABB, Eaton, Legrand, WEG, etc.), recitarlas en el chat o decir *"manejamos todas las marcas"* genera **parálisis por elección** y hace que el bot parezca un folleto automatizado intrusivo.
* **El Protocolo de Tres Reglas:**
  1. *Regla del Espejo:* Si el cliente pide una marca específica, el agente se restringe 100% a ella.
  2. *Solución Primero:* Si el cliente pide por parámetro (ej. *"breaker de 150A"*), se asesora directamente con la opción técnica estándar recomendada y se consulta de forma neutral si requiere homologación de obra.
  3. *Pregunta Directa:* Si el cliente pregunta qué marcas se manejan, se responde por familias técnicas y gamas, sin listar 20 nombres seguidos.

---

### 3. Síntesis de Archivos LaTeX Modificados

1. **`Docs/referencias/references.bib`:**
   * Agregadas las citas académicas de Robertson & Zaragoza (2009) para el algoritmo BM25 y Greshake et al. (2023) para la defensa contra inyecciones indirectas de prompt en LLMs.
2. **`Docs/secciones/06_marco_teorico.tex`:**
   * Incorporado el sustento formal de FTS5 BM25, triggers de sincronización relacional y el marco de defensa en profundidad (Zero Disk, anti-XXE, canary tokens).
3. **`Docs/secciones/07_metodologia.tex`:**
   * Actualizadas las fases metodológicas 1, 2 y 3 con la normalización del catálogo de 613 productos industriales, el diseño del pipeline seguro de documentos/imágenes y la política multimarca inteligente.
4. **`Docs/main.pdf`:**
   * Recompilado exitosamente con MiKTeX y Biber (30 páginas reglamentarias en formato APA 7ma Edición, sin errores de compilación ni referencias rotas).

---

### 4. Recomendaciones para la Presentación ante el Tutor y Tribunal (UPS)

* **Resaltar el principio de "Ingeniería Frugal" (Frugal Engineering):** Demostrar cómo se logró un sistema de alta precisión con cero costo recurrente, operando en AWS EC2 Free Tier bajo Kestrel y SQLite WAL.
* **Defender la elección de RAG Relacional vs. RAG Vectorial:** Justificar que en materiales eléctricos el código de producto y sus especificaciones técnicas exigen recuperación fáctica determinista sin tolerancia a alucinación.
* **Demostrar la robustez de Ciberseguridad:** Explicar cómo el sistema previene que un usuario intente saltarse las reglas o inyectar comandos a través de fotos o archivos de Excel.
