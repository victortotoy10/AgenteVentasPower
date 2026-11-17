#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de deduplicación, traducción técnica y poblado del Catálogo Oficial APC (by Schneider Electric)
en la base de datos relacional y motor de búsqueda FTS5 de AgenteVentasPower.

Análisis paso a paso de fuentes oficiales en Catalogos/apc:
1. 998-1257966_GMA-US_C_Español.pdf (Smart-UPS On-Line SRT 120/208/230V, 17 páginas)
2. APC Smart-UPS Ultra up to 5kW NAM Brochure 998-21402800 - 120V.pdf (13 páginas)
3. APC Smart-UPS Ultra 5kW 230V Brochure 998-21912450_230V.pdf (8 páginas)
4. VAGL-B39HBZ_R0_EN.pdf & VAGL-B3SJSX_R0_EN.pdf (Smart-UPS Interactivo SMT/SMX/SMC, 31 páginas)
5. APC Easy UPS On-Line Lithium-ion SRVL 230V & Easy UPS for ESS (17 páginas)
6. APC Back-UPS Pro B650_900G2I, BE Lite 500-700, BW650U1, BN1050M (Back-UPS residencial/oficina)
7. BMOE-7PDSSB_R0_ES.pdf (Symmetra PX modular trifásica, 8 páginas)
8. Rack ATS Technical Brochure.pdf (Interruptores automáticos de transferencia AP44xxA, 6 páginas)
9. Rack.pdf (NetShelter Enclosures y Racks AR3100/AR3300/AR100, 36 páginas)
10. Catalog_Easy Rack and PDUs solution for ET Channel & NetShelter rPDU (PDUs AP88xx/AP89xx/EPDU)

