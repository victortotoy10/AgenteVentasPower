# INFORME TÉCNICO Y COMERCIAL: ESTRATEGIA DE TELEMETRÍA DE DEMANDA Y RESOLUCIÓN MULTIMARCA ADAPTATIVA
**Proyecto de Titulación / Producto:** Agente Inteligente para la Atención Comercial y Cotización de Materiales Eléctricos  
**Empresa de Aplicación:** Power ElectriMK (Guayaquil, Ecuador)  
**Fecha:** Noviembre 2026  
**Autor:** Equipo de Desarrollo de Software e Inteligencia Artificial  

---

## 1. Resumen Ejecutivo

En el modelo de distribución de materiales eléctricos industriales de Power ElectriMK, un mismo requerimiento técnico (por ejemplo, un *contactor trifásico de 25 A* o un *interruptor termomagnético de 100 A*) puede ser satisfecho por múltiples fabricantes con calidades homologadas (Schneider Electric, Siemens, ABB, WEG y Weidmüller). 

Al tratarse de una empresa en fase de inicio y consolidación comercial, **no se dispone de una integración en tiempo real con un sistema ERP o WMS centralizado de bodega**. En este contexto, el presente informe formaliza la decisión de descartar categóricamente la selección aleatoria o estocástica de marcas y documenta la implementación de la **Estrategia de Telemetría de Demanda Empírica (Opción 4)**, un mecanismo auto-adaptativo que registra las intenciones de compra en WhatsApp para optimizar el ordenamiento de respuestas y brindar inteligencia de compras para la adquisición de inventario físico.

---

## 2. Justificación: Por qué la Aleatoriedad es Inviable

| Dimensión | Selección Aleatoria (Azar) | Telemetría de Demanda Empírica (Opción 4) |
| :--- | :--- | :--- |
| **Consistencia ante el Cliente** | Pésima. Cotizar el mismo producto por la mañana y por la tarde produce marcas y referencias distintas, generando desconfianza. | Alta. Ofrece la solución de mayor tracción comercial con total consistencia. |
| **Estrategia de Capital de Trabajo** | Nula. Ignora qué productos se venden y cuáles quedan estancados. | Estratégica. Informa a la gerencia qué productos exactos demandan los clientes en Guayaquil. |
| **Autoridad del Asesor** | Débil. Proyecta una postura indecisa y desordenada. | Consultiva. Recomienda con solvencia la solución estándar y abre la puerta a marcas homologadas. |
| **Sustentación ante el Jurado** | Indefendible. La aleatoriedad carece de rigor en ingeniería de software. | Sobresaliente. Se fundamenta en *Adaptive Information Retrieval* y *Demand Mining*. |

---

## 3. Arquitectura del Sistema de Telemetría

```
[Mensaje Cliente WhatsApp] 
         │
         ▼
[Motor FTS5 + BM25] ──► Ordenamiento Híbrido: (rank ASC, SearchCount DESC)
         │
         ▼
[Candidatos Óptimos] ──► Inyección en Contexto RAG a Gemini
         │
         ├──► Retorno Inmediato de Respuesta (< 2 segundos)
         │
         └──► [Segundo Plano Asíncrono - Cero Latencia]
                     │
                     ├──► UPDATE ProductsCatalog SET SearchCount = SearchCount + 1
                     └──► INSERT INTO ProductSearchAnalytics (Código, Marca, Familia, Cliente)
```

### 3.1. Esquema Relacional de Base de Datos
1. **Atributos en `ProductsCatalog`:**
   - `SearchCount INTEGER DEFAULT 0`: Acumulador histórico de veces que el producto formó parte de una cotización exitosa.
   - `LastQueriedAt DATETIME`: Marca temporal de la última vez que fue solicitado.

