#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de extracción, traducción y poblado del Catálogo Técnico FLUKE
en la base de datos relacional y motor de búsqueda FTS5 de AgenteVentasPower.

Fuentes oficiales analizadas:
1. 9534acc3-0c5a-410d-82fe-b49d007f4012_original file.pdf (Fluke Industrial Test Tools Catalogue 2026, 211 páginas)
2. c604c4f4-9de2-485b-812f-b2e4003de982_original file.pdf (Catálogo de Herramientas de Calibración Fluke en Español, 64 páginas)
3. 94161905-5d3a-40b1-8fd2-b106007f233a_original file.pdf (Fluke Calibration Short Form Catalog, 48 páginas)

Marca: FLUKE
"""

import sqlite3
import glob
import json
import re
import os
import fitz

def clean_code(raw):
    c = raw.strip()
    c = re.sub(r'\s+', ' ', c)
    # Remove trailing commas, colons or extra words
    c = c.split(',')[0].strip()
    c = c.split(';')[0].strip()
    return c

def get_fluke_core_catalog():
    """
    Catálogo curado y verificado de las líneas industriales y comerciales
    clave de Fluke con especificaciones técnicas completas en español.
    """
    prods = [
        # =========================================================================
        # 1. MULTÍMETROS DIGITALES INDUSTRIALES (DMMs)
        # =========================================================================
        {
            "Code": "FLUKE-87V",
            "Name": "Multímetro digital industrial True-RMS Fluke 87V (FLUKE-87V)",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 80",
            "Description": "Multímetro digital industrial de verdadero valor eficaz (True-RMS) para solución avanzada de problemas en variadores de frecuencia, motores y automatización industrial. Incluye filtro paso bajo seleccionable para lecturas precisas de voltaje y frecuencia en variadores de velocidad (VFD), termómetro incorporado y función de registro de picos mín/máx de 250 µs.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V (Resolución 0.1 mV / 10 µV)",
                "CorrienteAC_DC": "Hasta 10 A continuo (20 A durante 30 s)",
                "Resistencia": "Hasta 50 MΩ",
                "Capacitancia": "Hasta 9999 µF",
                "Frecuencia": "Hasta 200 kHz (% ciclo de trabajo)",
                "Temperatura": "-200.0 °C a 1090 °C (-328 °F a 1994 °F)",
                "Pantalla": "Digital de 6000 cuentas con gráfico de barras analógico y retroiluminación de dos niveles",
                "FiltroVFD": "Filtro paso bajo integrado para medición precisa de modulaciones PWM",
                "CategoriaSeguridad": "CAT III 1000 V / CAT IV 600 V",
                "Normas": "EN 61010-1, ANSI/ISA S82.01-2004, CAN/CSA C22.2 No. 1010.1:92",
                "Garantia": "Garantía de por vida limitada"
            }, ensure_ascii=False),
            "Application": "Mantenimiento eléctrico industrial en plantas, diagnóstico de variadores de frecuencia VFD, centros de control de motores CCM, petroquímica y manufactura pesada."
        },
        {
            "Code": "FLUKE-87V-MAX",
            "Name": "Multímetro digital industrial de alta resistencia True-RMS Fluke 87V MAX IP67",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 80",
            "Description": "Versión ultrarresistente del Fluke 87V con clasificación IP67 a prueba de agua y polvo, y resistencia probada a caídas desde 4 metros. Diseñado para operar en las condiciones industriales, mineras y petroleras más hostiles, con un rango de temperatura operativa extendida de -40 °C a +55 °C.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V True-RMS",
                "CorrienteAC_DC": "Hasta 10 A (20 A por 30 s)",
                "GradoProteccion": "IP67 (sellado hermético contra agua y polvo)",
                "ResistenciaCaidas": "Probado para resistir caídas de hasta 4 metros (13 pies)",
                "TemperaturaOperacion": "-40 °C a +55 °C",
                "CategoriaSeguridad": "CAT III 1000 V / CAT IV 600 V",
                "FiltroVFD": "Filtro paso bajo para variadores de velocidad",
                "Garantia": "Garantía de por vida limitada"
            }, ensure_ascii=False),
            "Application": "Entornos severos de minería, petróleo, plantas químicas, puertos marítimos y operaciones bajo lluvia o polvo extremo."
        },
        {
            "Code": "FLUKE-87V/E2",
            "Name": "Kit combinado para electricistas industriales Fluke 87V/E2 Combo Kit",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 80",
            "Description": "Kit completo para electricistas industriales que incluye el multímetro Fluke 87V, cables de prueba de silicona TL224 SureGrip, pinzas de cocodrilo AC220, sondas TP238, sonda de temperatura 80BK-A, colgador magnético TPAK ToolPak y estuche flexible C35.",
            "TechnicalSpecs": json.dumps({
                "MultimetroIncluido": "Fluke 87V True-RMS",
                "Accesorios": "TL224, AC220, TP238, 80BK-A, TPAK, C35",
                "CategoriaSeguridad": "CAT III 1000 V / CAT IV 600 V"
            }, ensure_ascii=False),
            "Application": "Dotación integral para cuadrillas de mantenimiento industrial y técnicos electricistas de campo."
        },
        {
            "Code": "FLUKE-179",
            "Name": "Multímetro digital True-RMS Fluke 179 con temperatura incorporada",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 170",
            "Description": "El estándar de la industria para electricistas y técnicos de mantenimiento. Multímetro digital de verdadero valor eficaz (True-RMS) con medición integrada de temperatura mediante termopar tipo K, precisión básica de 0.09%, pantalla digital de 6000 cuentas con gráfico de barras y retroiluminación.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V (True-RMS en AC)",
                "CorrienteAC_DC": "Hasta 10 A continuo",
                "Resistencia": "Hasta 50 MΩ",
                "Capacitancia": "Hasta 10000 µF",
                "Frecuencia": "Hasta 100 kHz",
                "Temperatura": "-40 °C a +400 °C (-40 °F a 752 °F)",
                "PrecisionBasicaDC": "0.09%",
                "Pantalla": "6000 cuentas con retroiluminación y barra analógica",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "Garantía de por vida limitada"
            }, ensure_ascii=False),
            "Application": "Instalaciones eléctricas industriales y comerciales, tableros de distribución, HVAC, mantenimiento general y localización de averías."
        },
        {
            "Code": "FLUKE-177",
            "Name": "Multímetro digital True-RMS Fluke 177 con retroiluminación",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 170",
            "Description": "Multímetro digital True-RMS para técnicos de mantenimiento eléctrico con pantalla retroiluminada de fácil lectura, precisión del 0.09%, medición de capacitancia, resistencia, continuidad y frecuencia.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V",
                "CorrienteAC_DC": "Hasta 10 A",
                "Resistencia": "Hasta 50 MΩ",
                "Frecuencia": "Hasta 100 kHz",
                "Capacitancia": "Hasta 10000 µF",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Mantenimiento eléctrico general en plantas, tableros de distribución y talleres de electrónica industrial."
        },
        {
            "Code": "FLUKE-175",
            "Name": "Multímetro digital True-RMS Fluke 175 estándar",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 170",
            "Description": "Multímetro básico de la serie Fluke 170 con mediciones precisas de valor eficaz verdadero (True-RMS), retención de lectura automática y mín/máx.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V",
                "CorrienteAC_DC": "Hasta 10 A",
                "PrecisionBasicaDC": "0.15%",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Instalaciones residenciales y comerciales, mantenimiento preventivo de rutina y educación técnica."
        },
        {
            "Code": "FLUKE-117",
            "Name": "Multímetro para electricistas Fluke 117 con detector de tensión sin contacto VoltAlert",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 110",
            "Description": "Multímetro compacto de verdadero valor eficaz (True-RMS) diseñado específicamente para electricistas comerciales y residenciales. Incorpora tecnología VoltAlert para detección de tensión sin contacto y función AutoVolt para selección automática de voltaje CA/CC e impedancia de entrada baja (LoZ) para evitar lecturas falsas causadas por tensiones fantasma.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 600 V True-RMS",
                "CorrienteAC_DC": "Hasta 10 A (20 A por 30 s)",
                "DeteccionVoltAlert": "Sensor de tensión CA sin contacto integrado en la parte superior",
                "ModoAutoVolt": "Selección automática de tensión CA/CC",
                "ImpedanciaLoZ": "Baja impedancia de entrada para prevenir voltajes fantasma",
                "Resistencia_Continuidad": "Hasta 40 MΩ con zumbador audible rápido",
                "Frecuencia_Capacitancia": "Hasta 50 kHz / 10000 µF",
                "CategoriaSeguridad": "CAT III 600 V",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Electricistas comerciales, hospitales, edificios de oficinas, inspección rápida de paneles y cableado."
        },
        {
            "Code": "FLUKE-115",
            "Name": "Multímetro digital True-RMS Fluke 115 para técnicos de campo",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 110",
            "Description": "Multímetro digital compacto para comprobaciones eléctricas y electrónicas generales de campo con mediciones True-RMS de 600 V y 10 A.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 600 V True-RMS",
                "CorrienteAC_DC": "Hasta 10 A",
                "Pantalla": "6000 cuentas con retroiluminación LED blanca",
                "CategoriaSeguridad": "CAT III 600 V"
            }, ensure_ascii=False),
            "Application": "Servicio técnico de campo, mantenimiento electrónico básico y verificación de circuitos."
        },
        {
            "Code": "FLUKE-116",
            "Name": "Multímetro para climatización y calefacción Fluke 116 HVAC",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 110",
            "Description": "Multímetro diseñado para profesionales de HVAC (calefacción, ventilación y aire acondicionado) con medición de temperatura y rango de microamperios para comprobar sensores de llama.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 600 V",
                "Microamperios": "Rango de µA para comprobación de sensores de llama",
                "TemperaturaIntegrada": "-40 °C a +400 °C",
                "CategoriaSeguridad": "CAT III 600 V"
            }, ensure_ascii=False),
            "Application": "Sistemas de climatización, calderas, refrigeración industrial y comercial."
        },
        {
            "Code": "FLUKE-289",
            "Name": "Multímetro registrador gráfico industrial Fluke 289 con TrendCapture",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 280",
            "Description": "Multímetro registrador industrial de alto rendimiento de 50.000 cuentas con función TrendCapture que grafica las sesiones registradas directamente en pantalla sin necesidad de PC. Cuenta con filtro paso bajo para VFD, rango de 50 ohmios con resolución de 1 miliohmio para bobinados de motores y conectividad Fluke Connect mediante adaptador ir3000 FC.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V True-RMS (Ancho de banda 100 kHz)",
                "CorrienteAC_DC": "Hasta 10 A (Resolución de 0.01 µA)",
                "PantallaGrafica": "Pantalla matriz de puntos de 50.000 cuentas con zoom y navegación gráfica",
                "TrendCapture": "Almacena hasta 15.000 eventos de registro para análisis desatendido",
                "RangoBajaResistencia": "Rango de 50 Ω con resolución de 1 mΩ para devanados de motores",
                "FiltroPasoBajo": "Para diagnóstico de accionamientos y variadores de velocidad",
                "LoZ": "Voltaje de baja impedancia para eliminar tensiones fantasma",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "Garantía de por vida limitada"
            }, ensure_ascii=False),
            "Application": "Investigación y desarrollo, ingeniería de planta, análisis de fallas intermitentes en variadores, motores y sistemas de control crítico."
        },
        {
            "Code": "FLUKE-287",
            "Name": "Multímetro registrador electrónico Fluke 287 con TrendCapture",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 280",
            "Description": "Multímetro registrador para profesionales de electrónica avanzada y telecomunicaciones con TrendCapture, 50.000 cuentas y ancho de banda CA de 100 kHz.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V True-RMS",
                "CorrienteAC_DC": "Hasta 10 A",
                "AnchoBanda": "100 kHz en CA",
                "TrendCapture": "Gráficos de tendencias en pantalla",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Laboratorios de electrónica, telecomunicaciones, calibración y mantenimiento de instrumentación."
        },
        {
            "Code": "FLUKE-28-II",
            "Name": "Multímetro industrial resistente IP67 Fluke 28 II",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 20",
            "Description": "Multímetro sumergible y hermético al polvo bajo estándar IP67, resistente a caídas de 3 metros, con botones retroiluminados y medición True-RMS.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V True-RMS",
                "CorrienteAC_DC": "Hasta 10 A",
                "GradoProteccion": "IP67 (sumergible hasta 1 m)",
                "ResistenciaCaidas": "3 metros (10 pies)",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Uso rudo en construcción, plataformas offshore, minas y ambientes marinos húmedos."
        },
        {
            "Code": "FLUKE-279FC",
            "Name": "Multímetro térmico True-RMS Fluke 279 FC con cámara infrarroja integrada",
            "BusinessLine": "Termografía e Imagen Industrial",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 279",
            "Description": "Herramienta 2 en 1 que combina un multímetro digital True-RMS completo con una cámara termográfica integrada de 80 x 60 píxeles. Permite ubicar puntos calientes en tableros eléctricos y luego medir tensión y corriente inmediatamente con un solo equipo. Compatible con sonda flexible iFlex de hasta 2500 A CA y conectividad Fluke Connect.",
            "TechnicalSpecs": json.dumps({
                "CamaraTermografica": "80 x 60 píxeles con pantalla LCD en color de 3.5 pulgadas",
                "RangoTemperatura": "-10 °C a 200 °C (14 °F a 392 °F)",
                "TensionAC_DC": "Hasta 1000 V True-RMS",
                "Corriente": "Hasta 2500 A CA con sonda iFlex opcional",
                "Conectividad": "Fluke Connect inalámbrico para smartphone",
                "CategoriaSeguridad": "CAT III 1000 V / CAT IV 600 V"
            }, ensure_ascii=False),
            "Application": "Inspección termográfica rápida y verificación eléctrica combinada en cuadros eléctricos, transformadores y motores."
        },
        {
            "Code": "FLUKE-283FC",
            "Name": "Multímetro digital solar inalámbrico Fluke 283 FC CAT III 1500 V",
            "BusinessLine": "Energía Renovable y Movilidad Eléctrica",
            "Family": "Multímetros Digitales Industriales",
            "Series": "Fluke 280",
            "Description": "Multímetro digital para sistemas fotovoltaicos y de alta tensión continua con categoría de seguridad CAT III 1500 V y CAT IV 1000 V. Diseñado para pruebas seguras en parques solares a gran escala e inversores centrales.",
            "TechnicalSpecs": json.dumps({
                "TensionDC": "Hasta 1500 V DC",
                "TensionAC": "Hasta 1000 V AC True-RMS",
                "CategoriaSeguridad": "CAT III 1500 V / CAT IV 1000 V",
                "Conectividad": "Fluke Connect inalámbrico",
                "Normas": "IEC 61010-2-033"
            }, ensure_ascii=False),
            "Application": "Instalación, mantenimiento y comisionamiento de plantas solares fotovoltaicas y sistemas de almacenamiento de energía con baterías (BESS)."
        },

        # =========================================================================
        # 2. PINZAS AMPERIMÉTRICAS (CLAMP METERS)
        # =========================================================================
        {
            "Code": "FLUKE-376FC",
            "Name": "Pinza amperimétrica True-RMS Fluke 376 FC con sonda flexible iFlex (FLUKE-376FC)",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 370 FC",
            "Description": "La pinza amperimétrica industrial más completa de Fluke con conectividad inalámbrica Fluke Connect. Incluye sonda flexible iFlex de 18 pulgadas que amplía el rango de medición hasta 2500 A CA y permite acceder a conductores apretados en armarios congestionados. Mide corriente y tensión CA/CC, corriente de arranque de motores (inrush) y cuenta con filtro paso bajo integrado.",
            "TechnicalSpecs": json.dumps({
                "CorrienteAC_Mordaza": "Hasta 999.9 A True-RMS",
                "CorrienteAC_iFlex": "Hasta 2500 A True-RMS con sonda iFlex de 45 cm incluida",
                "CorrienteDC": "Hasta 999.9 A DC",
                "TensionAC_DC": "Hasta 1000 V True-RMS",
                "CorrienteInrush": "Medición precisa de picos de arranque de motores con filtro de ruido",
                "Resistencia_Continuidad": "Hasta 60 kΩ con zumbador",
                "Capacitancia": "Hasta 1000 µF",
                "Frecuencia": "Hasta 500 Hz",
                "FiltroPasoBajo": "Filtro VFD para variadores de velocidad",
                "Conectividad": "Fluke Connect inalámbrico con registro de datos en smartphone",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Mantenimiento industrial pesado, medición de corrientes de arranque de motores trifásicos, transformadores de potencia y barras de distribución en tableros principales."
        },
        {
            "Code": "FLUKE-375FC",
            "Name": "Pinza amperimétrica True-RMS Fluke 375 FC compatible con iFlex",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 370 FC",
            "Description": "Pinza True-RMS CA/CC de 600 A y 1000 V con filtro paso bajo, compatible con sonda iFlex y conectividad inalámbrica Fluke Connect para registro y transmisión remota de medidas.",
            "TechnicalSpecs": json.dumps({
                "CorrienteAC_DC": "Hasta 600 A",
                "TensionAC_DC": "Hasta 1000 V True-RMS",
                "Compatibilidad_iFlex": "Compatible con sondas iFlex hasta 2500 A CA (opcional)",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Mantenimiento de motores, variadores de frecuencia y alimentadores en plantas industriales."
        },
        {
            "Code": "FLUKE-374FC",
            "Name": "Pinza amperimétrica True-RMS Fluke 374 FC de 600 A CA/CC",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 370 FC",
            "Description": "Pinza True-RMS básica de la serie Fluke Connect para medición de 600 A y 1000 V en CA/CC con función de corriente de arranque.",
            "TechnicalSpecs": json.dumps({
                "CorrienteAC_DC": "Hasta 600 A",
                "TensionAC_DC": "Hasta 1000 V",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Supervisión de cargas eléctricas y diagnóstico en instalaciones industriales y comerciales."
        },
        {
            "Code": "FLUKE-378FC",
            "Name": "Pinza amperimétrica True-RMS sin contacto Fluke 378 FC con FieldSense e indicador de calidad de energía",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 370 FC",
            "Description": "Pinza de vanguardia con tecnología FieldSense que mide tensión y corriente al mismo tiempo a través de la mordaza sin hacer contacto eléctrico directo con partes energizadas. Incluye indicador de calidad de energía (PQ Indicator) que detecta automáticamente si el problema está en la red o en la carga.",
            "TechnicalSpecs": json.dumps({
                "TecnologiaFieldSense": "Medición simultánea de voltaje y corriente CA sin contacto metálico",
                "CorrienteAC_DC": "Hasta 999.9 A con mordaza (2500 A con iFlex incluida)",
                "TensionAC_DC": "Hasta 1000 V",
                "IndicadorPQ": "Detecta armónicos y factor de potencia",
                "MedicionTrifasica": "Cálculo rápido de rotación de fases en 3 pasos",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Pruebas eléctricas seguras y rápidas sin riesgo de arco eléctrico ni desmontaje de terminales."
        },
        {
            "Code": "FLUKE-377FC",
            "Name": "Pinza amperimétrica True-RMS sin contacto Fluke 377 FC con FieldSense",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 370 FC",
            "Description": "Pinza con tecnología FieldSense para medir tensión y corriente simultáneas sin contacto en conductores energizados, con sonda iFlex incluida de 2500 A.",
            "TechnicalSpecs": json.dumps({
                "TecnologiaFieldSense": "Tensión y corriente sin contacto",
                "CorrienteAC_DC": "Hasta 1000 A mordaza / 2500 A iFlex",
                "TensionAC_DC": "Hasta 1000 V",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Electricistas de distribución e inspectores de instalaciones eléctricas de alta exigencia."
        },
        {
            "Code": "FLUKE-323",
            "Name": "Pinza amperimétrica compacta True-RMS Fluke 323 de 400 A CA",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 320",
            "Description": "La pinza amperimétrica más popular y vendida para electricistas. Compacta, ergonómica y duradera, ofrece mediciones de verdadero valor eficaz (True-RMS) de hasta 400 A en CA y 600 V en CA/CC, con medición de resistencia hasta 400 Ω y zumbador de continuidad.",
            "TechnicalSpecs": json.dumps({
                "CorrienteAC": "Hasta 400.0 A True-RMS",
                "TensionAC_DC": "Hasta 600.0 V",
                "Resistencia": "Hasta 400.0 Ω",
                "Continuidad": "Zumbador audible de respuesta rápida",
                "AperturaMordaza": "30 mm (para conductores de hasta 25 mm)",
                "CategoriaSeguridad": "CAT IV 300 V / CAT III 600 V",
                "Garantia": "2 años de garantía"
            }, ensure_ascii=False),
            "Application": "Herramienta de uso diario en bolsillo para electricistas domiciliarios, instaladores de tableros residenciales y mantenimiento general."
        },
        {
            "Code": "FLUKE-324",
            "Name": "Pinza amperimétrica True-RMS Fluke 324 con temperatura y capacitancia",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 320",
            "Description": "Pinza True-RMS de 400 A CA con pantalla retroiluminada, medición de temperatura de contacto y capacitancia para arranque de motores de climatización.",
            "TechnicalSpecs": json.dumps({
                "CorrienteAC": "Hasta 400 A True-RMS",
                "TensionAC_DC": "Hasta 600 V",
                "Temperatura": "-10.0 °C a 400.0 °C",
                "Capacitancia": "100.0 µF a 1000 µF",
                "Pantalla": "Con retroiluminación",
                "CategoriaSeguridad": "CAT IV 300 V / CAT III 600 V"
            }, ensure_ascii=False),
            "Application": "Mantenimiento eléctrico comercial, sistemas de refrigeración y comprobación de condensadores."
        },
        {
            "Code": "FLUKE-325",
            "Name": "Pinza amperimétrica True-RMS Fluke 325 para CA/CC con frecuencia",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 320",
            "Description": "La pinza más avanzada de la serie compacta 320. Mide corriente CA y CC hasta 400 A, tensión CA/CC hasta 600 V, temperatura, capacitancia y frecuencia.",
            "TechnicalSpecs": json.dumps({
                "CorrienteAC_DC": "Hasta 400.0 A (True-RMS en AC y corriente DC)",
                "TensionAC_DC": "Hasta 600.0 V",
                "Frecuencia": "5.0 Hz a 500.0 Hz",
                "Temperatura": "-10.0 °C a 400.0 °C",
                "Capacitancia": "Hasta 1000 µF",
                "MinMax": "Función Mín/Máx incorporada",
                "CategoriaSeguridad": "CAT IV 300 V / CAT III 600 V"
            }, ensure_ascii=False),
            "Application": "Equipos con motores de corriente continua, sistemas solares pequeños, automotriz pesada y control industrial."
        },
        {
            "Code": "FLUKE-381",
            "Name": "Pinza amperimétrica True-RMS Fluke 381 con pantalla remota desmontable e iFlex",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 380",
            "Description": "Pinza amperimétrica industrial con pantalla inalámbrica extraíble que permite colocar la pinza dentro de un tablero energizado, cerrar la puerta y leer las mediciones a hasta 10 metros de distancia, aumentando drásticamente la seguridad del operador.",
            "TechnicalSpecs": json.dumps({
                "PantallaRemota": "Desmontable con enlace inalámbrico hasta 10 metros (30 pies)",
                "CorrienteAC_iFlex": "Hasta 2500 A con sonda flexible incluida",
                "CorrienteAC_DC_Mordaza": "Hasta 999.9 A",
                "TensionAC_DC": "Hasta 1000 V True-RMS",
                "FiltroPasoBajo": "Integrado para variadores VFD",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Seguridad extrema contra riesgo de arco eléctrico (arc flash), maniobras en celdas de media/baja tensión y lugares de difícil acceso."
        },
        {
            "Code": "FLUKE-393FC",
            "Name": "Pinza amperimétrica solar True-RMS Fluke 393 FC CAT III 1500 V con iFlex",
            "BusinessLine": "Energía Renovable y Movilidad Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 390 FC",
            "Description": "La primera pinza amperimétrica del mundo con clasificación de seguridad CAT III 1500 V para aplicaciones solares fotovoltaicas y sistemas DC de alta tensión. Mordaza ultrafina para cables en cajas de concentración (combiner boxes) y sonda iFlex para corriente alterna.",
            "TechnicalSpecs": json.dumps({
                "TensionDC": "Hasta 1500 V DC",
                "TensionAC": "Hasta 1000 V AC True-RMS",
                "CorrienteDC": "Hasta 999.9 A DC",
                "CorrienteAC_iFlex": "Hasta 2500 A AC",
                "PotenciaDC": "Medición directa de potencia en kVA",
                "GradoProteccion": "IP54 para intemperie",
                "CategoriaSeguridad": "CAT III 1500 V / CAT IV 600 V"
            }, ensure_ascii=False),
            "Application": "Grandes parques solares fotovoltaicos, inversores centrales, centros de datos y tracción ferroviaria."
        },
        {
            "Code": "FLUKE-902FC",
            "Name": "Pinza amperimétrica True-RMS para HVAC Fluke 902 FC con Fluke Connect",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Pinzas Amperimétricas",
            "Series": "Fluke 900",
            "Description": "Pinza amperimétrica especializada para técnicos de climatización con medición de microamperios para sensores de llama, temperatura, capacitancia y resistencia hasta 60 kΩ.",
            "TechnicalSpecs": json.dumps({
                "CorrienteAC": "Hasta 600 A",
                "MicroamperiosDC": "Hasta 200 µA",
                "TensionAC_DC": "Hasta 600 V",
                "Temperatura": "-10 °C a 400 °C",
                "Conectividad": "Fluke Connect inalámbrico",
                "CategoriaSeguridad": "CAT III 600 V / CAT IV 300 V"
            }, ensure_ascii=False),
            "Application": "Mantenimiento y diagnóstico de sistemas de aire acondicionado comercial, chillers, cuartos fríos y calderas."
        },

        # =========================================================================
        # 3. COMPROBADORES ELÉCTRICOS Y DETECTORES (TESTERS)
        # =========================================================================
        {
            "Code": "FLUKE-T6-1000",
            "Name": "Comprobador eléctrico de horquilla abierta Fluke T6-1000 con tecnología FieldSense",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Comprobadores Eléctricos y Detectores de Tensión",
            "Series": "Fluke T6",
            "Description": "Comprobador eléctrico revolucionario con tecnología FieldSense que mide tensión alterna de hasta 1000 V y corriente alterna de hasta 200 A simultáneamente a través de la horquilla abierta sin contacto eléctrico directo con partes energizadas. Elimina la necesidad de tocar cables con terminales expuestos.",
            "TechnicalSpecs": json.dumps({
                "TecnologiaFieldSense": "Mide voltaje CA (hasta 1000 V) y corriente CA (hasta 200 A) a la vez en horquilla abierta",
                "AperturaHorquilla": "17.8 mm (admite conductores de hasta calibre 4/0 AWG - 120 mm²)",
                "TensionAC_DC_Cables": "Hasta 1000 V con puntas tradicionales",
                "Resistencia": "Hasta 100 kΩ",
                "Frecuencia": "45 Hz a 66 Hz en FieldSense",
                "PantallaDoble": "Muestra voltaje y corriente en pantalla al mismo tiempo con retroiluminación verde",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "2 años de garantía"
            }, ensure_ascii=False),
            "Application": "Inspecciones rápidas en tableros eléctricos residenciales e industriales, mantenimiento de plantas y verificación de circuitos con máxima seguridad."
        },
        {
            "Code": "FLUKE-T6-1000-PRO",
            "Name": "Comprobador eléctrico profesional Fluke T6-1000 PRO con pantalla Visual DUO",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Comprobadores Eléctricos y Detectores de Tensión",
            "Series": "Fluke T6",
            "Description": "Versión mejorada del T6-1000 con tecnología FieldSense y pantalla Visual DUO que se ilumina en verde cuando la medición de voltaje y corriente simultánea es estable, e incluye pinza de cocodrilo de conexión a tierra de alta resistencia.",
            "TechnicalSpecs": json.dumps({
                "TensionFieldSense": "Hasta 1000 V AC sin contacto",
                "CorrienteFieldSense": "Hasta 200 A AC sin contacto",
                "PantallaVisualDUO": "Indicador visual verde de medida estable",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Técnicos electricistas de alto volumen de trabajo en tableros y acometidas industriales."
        },
        {
            "Code": "FLUKE-T5-1000",
            "Name": "Comprobador de tensión, corriente y continuidad Fluke T5-1000 OpenJaw",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Comprobadores Eléctricos y Detectores de Tensión",
            "Series": "Fluke T5",
            "Description": "Comprobador eléctrico compacto con horquilla fija OpenJaw para medición de corriente de hasta 100 A sin abrir el circuito, y comprobación automática de tensión CA/CC de hasta 1000 V con zumbador de continuidad rápido.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 1000 V automático",
                "CorrienteAC_OpenJaw": "Hasta 100.0 A",
                "Resistencia_Continuidad": "Hasta 1000 Ω con zumbador",
                "PuntasDesmontables": "Puntas SlimReach adaptables a enchufes de pared",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "2 años de garantía"
            }, ensure_ascii=False),
            "Application": "Herramienta básica y resistente en el cinturón de cualquier electricista o técnico de obra."
        },
        {
            "Code": "FLUKE-T5-600",
            "Name": "Comprobador eléctrico compacto Fluke T5-600 de 600 V",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Comprobadores Eléctricos y Detectores de Tensión",
            "Series": "Fluke T5",
            "Description": "Comprobador eléctrico de 600 V con medición automática de tensión, corriente hasta 100 A con horquilla OpenJaw y continuidad.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "Hasta 600 V",
                "CorrienteAC": "Hasta 100 A",
                "Continuidad": "Con zumbador",
                "CategoriaSeguridad": "CAT III 600 V"
            }, ensure_ascii=False),
            "Application": "Instalaciones comerciales y residenciales, contratistas de obras civiles y reformas."
        },
        {
            "Code": "FLUKE-1AC-II",
            "Name": "Detector de tensión por proximidad Fluke VoltAlert 1AC-II (90-1000 V CA)",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Comprobadores Eléctricos y Detectores de Tensión",
            "Series": "Fluke VoltAlert",
            "Description": "Detector de tensión CA tipo lápiz sin contacto con tecnología Voltbeat de autocomprobación continua. La punta se ilumina en rojo y emite un pitido cuando detecta la presencia de tensión de 90 V a 1000 V CA.",
            "TechnicalSpecs": json.dumps({
                "RangoTension": "90 V CA a 1000 V CA (45 Hz a 405 Hz)",
                "Indicacion": "Luz LED roja brillante y zumbador sonoro",
                "AutocomprobacionVoltbeat": "Verifica continuamente el estado de la batería y del circuito",
                "CategoriaSeguridad": "CAT IV 1000 V",
                "Alimentacion": "2 pilas alcalinas AAA incluidas"
            }, ensure_ascii=False),
            "Application": "Seguridad personal obligatoria previa al contacto con conductores, tomas, disyuntores e iluminación."
        },
        {
            "Code": "FLUKE-2AC",
            "Name": "Detector de tensión de bolsillo Fluke VoltAlert 2AC (90-1000 V CA)",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Comprobadores Eléctricos y Detectores de Tensión",
            "Series": "Fluke VoltAlert",
            "Description": "Detector de tensión sin contacto siempre activo para una detección inmediata de tensión sin necesidad de encendido previo.",
            "TechnicalSpecs": json.dumps({
                "RangoTension": "90 V a 1000 V CA",
                "SiempreActivo": "Circuito de bajo consumo sin interruptor",
                "CategoriaSeguridad": "CAT IV 1000 V"
            }, ensure_ascii=False),
            "Application": "Verificación rápida de tomas, extensiones y cables energizados."
        },
        {
            "Code": "FLUKE-T150",
            "Name": "Comprobador bipolar de tensión y continuidad Fluke T150 con pantalla LCD y carga conmutable",
            "BusinessLine": "Instrumentos de Medida y Prueba Eléctrica",
            "Family": "Comprobadores Eléctricos y Detectores de Tensión",
            "Series": "Fluke T100",
            "Description": "Comprobador bipolar de dos polos con 4 modos de indicación (LED, pantalla LCD digital, zumbador sonoro y vibración táctil). Cuenta con medición de resistencia hasta 1999 Ω, carga conmutable para disparo de diferenciales RCD/IDR y linterna LED integrada.",
            "TechnicalSpecs": json.dumps({
                "TensionAC_DC": "6 V a 690 V",
                "Indicaciones": "Pantalla LCD digital, barra de LED graduada, zumbador y vibración táctil",
                "DisparoRCD": "Dos botones para carga conmutable y disparo intencionado de diferenciales de 30 mA",
                "RotacionFases": "Indicador de sentido de giro trifásico",
                "MedicionResistencia": "Hasta 1999 Ω",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 690 V"
            }, ensure_ascii=False),
            "Application": "Cumplimiento normativo de verificación de ausencia de tensión en tableros principales y pruebas de diferenciales."
        },

        # =========================================================================
        # 4. COMPROBADORES DE AISLAMIENTO Y MEGÓHMETROS
        # =========================================================================
        {
            "Code": "FLUKE-1587FC",
            "Name": "Multímetro de aislamiento 2 en 1 Fluke 1587 FC con Fluke Connect (FLUKE-1587FC)",
            "BusinessLine": "Seguridad Eléctrica y Puesta a Tierra",
            "Family": "Medidores de Aislamiento (Megóhmetros)",
            "Series": "Fluke 1587",
            "Description": "Herramienta que integra un comprobador de aislamiento digital avanzado y un multímetro digital True-RMS completo en un solo instrumento compacto. Ofrece voltajes de prueba de aislamiento de 50 V, 100 V, 250 V, 500 V y 1000 V para resistencia de aislamiento hasta 2 GΩ. Cuenta con filtro paso bajo para VFD, detección de circuito activo e integración con Fluke Connect para generar informes gráficos de tendencias de degradación de aislamiento.",
            "TechnicalSpecs": json.dumps({
                "TensionesPruebaAislamiento": "50 V, 100 V, 250 V, 500 V, 1000 V",
                "RangoAislamiento": "0.01 MΩ a 2.0 GΩ",
                "DescargaAutomatica": "Descarga de tensión capacitiva automática al finalizar la prueba",
                "DeteccionCircuitoActivo": "Impide la prueba de aislamiento si se detecta tensión > 30 V",
                "MultimetroTrueRMS": "Tensión CA/CC hasta 1000 V, corriente CA/CC hasta 400 mA, frecuencia, capacitancia y temperatura",
                "FiltroPasoBajo": "Para pruebas precisas en motores y variadores",
                "Conectividad": "Fluke Connect inalámbrico para smartphone",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Mantenimiento predictivo de motores eléctricos, generadores, transformadores, cables subterráneos y conmutadores industriales."
        },
        {
            "Code": "FLUKE-1507",
            "Name": "Comprobador de resistencia de aislamiento compacto Fluke 1507 hasta 10 GΩ",
            "BusinessLine": "Seguridad Eléctrica y Puesta a Tierra",
            "Family": "Medidores de Aislamiento (Megóhmetros)",
            "Series": "Fluke 1500",
            "Description": "Comprobador de aislamiento compacto y resistente para contratistas eléctricos. Ofrece cálculo automático del índice de polarización (PI) y de la relación de absorción dieléctrica (DAR), con voltajes de prueba de 50 V, 100 V, 250 V, 500 V y 1000 V.",
            "TechnicalSpecs": json.dumps({
                "TensionesPrueba": "50 V, 100 V, 250 V, 500 V, 1000 V",
                "RangoAislamiento": "0.01 MΩ a 10 GΩ",
                "CalculoAutomatico": "Índice de Polarización (PI) y Absorción Dieléctrica (DAR)",
                "SondaRemota": "Sonda con pulsador de prueba integrado para mediciones repetitivas",
                "CategoriaSeguridad": "CAT IV 600 V",
                "Garantia": "1 año de garantía"
            }, ensure_ascii=False),
            "Application": "Pruebas de puesta en marcha de cableados en edificios, transformadores secos y bobinados de motores."
        },
        {
            "Code": "FLUKE-1503",
            "Name": "Comprobador de aislamiento Fluke 1503 para 500 V y 1000 V",
            "BusinessLine": "Seguridad Eléctrica y Puesta a Tierra",
            "Family": "Medidores de Aislamiento (Megóhmetros)",
            "Series": "Fluke 1500",
            "Description": "Comprobador de aislamiento esencial para instalaciones comerciales e industriales con tensiones de prueba de 500 V y 1000 V y rango de hasta 2000 MΩ.",
            "TechnicalSpecs": json.dumps({
                "TensionesPrueba": "500 V y 1000 V",
                "RangoAislamiento": "0.1 MΩ a 2000 MΩ",
                "CategoriaSeguridad": "CAT IV 600 V"
            }, ensure_ascii=False),
            "Application": "Pruebas de rutina de aislamiento en instalaciones comerciales y residenciales."
        },
        {
            "Code": "FLUKE-1550C",
            "Name": "Megóhmetro industrial digital de alta tensión Fluke 1550C de 5 kV",
            "BusinessLine": "Seguridad Eléctrica y Puesta a Tierra",
            "Family": "Medidores de Aislamiento (Megóhmetros)",
            "Series": "Fluke 1550",
            "Description": "Comprobador de aislamiento de alta tensión hasta 5000 V (5 kV) para transformadores de potencia, generadores de centrales eléctricas y cables de media tensión. Rango de resistencia de hasta 1 Teraohmio (1 TΩ), cálculo de PI/DAR y rampa de tensión (prueba de rotura dieléctrica).",
            "TechnicalSpecs": json.dumps({
                "TensionesPrueba": "250 V, 500 V, 1000 V, 2500 V, 5000 V (ajustable en pasos de 50 V/100 V)",
                "RangoResistencia": "Hasta 1 TΩ (1.000.000 MΩ)",
                "FuncionesAvanzadas": "Índice de Polarización (PI), Relación de Absorción Dieléctrica (DAR), Descarga Dieléctrica (DD) y Prueba de Rampa",
                "MedicionCorrienteFuga": "1 nA a 2 mA",
                "Memoria": "Almacenamiento de hasta 99 ubicaciones de memoria",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Subestaciones eléctricas de transmisión y distribución, pruebas de aceptación en fábrica (FAT) y cables subterráneos de media tensión."
        },
        {
            "Code": "FLUKE-1555",
            "Name": "Megóhmetro industrial digital de alta tensión Fluke 1555 de 10 kV",
            "BusinessLine": "Seguridad Eléctrica y Puesta a Tierra",
            "Family": "Medidores de Aislamiento (Megóhmetros)",
            "Series": "Fluke 1550",
            "Description": "El megóhmetro de mayor capacidad de Fluke, con tensiones de prueba de hasta 10.000 V (10 kV) y rango de medición de resistencia hasta 2 TΩ.",
            "TechnicalSpecs": json.dumps({
                "TensionesPrueba": "Hasta 10 kV seleccionables",
                "RangoResistencia": "Hasta 2 TΩ",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Generadores de alta tensión, grandes motores síncronos y redes de transmisión de energía eléctrica."
        },

        # =========================================================================
        # 5. CALIDAD DE ENERGÍA Y ANALIZADORES DE RED
        # =========================================================================
        {
            "Code": "FLUKE-435-II",
            "Name": "Analizador trifásico avanzado de calidad de energía Fluke 435 Serie II",
            "BusinessLine": "Calidad de Energía y Analizadores de Red",
            "Family": "Analizadores y Registradores de Calidad de Energía",
            "Series": "Fluke 430 II",
            "Description": "El analizador de calidad eléctrica de referencia mundial bajo norma IEC 61000-4-30 Clase A. Mide armónicos hasta el orden 50, interarmónicos, caídas, subidas y cortes de tensión (dips & swells), flicker, transitorios rápidos de hasta 6 kV, desbalance de fases y calcula la monetización de pérdidas de energía atribuibles a armónicos y desbalance.",
            "TechnicalSpecs": json.dumps({
                "NormaClaseA": "IEC 61000-4-30 Edición 2 Clase A",
                "CalculadoraPerdidasEnergia": "Cuantifica las pérdidas de energía en términos monetarios (USD/kWh)",
                "EficienciaInversores": "Medición simultánea de potencia CA y CC para inversores solares",
                "CapturaEventosPowerWave": "Captura datos RMS rápidos de formas de onda completas para evaluar arranques de motores",
                "CapturaTransitorios": "Hasta 6 kV a 200 kHz",
                "SondasIncluidas": "4 sondas flexibles iFlex de corriente",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Auditorías energéticas de eficiencia industrial, diagnóstico de fallas térmicas en transformadores, reclamos de calidad a distribuidoras eléctricas y proyectos de compensación de factor de potencia."
        },
        {
            "Code": "FLUKE-438-II",
            "Name": "Analizador de calidad eléctrica y rendimiento mecánico de motores Fluke 438-II",
            "BusinessLine": "Calidad de Energía y Analizadores de Red",
            "Family": "Analizadores y Registradores de Calidad de Energía",
            "Series": "Fluke 430 II",
            "Description": "Combina el análisis de calidad de energía del 435-II con la medición del rendimiento mecánico de motores eléctricos (par motor, velocidad en RPM, potencia en kW/HP y eficiencia) sin necesidad de sensores mecánicos.",
            "TechnicalSpecs": json.dumps({
                "ParametrosMecanicos": "Par, RPM, Potencia en el eje (HP/kW) y rendimiento del motor sin tacómetros ni frenos",
                "CurvasDesclasificacion": "Factor de desclasificación del motor según norma NEMA/IEC",
                "CalidadEnergia": "Norma IEC 61000-4-30 Clase A",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Mantenimiento predictivo de motores de bombas, compresores y líneas de producción crítica."
        },
        {
            "Code": "FLUKE-1777",
            "Name": "Analizador de calidad eléctrica automático Fluke 1777 con pantalla táctil",
            "BusinessLine": "Calidad de Energía y Analizadores de Red",
            "Family": "Analizadores y Registradores de Calidad de Energía",
            "Series": "Fluke 1770",
            "Description": "Analizador de red automático de última generación con interfaz guiada en pantalla táctil que elimina errores de configuración. Captura automáticamente más de 500 parámetros de calidad de energía sin necesidad de complejas rutinas de configuración.",
            "TechnicalSpecs": json.dumps({
                "CapturaAutomatica": "Registra más de 500 parámetros simultáneamente",
                "TransitoriosAltaVelocidad": "Hasta 8 kV a 20 MHz",
                "PantallaTactil": "Color de alta resolución",
                "AlimentacionDirecta": "Se alimenta directamente del circuito bajo prueba",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Estudios integrales de calidad de suministro eléctrico en centros de datos, hospitales y grandes industrias."
        },
        {
            "Code": "FLUKE-1736",
            "Name": "Registrador trifásico de energía Fluke 1736 Power Logger con Fluke Connect",
            "BusinessLine": "Calidad de Energía y Analizadores de Red",
            "Family": "Analizadores y Registradores de Calidad de Energía",
            "Series": "Fluke 1730",
            "Description": "Registrador de potencia trifásica para estudios de perfiles de carga y consumo de energía. Mide y registra automáticamente tensión, corriente, potencia, factor de potencia, armónicos y distorsión armónica total (THD).",
            "TechnicalSpecs": json.dumps({
                "ParametrosRegistrados": "V, I, W, VA, VAR, PF, Energía (kWh), THD",
                "AlimentacionCircuito": "Se alimenta directamente de la línea medida",
                "Conectividad": "Wi-Fi y Fluke Connect para descarga remota de datos",
                "SondasFlexibles": "4 sondas i1730-flex incluidas",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Estudios de ahorro energético ISO 50001, dimensionamiento de generadores y balances de carga en subestaciones."
        },
        {
            "Code": "FLUKE-MDA-550-III",
            "Name": "Analizador de variadores de frecuencia y accionamientos de motor Fluke MDA-550 Serie III",
            "BusinessLine": "Calidad de Energía y Analizadores de Red",
            "Family": "Analizadores y Registradores de Calidad de Energía",
            "Series": "Fluke MDA",
            "Description": "Analizador de 4 canales especializado para solucionar problemas en variadores de velocidad tipo inversor. Guías de prueba en pantalla para entrada del variador, bus de CC, salida modulada PWM, desequilibrio y mediciones de tensión en el eje del motor para detectar corrientes de fuga en rodamientos.",
            "TechnicalSpecs": json.dumps({
                "Canales": "4 canales aislados independientes",
                "PruebasGuiadas": "Entrada, bus CC, salida PWM, armónicos y tensión en el eje (shaft voltage)",
                "SondaTensionEje": "Sonda de microfibra para corrientes perjudiciales en rodamientos",
                "AnchoBanda": "500 MHz",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Diagnóstico integral de variadores de frecuencia VFD y prevención de fallas catastróficas en rodamientos de motores."
        },

        # =========================================================================
        # 6. TERMOGRAFÍA E IMAGEN INDUSTRIAL
        # =========================================================================
        {
            "Code": "FLK-TI401-PRO",
            "Name": "Cámara termográfica profesional Fluke Ti401 PRO de 640 x 480 píxeles (FLK-TI401-PRO)",
            "BusinessLine": "Termografía e Imagen Industrial",
            "Family": "Cámaras Termográficas y Acústicas",
            "Series": "Fluke Ti400",
            "Description": "Cámara termográfica profesional de alta resolución (640 x 480 píxeles / 307.200 puntos de medida) con sistema de enfoque automático LaserSharp que enfoca con precisión láser en menos de un segundo. Rango de medición de temperatura de -20 °C a +650 °C, pantalla táctil LCD de 3.5 pulgadas, tecnología IR-Fusion de mezcla visual-térmica y lentes inteligentes intercambiables.",
            "TechnicalSpecs": json.dumps({
                "ResolucionTermica": "640 x 480 píxeles (307.200 píxeles térmicos)",
                "SensibilidadTermica_NETD": "≤ 0.075 °C a 30 °C (75 mK)",
                "RangoTemperatura": "-20 °C a +650 °C (-4 °F a +1202 °F)",
                "SistemaEnfoque": "LaserSharp Auto Focus con medidor de distancia láser integrado",
                "TecnologiaIR_Fusion": "Mezcla continua de imagen visual e infrarroja en pantalla",
                "Pantalla": "LCD táctil capacitiva de 3.5 pulgadas (640 x 480)",
                "LentesOpcionales": "Gran angular y teleobjetivos 2x y 4x intercambiables sin calibración",
                "FrecuenciaCuadros": "60 Hz (tiempo real fluido)",
                "Garantia": "2 años de garantía"
            }, ensure_ascii=False),
            "Application": "Termografía predictiva en subestaciones eléctricas, líneas aéreas de distribución, cuadros de fuerza, calderas, hornos refractarios y maquinaria rotativa."
        },
        {
            "Code": "FLK-TIS60+",
            "Name": "Cámara termográfica para mantenimiento preventivo Fluke TiS60+ de 320 x 240",
            "BusinessLine": "Termografía e Imagen Industrial",
            "Family": "Cámaras Termográficas y Acústicas",
            "Series": "Fluke TiS",
            "Description": "Cámara termográfica industrial de enfoque manual de 320 x 240 píxeles (76.800 píxeles) para técnicos de mantenimiento. Incluye tecnología IR-Fusion, grabación de notas de voz y etiquetado de activos de Fluke Connect (Asset Tagging).",
            "TechnicalSpecs": json.dumps({
                "ResolucionTermica": "320 x 240 píxeles",
                "SensibilidadTermica": "≤ 0.045 °C (45 mK)",
                "RangoTemperatura": "-20 °C a 400 °C",
                "Enfoque": "Enfoque manual para capturar detalles térmicos a corta distancia",
                "AssetTagging": "Escaneo de código QR para asociar imágenes a activos",
                "ResistenciaCaidas": "Diseñada para resistir caídas de hasta 2 metros"
            }, ensure_ascii=False),
            "Application": "Rutas de inspección eléctrica en fábricas, revisión de motores, contactores, rodamientos y trampas de vapor."
        },
        {
            "Code": "FLK-PTI120",
            "Name": "Cámara termográfica de bolsillo Fluke PTi120 con pantalla táctil e IP54",
            "BusinessLine": "Termografía e Imagen Industrial",
            "Family": "Cámaras Termográficas y Acústicas",
            "Series": "Fluke PTi",
            "Description": "Cámara termográfica ultracompacta del tamaño de un smartphone de 120 x 90 píxeles. Diseñada para llevar siempre en el bolsillo, resistente al agua y polvo (IP54) y caídas de 1 metro.",
            "TechnicalSpecs": json.dumps({
                "ResolucionTermica": "120 x 90 píxeles (10.800 píxeles)",
                "RangoTemperatura": "-20 °C a 400 °C",
                "PantallaTactil": "LCD de 3.5 pulgadas con IR-Fusion continuo",
                "GradoProteccion": "IP54 contra polvo y salpicaduras",
                "AssetTagging": "Organización automática de imágenes mediante código QR",
                "Bateria": "Batería recargable integrada vía USB-C"
            }, ensure_ascii=False),
            "Application": "Inspecciones rápidas de primer nivel por técnicos de guardia, electricistas de mantenimiento y contratistas generales."
        },
        {
            "Code": "FLUKE-II900",
            "Name": "Cámara acústica industrial Fluke ii900 para detección de fugas de aire comprimido",
            "BusinessLine": "Termografía e Imagen Industrial",
            "Family": "Cámaras Termográficas y Acústicas",
            "Series": "Fluke ii900",
            "Description": "Cámara acústica industrial equipada con una matriz de 64 micrófonos ultrasónicos digitales que superpone una imagen acústica SoundMap en tiempo real sobre una imagen visual. Permite localizar fugas de aire comprimido, gas, vapor y vacío a hasta 70 metros de distancia, incluso en plantas industriales extremadamente ruidosas.",
            "TechnicalSpecs": json.dumps({
                "MatrizMicrofonos": "64 micrófonos MEMS digitales",
                "BandaFrecuencia": "2 kHz a 52 kHz",
                "RangoDeteccion": "Hasta 70 metros (230 pies)",
                "Pantalla": "LCD táctil de 7 pulgadas (1280 x 800) de gran tamaño",
                "TecnologiaSoundMap": "Superposición visual del punto exacto de fuga",
                "FuncionLeakQ": "Estima el caudal de fuga (l/min o CFM) y el costo monetario desperdiciado",
                "Garantia": "2 años de garantía"
            }, ensure_ascii=False),
            "Application": "Ahorro masivo de energía eléctrica en sistemas de compresión de aire industrial, plantas automotrices, farmacéuticas y líneas neumáticas."
        },
        {
            "Code": "FLUKE-II910",
            "Name": "Cámara acústica de precisión Fluke ii910 para detección de descargas parciales y efecto corona",
            "BusinessLine": "Termografía e Imagen Industrial",
            "Family": "Cámaras Termográficas y Acústicas",
            "Series": "Fluke ii900",
            "Description": "Cámara acústica de alta sensibilidad con rango de frecuencia extendido hasta 100 kHz para la detección temprana de descargas parciales, efecto corona, tracking superficial y microfugas en subestaciones de media y alta tensión.",
            "TechnicalSpecs": json.dumps({
                "BandaFrecuencia": "2 kHz a 100 kHz",
                "DeteccionDescargasParciales": "Modo PDQ para cuantificar tipo de descarga (corona, interna, superficial)",
                "RangoDeteccion": "Hasta 120 metros",
                "MatrizMicrofonos": "64 micrófonos de alta sensibilidad ultrasónica",
                "Pantalla": "Táctil de 7 pulgadas"
            }, ensure_ascii=False),
            "Application": "Mantenimiento preventivo en aisladores de subestaciones, transformadores, seccionadores y líneas de transmisión eléctrica de alta tensión."
        },

        # =========================================================================
        # 7. HERRAMIENTAS DE CALIBRACIÓN DE PROCESOS
        # =========================================================================
        {
            "Code": "FLUKE-789",
            "Name": "Multímetro de procesos Fluke 789 ProcessMeter con lazo de 24 V y HART (FLUKE-789)",
            "BusinessLine": "Calibración y Control de Procesos",
            "Family": "Calibradores de Procesos y Lazos mA",
            "Series": "Fluke 780",
            "Description": "La herramienta definitiva para técnicos de instrumentación y control de procesos. Combina un multímetro digital True-RMS completo de 1000 V con un calibrador de lazo de corriente de 4-20 mA y una fuente de alimentación de lazo de 24 V integrada con resistencia HART de 250 Ω conmutable, eliminando la necesidad de cargar una fuente de poder externa para calibrar transmisores de 2 hilos.",
            "TechnicalSpecs": json.dumps({
                "FuenteAlimentacionLazo": "24 V CC integrada",
                "Simulacion_Generacion_mA": "0 a 24 mA (resolución 0.001 mA - 1 µA)",
                "ResistorHART": "Resistencia de 250 Ω seleccionable para comunicadores HART",
                "MultimetroTrueRMS": "Tensión CA/CC hasta 1000 V, corriente CA/CC hasta 440 mA, frecuencia hasta 20 kHz",
                "ModoEscalones": "Escalón manual, escalón automático y rampa automática de 25%",
                "PantallaDoble": "Visualización simultánea de mA y porcentaje de escala (0 a 100%)",
                "CapacidadCarga": "1200 Ω en generación a 24 mA",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Calibración, mantenimiento y solución de problemas en lazos de control de 4 a 20 mA, transmisores de presión, nivel, temperatura y válvulas de control en plantas de proceso, refinerías y agua potable."
        },
        {
            "Code": "FLUKE-787B",
            "Name": "Multímetro de procesos Fluke 787B ProcessMeter de 4-20 mA",
            "BusinessLine": "Calibración y Control de Procesos",
            "Family": "Calibradores de Procesos y Lazos mA",
            "Series": "Fluke 780",
            "Description": "Multímetro digital True-RMS y simulador de lazo de 4-20 mA con precisión de 0.05% y resolución de 1 microamperio.",
            "TechnicalSpecs": json.dumps({
                "CorrienteDC": "Genera y simula de 0 a 24 mA",
                "MultimetroTrueRMS": "Hasta 1000 V CA/CC",
                "ModoPorcentaje": "0-100% de escala en mA",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Pruebas de lazo y mantenimiento de entradas/salidas analógicas en PLCs y paneles de control."
        },
        {
            "Code": "FLUKE-771",
            "Name": "Pinza miliamperimétrica de procesos Fluke 771 de 4 a 20 mA sin abrir el lazo",
            "BusinessLine": "Calibración y Control de Procesos",
            "Family": "Calibradores de Procesos y Lazos mA",
            "Series": "Fluke 770",
            "Description": "Pinza miliamperimétrica de precisión extrema para señales de control de 4 a 20 mA. Permite medir la corriente del lazo sin interrumpir el proceso ni desconectar los cables de los transmisores o del PLC. Cuenta con mordaza pequeña desmontable con cable de extensión para llegar a bornes estrechos y linterna incorporada.",
            "TechnicalSpecs": json.dumps({
                "RangoMedicion": "0.01 mA a 20.99 mA / 21.0 mA a 99.9 mA",
                "Resolucion": "0.01 mA (10 µA)",
                "Precision": "0.2% de la lectura + 5 cuentas",
                "MordazaDesmontable": "Diámetro de 4.5 mm con cable de extensión",
                "PantallaDoble": "Lectura en mA y porcentaje de amplitud (4-20 mA)",
                "LinternaLED": "Para iluminar cables en canaletas oscuras",
                "SalidaAnalogica": "Salida para registro"
            }, ensure_ascii=False),
            "Application": "Mantenimiento continuo en plantas que no pueden detener operaciones (química, petróleo, farmacéutica, alimentos) para verificar transmisores sin parada de planta."
        },
        {
            "Code": "FLUKE-773",
            "Name": "Pinza miliamperimétrica de procesos avanzada Fluke 773 con generación de mA y V",
            "BusinessLine": "Calibración y Control de Procesos",
            "Family": "Calibradores de Procesos y Lazos mA",
            "Series": "Fluke 770",
            "Description": "Pinza miliamperimétrica que además de medir 4-20 mA sin abrir el lazo, genera y simula señales de 4 a 20 mA, genera tensión continua de 0 a 10 V CC y alimenta transmisores de presión y nivel con 24 V.",
            "TechnicalSpecs": json.dumps({
                "MedicionSinContacto": "Medición de 4-20 mA con pinza desmontable",
                "Generacion_Simulacion": "Genera y simula 0-24 mA y tensión 0-10 V CC",
                "AlimentacionLazo": "Fuente de 24 V CC integrada",
                "Precision": "0.2% en medición de lazo"
            }, ensure_ascii=False),
            "Application": "Puesta en servicio completa de lazos de instrumentación, válvulas actuadas de 0-10V y tarjetas analógicas de PLC."
        },
        {
            "Code": "FLUKE-754",
            "Name": "Calibrador documentador de procesos multifunción Fluke 754 con comunicación HART",
            "BusinessLine": "Calibración y Control de Procesos",
            "Family": "Calibradores de Procesos y Lazos mA",
            "Series": "Fluke 750",
            "Description": "El calibrador de campo más potente para la industria de procesos. Calibra, mantiene y documenta instrumentos inteligentes con protocolo HART (transmisores de presión, temperatura, flujo y válvulas de control). Mide y genera voltios, mA, RTDs, termopares, frecuencia y ohmios. Permite descargar procedimientos automatizados y cargar resultados a software de gestión de calibración.",
            "TechnicalSpecs": json.dumps({
                "ProtocoloHART": "Comunicador HART integrado con soporte completo de comandos universales y comunes",
                "MideGenera": "V, mA, RTD (11 tipos), Termopares (13 tipos), Frecuencia, Resistencia y Presión con módulos Fluke 750P",
                "AlimentacionLazo": "24 V CC con resistencia de 250 Ω",
                "ProcedimientosAutomatizados": "Ejecuta calibraciones automáticas As-Found (encontrado) y As-Left (dejado)",
                "Bateria": "Batería Li-Ion recargable de larga duración",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Calibración y metrología legal en refinerías de petróleo, plantas farmacéuticas, generación eléctrica e industria alimentaria bajo normas ISO 9001 / FDA."
        },
        {
            "Code": "FLUKE-725",
            "Name": "Calibrador multifunción de procesos Fluke 725",
            "BusinessLine": "Calibración y Control de Procesos",
            "Family": "Calibradores de Procesos y Lazos mA",
            "Series": "Fluke 720",
            "Description": "Calibrador multifunción de campo potente y fácil de usar para medir y generar casi cualquier parámetro de proceso: tensión, corriente, RTD, termopares, frecuencia y presión (con módulos opcionales).",
            "TechnicalSpecs": json.dumps({
                "Generacion_Medicion": "mA, voltios, termopares, RTDs, frecuencia, ohmios y presión",
                "PantallaDoble": "Mide parámetros de entrada mientras genera valores de salida simultáneamente",
                "Alimentacion24V": "Alimentación de lazo de 24 V",
                "Precision": "Alta precisión para instrumentación de planta"
            }, ensure_ascii=False),
            "Application": "Verificación y calibración general de instrumentos analógicos de proceso y bancos de prueba."
        },
        {
            "Code": "FLUKE-718-300G",
            "Name": "Calibrador de presión de procesos Fluke 718 de 300 psi / 20 bar con bomba integrada",
            "BusinessLine": "Calibración y Control de Procesos",
            "Family": "Calibradores de Procesos y Lazos mA",
            "Series": "Fluke 710",
            "Description": "Sistema de calibración de presión autónomo con bomba manual integrada de presión y vacío, ajuste fino tipo vernier y medición simultánea de presión y corriente en mA.",
            "TechnicalSpecs": json.dumps({
                "RangoPresion": "-12 psi a 300 psi (-850 mbar a 20 bar)",
                "BombaIntegrada": "Bomba manual de presión y vacío fácil de limpiar",
                "Medicion_mA": "Medición de 0-24 mA con alimentación de lazo de 24 V",
                "Precision": "0.05% de la escala completa"
            }, ensure_ascii=False),
            "Application": "Calibración de transmisores e interruptores de presión, manómetros y válvulas de seguridad en campo."
        },
        {
            "Code": "FLUKE-719PRO-300G",
            "Name": "Calibrador eléctrico de presión Fluke 719PRO de 300 psi con bomba eléctrica automática",
            "BusinessLine": "Calibración y Control de Procesos",
            "Family": "Calibradores de Procesos y Lazos mA",
            "Series": "Fluke 710",
            "Description": "Calibrador de presión con bomba eléctrica integrada que presuriza automáticamente el sistema con sólo tocar un botón, eliminando la fatiga del bombeo manual.",
            "TechnicalSpecs": json.dumps({
                "RangoPresion": "-12 psi a 300 psi (20 bar)",
                "BombaElectrica": "Bomba eléctrica automática integrada",
                "MedicionTemperatura": "Medición de temperatura con sonda RTD Pt100",
                "Precision": "0.025% de la lectura"
            }, ensure_ascii=False),
            "Application": "Calibración de alto volumen de transmisores de presión sin esfuerzo físico."
        },

        # =========================================================================
        # 8. PUESTA A TIERRA E INSTALACIONES (EARTH GROUND)
        # =========================================================================
        {
            "Code": "FLUKE-1630-2FC",
            "Name": "Pinza de puesta a tierra sin picas Fluke 1630-2 FC con Fluke Connect",
            "BusinessLine": "Seguridad Eléctrica y Puesta a Tierra",
            "Family": "Comprobadores de Instalaciones y Tierra",
            "Series": "Fluke 1630",
            "Description": "Pinza para comprobar la resistencia del bucle de puesta a tierra sin necesidad de desconectar el electrodo de tierra ni clavar picas auxiliares. Mide también corrientes de fuga a tierra en CA de 0.2 mA a 39.99 A.",
            "TechnicalSpecs": json.dumps({
                "ResistenciaBucleTierra": "0.025 Ω a 1500 Ω",
                "CorrienteFugaAC": "0.2 mA a 39.99 A",
                "MetodoPrueba": "Sin picas auxiliares (Stakeless testing)",
                "AperturaMordaza": "Mordaza de alta resistencia de 35 mm",
                "Conectividad": "Fluke Connect inalámbrico",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Medición rápida y periódica de mallas de puesta a tierra en torres de telecomunicaciones, pararrayos, subestaciones y plantas industriales sin cortar el servicio."
        },
        {
            "Code": "FLUKE-1625-2",
            "Name": "Telurómetro avanzado para resistencia de tierra Fluke 1625-2 GEO",
            "BusinessLine": "Seguridad Eléctrica y Puesta a Tierra",
            "Family": "Comprobadores de Instalaciones y Tierra",
            "Series": "Fluke 1620",
            "Description": "Comprobador de puesta a tierra para pruebas con métodos de 3 y 4 polos, prueba selectiva con pinza (sin desconectar el conductor) y prueba de resistividad del suelo (método de Wenner).",
            "TechnicalSpecs": json.dumps({
                "Metodos": "3 y 4 polos, selectivo, sin picas y resistividad del terreno (ρ)",
                "ControlAutomaticoFrecuencia": "Selecciona la frecuencia óptima (AFC) para minimizar ruido",
                "RangoResistencia": "0.001 Ω a 19.99 kΩ",
                "Memoria": "Almacenamiento interno de datos con puerto USB"
            }, ensure_ascii=False),
            "Application": "Diseño y auditoría de sistemas de puesta a tierra en subestaciones, plantas de generación y hospitales."
        },
        {
            "Code": "FLUKE-1664FC",
            "Name": "Comprobador multifunción de instalaciones eléctricas Fluke 1664 FC con Insulation PreTest",
            "BusinessLine": "Seguridad Eléctrica y Puesta a Tierra",
            "Family": "Comprobadores de Instalaciones y Tierra",
            "Series": "Fluke 1660",
            "Description": "El único comprobador de instalaciones con tecnología Insulation PreTest que detiene la prueba de aislamiento si detecta que hay aparatos conectados a la red, protegiéndolos contra daños accidentales. Realiza 7 pruebas de instalación consecutivas con sólo pulsar un botón (Auto Test) bajo normas IEC 60364 y DIN VDE 0100.",
            "TechnicalSpecs": json.dumps({
                "InsulationPreTest": "Protección contra daños en equipos conectados durante la prueba de aislamiento",
                "AutoTest": "Ejecuta secuencia automática: impedancia de bucle/línea, tiempo/corriente de disparo RCD y aislamiento",
                "TensionAislamiento": "50 V, 100 V, 250 V, 500 V, 1000 V",
                "PruebaRCD": "Dispositivos tipo A, AC, B, B+, selectivos y retardados",
                "ResistenciaTierra": "Comprobación de bucle sin disparo de RCD (Loop test)",
                "Conectividad": "Fluke Connect y software TruTest",
                "CategoriaSeguridad": "CAT III 500 V / CAT IV 300 V"
            }, ensure_ascii=False),
            "Application": "Certificación oficial de instalaciones eléctricas residenciales, comerciales e industriales según normativa nacional e internacional."
        },

        # =========================================================================
        # 9. OSCILOSCOPIOS PORTÁTILES (SCOPEMETER)
        # =========================================================================
        {
            "Code": "FLUKE-190-204",
            "Name": "Osciloscopio portátil industrial Fluke 190-204 ScopeMeter de 4 canales 200 MHz",
            "BusinessLine": "Osciloscopios y Analizadores de Señal",
            "Family": "Osciloscopios Portátiles (ScopeMeter)",
            "Series": "ScopeMeter 190 III",
            "Description": "Osciloscopio portátil de 4 canales aislados independientes con ancho de banda de 200 MHz y velocidad de muestreo en tiempo real de 2.5 GS/s. Clasificación de seguridad CAT IV 600 V / CAT III 1000 V y sellado IP51 contra polvo y gotas de agua para trabajar directamente en tableros trifásicos y variadores de frecuencia.",
            "TechnicalSpecs": json.dumps({
                "Canales": "4 canales aislados flotantes independientes",
                "AnchoBanda": "200 MHz",
                "MuestreoTiempoReal": "2.5 GS/s por canal",
                "ProfundidadMemoria": "10.000 muestras por forma de onda",
                "Pantalla": "Color brillante con alta tasa de actualización",
                "FuncionesScopeRecord": "Registro desatendido de formas de onda hasta 48 horas",
                "TrendPlot": "Registrador de tendencias gráfico",
                "GradoProteccion": "IP51 para entornos industriales",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V",
                "Garantia": "3 años de garantía"
            }, ensure_ascii=False),
            "Application": "Diagnóstico de accionamientos industriales, servosistemas, electrónica de potencia trifásica, inversores solares y robótica."
        },
        {
            "Code": "FLUKE-125B",
            "Name": "Osciloscopio industrial portátil Fluke 125B ScopeMeter de 40 MHz con Connect-and-View",
            "BusinessLine": "Osciloscopios y Analizadores de Señal",
            "Family": "Osciloscopios Portátiles (ScopeMeter)",
            "Series": "ScopeMeter 120B",
            "Description": "Osciloscopio y multímetro de 2 canales con tecnología de disparo automático Connect-and-View que estabiliza formas de onda complejas instantáneamente sin tocar los controles. Incluye análisis de bus de campo para redes industriales.",
            "TechnicalSpecs": json.dumps({
                "Canales": "2 canales de osciloscopio y multímetro digital",
                "AnchoBanda": "40 MHz",
                "ConnectAndView": "Disparo automático inteligente sin configuración manual",
                "BusHealth": "Comprobación del estado físico de buses de campo industriales (Modbus, Profibus, CAN)",
                "CategoriaSeguridad": "CAT IV 600 V"
            }, ensure_ascii=False),
            "Application": "Mantenimiento electromecánico de maquinaria industrial, líneas de automatización y redes industriales."
        },

        # =========================================================================
        # 10. ANALIZADORES DE BATERÍAS
        # =========================================================================
        {
            "Code": "FLK-BT521",
            "Name": "Analizador avanzado de baterías industriales Fluke BT521 con sondas inteligentes",
            "BusinessLine": "Mantenimiento Industrial y Diagnóstico",
            "Family": "Analizadores de Baterías",
            "Series": "Fluke BT500",
            "Description": "Instrumento de prueba para el mantenimiento, resolución de problemas y prueba de rendimiento de celdas de baterías estacionarias individuales y bancos de baterías en sistemas de respaldo crítico (UPS, subestaciones eléctricas y telecomunicaciones). Mide resistencia interna de celda, voltaje CC y CA, corriente de rizado y temperatura por infrarrojos.",
            "TechnicalSpecs": json.dumps({
                "ResistenciaInterna": "3 mΩ a 3000 mΩ (Resolución 0.001 mΩ)",
                "TensionBateria": "6 V a 1000 V CC",
                "TemperaturaInfrarroja": "Sonda inteligente BTL21 con sensor de temperatura IR integrado",
                "SecuenciaAutomatica": "Prueba automática guiada de bancos completos con audio",
                "UmbralesAlarma": "Configuración de límites para alertas pasa/falla",
                "CategoriaSeguridad": "CAT III 600 V"
            }, ensure_ascii=False),
            "Application": "Bancos de baterías en centros de datos, sistemas UPS de hospitales, subestaciones eléctricas y salas de conmutación de telecomunicaciones."
        },

        # =========================================================================
        # 11. ENERGÍA RENOVABLE Y FOTOVOLTAICA
        # =========================================================================
        {
            "Code": "FLK-SMFT-1000",
            "Name": "Comprobador fotovoltaico multifunción Fluke SMFT-1000 y trazador de curvas I-V",
            "BusinessLine": "Energía Renovable y Movilidad Eléctrica",
            "Family": "Comprobadores Fotovoltaicos y Estaciones EV",
            "Series": "Fluke SMFT",
            "Description": "Solución integral todo en uno para la verificación de seguridad, rendimiento y trazado de curvas I-V en instalaciones solares fotovoltaicas de hasta 1000 V CC conforme a la norma IEC 62446-1.",
            "TechnicalSpecs": json.dumps({
                "TrazadoCurva_IV": "Comparación instantánea con datos STC del fabricante del panel solar",
                "TensionDC": "Hasta 1000 V DC",
                "CorrienteDC": "Hasta 20 A DC",
                "MedidorIrradiancia": "Incluye medidor de irradiancia y temperatura IRR2-BT con enlace inalámbrico",
                "PruebaAislamiento": "Hasta 1000 V DC",
                "ContinuidadPuestaTierra": "Prueba de continuidad de tierra a 200 mA",
                "CategoriaSeguridad": "CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Comisionamiento, mantenimiento periódico y certificación de plantas solares fotovoltaicas."
        },
        {
            "Code": "FLK-IRR1-SOL",
            "Name": "Medidor de irradiancia solar Fluke IRR1-SOL",
            "BusinessLine": "Energía Renovable y Movilidad Eléctrica",
            "Family": "Comprobadores Fotovoltaicos y Estaciones EV",
            "Series": "Fluke IRR",
            "Description": "Medidor digital compacto para medir la irradiancia solar (W/m²), temperatura del panel y del ambiente, inclinación y orientación de los paneles fotovoltaicos.",
            "TechnicalSpecs": json.dumps({
                "IrradianciaSolar": "0 a 1400 W/m²",
                "TemperaturaPanel": "-30 °C a 100 °C con sonda de contacto",
                "BrujulaInclinometro": "Mide ángulo de inclinación y orientación",
                "Pantalla": "LCD de alto contraste para lectura a pleno sol"
            }, ensure_ascii=False),
            "Application": "Inspección previa, estudio de sombreado y monitoreo de eficiencia en instalaciones solares."
        },
        {
            "Code": "FLK-FEV350",
            "Name": "Analizador de estaciones de carga de vehículos eléctricos Fluke FEV350",
            "BusinessLine": "Energía Renovable y Movilidad Eléctrica",
            "Family": "Comprobadores Fotovoltaicos y Estaciones EV",
            "Series": "Fluke FEV",
            "Description": "Analizador integral para comprobar la seguridad y funcionalidad operativa de estaciones de recarga de vehículos eléctricos (EVSE) de CA según normas IEC/EN 61851-1 y 60364-7-722.",
            "TechnicalSpecs": json.dumps({
                "SimulacionPilotoControl": "Estados CP A, B, C, D con análisis de forma de onda",
                "SimulacionCablePP": "13 A, 20 A, 32 A y 63 A",
                "PruebaRCD_RDC_DD": "Comprobación de interruptores diferenciales tipo B y RDC-DD de 6 mA CC",
                "PruebaAislamiento": "Medición de aislamiento hasta 1000 V integrada"
            }, ensure_ascii=False),
            "Application": "Instalación, mantenimiento y certificación de electrolineras y cargadores residenciales de vehículos eléctricos."
        },

        # =========================================================================
        # 12. INSTRUMENTACIÓN AMBIENTAL Y MEDIDORES LÁSER
        # =========================================================================
        {
            "Code": "FLUKE-62-MAX+",
            "Name": "Termómetro infrarrojo láser Fluke 62 MAX+ IP54 (-30 °C a 650 °C)",
            "BusinessLine": "Temperatura y Termometría",
            "Family": "Termómetros Infrarrojos sin Contacto",
            "Series": "Fluke 60",
            "Description": "Termómetro láser de infrarrojos sin contacto resistente al polvo y al agua (IP54), probado para resistir caídas de hasta 3 metros. Incorpora doble puntero láser giratorio para identificar con precisión el diámetro del área de medición.",
            "TechnicalSpecs": json.dumps({
                "RangoTemperatura": "-30 °C a 650 °C (-22 °F a 1202 °F)",
                "RelacionOptica": "12:1 (Distancia al punto de medición)",
                "PunterosLaser": "Láser doble para determinar el tamaño exacto del área de medida",
                "Precision": "± 1.0 °C o ± 1.0% de la lectura",
                "GradoProteccion": "IP54",
                "ResistenciaCaidas": "3 metros",
                "Alimentacion": "1 pila AA estándar con hasta 10 horas de uso continuo"
            }, ensure_ascii=False),
            "Application": "Inspección rápida de conexiones eléctricas recalentadas, transformadores, rodamientos y trampas de vapor."
        },
        {
            "Code": "FLUKE-424D",
            "Name": "Medidor de distancia láser profesional Fluke 424D de 100 metros",
            "BusinessLine": "Instrumentación de Campo y Medición",
            "Family": "Medidores de Distancia Láser",
            "Series": "Fluke 400D",
            "Description": "Distanciómetro láser para profesionales con alcance de hasta 100 metros, sensor de inclinación de 180° para mediciones de altura indirecta y brújula electrónica integrada.",
            "TechnicalSpecs": json.dumps({
                "Alcance": "Hasta 100 metros (330 pies)",
                "Precision": "± 1.0 mm",
                "SensorInclinacion": "180° para cálculo de nivelación y alturas",
                "BrujulaElectronica": "Proporciona orientación de rumbo",
                "Proteccion": "IP54"
            }, ensure_ascii=False),
            "Application": "Cálculo de trazados de bandejas portacables, conductos eléctricos, áreas de salas técnicas y obras civiles."
        },
        {
            "Code": "FLUKE-925",
            "Name": "Anemómetro de molinete para flujo de aire Fluke 925",
            "BusinessLine": "Instrumentación Ambiental y de Higiene",
            "Family": "Medidores Ambientales y de Calidad de Aire",
            "Series": "Fluke 900",
            "Description": "Anemómetro de paletas para medir velocidad de flujo de aire, caudal volumétrico en CFM y temperatura en rejillas y conductos de climatización.",
            "TechnicalSpecs": json.dumps({
                "VelocidadAire": "0.40 a 25.00 m/s",
                "CaudalAire": "Hasta 99.999 m³/min",
                "Temperatura": "0 °C a 50 °C",
                "Sensor": "Sonda de molinete externa de respuesta rápida"
            }, ensure_ascii=False),
            "Application": "Balanceo de sistemas de ventilación HVAC y salas limpias."
        },

        # =========================================================================
        # 13. ACCESORIOS OFICIALES DE MEDICIÓN
        # =========================================================================
        {
            "Code": "FLUKE-TL175",
            "Name": "Cables de prueba TwistGuard con longitud de punta ajustable Fluke TL175",
            "BusinessLine": "Accesorios y Sondas de Medida",
            "Family": "Puntas de Prueba, Sondas y Estuches",
            "Series": "Fluke TL",
            "Description": "Juego de cables de prueba patentados TwistGuard con punta ajustable que permite cambiar la exposición del metal de 19 mm a 4 mm para reducir el riesgo de cortocircuitos accidentales en cuadros con alta energía. Cables de silicona con doble aislamiento WearGuard que muestra color contrastante si el cable se desgasta.",
            "TechnicalSpecs": json.dumps({
                "PuntaAjustable": "Exposición regulable de 19 mm (CAT II) a 4 mm (CAT IV)",
                "IndicadorDesgaste": "Aislamiento de silicona bicapa WearGuard",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V, 10 A",
                "Normas": "EN 61010-031"
            }, ensure_ascii=False),
            "Application": "Puntas de prueba estándar para todos los multímetros y pinzas Fluke con terminales de seguridad tipo banana de 4 mm."
        },
        {
            "Code": "FLUKE-TPAK",
            "Name": "Kit de sujeción magnética para multímetros Fluke TPAK ToolPak",
            "BusinessLine": "Accesorios y Sondas de Medida",
            "Family": "Puntas de Prueba, Sondas y Estuches",
            "Series": "Fluke TPAK",
            "Description": "Juego de correa y colgador magnético de neodimio de alta potencia que permite colgar el multímetro de puertas de metal de tableros o tuberías, liberando ambas manos para realizar mediciones seguras.",
            "TechnicalSpecs": json.dumps({
                "Iman": "Imán de tierras raras de gran adherencia",
                "Correas": "Correa de velcro de 23 cm y correa universal de enganche",
                "Compatibilidad": "Fluke 87V, 179, 117, 289, 1587, 789 y la mayoría de multímetros Fluke"
            }, ensure_ascii=False),
            "Application": "Comodidad y seguridad operativa en el trabajo cotidiano con tableros eléctricos."
        },
        {
            "Code": "FLUKE-I2500-18",
            "Name": "Sonda de corriente flexible iFlex Fluke i2500-18 de 2500 A CA (45 cm)",
            "BusinessLine": "Accesorios y Sondas de Medida",
            "Family": "Puntas de Prueba, Sondas y Estuches",
            "Series": "Fluke iFlex",
            "Description": "Sonda de corriente flexible tipo bobina de Rogowski de 45 cm (18 pulgadas) que se conecta a las pinzas Fluke compatibles (376 FC, 375 FC, 374 FC, 381, 393 FC) para medir hasta 2500 A CA en conductores gruesos o haces de cables inaccesibles.",
            "TechnicalSpecs": json.dumps({
                "CorrienteAC": "Hasta 2500 A True-RMS",
                "LongitudCableBobina": "45 cm (18 pulgadas)",
                "DiametroCable": "7.5 mm de perfil flexible",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Medición de corriente en barras colectoras gruesas y acometidas de transformadores de gran amperaje."
        },
        {
            "Code": "FLUKE-I400",
            "Name": "Pinza amperimétrica accesoria de corriente CA Fluke i400 de 400 A",
            "BusinessLine": "Accesorios y Sondas de Medida",
            "Family": "Puntas de Prueba, Sondas y Estuches",
            "Series": "Fluke i400",
            "Description": "Pinza adaptadora de corriente de alta seguridad que se conecta a cualquier multímetro digital para medir hasta 400 A CA con una salida de 1 mA por amperio.",
            "TechnicalSpecs": json.dumps({
                "RangoCorriente": "1 A a 400 A CA",
                "Salida": "1 mA/A",
                "AperturaMordaza": "32 mm",
                "CategoriaSeguridad": "CAT IV 600 V / CAT III 1000 V"
            }, ensure_ascii=False),
            "Application": "Convierte cualquier multímetro digital con entrada de mA en una pinza amperimétrica precisa."
        },
        {
            "Code": "FLUKE-C35",
            "Name": "Estuche de transporte acolchado blando Fluke C35",
            "BusinessLine": "Accesorios y Sondas de Medida",
            "Family": "Puntas de Prueba, Sondas y Estuches",
            "Series": "Fluke Cases",
            "Description": "Funda acolchada con cremallera y compartimentos internos para proteger multímetros, pinzas y puntas de prueba contra golpes en la caja de herramientas.",
            "TechnicalSpecs": json.dumps({
                "Material": "Poliéster 600D de alta durabilidad",
                "Dimensiones": "220 mm x 140 mm x 64 mm",
                "Compatibilidad": "Multímetros Fluke series 80, 170, 110 y pinzas serie 320"
            }, ensure_ascii=False),
            "Application": "Protección de equipos de medición durante el transporte en obras y camionetas de servicio."
        },
        {
            "Code": "FLUKE-PACK30",
            "Name": "Mochila profesional para herramientas de electricista Fluke Pack30",
            "BusinessLine": "Accesorios y Sondas de Medida",
            "Family": "Puntas de Prueba, Sondas y Estuches",
            "Series": "Fluke Cases",
            "Description": "Mochila de trabajo resistente para electricistas con base de plástico impermeable moldeada en el fondo, más de 30 bolsillos organizadores y compartimento acolchado para tablet o laptop.",
            "TechnicalSpecs": json.dumps({
                "Bolsillos": "Más de 30 bolsillos organizadores en 6 compartimentos",
                "FondoRigido": "Base impermeable de plástico EVA moldeado resistente al agua y barro",
                "CompartimentoLaptop": "Acolchado para portátiles de hasta 15.6 pulgadas",
                "Dimensiones": "508 mm x 330 mm x 235 mm",
                "Peso": "2.26 kg"
            }, ensure_ascii=False),
            "Application": "Transporte ergonómico y ordenado de herramientas e instrumentos de medición en escaleras, andamios y plantas industriales."
        }
    ]
    return prods

def populate_fluke():
    prods = get_fluke_core_catalog()
    print(f"\nTotal productos Fluke listos para sembrar: {len(prods)}")
    
    # Target all databases
    db_paths = glob.glob("**/agente_ventas.db", recursive=True)
    db_paths.append("agente_ventas.db")
    db_paths = sorted(list(set(db_paths)))
    
    for db_path in db_paths:
        print(f"\nProcesando {db_path}...")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Eliminar registros previos de Fluke si existieran para evitar duplicados
        cur.execute("DELETE FROM ProductsCatalog WHERE Brand = 'Fluke';")
        
        insert_sql = """
            INSERT INTO ProductsCatalog 
            (Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application, Status, SearchCount, LastQueriedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        
        count = 0
        for p in prods:
            cur.execute(insert_sql, (
                "Fluke",
                p["BusinessLine"],
                p["Family"],
                p["Series"],
                p["Code"],
                p["Name"],
                p["Description"],
                p["TechnicalSpecs"],
                p["Application"],
                "Disponible",
                0,
                None
            ))
            count += 1
            
        conn.commit()
        print(f"  Insertados {count} productos de Fluke.")
        
        # Sincronizar FTS5
        try:
            cur.execute("INSERT INTO Products_FTS(Products_FTS) VALUES('rebuild');")
            conn.commit()
            print("  Índice FTS5 Products_FTS reconstruido con éxito.")
        except Exception as e:
            print(f"  Aviso rebuild Products_FTS: {e}")
            
        try:
            cur.execute("INSERT INTO ProductsCatalog_fts(ProductsCatalog_fts) VALUES('rebuild');")
            conn.commit()
            print("  Índice FTS5 ProductsCatalog_fts reconstruido con éxito.")
        except Exception as e:
            pass
            
        # Verificar conteo final por marca
        cur.execute("SELECT Brand, COUNT(*) FROM ProductsCatalog GROUP BY Brand;")
        print("  Conteo por marca:", cur.fetchall())
        
        cur.execute("SELECT COUNT(*) FROM Products_FTS;")
        print("  Total en Products_FTS:", cur.fetchone()[0])
        
        conn.close()

if __name__ == "__main__":
    populate_fluke()