Manejo estricto de productos repetidos:
- Deduplicación por Código canónico (Part Number).
- Prioridad de fuentes en español sobre inglés.
- Consolidación de especificaciones técnicas y aplicaciones en español técnico.
"""

import sqlite3
import glob
import json
import re
import os

def get_apc_master_catalog():
    """
    Retorna el catálogo consolidado y deduplicado de APC.
    """
    raw_products = [
        # =========================================================================
        # 1. SMART-UPS ON-LINE DE DOBLE CONVERSIÓN (SERIE SRT)
        # =========================================================================
        {
            "Code": "SRT1000XLA",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 1000VA 120V Torre/Rack (SRT1000XLA)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de doble conversión de alta densidad con tiempo de transferencia cero a batería, factor de potencia unitario y pantalla LCD gráfica. Proporciona protección eléctrica pura de onda senoidal para servidores críticos, switches y almacenamiento.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1000 VA / 900 W (FP = 0.9)",
                "TensionEntrada": "120 V CA (rango 100 - 275 V)",
                "TensionSalida": "120 V CA configurable",
                "Topologia": "Online Doble Conversión (Tiempo de transferencia 0 ms)",
                "ConexionesSalida": "(6) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-15P con cable de 1.83 m",
                "Formato": "Torre / Rack convertible 2U",
                "EficienciaModoVerde": "97 %",
                "AutonomiaMediaCarga": "14 min a 450 W"
            }, ensure_ascii=False),
            "Application": "Protección de conmutadores de red, servidores de borde (Edge computing), telefonía IP y sistemas de seguridad."
        },
        {
            "Code": "SRT1500XLA",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 1500VA 120V Torre/Rack (SRT1500XLA)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS de doble conversión en línea con bypass estático automático interno y capacidad de ampliación de autonomía con módulos de baterías externas. Dispone de ranura SmartSlot para tarjeta de gestión de red.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1500 VA / 1350 W",
                "TensionEntrada": "120 V CA",
                "TensionSalida": "120 V CA nominal",
                "Topologia": "Online Doble Conversión",
                "ConexionesSalida": "(6) NEMA 5-15R (con 2 grupos de tomas controlables)",
                "ConexionesEntrada": "NEMA 5-15P",
                "Formato": "Torre / Rack 2U",
                "RanuraSmartSlot": "1 ranura libre para NMC AP9630/AP9631",
                "BateriasExternasCompatibles": "SRT48BP / SRT48RMBP"
            }, ensure_ascii=False),
            "Application": "Servidores de rango medio, sistemas de almacenamiento SAN/NAS y equipos médicos de diagnóstico."
        },
        {
            "Code": "SRT2200XLA",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 2200VA 120V Torre/Rack (SRT2200XLA)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line monofásico de 2200VA con pantalla LCD interactiva a color, bypass interno automático y modo de operación Green Mode de alta eficiencia que alcanza hasta el 98%. Diseñado para servidores corporativos de alta demanda.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "2200 VA / 1980 W",
                "TensionEntrada": "120 V CA (rango 100 - 275 V)",
                "TensionSalida": "120 V CA",
                "Topologia": "Online Doble Conversión pura",
                "ConexionesSalida": "(6) NEMA 5-15R, (1) NEMA 5-20R, (1) NEMA L5-20R",
                "ConexionesEntrada": "NEMA 5-20P",
                "Formato": "Torre / Rack 2U",
                "PuertosComunicacion": "RJ-45 Serial, SmartSlot, USB",
                "BateriasExternas": "Soporta hasta 10 bancos de baterías SRT72BP / SRT72RMBP"
            }, ensure_ascii=False),
            "Application": "Centros de cómputo medianos, cuartos de comunicaciones de edificios y salas de control industrial."
        },
        {
            "Code": "SRT2200RMXLA",
            "Name": "UPS On-Line Rackeable APC Smart-UPS SRT 2200VA 120V 2U con rieles (SRT2200RMXLA)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Versión preconfigurada para montaje en bastidor de 19 pulgadas que incluye kit completo de rieles de 4 postes. Alimentación continua con factor de cresta 3:1 y distorsión armónica inferior al 2%.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "2200 VA / 1980 W",
                "TensionEntradaSalida": "120 V CA",
                "Formato": "Montaje en Rack 2U (Rieles incluidos)",
                "ConexionesSalida": "(6) NEMA 5-15R, (1) NEMA 5-20R, (1) NEMA L5-20R",
                "ConexionesEntrada": "NEMA 5-20P con cable de 1.83 m",
                "Bypass": "Bypass estático incorporado automático y manual",
                "RBCReemplazo": "APCRBC141"
            }, ensure_ascii=False),
            "Application": "Gabinete rackeado de telecomunicaciones y servidores blade de centros de datos."
        },
        {
            "Code": "SRT2200RMXLA-NC",
            "Name": "UPS On-Line APC Smart-UPS SRT 2200VA 120V con Tarjeta de Red AP9631 preinstalada (SRT2200RMXLA-NC)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de 2.2kVA que incluye de fábrica la tarjeta de administración de red Network Management Card AP9631 con monitoreo ambiental, sensor de temperatura y apagado controlado PowerChute Network Shutdown.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "2200 VA / 1980 W",
                "TensionEntradaSalida": "120 V CA",
                "TarjetaRedIncluida": "AP9631 (Ethernet 10/100, SNMP v1/v3, HTTPS, Modbus TCP)",
                "SensoresIncluidos": "Sonda de temperatura AP9335T",
                "Formato": "Montaje en Rack 2U",
                "Salidas": "(6) NEMA 5-15R, (1) NEMA 5-20R, (1) NEMA L5-20R",
                "GestionRemota": "Completa vía navegador web, CLI y EcoStruxure IT"
            }, ensure_ascii=False),
            "Application": "Sitios remotos desatendidos, sucursales bancarias y salas de servidores críticas con monitoreo centralizado."
        },
        {
            "Code": "SRT3000XLA",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 3000VA 120V Torre/Rack (SRT3000XLA)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de 3kVA a 120V con factor de potencia de 0.9, capacidad para 2700 vatios y clavija de entrada NEMA L5-30P de giro y bloqueo (twist-lock). Incluye pantalla LCD gráfica con rotación automática.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 2700 W",
                "TensionEntrada": "120 V CA (rango 100 - 275 V)",
                "TensionSalida": "120 V CA",
                "ConexionesSalida": "(6) NEMA 5-15R, (2) NEMA 5-20R, (1) NEMA L5-30R",
                "ConexionesEntrada": "NEMA L5-30P (Twist-Lock 30A)",
                "Formato": "Torre / Rack convertible 2U",
                "Eficiencia": "96.5 % en modo On-Line / 98 % en Green Mode",
                "BateriasExternas": "SRT96BP / SRT96RMBP",
                "RBCReemplazo": "APCRBC152"
            }, ensure_ascii=False),
            "Application": "Servidores empresariales de alta densidad, almacenamiento de red empresarial y racks completos de TI."
        },
        {
            "Code": "SRT3000RMXLA",
            "Name": "UPS On-Line Rackeable APC Smart-UPS SRT 3000VA 120V 2U con rieles (SRT3000RMXLA)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Versión en rack de 2U del Smart-UPS On-Line de 3000VA a 120V. Suministra 2700 vatios regulados sin microcortes ante cortes de energía, caídas de tensión o transitorios electromagnéticos.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 2700 W",
                "TensionEntradaSalida": "120 V CA",
                "Formato": "Rack 2U con kit de montaje de 4 postes",
                "ConexionesSalida": "(6) NEMA 5-15R, (2) NEMA 5-20R, (1) NEMA L5-30R",
                "ConexionesEntrada": "NEMA L5-30P",
                "GruposConmutados": "2 grupos de tomas independientes para reinicio secuencial de carga"
            }, ensure_ascii=False),
            "Application": "Infraestructura crítica en racks de 19 pulgadas y sistemas de virtualización VMware/Hyper-V."
        },
        {
            "Code": "SRT3000XLT",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 3000VA 208V Torre/Rack (SRT3000XLT)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line para instalaciones de servidores a 208V. Factor de potencia unitario de 3000 VA / 2700 W, salidas NEMA L6-20R y L6-30R con onda senoidal perfecta para alimentación bifásica industrial.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 2700 W",
                "TensionEntrada": "208 V CA nominal (configurable 208V, 240V)",
                "TensionSalida": "208 V / 240 V CA",
                "ConexionesSalida": "(2) NEMA L6-20R, (1) NEMA L6-30R",
                "ConexionesEntrada": "NEMA L6-20P",
                "Formato": "Torre / Rack 2U",
                "DistorsionArmonica": "< 2 % a plena carga"
            }, ensure_ascii=False),
            "Application": "Servidores corporativos y conmutadores de red alimentados a 208V en data centers industriales."
        },
        {
            "Code": "SRT5KXLT",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 5000VA 208V Torre/Rack (SRT5KXLT)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line trifásico/bifásico de alta potencia de 5000 VA / 4800 W con factor de potencia de 0.96. Integra pantalla gráfica LCD, ranura SmartSlot para tarjeta de red y bypass manual de mantenimiento.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "5000 VA / 4800 W",
                "TensionEntrada": "208 V CA (rango 100 - 275 V)",
                "TensionSalida": "208 V CA (opcional 240V)",
                "ConexionesSalida": "(2) NEMA L6-20R, (2) NEMA L6-30R",
                "ConexionesEntrada": "NEMA L6-30P",
                "Formato": "Torre / Rack 3U",
                "Eficiencia": "98.5 % en modo Green Mode",
                "AutonomiaCargaCompleta": "4 min a 4800 W (ampliable con bancos SRT192BP)",
                "RBCReemplazo": "APCRBC140"
            }, ensure_ascii=False),
            "Application": "Alimentación de gabinetes blade, almacenamiento masivo SAN y clusters de servidores de alta disponibilidad."
        },
        {
            "Code": "SRT5KRMXLT",
            "Name": "UPS On-Line Rackeable APC Smart-UPS SRT 5000VA 208V 3U con rieles (SRT5KRMXLT)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Configuración en bastidor de 3U del Smart-UPS On-Line de 5 kVA a 208V. Incluye kit de montaje en rack, tarjeta de red NMC y tomas de alta corriente con protección térmica individual.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "5000 VA / 4800 W",
                "TensionEntradaSalida": "208 V CA",
                "Formato": "Montaje en Rack 3U",
                "ConexionesSalida": "(2) NEMA L6-20R, (2) NEMA L6-30R",
                "ConexionesEntrada": "NEMA L6-30P",
                "NMCIntegrada": "Incluye tarjeta AP9631 con doble puerto Ethernet y sensores ambientales",
                "ModulosBateriaExternos": "Soporta módulos SRT192RMBP en rack"
            }, ensure_ascii=False),
            "Application": "Salas de servidores empresariales, telecomunicaciones y sistemas de automatización SCADA."
        },
        {
            "Code": "SRT6KXLT",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 6000VA 208V Torre/Rack (SRT6KXLT)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de 6kVA con factor de potencia unitario de 6000 VA / 6000 W (1.0). Alimenta cargas de servidores de alta densidad sin pérdida de potencia activa, con bypass de estado sólido ultra-rápido.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "6000 VA / 6000 W (FP = 1.0)",
                "TensionEntrada": "208 V CA (Hardwire o bornera)",
                "TensionSalida": "208 V / 240 V CA",
                "ConexionesSalida": "(2) NEMA L6-20R, (2) NEMA L6-30R",
                "ConexionesEntrada": "Cableado fijo (Hardwire 3-wire L1+L2+G)",
                "Formato": "Torre / Rack 4U",
                "RBCReemplazo": "APCRBC140"
            }, ensure_ascii=False),
            "Application": "Infraestructura de centros de datos de misión crítica, servidores cloud y sistemas de respaldo continuo."
        },
        {
            "Code": "SRT8KXLT",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 8000VA 208V Torre/Rack (SRT8KXLT)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de 8kVA / 8000W para grandes salas de servidores. Suministro eléctrico ininterrumpido con conmutación en caliente de baterías y tarjeta de red integrada con soporte SNMPv3.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "8000 VA / 8000 W (FP = 1.0)",
                "TensionEntradaSalida": "208 V / 240 V CA",
                "Topologia": "Online Doble Conversión",
                "ConexionesSalida": "Bornera de cableado fijo Hardwire, (2) NEMA L6-20R, (2) NEMA L6-30R",
                "ConexionesEntrada": "Hardwire 3 hilos",
                "Formato": "Torre / Rack 6U",
                "NMCIntegrada": "Tarjeta de red gigabit con ciberseguridad avanzada"
            }, ensure_ascii=False),
            "Application": "Salas principales de cómputo, centros de datos corporativos e instalaciones médicas de diagnóstico por imágenes."
        },
        {
            "Code": "SRT10KXLT",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 10000VA 208V Torre/Rack (SRT10KXLT)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line insignia de 10kVA / 10kW con factor de potencia 1.0. Proporciona protección total contra cualquier anomalía de red eléctrica para instalaciones corporativas completas.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "10000 VA / 10000 W (FP = 1.0)",
                "TensionEntrada": "208 V / 240 V CA nominal",
                "TensionSalida": "208 V / 240 V CA regulada ± 1%",
                "Topologia": "Online Doble Conversión con tiempo de transferencia cero",
                "ConexionesSalida": "Hardwire 3-wire, (2) NEMA L6-20R, (2) NEMA L6-30R",
                "ConexionesEntrada": "Hardwire 3-wire (L1+L2+G)",
                "Formato": "Torre / Rack 6U",
                "TarjetaRed": "AP9631 preinstalada de serie",
                "BateriasExternas": "SRT192BP2 (admite hasta 10 bancos de baterías)"
            }, ensure_ascii=False),
            "Application": "Backbone de centros de datos, hospitales, entidades bancarias e infraestructura crítica de telecomunicaciones."
        },
        {
            "Code": "SRT1000XLI",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 1000VA 230V Internacional (SRT1000XLI)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de 1kVA a 230V para servidores con tomas estándar IEC C13 y rango extendido de voltaje de entrada.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1000 VA / 900 W",
                "TensionEntradaSalida": "230 V CA (220V, 230V, 240V)",
                "ConexionesSalida": "(6) IEC 320 C13",
                "ConexionesEntrada": "IEC 320 C14",
                "Formato": "Torre / Rack 2U",
                "RBCReemplazo": "APCRBC155"
            }, ensure_ascii=False),
            "Application": "Servidores y racks con distribución eléctrica a 220/230V monofásico."
        },
        {
            "Code": "SRT3000XLI",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 3000VA 230V Internacional (SRT3000XLI)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de 3kVA a 230V con factor de potencia de 0.9 (2700W), salidas IEC C13 y C19 con dos grupos de tomas controlables independientemente.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 2700 W",
                "TensionEntradaSalida": "230 V CA nominal",
                "ConexionesSalida": "(8) IEC 320 C13, (2) IEC 320 C19",
                "ConexionesEntrada": "IEC 320 C20 con cable británico / Schuko",
                "Formato": "Torre / Rack 2U"
            }, ensure_ascii=False),
            "Application": "Infraestructura de servidores a 230V en cuartos de telecomunicaciones."
        },
        {
            "Code": "SRT5KXLI",
            "Name": "UPS On-Line Doble Conversión APC Smart-UPS SRT 5000VA 230V Internacional (SRT5KXLI)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de 5000VA / 4500W a 230V con salidas IEC C13 y C19 y bornera de conexión directa Hardwire.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "5000 VA / 4500 W",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesSalida": "(6) IEC 320 C13, (4) IEC 320 C19, Bornera Hardwire 3-wire",
                "ConexionesEntrada": "Hardwire 3-wire (1PH+N+G)",
                "Formato": "Torre / Rack 3U",
                "RBCReemplazo": "APCRBC140"
            }, ensure_ascii=False),
            "Application": "Racks de servidores a 230V y equipamiento de laboratorio de calibración y prueba."
        },

        # =========================================================================
        # 2. SMART-UPS ULTRA DE IONES DE LITIO (SERIE SRTL)
        # =========================================================================
        {
            "Code": "SRTL2K2RM1UC",
            "Name": "UPS On-Line Litio APC Smart-UPS Ultra 2200VA 120V 1U Ultracompacto (SRTL2K2RM1UC)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Litio Ultracompactos",
            "Series": "Smart-UPS Ultra SRTL",
            "Description": "La tecnología de UPS más avanzada de APC: 50% más pequeña y ligera gracias a las baterías de iones de litio. Ocupa solo 1U de espacio en rack y ofrece hasta el triple de vida útil de batería (8 a 10 años) sin necesidad de reemplazo frecuente.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "2200 VA / 1950 W a 125V (1870 W a 120V)",
                "Bateria": "Iones de litio (Vida útil estimada: 8 a 10 años)",
                "Formato": "Ultra delgado 1U (Alto 43 mm x Prof 560 mm)",
                "Peso": "15.9 kg (50 % más ligero que plomo-ácido)",
                "TensionEntradaSalida": "120 V / 125 V CA",
                "ConexionesSalida": "(5) NEMA 5-20R, (1) L5-20R con cable flexible",
                "ConexionesEntrada": "NEMA 5-20P",
                "Monitoreo": "Puerto Ethernet SmartConnect y Modbus TCP"
            }, ensure_ascii=False),
            "Application": "Edge computing, micro data centers, gabinetes de pared con espacio limitado y salas de telecomunicaciones modernas."
        },
        {
            "Code": "SRTL3KRM1UNC",
            "Name": "UPS On-Line Litio APC Smart-UPS Ultra 3000VA 120V 1U con Tarjeta de Red integrada (SRTL3KRM1UNC)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Litio Ultracompactos",
            "Series": "Smart-UPS Ultra SRTL",
            "Description": "UPS On-Line de 3000 VA / 3000 W en un increíble factor de forma de 1U. Baterías de iones de litio, factor de potencia 1.0 y tarjeta de administración de red Gigabit incorporada con pantalla táctil virtual.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 3000 W (FP = 1.0)",
                "Bateria": "Iones de litio de alta densidad",
                "Formato": "1U para montaje en rack de 19 pulgadas",
                "TensionEntradaSalida": "120 V / 125 V CA",
                "ConexionesSalida": "(5) NEMA 5-20R, (1) NEMA L5-30R con chicote flexible",
                "ConexionesEntrada": "NEMA L5-30P",
                "GestionRed": "Tarjeta de gestión de red Gigabit NMC preintegrada",
                "EficienciaModoVerde": "97 %",
                "BateriasExternas": "Admite hasta 5 bancos SRTL50RMBP1U-LI"
            }, ensure_ascii=False),
            "Application": "Servidores de alto rendimiento en racks saturados donde cada unidad U es crítica."
        },
        {
            "Code": "SRTL5KRM2UT",
            "Name": "UPS On-Line Litio APC Smart-UPS Ultra 5000VA 208V 2U (SRTL5KRM2UT)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Litio Ultracompactos",
            "Series": "Smart-UPS Ultra SRTL",
            "Description": "UPS On-Line de 5kW ultracompacto en solo 2U de altura para alimentación a 208V/240V. Incorpora baterías de iones de litio, eficiencia verde del 98.5% y pantalla LCD multicolor con rotación giroscópica automática.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "5000 VA / 5000 W a 240V (4900 W a 208V)",
                "Bateria": "Iones de litio",
                "Formato": "2U de rack (86 mm de altura)",
                "PesoNeto": "30 kg",
                "TensionEntradaSalida": "208 V / 240 V CA nominal",
                "ConexionesSalida": "(2) NEMA L6-20R, (2) NEMA L6-30R",
                "ConexionesEntrada": "NEMA L6-30P",
                "Eficiencia": "98.5 % en modo ecológico",
                "BateriasExternas": "SRTL180RM2UBP (hasta 10 módulos de batería externa)"
            }, ensure_ascii=False),
            "Application": "Centros de datos de inteligencia artificial, servidores hiperconvergentes y virtualización."
        },
        {
            "Code": "SRTL5KRM2UI",
            "Name": "UPS On-Line Litio APC Smart-UPS Ultra 5000VA 230V 2U Internacional (SRTL5KRM2UI)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Litio Ultracompactos",
            "Series": "Smart-UPS Ultra SRTL",
            "Description": "Versión internacional a 230V del Smart-UPS Ultra de 5kW 2U con salidas IEC C13 y C19 y bornera de entrada cableada fija.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "5000 VA / 5000 W (FP = 1.0)",
                "TensionEntradaSalida": "220 V / 230 V / 240 V CA",
                "ConexionesSalida": "(6) IEC 320 C13 (10A CB), (4) IEC 320 C19 (16A CB)",
                "ConexionesEntrada": "Bornera Hardwire",
                "Bateria": "Iones de litio (8-10 años de vida)",
                "Formato": "2U Rack / Torre",
                "Peso": "27.2 kg"
            }, ensure_ascii=False),
            "Application": "Infraestructura de TI internacional y distribución a 230V en racks de alta potencia."
        },
        {
            "Code": "SRTL50RMBP1U-LI",
            "Name": "Módulo de Batería Externa de Iones de Litio APC Smart-UPS Ultra 1U (SRTL50RMBP1U-LI)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "Smart-UPS Ultra SRTL",
            "Description": "Paquete de batería externa de iones de litio en formato de 1U para extender la autonomía de los UPS Smart-UPS Ultra de 2.2kW y 3kW.",
            "TechnicalSpecs": json.dumps({
                "TipoBateria": "Iones de litio (Li-ion)",
                "VoltajeBateria": "50 V CC",
                "Formato": "1U para montaje en rack",
                "Compatibilidad": "SRTL2K2RM1UC, SRTL2K2RM1UNC, SRTL3KRM1UC, SRTL3KRM1UNC",
                "Peso": "12.5 kg"
            }, ensure_ascii=False),
            "Application": "Extensión de autonomía en servidores de misión crítica durante cortes de energía prolongados."
        },

        # =========================================================================
        # 3. SMART-UPS INTERACTIVO LCD PARA SERVIDORES (SERIES SMT / SMX / SMC)
        # =========================================================================
        {
            "Code": "SMT750C",
            "Name": "UPS Interactivo APC Smart-UPS 750VA 120V LCD con SmartConnect (SMT750C)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "UPS interactivo de onda senoidal pura para servidores de torre y equipos de red básicos. Dispone de pantalla LCD intuitiva y monitoreo en la nube SmartConnect para supervisión remota sin costo adicional.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "750 VA / 500 W",
                "TensionEntradaSalida": "120 V CA (rango 82 - 144 V)",
                "Topologia": "Línea Interactiva con AVR (Regulación automática de voltaje)",
                "TipoOnda": "Onda senoidal pura",
                "ConexionesSalida": "(6) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-15P",
                "Formato": "Torre",
                "MonitoreoRemoto": "APC SmartConnect (habilitado para la nube)",
                "RBCReemplazo": "RBC48"
            }, ensure_ascii=False),
            "Application": "Servidores torre en pequeñas oficinas, puntos de venta (POS) y switches de borde."
        },
        {
            "Code": "SMT1000C",
            "Name": "UPS Interactivo APC Smart-UPS 1000VA 120V LCD Torre con SmartConnect (SMT1000C)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "UPS interactivo de 1kVA / 700W con onda senoidal pura, interfaz LCD con medidor de energía en kWh y puertos de apagado de emergencia.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1000 VA / 700 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(8) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-15P",
                "Formato": "Torre",
                "RBCReemplazo": "RBC6"
            }, ensure_ascii=False),
            "Application": "Servidores departamentales, almacenamiento NAS y estaciones de trabajo de alto rendimiento."
        },
        {
            "Code": "SMT1500C",
            "Name": "UPS Interactivo APC Smart-UPS 1500VA 120V LCD Torre con SmartConnect (SMT1500C)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "El estándar de la industria en protección para servidores. Suministra 1500 VA / 1000 W con regulación automática de voltaje AVR de doble etapa y monitoreo en la nube APC SmartConnect.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1500 VA / 1000 W",
                "TensionEntradaSalida": "120 V CA (rango 75 - 154 V)",
                "ConexionesSalida": "(8) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-15P con cable de 1.83 m",
                "Formato": "Torre",
                "AutonomiaMediaCarga": "23 min a 500 W",
                "RBCReemplazo": "RBC7"
            }, ensure_ascii=False),
            "Application": "Servidores de archivos, conmutadores PoE empresariales y equipamiento médico."
        },
        {
            "Code": "SMT1500RM2UC",
            "Name": "UPS Interactivo Rackeable APC Smart-UPS 1500VA 120V 2U con SmartConnect (SMT1500RM2UC)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "Versión en rack de 2U del clásico Smart-UPS 1500VA. Incluye rieles de montaje de 4 postes, pantalla LCD abatible y 6 tomas NEMA 5-15R divididas en grupos controlados.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1500 VA / 1000 W",
                "TensionEntradaSalida": "120 V CA",
                "Formato": "Montaje en Rack 2U",
                "ConexionesSalida": "(6) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-15P",
                "RBCReemplazo": "APCRBC159"
            }, ensure_ascii=False),
            "Application": "Racks de comunicaciones, servidores en rack de 1U/2U y conmutadores de fibra óptica."
        },
        {
            "Code": "SMT2200",
            "Name": "UPS Interactivo APC Smart-UPS 2200VA 120V LCD Torre (SMT2200)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "UPS interactivo de alta capacidad en torre para alimentar hasta 1980 vatios de servidores críticos. Incorpora tomas de 20A y ranura SmartSlot para integración SNMP.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "2200 VA / 1980 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(8) NEMA 5-15R, (2) NEMA 5-20R",
                "ConexionesEntrada": "NEMA 5-20P",
                "Formato": "Torre",
                "RBCReemplazo": "RBC55"
            }, ensure_ascii=False),
            "Application": "Salas de servidores con múltiples máquinas conectadas y sistemas de telefonía PBX."
        },
        {
            "Code": "SMT3000",
            "Name": "UPS Interactivo APC Smart-UPS 3000VA 120V LCD Torre (SMT3000)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "UPS interactivo de 3kVA en formato torre con clavija NEMA L5-30P. Proporciona 2700 vatios de respaldo con onda senoidal perfecta para grandes bancos de discos y servidores blade.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 2700 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(8) NEMA 5-15R, (2) NEMA 5-20R",
                "ConexionesEntrada": "NEMA L5-30P (Twist-Lock 30A)",
                "Formato": "Torre",
                "RBCReemplazo": "RBC55"
            }, ensure_ascii=False),
            "Application": "Protección centralizada de cuartos de telecomunicaciones y sistemas de seguridad de edificios."
        },
        {
            "Code": "SMX1500RM2U",
            "Name": "UPS Interactivo APC Smart-UPS X 1500VA 120V con Autonomía Extendida (SMX1500RM2U)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "UPS de la serie X con capacidad de conectar módulos externos de batería SMX48RMBP2U para lograr horas completas de autonomía ante cortes prolongados de energía.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1500 VA / 1200 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(8) NEMA 5-15R",
                "Formato": "Rack / Torre convertible 2U",
                "AutonomiaExtendida": "Soporta bancos de batería externos plug-and-play SMX48RMBP2U",
                "RBCReemplazo": "APCRBC115"
            }, ensure_ascii=False),
            "Application": "Instalaciones en zonas con cortes de energía de larga duración donde se requiere continuidad operativa."
        },
        {
            "Code": "SMC1000C",
            "Name": "UPS Interactivo Entry-Level APC Smart-UPS C 1000VA 120V LCD (SMC1000C)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "Solución costo-efectiva de la familia Smart-UPS con onda senoidal pura y pantalla LCD intuitiva para servidores de nivel de entrada y enrutadores.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1000 VA / 600 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(8) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-15P",
                "Formato": "Torre",
                "RBCReemplazo": "APCRBC142"
            }, ensure_ascii=False),
            "Application": "Protección económica de switches no gestionados, routers y servidores pequeños."
        },
        {
            "Code": "SMC1500C",
            "Name": "UPS Interactivo Entry-Level APC Smart-UPS C 1500VA 120V LCD (SMC1500C)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Interactivos para Servidores",
            "Series": "Smart-UPS SMT/SMX/SMC",
            "Description": "UPS interactivo de 1500VA / 900W con onda senoidal pura y monitoreo en la nube SmartConnect para empresas que buscan la confiabilidad de Smart-UPS a un costo accesible.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1500 VA / 900 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(8) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-15P",
                "Formato": "Torre",
                "RBCReemplazo": "APCRBC142"
            }, ensure_ascii=False),
            "Application": "Equipos de videovigilancia NVR, servidores de punto de venta y telefonía IP comercial."
        },

        # =========================================================================
        # 4. EASY UPS ON-LINE (SERIES SRV / SRVL)
        # =========================================================================
        {
            "Code": "SRV1KI",
            "Name": "UPS On-Line Doble Conversión APC Easy UPS SRV 1000VA 230V Torre (SRV1KI)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Easy UPS SRV/SRVL",
            "Description": "UPS On-Line de doble conversión de excelente relación costo-beneficio para protección de potencia limpia en entornos eléctricos inestables con rango ultra amplio de voltaje de entrada.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1000 VA / 800 W",
                "TensionEntrada": "230 V CA (rango 160 - 280 V a plena carga, 110 - 285 V a media carga)",
                "TensionSalida": "230 V CA (configurable 220V, 240V)",
                "ConexionesSalida": "(3) IEC 320 C13",
                "ConexionesEntrada": "IEC 320 C14",
                "Formato": "Torre compacta",
                "Pantalla": "LCD interactiva con estado de carga y baterías"
            }, ensure_ascii=False),
            "Application": "Protección de equipos electrónicos sensibles, maquinaria ligera de laboratorio y servidores de sucursal."
        },
        {
            "Code": "SRV2KI",
            "Name": "UPS On-Line Doble Conversión APC Easy UPS SRV 2000VA 230V Torre (SRV2KI)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Easy UPS SRV/SRVL",
            "Description": "UPS On-Line de 2kVA / 1600W de doble conversión para servidores de red medianos y estaciones de trabajo de control industrial.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "2000 VA / 1600 W",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesSalida": "(4) IEC 320 C13",
                "ConexionesEntrada": "IEC 320 C14",
                "Formato": "Torre"
            }, ensure_ascii=False),
            "Application": "Controladores industriales, sistemas de pesaje electrónico y terminales de cajeros automáticos."
        },
        {
            "Code": "SRV3KI",
            "Name": "UPS On-Line Doble Conversión APC Easy UPS SRV 3000VA 230V Torre (SRV3KI)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Easy UPS SRV/SRVL",
            "Description": "UPS On-Line de 3000VA / 2400W con salidas IEC C13 y C19, bypass automático y modo ecológico ECO para máxima eficiencia de energía.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 2400 W",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesSalida": "(6) IEC 320 C13, (1) IEC 320 C19",
                "ConexionesEntrada": "IEC 320 C20",
                "Formato": "Torre"
            }, ensure_ascii=False),
            "Application": "Protección de racks completos en redes comerciales y sistemas de grabación CCTV."
        },
        {
            "Code": "SRVL1KRIL",
            "Name": "UPS On-Line Litio APC Easy UPS SRVL 1000VA 230V 2U Rack/Torre (SRVL1KRIL)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Litio Ultracompactos",
            "Series": "Easy UPS SRV/SRVL",
            "Description": "UPS On-Line con batería de iones de litio integrada de bajo perfil en formato de 2U. Diseñado para soportar altas temperaturas de operación de hasta 40°C sin degradación acelerada.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1000 VA / 900 W",
                "Bateria": "Iones de litio (Vida útil de hasta 10 años)",
                "TensionEntradaSalida": "230 V CA",
                "Formato": "Rack / Torre 2U",
                "ConexionesSalida": "(3) IEC C13",
                "ConexionesEntrada": "IEC C14"
            }, ensure_ascii=False),
            "Application": "Cuartos de comunicación con climatización intermitente y sitios industriales edge."
        },
        {
            "Code": "SRVL3KRIL",
            "Name": "UPS On-Line Litio APC Easy UPS SRVL 3000VA 230V 2U Rack/Torre (SRVL3KRIL)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Litio Ultracompactos",
            "Series": "Easy UPS SRV/SRVL",
            "Description": "UPS On-Line de 3kVA con tecnología de litio para montaje en bastidor de 19 pulgadas. Proporciona 2700 vatios de protección continua con recarga ultrarrápida.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 2700 W",
                "Bateria": "Iones de litio",
                "TensionEntradaSalida": "230 V CA",
                "Formato": "Rack 2U",
                "ConexionesSalida": "(6) IEC C13, (1) IEC C19"
            }, ensure_ascii=False),
            "Application": "Sistemas de telecomunicaciones en armarios exteriores y subestaciones eléctricas."
        },

        # =========================================================================
        # 5. BACK-UPS Y BACK-UPS PRO (HOGAR, OFICINA Y PUNTOS DE VENTA)
        # =========================================================================
        {
            "Code": "BE500G3",
            "Name": "UPS Residencial APC Back-UPS BE Lite 500VA 120V con puertos de carga USB (BE500G3)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS compacto de suelo o pared para dispositivos domésticos y de teletrabajo. Proporciona respaldo por batería para mantener routers Wi-Fi y computadoras encendidas durante apagones.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "500 VA / 300 W",
                "TensionEntradaSalida": "120 V CA",
                "Tomas": "6 tomas NEMA 5-15R (4 con respaldo y supresión, 2 solo supresión)",
                "CargaUSB": "1 puerto USB-A de carga para móviles",
                "Montaje": "Suelo o pared mediante ranuras ojo de cerradura"
            }, ensure_ascii=False),
            "Application": "Respaldo de modems de fibra óptica, routers Wi-Fi, laptops y puntos de acceso en el hogar."
        },
        {
            "Code": "BE700G3",
            "Name": "UPS Residencial APC Back-UPS BE Lite 700VA 120V con carga USB (BE700G3)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS de 700VA / 420W para estaciones de trabajo de oficina en casa, computadoras de escritorio y pantallas de monitoreo.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "700 VA / 420 W",
                "TensionEntradaSalida": "120 V CA",
                "Tomas": "8 tomas NEMA (6 con batería y supresión, 2 solo supresión)",
                "CargaUSB": "Puertos USB Type-A para smartphones"
            }, ensure_ascii=False),
            "Application": "Computadoras de escritorio, pantallas LCD, consolas de videojuegos y routers corporativos."
        },
        {
            "Code": "BW650U1",
            "Name": "UPS Compacto APC Back-UPS BW650U1 650VA 120V con 7 tomas (BW650U1)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS confiable de 650VA con 7 tomas de salida, supresión de sobretensiones de 490 Joules y puerto USB de carga de 2.4A.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "650 VA / 360 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "7 tomas NEMA 5-15R (5 con respaldo de batería, 2 solo supresión)",
                "SupresionPicos": "490 Joules",
                "PuertoUSB": "1 puerto USB Type-A de 2.4A para carga rápida",
                "ClavijaEntrada": "NEMA 5-15P en ángulo recto de 90°"
            }, ensure_ascii=False),
            "Application": "Oficinas, puestos de facturación, computadoras personales y routers."
        },
        {
            "Code": "BN1050M",
            "Name": "UPS APC Back-UPS BN1050M 1050VA 120V con pantalla LCD interactiva (BN1050M)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS interactivo de alto rendimiento de 1050VA con pantalla LCD para monitorear autonomía en minutos, carga conectada y estado de la red eléctrica.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1050 VA / 600 W",
                "TensionEntradaSalida": "120 V CA",
                "Tomas": "8 tomas NEMA 5-15R",
                "Pantalla": "LCD multifunción con botón de silenciamiento de alarmas",
                "ProteccionDatos": "Protección de línea de red Ethernet Gigabit RJ-45"
            }, ensure_ascii=False),
            "Application": "Estaciones de trabajo de diseño gráfico, sistemas de audio profesional y servidores domésticos."
        },
        {
            "Code": "BR650G2I",
            "Name": "UPS Profesional APC Back-UPS Pro BR650G2I 650VA 230V con LCD y USB-C (BR650G2I)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS premium de línea interactiva con regulación automática de voltaje AVR, pantalla LCD frontal y dos puertos de carga USB Type-C de 15W.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "650 VA / 400 W",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesSalida": "(6) IEC 320 C13 (4 con batería, 2 solo supresión)",
                "CargaUSB": "2 puertos USB Type-C (5V / 15W)",
                "SupresionPicos": "1080 Joules",
                "ProteccionRed": "1 Gbps Ethernet RJ-45",
                "RBCReemplazo": "APCRBC164"
            }, ensure_ascii=False),
            "Application": "Oficinas de ingeniería, estaciones de trabajo con periféricos avanzados y puestos bancarios."
        },
        {
            "Code": "BR900G2I",
            "Name": "UPS Profesional APC Back-UPS Pro BR900G2I 900VA 230V con LCD y USB-C (BR900G2I)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS profesional de 900VA / 540W con tomas IEC, pantalla de diagnóstico en tiempo real y protección de datos para redes de alta velocidad.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "900 VA / 540 W",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesSalida": "(6) IEC 320 C13 (4 batería, 2 supresión)",
                "CargaUSB": "2 puertos USB Type-C (15W)",
                "SupresionPicos": "1080 Joules",
                "RBCReemplazo": "APCRBC164"
            }, ensure_ascii=False),
            "Application": "Computadoras corporativas de gama alta, almacenamiento NAS y equipos de red de oficina."
        },
        {
            "Code": "BVX700L-LM",
            "Name": "UPS Interactivo APC Easy UPS BVX 700VA 120V con tomas NEMA (BVX700L-LM)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS de línea interactiva de gran versatilidad con regulación de voltaje AVR que estabiliza caídas de tensión prolongadas sin consumir energía de la batería.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "700 VA / 360 W",
                "TensionEntradaSalida": "120 V CA (rango 89 - 145 V)",
                "ConexionesSalida": "(6) NEMA 5-15R protegidas por batería y supresor",
                "ConexionesEntrada": "NEMA 5-15P",
                "Formato": "Torre compacta",
                "Indicadores": "LED frontal de estado de red/batería"
            }, ensure_ascii=False),
            "Application": "Puntos de venta (POS), computadoras de escritorio comerciales y módems residenciales."
        },
        {
            "Code": "BVX1200L-LM",
            "Name": "UPS Interactivo APC Easy UPS BVX 1200VA 120V con tomas NEMA (BVX1200L-LM)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS interactivo de 1200VA / 650W con 6 tomas NEMA para proteger múltiples periféricos de oficina contra anomalías eléctricas.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1200 VA / 650 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(6) NEMA 5-15R con batería y supresión",
                "ConexionesEntrada": "NEMA 5-15P",
                "Formato": "Torre compacta con carcasa retardante a la llama"
            }, ensure_ascii=False),
            "Application": "Estaciones de trabajo de oficina, sistemas de control de acceso y centrales telefónicas IP."
        },
        {
            "Code": "BVX2200L-LM",
            "Name": "UPS Interactivo APC Easy UPS BVX 2200VA 120V con tomas NEMA (BVX2200L-LM)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "El modelo más potente de la serie BVX: 2200VA / 1200W con tomas NEMA para respaldar estaciones de diseño o múltiples PCs simultáneas.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "2200 VA / 1200 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(6) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-20P con cable de servicio pesado",
                "Topologia": "Línea Interactiva con AVR"
            }, ensure_ascii=False),
            "Application": "Estaciones gráficas pesadas, servidores locales de pequeñas empresas y centros de videovigilancia."
        },

        # =========================================================================
        # 6. SYMMETRA PX / LX (UPS MODULAR ESCALABLE PARA DATA CENTERS)
        # =========================================================================
        {
            "Code": "SY16K48H-PD",
            "Name": "UPS Modular Trifásico APC Symmetra PX 16kVA escalable a 48kVA 208V/480V (SY16K48H-PD)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Modulares Escalables (Symmetra)",
            "Series": "Symmetra PX",
            "Description": "Sistema de UPS modular trifásico de ultra alta eficiencia con redundancia N+1 a nivel de módulos de potencia y baterías. Permite aumentar la potencia o autonomía en caliente sin apagar la carga conectada.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "16 kVA / 16 kW escalable hasta 48 kVA / 48 kW (FP = 1.0)",
                "TensionEntradaSalida": "208 V trifásico / 480 V (con transformador)",
                "Topologia": "Online Doble Conversión Modular",
                "ModulosPotencia": "Módulos de 16 kVA hot-swap intercambiables en caliente (SYPM10K16H)",
                "BateriasModulares": "Módulos de batería hot-swap con monitoreo individual por celda",
                "Eficiencia": "Hasta 96 % a media carga y carga completa"
            }, ensure_ascii=False),
            "Application": "Data centers medianos y grandes, salas de telecomunicaciones corporativas y procesos industriales continuos."
        },
        {
            "Code": "SY32K48H-PD",
            "Name": "UPS Modular Trifásico APC Symmetra PX 32kVA escalable a 48kVA N+1 (SY32K48H-PD)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Modulares Escalables (Symmetra)",
            "Series": "Symmetra PX",
            "Description": "UPS modular con 32kVA de potencia instalada con configuración redundante N+1 que garantiza máxima tolerancia a fallas de componentes internos.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "32 kVA / 32 kW",
                "Escalabilidad": "Hasta 48 kVA en el mismo bastidor",
                "Redundancia": "N+1 a nivel de módulo de potencia",
                "GestionRed": "NMC preinstalada con monitoreo de baterías StruxureWare"
            }, ensure_ascii=False),
            "Application": "Salas de servidores de bancos, infraestructuras hospitalarias críticas y telecomunicaciones."
        },
        {
            "Code": "SYPM10K16H",
            "Name": "Módulo de Potencia de 16kVA para APC Symmetra PX (SYPM10K16H)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "Symmetra PX",
            "Description": "Módulo de potencia de repuesto o expansión de 16kVA / 16kW para bastidores Symmetra PX de 48kVA, 96kVA y 160kVA con conexión en caliente (hot-swap).",
            "TechnicalSpecs": json.dumps({
                "PotenciaNominal": "16 kVA / 16 kW (FP = 1.0)",
                "Caracteristica": "Intercambiable en caliente (Hot-Swap)",
                "Compatibilidad": "Bastidores Symmetra PX de 48kW, 96kW y 160kW"
            }, ensure_ascii=False),
            "Application": "Ampliación de capacidad o sustitución inmediata en caliente en centros de cómputo."
        },

        # =========================================================================
        # 7. CONMUTADORES AUTOMÁTICOS DE TRANSFERENCIA EN RACK (RACK ATS - AP44xxA)
        # =========================================================================
        {
            "Code": "AP4421A",
            "Name": "Conmutador Automático de Transferencia en Rack APC NetShelter ATS 10A 230V 1U (AP4421A)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Interruptores de Transferencia en Rack (Rack ATS)",
            "Series": "NetShelter ATS AP44xxA",
            "Description": "Conmutador automático de transferencia de 5ta generación para alimentar equipos de un solo cable desde dos fuentes independientes de CA. Tiempo de transferencia típico de 8 a 12 ms sin interrupción de funcionamiento de las fuentes de poder de TI.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "10 A",
                "TensionEntradaSalida": "230 V CA nominal",
                "TiempoTransferencia": "8 a 12 ms típico (transferencia ultra rápida fuera de fase)",
                "ConexionesEntrada": "(2) IEC 320 C14 (Entrada A y Entrada B)",
                "ConexionesSalida": "(12) IEC 320 C13",
                "Formato": "Montaje en Rack 1U",
                "GestionRed": "Interfaz de red integrada con SNMP, HTTPS, CLI y pantalla LCD táctil"
            }, ensure_ascii=False),
            "Application": "Suministro de energía redundante a servidores y conmutadores de red monotoma conectados a dos UPS distintas."
        },
        {
            "Code": "AP4422A",
            "Name": "Conmutador Automático de Transferencia en Rack APC NetShelter ATS 16A 230V 1U (AP4422A)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Interruptores de Transferencia en Rack (Rack ATS)",
            "Series": "NetShelter ATS AP44xxA",
            "Description": "Rack ATS de 16A a 230V con tomas de alta corriente IEC C19 y C13 para equipos de mayor consumo energético.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "16 A",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesEntrada": "(2) IEC 320 C20",
                "ConexionesSalida": "(12) IEC 320 C13, (2) IEC 320 C19",
                "Formato": "1U Rack",
                "Monitoreo": "Medición de corriente por fase y estado de ambas fuentes en pantalla LCD"
            }, ensure_ascii=False),
            "Application": "Distribución redundante para conmutadores de red de chasis de alta densidad a 230V."
        },
        {
            "Code": "AP4423A",
            "Name": "Conmutador Automático de Transferencia en Rack APC NetShelter ATS 20A 120V 1U (AP4423A)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Interruptores de Transferencia en Rack (Rack ATS)",
            "Series": "NetShelter ATS AP44xxA",
            "Description": "Rack ATS de 20A a 120V con 10 salidas NEMA 5-20R y dos entradas independientes NEMA L5-20P con monitoreo de red y gestión de alarmas por sobrecorriente.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "20 A (16 A continuo UL)",
                "TensionEntradaSalida": "120 V CA nominal",
                "ConexionesEntrada": "(2) NEMA L5-20P con cables de 2.4 m",
                "ConexionesSalida": "(10) NEMA 5-20R",
                "Formato": "1U Rack",
                "GestionRed": "Doble puerto Ethernet para redundancia de red (NMC3 integrado)"
            }, ensure_ascii=False),
            "Application": "Servidores y dispositivos de red monotoma a 120V en cuartos de telecomunicaciones."
        },
        {
            "Code": "AP4430A",
            "Name": "Conmutador Automático de Transferencia en Rack APC NetShelter ATS 15A 120V 1U (AP4430A)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Interruptores de Transferencia en Rack (Rack ATS)",
            "Series": "NetShelter ATS AP44xxA",
            "Description": "Rack ATS de 15A para tomas estándar NEMA 5-15R con conmutación en menos de 10 ms y supervisión continua del voltaje y sincronismo de las fases de entrada.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "15 A (12 A continuo según norma)",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesEntrada": "(2) NEMA 5-15P",
                "ConexionesSalida": "(10) NEMA 5-15R",
                "Formato": "1U Rack",
                "Pantalla": "LCD táctil para visualización y control"
            }, ensure_ascii=False),
            "Application": "Redundancia eléctrica en routers de borde, firewalls y servidores web compactos."
        },
        {
            "Code": "AP4432A",
            "Name": "Conmutador Automático de Transferencia en Rack APC NetShelter ATS 30A 120V 2U (AP4432A)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Interruptores de Transferencia en Rack (Rack ATS)",
            "Series": "NetShelter ATS AP44xxA",
            "Description": "Conmutador de alta corriente de 30A a 120V en formato 2U para alimentar múltiples tomas de alta potencia desde dos alimentadores independientes.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "30 A (24 A continuo)",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesEntrada": "(2) NEMA L5-30P Twist-Lock",
                "ConexionesSalida": "(16) NEMA 5-20R, (1) NEMA L5-30R",
                "Formato": "2U Rack",
                "Disyuntores": "Protección magnetotérmica individual por bancos"
            }, ensure_ascii=False),
            "Application": "Centros de datos con distribución de alta potencia a 120V en racks completos."
        },
        {
            "Code": "AP4450A",
            "Name": "Conmutador Automático de Transferencia en Rack APC NetShelter ATS 16A 230V 1U tomas C19 (AP4450A)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Interruptores de Transferencia en Rack (Rack ATS)",
            "Series": "NetShelter ATS AP44xxA",
            "Description": "Rack ATS de 16A a 230V equipado con una salida de alta corriente IEC C19 y 8 salidas C13.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "16 A",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesEntrada": "(2) IEC 320 C20",
                "ConexionesSalida": "(8) IEC 320 C13, (1) IEC 320 C19",
                "Formato": "1U Rack"
            }, ensure_ascii=False),
            "Application": "Alimentación de PDUs secundarias o servidores de alta gama en racks europeos e industriales."
        },

        # =========================================================================
        # 8. DISTRIBUCIÓN DE ENERGÍA EN RACK (RACK PDU - BÁSICA, CONMUTADA Y MONITORIZADA)
        # =========================================================================
        {
            "Code": "AP8858EU3",
            "Name": "PDU de Rack Conmutada APC NetShelter Switched Rack PDU 16A 230V Zero-U (AP8858EU3)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Unidades de Distribución en Rack (Rack PDU)",
            "Series": "NetShelter rPDU",
            "Description": "PDU vertical de 0U conmutada inteligente que permite encender, apagar o reiniciar de forma remota tomas individuales. Proporciona medición precisa de energía en tiempo real (voltaje, corriente, potencia activa en kWh).",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "16 A",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesEntrada": "IEC 320 C20 con cable de 3 metros",
                "ConexionesSalida": "(18) IEC 320 C13, (2) IEC 320 C19",
                "Formato": "Montaje vertical Zero-U (no ocupa espacio de servidores)",
                "GestionIndividual": "Control on/off por toma para reinicio remoto de servidores bloqueados",
                "Medicion": "Medición de corriente y energía con precisión de facturación del 1%"
            }, ensure_ascii=False),
            "Application": "Gestión remota de infraestructura de servidores en centros de datos y colocación (colocation)."
        },
        {
            "Code": "AP8959EU3",
            "Name": "PDU de Rack con Medición por Toma APC Switched Outlet Metered PDU 16A 230V (AP8959EU3)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Unidades de Distribución en Rack (Rack PDU)",
            "Series": "NetShelter rPDU",
            "Description": "PDU de rack de máxima visibilidad que mide el consumo individual de energía por cada toma de salida y permite la conmutación remota para evitar sobrecargas y auditar costos por servidor.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "16 A",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesSalida": "(21) IEC 320 C13, (3) IEC 320 C19",
                "ConexionesEntrada": "IEC 320 C20",
                "Formato": "Vertical 0U",
                "MedicionPorToma": "Monitoreo individual de amperaje y vatios por cada equipo conectado"
            }, ensure_ascii=False),
            "Application": "Centros de datos multiinquilino (Multi-tenant) y auditorías de consumo energético detalladas."
        },
        {
            "Code": "AP7921B",
            "Name": "PDU de Rack Conmutada APC Switched Rack PDU 16A 208/230V 1U Horizontal (AP7921B)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Unidades de Distribución en Rack (Rack PDU)",
            "Series": "NetShelter rPDU",
            "Description": "PDU conmutada de montaje horizontal de 1U para bastidores de 19 pulgadas. Ofrece 8 salidas IEC C13 con control individual y supervisión de corriente agregada.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "16 A",
                "TensionEntradaSalida": "208 V / 230 V CA",
                "ConexionesSalida": "(8) IEC 320 C13 conmutables",
                "ConexionesEntrada": "IEC 320 C20",
                "Formato": "Montaje Horizontal 1U",
                "GestionRed": "SNMP, Telnet, Web HTTPS"
            }, ensure_ascii=False),
            "Application": "Gabinetes pequeños de TI y racks de conmutación de red donde no cabe una PDU vertical."
        },
        {
            "Code": "AP7553",
            "Name": "PDU de Rack Básica APC Basic Rack PDU 32A 230V Zero-U (AP7553)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Unidades de Distribución en Rack (Rack PDU)",
            "Series": "NetShelter rPDU",
            "Description": "PDU vertical básica y robusta para distribución de alta corriente (32A) a múltiples servidores sin necesidad de funciones de red.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "32 A",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesSalida": "(20) IEC 320 C13, (4) IEC 320 C19",
                "ConexionesEntrada": "Clavija industrial IEC 309 32A 2P+E",
                "Formato": "Vertical 0U"
            }, ensure_ascii=False),
            "Application": "Distribución confiable y económica de energía en racks de servidores estándar."
        },
        {
            "Code": "EPDU1132M",
            "Name": "PDU de Rack con Medición APC Easy Rack PDU Metered 32A 230V Zero-U (EPDU1132M)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Unidades de Distribución en Rack (Rack PDU)",
            "Series": "NetShelter rPDU",
            "Description": "PDU de la serie Easy Rack con pantalla digital para monitorear la corriente agregada en amperios y evitar disparos intempestivos por sobrecarga.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "32 A",
                "TensionEntradaSalida": "230 V CA",
                "ConexionesSalida": "(20) IEC C13, (4) IEC C19",
                "ConexionesEntrada": "IEC 309 32A",
                "Formato": "0U vertical con pantalla digital LED"
            }, ensure_ascii=False),
            "Application": "Distribución en racks de TI comerciales con supervisión local de carga."
        },

        # =========================================================================
        # 9. ARMARIOS, RACKS Y GABINETES DE TI (NETSHELTER)
        # =========================================================================
        {
            "Code": "AR3100",
            "Name": "Gabinete Rack para Servidores APC NetShelter SX 42U 600x1070mm con puertas ventiladas (AR3100)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "NetShelter SX",
            "Description": "El gabinete de TI más vendido del mundo: rack estándar de 42U con diseño optimizado para flujo de aire frío/caliente, puertas perforadas con 65% de ventilación, paneles laterales removibles con cerradura y canales verticales integrados para cables.",
            "TechnicalSpecs": json.dumps({
                "CapacidadEspacio": "42U de 19 pulgadas",
                "Dimensiones": "Alto 1991 mm x Ancho 600 mm x Profundidad 1070 mm",
                "CapacidadCargaEstatica": "1363 kg (3000 lbs)",
                "CapacidadCargaDinamica": "1022 kg (2250 lbs)",
                "Puertas": "Delantera curva y trasera dividida, perforadas con patrón hexagonal",
                "RuedasYPies": "Ruedas de uso pesado y pies niveladores ajustables preinstalados",
                "GestionCables": "Canales verticales Zero-U para instalación de PDUs sin herramientas"
            }, ensure_ascii=False),
            "Application": "Alojamiento de servidores blade, conmutadores troncales, almacenamiento masivo y PDUs en salas de TI."
        },
        {
            "Code": "AR3300",
            "Name": "Gabinete Rack Profundo APC NetShelter SX 42U 600x1200mm para Servidores Densos (AR3300)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "NetShelter SX",
            "Description": "Gabinete con profundidad extendida de 1200 mm para alojar servidores modernos extra largos y dejar amplio espacio trasero para organización de cableado estructurado y canaletas de PDU.",
            "TechnicalSpecs": json.dumps({
                "CapacidadEspacio": "42U",
                "Dimensiones": "Alto 1991 mm x Ancho 600 mm x Profundidad 1200 mm",
                "CargaEstatica": "1363 kg",
                "EspacioPosterior": "Profundidad extra de 130 mm para cables y accesorios"
            }, ensure_ascii=False),
            "Application": "Centros de datos con servidores multinodo de gran profundidad y alta densidad de cableado."
        },
        {
            "Code": "AR3150",
            "Name": "Gabinete Rack Ancho APC NetShelter SX 42U 750x1070mm para Redes y Conmutación (AR3150)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "NetShelter SX",
            "Description": "Gabinete ancho de 750 mm con canales laterales adicionales para acomodar grandes haces de cables de red de cobre (Cat6A) y fibra óptica en conmutadores de core.",
            "TechnicalSpecs": json.dumps({
                "CapacidadEspacio": "42U",
                "Dimensiones": "Alto 1991 mm x Ancho 750 mm x Profundidad 1070 mm",
                "CargaEstatica": "1363 kg",
                "CanalesLaterales": "Espacio lateral dedicado para peinado y sujeción vertical de cableado"
            }, ensure_ascii=False),
            "Application": "Racks de telecomunicaciones, conmutadores Cisco Nexus / Catalyst y cuadros principales de distribución (MDF)."
        },
        {
            "Code": "AR3104",
            "Name": "Gabinete Rack Mediano APC NetShelter SX 24U 600x1070mm (AR3104)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "NetShelter SX",
            "Description": "Rack de media altura (24U) diseñado para sucursales, oficinas remotas y cuartos de control donde la altura de techo es limitada.",
            "TechnicalSpecs": json.dumps({
                "CapacidadEspacio": "24U",
                "Dimensiones": "Alto 1200 mm x Ancho 600 mm x Profundidad 1070 mm",
                "CargaEstatica": "907 kg (2000 lbs)"
            }, ensure_ascii=False),
            "Application": "Sucursales bancarias, plantas industriales y salas de automatización con espacio restringido."
        },
        {
            "Code": "AR100",
            "Name": "Gabinete de Pared para TI APC NetShelter WX 13U de montaje mural (AR100)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "NetShelter SX",
            "Description": "Gabinete metálico para montaje en pared con puerta frontal de vidrio de seguridad templado, cerradura con llave y panel trasero abatible para fácil acceso al cableado.",
            "TechnicalSpecs": json.dumps({
                "CapacidadEspacio": "13U de 19 pulgadas",
                "Dimensiones": "Alto 663 mm x Ancho 584 mm x Profundidad 631 mm",
                "CapacidadCarga": "91 kg fijado a pared",
                "Puerta": "Vidrio templado reversible con cerradura"
            }, ensure_ascii=False),
            "Application": "Instalación mural de switches, patch panels y UPS en pasillos, aulas y oficinas comerciales."
        },
        {
            "Code": "AR3812",
            "Name": "Gabinete Insonorizado para Oficina APC NetShelter CX 24U con Acabado en Madera (AR3812)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "NetShelter SX",
            "Description": "Rack de servidores con insonorización activa de hasta 18.5 dB y acabado tipo mueble de oficina. Permite colocar servidores ruidosos directamente en áreas de trabajo o salas de reuniones sin molestar.",
            "TechnicalSpecs": json.dumps({
                "CapacidadEspacio": "24U",
                "ReduccionRuido": "Atenuación acústica de 18.5 dB",
                "DisipacionTermica": "Hasta 2.4 kW con ventiladores ultrasilenciosos integrados",
                "Acabado": "Laminado de roble cálido con ruedas integradas"
            }, ensure_ascii=False),
            "Application": "Oficinas abiertas, consultorios médicos, agencias y estudios de grabación sin cuarto de servidores dedicado."
        },

        # =========================================================================
        # 10. REGULADORES AUTOMÁTICOS DE VOLTAJE (LINE-R)
        # =========================================================================
        {
            "Code": "LE600-LM",
            "Name": "Regulador Automático de Voltaje APC Line-R 600VA 120V con 4 tomas (LE600-LM)",
            "BusinessLine": "Protección Eléctrica y Regulación",
            "Family": "Reguladores Automáticos de Voltaje (Line-R)",
            "Series": "Line-R",
            "Description": "Regulador de tensión electrónico compacto que corrige caídas y sobretensiones sin consumir baterías, garantizando un voltaje estable para aparatos electrónicos del hogar y oficina.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "600 VA / 300 W",
                "TensionEntrada": "120 V CA (rango de regulación 90 - 145 V)",
                "TensionSalida": "120 V CA ± 10%",
                "ConexionesSalida": "(4) NEMA 5-15R reguladas",
                "ConexionesEntrada": "NEMA 5-15P con interruptor automático térmico de reset"
            }, ensure_ascii=False),
            "Application": "Protección de televisores, computadoras personales, impresoras y consolas contra fluctuaciones de red."
        },
        {
            "Code": "LE1200-LM",
            "Name": "Regulador Automático de Voltaje APC Line-R 1200VA 120V con 8 tomas (LE1200-LM)",
            "BusinessLine": "Protección Eléctrica y Regulación",
            "Family": "Reguladores Automáticos de Voltaje (Line-R)",
            "Series": "Line-R",
            "Description": "Regulador de voltaje de alta capacidad de 1200VA / 600W con 8 tomas protegidas y supresor de picos transitorios integrado.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1200 VA / 600 W",
                "TensionEntrada": "120 V CA (rango 90 - 145 V)",
                "TensionSalida": "120 V CA ± 10%",
                "ConexionesSalida": "(8) NEMA 5-15R",
                "ProteccionSobretension": "Supresor de picos integrado",
                "IndicadoresLED": "LEDs indicadores de tensión normal, alta o baja"
            }, ensure_ascii=False),
            "Application": "Equipos de sonido, sistemas de cine en casa, servidores pequeños y copiadoras de oficina."
        },
        {
            "Code": "LE1200I",
            "Name": "Regulador Automático de Voltaje APC Line-R 1200VA 230V con tomas IEC/Schuko (LE1200I)",
            "BusinessLine": "Protección Eléctrica y Regulación",
            "Family": "Reguladores Automáticos de Voltaje (Line-R)",
            "Series": "Line-R",
            "Description": "Regulador de voltaje de 1200VA para sistemas a 230V que protege electrodomésticos y equipos sensibles contra sobrevoltajes.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1200 VA / 1200 W (FP = 1.0)",
                "TensionEntrada": "230 V CA (rango 160 - 290 V)",
                "TensionSalida": "230 V CA regulada",
                "ConexionesSalida": "(4) IEC 320 C13"
            }, ensure_ascii=False),
            "Application": "Equipamiento de laboratorio y electrodomésticos en instalaciones a 220V."
        },

        # =========================================================================
        # 11. SUPRESORES DE SOBRETENSIÓN Y FILTROS (SURGEARREST)
        # =========================================================================
        {
            "Code": "PM5-GR",
            "Name": "Supresor de Sobretensión APC SurgeArrest Essential de 5 tomas con filtro EMI/RFI (PM5-GR)",
            "BusinessLine": "Protección Eléctrica y Regulación",
            "Family": "Supresores de Sobretensión (SurgeArrest)",
            "Series": "SurgeArrest",
            "Description": "Regleta de supresión de picos contra rayos y descargas atmosféricas con indicador luminoso de falla de tierra del cableado del edificio y modo a prueba de fallos.",
            "TechnicalSpecs": json.dumps({
                "NumeroTomas": "5 tomas de corriente protegidas",
                "TensionNominal": "230 V CA / 10 A",
                "ClasificacionEnergia": "918 Joules",
                "FiltroRuido": "Atenuación de ruido EMI/RFI < 40 dB",
                "Garantia": "Protección de por vida para equipos conectados"
            }, ensure_ascii=False),
            "Application": "Protección de computadoras de escritorio, pantallas y electrodomésticos del hogar."
        },
        {
            "Code": "PM6-GR",
            "Name": "Supresor de Sobretensión APC SurgeArrest Performance de 6 tomas (PM6-GR)",
            "BusinessLine": "Protección Eléctrica y Regulación",
            "Family": "Supresores de Sobretensión (SurgeArrest)",
            "Series": "SurgeArrest",
            "Description": "Supresor de sobretensiones de alto rendimiento con 6 salidas protegidas y diseño con amplio espaciado para transformadores grandes.",
            "TechnicalSpecs": json.dumps({
                "NumeroTomas": "6 tomas",
                "EnergiaSupresion": "1836 Joules",
                "CorrientePicoMaxima": "48 kA"
            }, ensure_ascii=False),
            "Application": "Centros de entretenimiento audiovisual y estaciones de trabajo de oficina."
        },
        {
            "Code": "PM8-GR",
            "Name": "Supresor de Sobretensión APC SurgeArrest Performance de 8 tomas con protección de antena (PM8-GR)",
            "BusinessLine": "Protección Eléctrica y Regulación",
            "Family": "Supresores de Sobretensión (SurgeArrest)",
            "Series": "SurgeArrest",
            "Description": "Supresor avanzado de 8 tomas con protección coaxial para televisión por cable y protección de línea telefónica / módem.",
            "TechnicalSpecs": json.dumps({
                "NumeroTomas": "8 tomas",
                "ClasificacionEnergia": "2693 Joules",
                "ProteccionLineasDatos": "Conector coaxial F y conectores telefónicos RJ-11"
            }, ensure_ascii=False),
            "Application": "Equipos de telecomunicaciones y televisores Smart conectados a cableoperadores."
        },

        # =========================================================================
        # 12. CARTUCHOS DE BATERÍA DE REEMPLAZO (RBC) Y TARJETAS DE GESTIÓN
        # =========================================================================
        {
            "Code": "RBC7",
            "Name": "Cartucho de Batería de Reemplazo APC RBC7 para Smart-UPS 1500 (RBC7)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "RBC Replacement Batteries",
            "Description": "Cartucho de batería de reemplazo original certificado por APC, sellado a prueba de fugas y sin mantenimiento para restaurar el rendimiento original del UPS.",
            "TechnicalSpecs": json.dumps({
                "TipoBateria": "Batería sellada de plomo-ácido regulada por válvula (VRLA)",
                "MontajeBateria": "Cartucho de batería cerrado plug-and-play",
                "Voltaje": "24 V CC",
                "Compatibilidad": "SMT1500, SMT1500I, SU1400, BP1400, DLA1500",
                "VidaUtil": "3 a 5 años"
            }, ensure_ascii=False),
            "Application": "Renovación preventiva de baterías para garantizar la autonomía en Smart-UPS 1500."
        },
        {
            "Code": "RBC55",
            "Name": "Cartucho de Batería de Reemplazo APC RBC55 para Smart-UPS 2200 / 3000 (RBC55)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "RBC Replacement Batteries",
            "Description": "Cartucho de batería de repuesto original de alta capacidad para modelos Smart-UPS de 2200VA y 3000VA con conexión rápida e instalación sin herramientas.",
            "TechnicalSpecs": json.dumps({
                "TipoBateria": "Plomo ácido VRLA a prueba de derrames",
                "Voltaje": "48 V CC",
                "Compatibilidad": "SMT2200, SMT3000, SUA2200, SUA3000",
                "Peso": "24.2 kg"
            }, ensure_ascii=False),
            "Application": "Reemplazo de baterías en UPS corporativos de 2.2kVA y 3kVA."
        },
        {
            "Code": "APCRBC140",
            "Name": "Cartucho de Batería de Reemplazo APC APCRBC140 para Smart-UPS On-Line SRT 5kVA - 10kVA (APCRBC140)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "RBC Replacement Batteries",
            "Description": "Cartucho modular original para los sistemas Smart-UPS On-Line de 5 kVA, 6 kVA, 8 kVA y 10 kVA. Instalación en caliente durante el funcionamiento normal sin apagar los servidores.",
            "TechnicalSpecs": json.dumps({
                "TipoBateria": "Plomo ácido VRLA de alta descarga",
                "Voltaje": "192 V CC nominal (módulo modular)",
                "Compatibilidad": "SRT5KXLT, SRT5KRMXLT, SRT6KXLT, SRT8KXLT, SRT10KXLT, SRT192BP",
                "Peso": "34.5 kg"
            }, ensure_ascii=False),
            "Application": "Mantenimiento crítico de bancos de baterías en centros de datos de misión continua."
        },
        {
            "Code": "APCRBC152",
            "Name": "Cartucho de Batería de Reemplazo APC APCRBC152 para Smart-UPS On-Line SRT 3000 (APCRBC152)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "RBC Replacement Batteries",
            "Description": "Cartucho original para Smart-UPS On-Line de 3000VA de las series SRT3000XLA y SRT3000RMXLA.",
            "TechnicalSpecs": json.dumps({
                "TipoBateria": "Plomo ácido VRLA",
                "Voltaje": "96 V CC",
                "Compatibilidad": "SRT3000XLA, SRT3000RMXLA, SRT96BP"
            }, ensure_ascii=False),
            "Application": "Sustitución de baterías en UPS On-Line de 3 kVA."
        },
        {
            "Code": "AP9630",
            "Name": "Tarjeta de Administración de Red APC UPS Network Management Card 2 (AP9630)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Tarjetas de Gestión y Monitoreo",
            "Series": "APC Network Management Cards",
            "Description": "Tarjeta de red para insertar en ranura SmartSlot de cualquier UPS APC. Permite la monitorización segura y el apagado automático desatendido de servidores físicos y virtuales mediante protocolo SNMP y HTTPS.",
            "TechnicalSpecs": json.dumps({
                "Protocolos": "SNMP v1/v3, HTTP/HTTPS, SSH, Telnet, Radius, Syslog",
                "ConexionRed": "Puerto Ethernet RJ-45 10/100 Mbps",
                "CompatibilidadUPS": "Todas las unidades Smart-UPS, Matrix-UPS y Symmetra con SmartSlot",
                "ApagadoControlado": "Licencia y soporte para software PowerChute Network Shutdown"
            }, ensure_ascii=False),
            "Application": "Gestión remota por red de UPS en armarios de telecomunicaciones sin requerir PC conectada por USB."
        },
        {
            "Code": "AP9631",
            "Name": "Tarjeta de Administración de Red Ambiental APC Network Management Card 2 con Monitoreo de Temperatura (AP9631)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Tarjetas de Gestión y Monitoreo",
            "Series": "APC Network Management Cards",
            "Description": "Tarjeta de gestión avanzada con 2 puertos para sensores ambientales externos (temperatura y humedad) y 2 puertos de entrada de contactos secos para alarmas de apertura de puerta de gabinete.",
            "TechnicalSpecs": json.dumps({
                "Protocolos": "SNMP v1/v3, HTTPS, SSH, Modbus TCP",
                "PuertosSensores": "2 puertos universales de entrada/salida para sondas AP9335T / AP9335TH",
                "ContactosSecos": "2 relevadores de entrada para sensores de puerta o humo",
                "SondaIncluida": "Incluye sonda de temperatura AP9335T de 3.9 metros"
            }, ensure_ascii=False),
            "Application": "Supervisión ambiental y eléctrica unificada de racks de servidores remotos."
        },
        {
            "Code": "AP9640",
            "Name": "Tarjeta de Administración de Red de 3ra Generación APC Network Management Card 3 Gigabit (AP9640)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Tarjetas de Gestión y Monitoreo",
            "Series": "APC Network Management Cards",
            "Description": "Tarjeta de gestión de última generación con procesador de alta velocidad, conexión Gigabit Ethernet y arquitectura de ciberseguridad avanzada con arranque seguro (Secure Boot).",
            "TechnicalSpecs": json.dumps({
                "VelocidadRed": "Gigabit Ethernet 10/100/1000 Mbps",
                "Ciberseguridad": "Certificación de seguridad estricta, arranque seguro y soporte TLS 1.3",
                "AlmacenamientoRegistros": "Memoria flash expandida para historial de eventos y caídas de red",
                "Compatibilidad": "Smart-UPS SMT, SMX, SRT y Galaxy"
            }, ensure_ascii=False),
            "Application": "Data centers con normativas estrictas de ciberseguridad corporativa e infraestructura crítica."
        },
        {
            "Code": "AP9335TH",
            "Name": "Sensor Ambiental de Temperatura y Humedad APC para tarjetas NMC (AP9335TH)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Tarjetas de Gestión y Monitoreo",
            "Series": "APC Network Management Cards",
            "Description": "Sonda ambiental de precisión de 3.9 metros para conectar a tarjetas de red AP9631 o AP9641 y monitorear temperatura y humedad relativa dentro del rack de servidores.",
            "TechnicalSpecs": json.dumps({
                "RangoTemperatura": "0 °C a 55 °C (precisión ± 1 °C)",
                "RangoHumedad": "10 % a 90 % de humedad relativa (precisión ± 5 %)",
                "LongitudCable": "3.9 metros (12.8 pies)",
                "Conector": "RJ-45 para puertos de sensor universal"
            }, ensure_ascii=False),
            "Application": "Prevención de fallas por sobrecalentamiento o condensación en armarios de centros de datos."
        },
        # =========================================================================
        # 13. MÓDULOS DE BATERÍA EXTERNA SMART-UPS ON-LINE (SRT)
        # =========================================================================
        {
            "Code": "SRT192BP",
            "Name": "Módulo de Batería Externa 192V Torre APC Smart-UPS SRT para 5kVA - 10kVA (SRT192BP)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Banco de baterías externo de 192V en formato torre para extender la autonomía de Smart-UPS On-Line de 5 kVA a 10 kVA. Conexión en cadena tipo margarita (daisy-chain) que permite acoplar hasta 10 módulos en paralelo.",
            "TechnicalSpecs": json.dumps({
                "VoltajeBateria": "192 V CC",
                "Formato": "Torre",
                "TipoBateria": "Batería sellada de plomo-ácido VRLA",
                "Compatibilidad": "SRT5KXLT, SRT6KXLT, SRT8KXLT, SRT10KXLT",
                "Peso": "91 kg"
            }, ensure_ascii=False),
            "Application": "Suministro de energía ininterrumpida de varias horas durante cortes prolongados de la red eléctrica."
        },
        {
            "Code": "SRT192RMBP",
            "Name": "Módulo de Batería Externa 192V Rack 3U APC Smart-UPS SRT para 5kVA - 10kVA (SRT192RMBP)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Módulo de batería para montaje en bastidor de 19 pulgadas en 3U de altura. Incluye rieles de montaje en rack para acoplarse directamente bajo los UPS de 5kVA a 10kVA.",
            "TechnicalSpecs": json.dumps({
                "VoltajeBateria": "192 V CC",
                "Formato": "Montaje en Rack 3U (con rieles)",
                "Compatibilidad": "SRT5KRMXLT, SRT6KRMXLT, SRT8KRMXLT, SRT10KRMXLT",
                "Peso": "91 kg"
            }, ensure_ascii=False),
            "Application": "Centros de datos que exigen alta autonomía sin ocupar espacio de suelo fuera del rack."
        },
        {
            "Code": "SRT72BP",
            "Name": "Módulo de Batería Externa 72V Torre APC Smart-UPS SRT 2.2kVA (SRT72BP)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Módulo de batería externa de 72V para Smart-UPS On-Line de 2200VA en formato torre.",
            "TechnicalSpecs": json.dumps({
                "VoltajeBateria": "72 V CC",
                "Formato": "Torre",
                "Compatibilidad": "SRT2200XLA, SRT2200XLI"
            }, ensure_ascii=False),
            "Application": "Extensión de autonomía en servidores de rango medio y conmutadores telefónicos."
        },
        {
            "Code": "SRT72RMBP",
            "Name": "Módulo de Batería Externa 72V Rack 2U APC Smart-UPS SRT 2.2kVA (SRT72RMBP)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Módulo de batería en rack de 2U con rieles incluidos para Smart-UPS On-Line de 2.2kVA.",
            "TechnicalSpecs": json.dumps({
                "VoltajeBateria": "72 V CC",
                "Formato": "Rack 2U",
                "Compatibilidad": "SRT2200RMXLA, SRT2200RMXLA-NC"
            }, ensure_ascii=False),
            "Application": "Racks de comunicaciones con respaldo extendido para equipos de networking."
        },
        {
            "Code": "SRT96BP",
            "Name": "Módulo de Batería Externa 96V Torre APC Smart-UPS SRT 3kVA (SRT96BP)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Módulo de baterías de 96V para Smart-UPS On-Line de 3000VA en torre.",
            "TechnicalSpecs": json.dumps({
                "VoltajeBateria": "96 V CC",
                "Formato": "Torre",
                "Compatibilidad": "SRT3000XLA, SRT3000XLT, SRT3000XLI"
            }, ensure_ascii=False),
            "Application": "Prolongación de tiempo de respaldo en cuartos de telecomunicaciones."
        },
        {
            "Code": "SRT96RMBP",
            "Name": "Módulo de Batería Externa 96V Rack 2U APC Smart-UPS SRT 3kVA (SRT96RMBP)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Módulo de batería externa de 96V para montaje en bastidor de 2U con rieles para SRT3000RMXLA.",
            "TechnicalSpecs": json.dumps({
                "VoltajeBateria": "96 V CC",
                "Formato": "Rack 2U con rieles",
                "Compatibilidad": "SRT3000RMXLA, SRT3000RMXLT"
            }, ensure_ascii=False),
            "Application": "Respaldo prolongado de racks de servidores virtualizados."
        },
        # =========================================================================
        # 14. UPS CON TRANSFORMADOR REDUCTOR DE AISLAMIENTO (SERIE STEP-DOWN)
        # =========================================================================
        {
            "Code": "SRT3000XLT-5KTF",
            "Name": "UPS On-Line APC Smart-UPS SRT 3000VA 208V con Transformador Reductor a 120V (SRT3000XLT-5KTF)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Paquete que integra el UPS Smart-UPS On-Line de 3kVA a 208V con un transformador reductor (Step-Down Transformer) para entregar simultáneamente alimentación a 208V y 120V a través de tomas NEMA 5-20R.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "3000 VA / 2700 W",
                "TensionEntrada": "208 V CA nominal",
                "TensionesSalida": "208 V y 120 V CA simultáneas",
                "TomasSalida": "(2) NEMA L6-20R, (1) NEMA L6-30R, (12) NEMA 5-20R",
                "TransformadorAislamiento": "Step-Down Transformer integrado para desacoplo galvánico"
            }, ensure_ascii=False),
            "Application": "Racks mixtos que albergan tanto servidores de alta potencia a 208V como switches y routers a 120V."
        },
        {
            "Code": "SRT5KXLT-5KTF",
            "Name": "UPS On-Line APC Smart-UPS SRT 5000VA 208V con Transformador Reductor a 120V (SRT5KXLT-5KTF)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "UPS On-Line de 5kVA a 208V con módulo transformador reductor de 5kVA para brindar 12 tomas a 120V (NEMA 5-20R) y tomas a 208V (NEMA L6-20R y L6-30R).",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "5000 VA / 4800 W",
                "TensionEntrada": "208 V CA",
                "TensionesSalida": "208 V y 120 V CA",
                "TomasSalida": "(2) L6-20R, (2) L6-30R, (12) NEMA 5-20R",
                "Formato": "Torre / Rack combinado"
            }, ensure_ascii=False),
            "Application": "Centros de cómputo medianos con equipamiento heterogéneo de 120V y 208V."
        },
        {
            "Code": "SRT10KXLT-10KTF",
            "Name": "UPS On-Line APC Smart-UPS SRT 10000VA 208V con Transformador Reductor a 120V (SRT10KXLT-10KTF)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS On-Line de Doble Conversión",
            "Series": "Smart-UPS On-Line SRT",
            "Description": "Solución de energía completa de 10kVA con transformador de 10kVA para distribuir energía a 120V y 208V a múltiples racks de servidores desde una sola acometida.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "10000 VA / 10000 W (FP = 1.0)",
                "TensionEntrada": "208 V / 240 V CA",
                "TensionesSalida": "208 V y 120 V CA aisladas",
                "TomasSalida": "Bornera Hardwire, tomas L6-20R, L6-30R y múltiples grupos de tomas NEMA 5-20R"
            }, ensure_ascii=False),
            "Application": "Distribución eléctrica principal para salas de servidores completas con cargas mixtas."
        },
        # =========================================================================
        # 15. RACKS NETSHELTER ADICIONALES Y PDU DE ALTA DENSIDAD
        # =========================================================================
        {
            "Code": "AR3107",
            "Name": "Gabinete Rack de Alta Capacidad APC NetShelter SX 48U 600x1070mm (AR3107)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "NetShelter SX",
            "Description": "Gabinete de altura ampliada de 48U que maximiza la densidad vertical de servidores y patch panels en centros de datos con techos altos.",
            "TechnicalSpecs": json.dumps({
                "CapacidadEspacio": "48U de 19 pulgadas",
                "Dimensiones": "Alto 2258 mm x Ancho 600 mm x Profundidad 1070 mm",
                "CapacidadCarga": "1363 kg estática"
            }, ensure_ascii=False),
            "Application": "Centros de datos masivos y empresas de colocación de servidores."
        },
        {
            "Code": "AR3810",
            "Name": "Gabinete Insonorizado para Oficina APC NetShelter CX 18U (AR3810)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "NetShelter SX",
            "Description": "Gabinete compacto insonorizado de 18U con acabado en madera para colocar servidores y switches en oficinas sin cuarto de servidores.",
            "TechnicalSpecs": json.dumps({
                "CapacidadEspacio": "18U",
                "AtenuacionAcustica": "18.5 dB",
                "DisipacionTermica": "Hasta 1.8 kW"
            }, ensure_ascii=False),
            "Application": "Oficinas corporativas, estudios de diseño y sucursales sin espacio técnico aislado."
        },
        {
            "Code": "AP9562",
            "Name": "PDU de Rack Básica APC Basic Rack PDU 15A 120V 1U con 10 tomas NEMA (AP9562)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Unidades de Distribución en Rack (Rack PDU)",
            "Series": "NetShelter rPDU",
            "Description": "Regleta PDU de 1U de montaje horizontal para bastidores de 19 pulgadas con 10 tomas NEMA 5-15R e interruptor automático térmico.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "15 A (12 A continuo UL)",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(10) NEMA 5-15R",
                "ConexionesEntrada": "NEMA 5-15P con cable de 3.66 metros",
                "Formato": "Montaje Horizontal 1U"
            }, ensure_ascii=False),
            "Application": "Distribución confiable de energía para equipos de red y servidores compactos a 120V."
        },
        {
            "Code": "AP8866",
            "Name": "PDU de Rack Trifásica Monitorizada APC NetShelter Metered PDU 30A 208V 3PH (AP8866)",
            "BusinessLine": "Infraestructura de Racks y Distribución de Energía (PDU)",
            "Family": "Unidades de Distribución en Rack (Rack PDU)",
            "Series": "NetShelter rPDU",
            "Description": "PDU trifásica vertical de alta potencia con monitoreo en tiempo real por fase para servidores de Inteligencia Artificial y computación GPU.",
            "TechnicalSpecs": json.dumps({
                "CorrienteNominal": "30 A trifásica",
                "TensionEntrada": "208 V trifásico 3PH+G",
                "ConexionesSalida": "(30) IEC C13, (12) IEC C19",
                "ConexionesEntrada": "Clavija NEMA L21-30P",
                "Formato": "Vertical Zero-U"
            }, ensure_ascii=False),
            "Application": "Racks de servidores de alto cómputo, renderizado y servidores de IA con aceleradores GPU."
        },
        # =========================================================================
        # 16. MODELOS ADICIONALES DE BACK-UPS Y BATERÍAS RBC
        # =========================================================================
        {
            "Code": "BR1500MS",
            "Name": "UPS Interactivo de Alta Gama APC Back-UPS Pro 1500VA 120V con LCD y USB-C (BR1500MS)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS interactivo de 1500VA / 900W con onda senoidal aproximada, pantalla LCD interactiva con diagnóstico de autonomía en minutos, regulación de voltaje AVR y puertos USB Type-C de carga rápida.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1500 VA / 900 W",
                "TensionEntradaSalida": "120 V CA",
                "Tomas": "10 tomas NEMA 5-15R (6 con batería y supresión, 4 solo supresión)",
                "CargaUSB": "1 puerto USB Type-C y 1 puerto USB Type-A",
                "ProteccionRed": "Línea Ethernet Gigabit de 1 Gbps",
                "BateriasExternas": "Compatible con paquete de batería externa BR24BPG para autonomía extendida"
            }, ensure_ascii=False),
            "Application": "Estaciones de trabajo de ingeniería, computadoras de gaming avanzadas y servidores NAS de oficina."
        },
        {
            "Code": "BVX900L-LM",
            "Name": "UPS Interactivo APC Easy UPS BVX 900VA 120V con tomas NEMA (BVX900L-LM)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS interactivo de 900VA / 480W con regulación automática de voltaje AVR para proteger equipos electrónicos ante caídas y subidas de tensión.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "900 VA / 480 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(6) NEMA 5-15R protegidas",
                "Formato": "Torre compacta"
            }, ensure_ascii=False),
            "Application": "Oficinas, puestos de cajero, computadoras con doble monitor y puntos de acceso Wi-Fi."
        },
        {
            "Code": "BVX1600L-LM",
            "Name": "UPS Interactivo APC Easy UPS BVX 1600VA 120V con tomas NEMA (BVX1600L-LM)",
            "BusinessLine": "Sistemas de Alimentación Ininterrumpida (UPS)",
            "Family": "UPS Residenciales y Oficina (Back-UPS)",
            "Series": "Back-UPS / Back-UPS Pro",
            "Description": "UPS interactivo de 1600VA / 900W con 6 tomas NEMA para proteger computadoras de diseño y servidores de punto de venta.",
            "TechnicalSpecs": json.dumps({
                "CapacidadPotencia": "1600 VA / 900 W",
                "TensionEntradaSalida": "120 V CA",
                "ConexionesSalida": "(6) NEMA 5-15R",
                "Formato": "Torre"
            }, ensure_ascii=False),
            "Application": "Estaciones de trabajo de oficinas medianas y centrales de seguridad."
        },
        {
            "Code": "RBC24",
            "Name": "Cartucho de Batería de Reemplazo APC RBC24 para Smart-UPS XL (RBC24)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "RBC Replacement Batteries",
            "Description": "Cartucho de batería de reemplazo original certificado APC sellado y libre de mantenimiento.",
            "TechnicalSpecs": json.dumps({
                "TipoBateria": "Plomo ácido VRLA",
                "Voltaje": "24 V CC",
                "Compatibilidad": "Smart-UPS XL 1400VA, SUA1400RMXL3U, SUA750XL"
            }, ensure_ascii=False),
            "Application": "Reemplazo de baterías en UPS modulares de servidores."
        },
        {
            "Code": "RBC43",
            "Name": "Cartucho de Batería de Reemplazo APC RBC43 para Smart-UPS RM 2U (RBC43)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "RBC Replacement Batteries",
            "Description": "Cartucho original para modelos de Smart-UPS en rack de 2U como SUA2200RM2U y SUA3000RM2U.",
            "TechnicalSpecs": json.dumps({
                "TipoBateria": "Plomo ácido VRLA",
                "Voltaje": "48 V CC",
                "Compatibilidad": "SUA2200RM2U, SUA3000RM2U, SUM1500RMXL2U, SUM3000RMXL2U",
                "Peso": "19.1 kg"
            }, ensure_ascii=False),
            "Application": "Mantenimiento de UPS en bastidor de centros de datos."
        },
        {
            "Code": "APCRBC141",
            "Name": "Cartucho de Batería de Reemplazo APC APCRBC141 para Smart-UPS SRT 2.2kVA (APCRBC141)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Baterías de Reemplazo y Módulos Externos",
            "Series": "RBC Replacement Batteries",
            "Description": "Cartucho original sellado para Smart-UPS On-Line de 2200VA (SRT2200XLA y SRT2200RMXLA).",
            "TechnicalSpecs": json.dumps({
                "TipoBateria": "Plomo ácido VRLA",
                "Voltaje": "72 V CC",
                "Compatibilidad": "SRT2200XLA, SRT2200RMXLA, SRT72BP, SRT72RMBP",
                "Peso": "25 kg"
            }, ensure_ascii=False),
            "Application": "Reemplazo de batería en UPS On-Line de 2.2 kVA."
        },
        {
            "Code": "AP9641",
            "Name": "Tarjeta de Administración de Red APC Network Management Card 3 con Monitoreo Ambiental (AP9641)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Tarjetas de Gestión y Monitoreo",
            "Series": "APC Network Management Cards",
            "Description": "Tarjeta de gestión de red Gigabit de 3ra generación que incluye puertos para sensores ambientales externos de temperatura y humedad con seguridad HTTPS y TLS 1.3.",
            "TechnicalSpecs": json.dumps({
                "ConexionRed": "Gigabit Ethernet 10/100/1000 Mbps",
                "Protocolos": "SNMP v1/v3, HTTPS, SSH, Modbus TCP, BACnet",
                "PuertosSensores": "2 puertos universales para sensores ambientales AP9335T / AP9335TH",
                "Ciberseguridad": "Arranque seguro (Secure Boot) y cifrado fuerte"
            }, ensure_ascii=False),
            "Application": "Gestión remota con supervisión ambiental de centros de datos modernos de misión crítica."
        },
        {
            "Code": "SRVRK1",
            "Name": "Kit de Rieles de Montaje en Rack de 4 Postes APC Easy UPS SRV 1kVA - 3kVA (SRVRK1)",
            "BusinessLine": "Accesorios y Baterías de Respaldo",
            "Family": "Armarios y Racks de TI (NetShelter)",
            "Series": "Easy UPS SRV/SRVL",
            "Description": "Kit de rieles ajustables de acero galvanizado para instalar modelos Easy UPS SRV de 1kVA a 3kVA en bastidores estándar de 19 pulgadas.",
            "TechnicalSpecs": json.dumps({
                "AjusteProfundidad": "520 mm a 910 mm",
                "Compatibilidad": "Easy UPS SRV 1kVA, 2kVA, 3kVA en rack",
                "Material": "Acero zincado de alta resistencia"
            }, ensure_ascii=False),
            "Application": "Montaje seguro en bastidor de 19 pulgadas de UPS y bancos de batería."
        }
    ]

    # DEDUPLICACIÓN ESTRICTA Y LOG DE REPETIDOS
    seen_codes = {}
    duplicates_detected = []
    
    for p in raw_products:
        code_key = p["Code"].strip().upper()
        if code_key in seen_codes:
            duplicates_detected.append(code_key)
            # Conservar la versión con especificaciones técnicas más ricas o descriptivas
            existing = seen_codes[code_key]
            if len(p.get("Description", "")) > len(existing.get("Description", "")):
                seen_codes[code_key] = p
        else:
            seen_codes[code_key] = p

    print(f"\n[DEDUPLICACIÓN APC]")
    print(f"  Total productos analizados en memoria: {len(raw_products)}")
    print(f"  Duplicados detectados y consolidados: {len(duplicates_detected)}")
    if duplicates_detected:
        print(f"  Códigos duplicados resueltos: {duplicates_detected}")
    print(f"  Total productos únicos resultantes: {len(seen_codes)}")
    
    return list(seen_codes.values())

def populate_apc():
    prods = get_apc_master_catalog()
    print(f"\nTotal productos APC listos para sembrar: {len(prods)}")
    
    # Target all databases
    db_paths = glob.glob("**/agente_ventas.db", recursive=True)
    db_paths.append("agente_ventas.db")
    db_paths = sorted(list(set(db_paths)))
    
    for db_path in db_paths:
        print(f"\nProcesando {db_path}...")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Eliminar registros previos de APC si existieran para evitar duplicados
        cur.execute("DELETE FROM ProductsCatalog WHERE Brand = 'APC';")
        
        insert_sql = """
            INSERT INTO ProductsCatalog 
            (Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application, Status, SearchCount, LastQueriedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        
        count = 0
        for p in prods:
            cur.execute(insert_sql, (
                "APC",
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
        print(f"  Insertados {count} productos de APC.")
        
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
    populate_apc()