2. **Tabla de Eventos Transaccionales (`ProductSearchAnalytics`):**
   ```sql
   CREATE TABLE IF NOT EXISTS ProductSearchAnalytics (
       Id INTEGER PRIMARY KEY AUTOINCREMENT,
       ProductCode TEXT NOT NULL,
       Brand TEXT NOT NULL,
       Family TEXT NOT NULL,
       Series TEXT,
       QueryTerm TEXT NOT NULL,
       CustomerNumber TEXT,
       CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
   );
   CREATE INDEX IF NOT EXISTS idx_analytics_code ON ProductSearchAnalytics (ProductCode);
   CREATE INDEX IF NOT EXISTS idx_analytics_family ON ProductSearchAnalytics (Family);
   CREATE INDEX IF NOT EXISTS idx_analytics_brand ON ProductSearchAnalytics (Brand);
   CREATE INDEX IF NOT EXISTS idx_analytics_created ON ProductSearchAnalytics (CreatedAt);
   ```

3. **Optimización de Desempeño y Prevención de Churn FTS5:**
   En SQLite FTS5 con tablas externas (`content='ProductsCatalog'`), un disparador convencional `AFTER UPDATE` provocaría la reindexación innecesaria de todo el índice de búsqueda en cada consulta. Para evitarlo, el disparador se limitó estrictamente a las columnas de contenido técnico:
   ```sql
   CREATE TRIGGER trg_products_update 
   AFTER UPDATE OF Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application 
   ON ProductsCatalog BEGIN ... END;
   ```
   *Resultado:* La actualización del contador de demanda se ejecuta en $<0.5\text{ ms}$ sin penalizar el rendimiento del servidor.

---

## 4. Algoritmo de Decisión Comercial en Consultas Genéricas

Cuando un cliente solicita un equipo sin especificar fabricante (*"necesito un contactor de 25A en 220V"* o *"breaker trifásico de 50A"*):

1. **Fase 1 (Recuperación Léxico-Probabilística):**
   El motor FTS5 extrae los candidatos que satisfacen los parámetros técnicos mediante BM25.
2. **Fase 2 (Ponderación por Tracción de Mercado):**
   La consulta SQL ordena los resultados priorizando el menor `rank` (mayor relevancia léxica) y desempatando por `SearchCount DESC`. Aquellos productos que los clientes de la distribuidora han consultado más veces se ubican en la primera posición.
3. **Fase 3 (Técnica Comercial del Anclaje y Alternativa en Prompt):**
   Gemini presenta la solución líder con seguridad técnica, indicando su aplicación y fiabilidad, y cierra con una pregunta orientativa:
   > *"Te recomendamos nuestra opción de alta rotación en **[Marca] [Modelo]**, ideal para este tipo de aplicación por su fiabilidad y disponibilidad.*  
   > *¿Tu proyecto exige alguna marca específica homologada (como Schneider, Siemens, ABB o WEG), o procedemos con esta opción recomendada para tu proforma?"*
4. **Fase 4 (Derivación Humana):**
   La validación final de existencias físicas se deriva formalmente a la *Ing. Kely Pacalla*, garantizando que no se comprometan entregas sin confirmación de bodega.

---

## 5. Inteligencia de Negocios para Adquisición de Inventario (Compras)

Para una empresa en fase de despegue como Power ElectriMK, este módulo aporta una ventaja operativa trascendental: **resuelve la incertidumbre sobre en qué productos invertir el capital de trabajo**.

Se habilitó el endpoint de analítica:
`GET /api/analytics/demanda`

El cual entrega en formato estructurado:
* **Top 20 Productos Más Demandados:** Permite ordenar pedidos de reposición prioritaria.
* **Distribución de Demanda por Marca:** Identifica la afinidad de la cartera de clientes de Guayaquil (e.g., preferencia de WEG en arranque y motores vs. Schneider en distribución modular).
* **Demanda por Familia Técnica:** Muestra qué líneas presentan mayor volumen de consulta (Contactores, Variadores, Breakers de Caja Moldeada, etc.).

---

## 6. Conclusión y Aporte a la Tesis

La implementación de la **Opción 4** transforma al agente de un simple procesador conversacional a un **sistema inteligente adaptativo con capacidad de aprendizaje de mercado**. Se alinea de manera óptima con los objetivos académicos de la titulación al evidenciar diseño de software robusto, mitigación de cuellos de botella mediante microtransacciones asíncronas y resolución metodológica de restricciones del mundo real sin incurrir en costos de licencias ERP de gran escala.
