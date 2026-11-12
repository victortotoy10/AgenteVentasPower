# Análisis Técnico, Metodológico y Estratégico: Roadmap de Evolución del Agente Conversacional en Power Electrimk

---

## 1. Resumen Ejecutivo y Veredicto de Viabilidad

> **Veredicto Global:** La incorporación de **reconocimiento de imágenes**, **pase a humano (human handoff)**, **seguimiento automatizado (follow-up)** y **conexión a CRM** es **100% correcta, técnicamente viable y de altísimo valor comercial para Power Electrimk**. 
> Sin embargo, para efectos del **Anteproyecto de Titulación en la Universidad Politécnica Salesiana (UPS)**, se debe aplicar una **estrategia de desacoplamiento de alcance** para evitar objeciones por *scope creep* (desbordamiento de horas de trabajo) ante el tribunal evaluador.

| Capacidad Propuesta | Viabilidad Técnica | Esfuerzo Estimado | Pertinencia en Titulación (400 h) | Ubicación Estratégica Recomendada |
| :--- | :---: | :---: | :---: | :--- |
| **1. Reconocimiento de Imágenes** | **Muy Alta** | Media (30 h) | Alta (demostrable) | Módulo Multimodal de Extensión / Validación |
| **2. Pase a Humano (Handoff)** | **Muy Alta** | Baja (15 h) | Muy Alta (resuelve casos borde) | Control de Excepciones del Núcleo |
| **3. Seguimiento Comercial** | **Alta** | Baja (15 h) | Media (orientado a negocio) | Servicio en Segundo Plano (Fase 2) |
| **4. Conexión / Creación de CRM** | **Media** | Muy Alta (si es desde cero) | Peligrosa si es desde cero | **Conector vía Webhooks / API REST** |

---

## 2. Análisis Técnico Paso a Paso de las Nuevas Capacidades

### 2.1. Reconocimiento de Imágenes Multimodal (Computer Vision aplicada a Materiales Eléctricos)

#### El Problema Operativo Real:
En las distribuidoras eléctricas de Guayaquil, maestros instaladores y electricistas de obra no siempre conocen el código de fábrica exacto (*SKU*). Lo habitual es que tomen una fotografía con su teléfono a:
1. Una pieza dañada o quemada que necesitan reemplazar.
2. La placa metálica de características técnicas de un disyuntor, contactor o transformador.
3. El calibre impreso sobre la cubierta de un cable conductor.

#### Ventaja de la Arquitectura Seleccionada:
* **Cero entrenamiento de modelos locales:** No se requiere entrenar un modelo convolucional propio (YOLO, ResNet) ni alquilar instancias con GPU en la nube.
* **Aprovechamiento de Gemini 1.5 Flash:** Al ser un modelo fundacional multimodal nativo, procesa imágenes a un costo insignificante (~$0.00002 USD por imagen) y con latencia inferior a 1.5 segundos.
* **Extracción Guiada por System Prompt:** Se instruye al modelo para que responda exclusivamente un JSON con los atributos detectados:
  ```json
  {
    "tipo_producto": "Disyuntor termomagnético",
    "marca_detectada": "Schneider Electric",
    "amperaje": "20A",
    "polos": 1,
    "confianza_extraccion": 0.95
  }
  ```
* Ese JSON alimenta de inmediato la consulta indexada en SQLite, garantizando que el precio emitido sea el oficial de Power Electrimk.

---

### 2.2. Sistema de Pase a Humano (Human-in-the-Loop / Handoff)

#### Por qué es indispensable en ingeniería de software:
Ningún agente inteligente autónomo debe operar sin una válvula de escape. En ventas B2B de materiales eléctricos existen escenarios donde la IA **no debe cerrar la venta sola**:
* Solicitudes de crédito comercial o plazos de pago a 30/60 días.
* Cotizaciones de gran volumen (proyectos de edificios o urbanizaciones con descuentos especiales).
* Reclamos técnicos o frustración detectada en el usuario.

#### Arquitectura de Estados en .NET 8 (State Pattern):
Se gestiona el estado de cada sesión en la base de datos SQLite embebida:
* **`BotActivo`:** El agente responde cotizaciones de catálogo automáticamente.
* **`HandoffSolicitado`:** Se detecta intención de crédito o compra mayorista.
* **`HumanoActivo`:** El asesor comercial toma la conversación en WhatsApp.
* **Mecanismo de Alerta:** Cuando el estado pasa a `HandoffSolicitado`, el backend emite una notificación instantánea (vía webhook interno, mensaje a un grupo de WhatsApp de vendedores o correo) indicando la necesidad de intervención.

---

### 2.3. Motor de Seguimiento Automatizado (Follow-up Engine)

#### El Problema Comercial:
Más del 60% de las cotizaciones emitidas por WhatsApp se enfrían porque el asesor comercial olvida hacer seguimiento al día siguiente.

#### Implementación Técnica Ligera:
* Se implementa un **`BackgroundService` (Worker asíncrono)** nativo en .NET 8 que corre periódicamente inspeccionando SQLite.
* **Regla de negocio:** Si una sesión tiene una cotización generada, no tiene mensajes posteriores en 24 horas hábiles y no se ha cerrado la venta, se dispara un mensaje de re-contacto amable:
  > *"Hola [Nombre], ¿deseas que coordinemos el despacho de los materiales cotizados o requieres alguna asesoría técnica adicional con un asesor?"*

---

### 2.4. Conexión a CRM vs. Creación de un CRM Propio

> **Advertencia Crítica de Alcance:**
> Intentar programar un CRM completo desde cero (con autenticación, roles, embudos de venta, reportería, facturación y UI web) dentro de un proyecto de titulación de dos personas es un **error clásico de desbordamiento de alcance** que los tribunales de la UPS objetan.

#### La Solución de Ingeniería Correcta:
1. **No programar un CRM monolítico:** El objetivo del anteproyecto es el **agente conversacional inteligente**, no la reinvención de un software administrativo.
2. **Implementar una Arquitectura de Conectores (API Gateway / Webhooks):**
   * Se crea una interfaz en C#: `ICrmIntegrationService`.
   * Permite disparar eventos asíncronos cuando se emite una cotización exportando JSON estructurado hacia el CRM que use Power Electrimk (HubSpot, Zoho, Odoo) o hacia un almacenamiento relacional que consuma su sistema contable.

---

## 3. Estrategia Académica para la Defensa del Anteproyecto (UPS Sede Guayaquil)

### Cómo presentar esto ante el Director y el Tribunal:

1. **El Núcleo Contractual de Titulación (Las 400 horas obligatorias):**
   * Agente conversacional asíncrono en .NET 8 conectado a WhatsApp Cloud API.
   * Motor de recuperación determinista local en SQLite con registro WAL sobre catálogo de Power Electrimk.
   * Inferencia en lenguaje natural gobernada por Gemini 1.5.
   * Validación experimental de 50 casos de prueba ($Acc_{\text{cot}} \ge 95\%$, $H_{\text{rate}} = 0\%$, $P95 < 4.0\text{ s}$, $\text{RAM} < 250\text{ MB}$).

2. **La Extensión de Ingeniería (Roadmap / Arquitectura Preparada):**
   * En el capítulo de arquitectura de software, se demuestra que el código cumple con los principios **SOLID** y **Clean Architecture**.
   * Se presenta el diagrama de componentes donde los módulos de **Visión Multimodal**, **Pase a Humano**, **Seguimiento** y **CRM** entran como servicios desacoplados mediante inyección de dependencias (`Dependency Injection`).
   * Esto demuestra ante el tribunal una madurez de diseño superior a la media de anteproyectos sin poner en riesgo el cronograma de titulación.

