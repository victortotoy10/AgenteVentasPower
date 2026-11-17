import os
import sqlite3
import json
import shutil

def get_db_paths():
    paths = [
        os.path.abspath("agente_ventas.db"),
        os.path.abspath("AgentePower/agente_ventas.db"),
        os.path.abspath("AgentePower/bin/Debug/net8.0/agente_ventas.db"),
        os.path.abspath("AgentePower/bin/Release/net8.0/agente_ventas.db"),
        os.path.abspath("publish/agente_ventas.db")
    ]
    valid = []
    for p in paths:
        if os.path.exists(p) and os.path.getsize(p) > 0:
            valid.append(p)
    return valid

def get_abb_catalog_data():
    brand = "ABB"
    items = []

    # =========================================================================
    # 1. LÍNEA: DISTRIBUCIÓN ELÉCTRICA EN BAJA TENSIÓN
    # =========================================================================
    line_dist = "Distribución Eléctrica"

    # 1.1 Interruptores Termomagnéticos Modulares System pro M compact S200 / S200M (6 kA / 10 kA Curva C)
    currents_s200 = [6, 10, 16, 20, 25, 32, 40, 50, 63]
    for c in currents_s200:
        # 1P
        code_1p = f"S201-C{c}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "System pro M compact S200", code_1p,
            f"Interruptor Automático Modular S201-C{c} 1P {c}A Curva C 6kA/10kA",
            f"Interruptor magnetotérmico unipolar para protección contra sobrecargas y cortocircuitos en instalaciones terciarias e industriales",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "6 kA (IEC/EN 60898-1) / 10 kA (IEC/EN 60947-2)", "Tension": "230/400V AC", "Montaje": "Riel DIN 35mm"}),
            "Protección de circuitos monofásicos de iluminación, tomas y control en tableros de distribución"
        ))
        # 2P
        code_2p = f"S202-C{c}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "System pro M compact S200", code_2p,
            f"Interruptor Automático Modular S202-C{c} 2P {c}A Curva C 6kA/10kA",
            f"Interruptor magnetotérmico bipolar para protección de circuitos derivados monofásicos bifilares y bifásicos",
            json.dumps({"Polos": "2P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "6 kA / 10 kA", "Tension": "400V AC", "Montaje": "Riel DIN 35mm"}),
            "Protección de equipos bifásicos, acondicionadores de aire, UPS y alimentadores secundarios"
        ))
        # 3P
        code_3p = f"S203-C{c}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "System pro M compact S200", code_3p,
            f"Interruptor Automático Modular S203-C{c} 3P {c}A Curva C 6kA/10kA",
            f"Interruptor magnetotérmico tripolar industrial para protección de cargas trifásicas y alimentadores",
            json.dumps({"Polos": "3P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "6 kA / 10 kA", "Tension": "400V AC", "Montaje": "Riel DIN 35mm"}),
            "Distribución trifásica en centros de control de motores, tableros de fuerza y climatización"
        ))

    # 1.2 Interruptores Diferenciales Puros System pro M compact F200 (RCCBs)
    items.extend([
        (brand, line_dist, "Interruptores Diferenciales", "System pro M compact F200", "F202AC-25/0.03", "Interruptor Diferencial F202 AC 2P 25A 30mA", "Dispositivo de corriente residual bipolar para protección de personas contra contactos directos e indirectos", json.dumps({"Polos": "2P", "Corriente": "25A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC", "Norma": "IEC/EN 61008"}), "Protección diferencial en circuitos monofásicos comerciales y residenciales"),
        (brand, line_dist, "Interruptores Diferenciales", "System pro M compact F200", "F202AC-40/0.03", "Interruptor Diferencial F202 AC 2P 40A 30mA", "Interruptor diferencial bipolar de 40A clase AC para cuadros generales", json.dumps({"Polos": "2P", "Corriente": "40A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC"}), "Cabecera de tableros de distribución monofásicos de 40A"),
        (brand, line_dist, "Interruptores Diferenciales", "System pro M compact F200", "F202AC-63/0.03", "Interruptor Diferencial F202 AC 2P 63A 30mA", "Interruptor diferencial bipolar de 63A para acometidas monofásicas de alta demanda", json.dumps({"Polos": "2P", "Corriente": "63A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC"}), "Protección de acometidas monofásicas industriales y comerciales"),
        (brand, line_dist, "Interruptores Diferenciales", "System pro M compact F200", "F204AC-25/0.03", "Interruptor Diferencial F204 AC 4P 25A 30mA", "Dispositivo de corriente residual tetrapolar para circuitos trifásicos con neutro", json.dumps({"Polos": "4P", "Corriente": "25A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Protección diferencial en talleres, laboratorios y tableros trifásicos"),
        (brand, line_dist, "Interruptores Diferenciales", "System pro M compact F200", "F204AC-40/0.03", "Interruptor Diferencial F204 AC 4P 40A 30mA", "Interruptor diferencial industrial tetrapolar de 40A para protección humana y contra incendios", json.dumps({"Polos": "4P", "Corriente": "40A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Cuadros generales de plantas industriales y edificios comerciales"),
        (brand, line_dist, "Interruptores Diferenciales", "System pro M compact F200", "F204AC-63/0.03", "Interruptor Diferencial F204 AC 4P 63A 30mA", "Interruptor diferencial tetrapolar de alta capacidad para 63A clase AC", json.dumps({"Polos": "4P", "Corriente": "63A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Cabecera de cuadros de fuerza y distribución en media industria")
    ])

    # 1.3 Protectores contra Sobretensiones Transitorias OVR (DPS / SPD)
    items.extend([
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "OVR", "OVR T2 1N 40-275 P", "Protector de Sobretensiones OVR Tipo 2 1P+N 40kA", "Descargador de sobretensiones transitorias monofásico enchufable para protección de equipos electrónicos sensibles", json.dumps({"Polos": "1P+N", "Tipo": "Tipo 2", "Imax": "40 kA", "In": "20 kA", "Up": "1.4 kV", "Tension": "230V AC", "Cartuchos": "Enchufables recambiables"}), "Protección de equipos electrónicos, racks de comunicaciones y servidores monofásicos"),
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "OVR", "OVR T2 3N 40-275 P TS", "Protector de Sobretensiones OVR Tipo 2 3P+N 40kA con Contacto Remoto", "Descargador industrial tetrapolar para redes trifásicas con neutro y contacto de señalización a distancia (TS)", json.dumps({"Polos": "3P+N", "Tipo": "Tipo 2", "Imax": "40 kA", "In": "20 kA", "Up": "1.4 kV", "Tension": "230/400V AC", "ContactoAuxiliar": "1 C/O remoto"}), "Cabecera de tableros de distribución trifásicos en fábricas y edificios terciarios"),
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "OVR", "OVR T1-T2 3N 12.5-275S P", "Protector Combinado contra Rayos y Sobretensiones Tipo 1+2 3P+N 50kA", "Descargador combinado de corrientes de rayo y sobretensiones transitorias para acometidas principales", json.dumps({"Polos": "3P+N", "Tipo": "Tipo 1+2", "Iimp": "12.5 kA por polo", "Imax": "50 kA", "Up": "1.5 kV", "Norma": "IEC 61643-11"}), "Acometidas principales de edificios equipados con pararrayos y subestaciones eléctricas")
    ])

    # =========================================================================
    # 1.3b GAMA SYSTEM PRO M COMPACT DIN RAIL (UL 489 / UL 1077 / INDUSTRIAL)
    # Ref: Catálogo Oficial ABB 7.31 1SXU400208C0201_REV Y System pro M compact
    # =========================================================================

    # 1.3b.1 Interruptores Termomagnéticos Modulares UL 489 - Serie SU200M (Curva C, 10 kA a 277/480Y VAC)
    currents_su200m = [0.5, 1, 2, 5, 6, 10, 15, 16, 20, 25, 30, 32, 40, 50, 63]
    for c in currents_su200m:
        # 1P
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos UL 489", "System pro M compact SU200M", f"SU201M-C{c}",
            f"Interruptor Automático UL 489 SU201M-C{c} 1P {c}A Curva C 10kA",
            f"Interruptor magnetotérmico unipolar listado UL 489 / CSA 22.2 No. 5 para protección de circuitos derivados ramales",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "10 kA a 277V AC", "Certificacion": "UL 489 / CSA 22.2 No. 5 / IEC 60947-2", "Tension": "277V AC / 48V DC", "Montaje": "Riel DIN 35mm"}),
            "Protección de circuitos ramales terciarios, industriales y tableros bajo norma americana UL en exportación"
        ))
        # 2P (para calibres >= 10A)
        if c >= 10:
            items.append((
                brand, line_dist, "Interruptores Termomagnéticos UL 489", "System pro M compact SU200M", f"SU202M-C{c}",
                f"Interruptor Automático UL 489 SU202M-C{c} 2P {c}A Curva C 10kA",
                f"Interruptor magnetotérmico bipolar listado UL 489 para protección de circuitos bifásicos y alimentadores secundarios",
                json.dumps({"Polos": "2P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "10 kA a 480Y/277V AC", "Certificacion": "UL 489 / CSA 22.2 No. 5", "Tension": "480Y/277V AC", "Montaje": "Riel DIN 35mm"}),
                "Protección de cargas bifásicas, aires acondicionados, UPS y maquinaria industrial bajo certificación UL"
            ))
            # 3P (para calibres >= 10A)
            items.append((
                brand, line_dist, "Interruptores Termomagnéticos UL 489", "System pro M compact SU200M", f"SU203M-C{c}",
                f"Interruptor Automático UL 489 SU203M-C{c} 3P {c}A Curva C 10kA",
                f"Interruptor magnetotérmico tripolar industrial UL 489 para alimentadores y cargas trifásicas",
                json.dumps({"Polos": "3P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "10 kA a 480Y/277V AC", "Certificacion": "UL 489 / CSA 22.2 No. 5", "Tension": "480Y/277V AC", "Montaje": "Riel DIN 35mm"}),
                "Tableros de fuerza trifásica, centros de control de motores y tableros OEM de exportación"
            ))

    # 1.3b.2 Interruptores Termomagnéticos para Corriente Continua (DC) UL 489 - Serie SU200DC (Curva K)
    currents_su200dc = [10, 16, 20, 25, 32, 40, 50, 63]
    for c in currents_su200dc:
        # 1P (hasta 96V DC)
        items.append((
            brand, line_dist, "Interruptores DC Riel DIN UL 489", "System pro M compact SU200DC", f"SU201DC-K{c}",
            f"Interruptor DC UL 489 SU201DC-K{c} 1P {c}A Curva K 14kA",
            f"Interruptor termomagnético unipolar especializado para corriente continua hasta 96V DC bajo norma UL 489",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "K", "Tension": "96V DC", "PoderCorte": "14 kA a 96V DC", "Certificacion": "UL 489", "Montaje": "Riel DIN 35mm"}),
            "Sistemas de baterías, telecomunicaciones, subestaciones eléctricas y bancos de control DC"
        ))
        # 2P (hasta 192V DC)
        items.append((
            brand, line_dist, "Interruptores DC Riel DIN UL 489", "System pro M compact SU200DC", f"SU202DC-K{c}",
            f"Interruptor DC UL 489 SU202DC-K{c} 2P {c}A Curva K 14kA",
            f"Interruptor bipolar para corriente continua hasta 192V DC con extinción magnética de arco reforzada",
            json.dumps({"Polos": "2P", "Corriente": f"{c}A", "Curva": "K", "Tension": "192V DC", "PoderCorte": "14 kA a 192V DC", "Certificacion": "UL 489", "Montaje": "Riel DIN 35mm"}),
            "Protección de bancos de baterías de tracción, inversores fotovoltaicos y centros de datos"
        ))

    # 1.3b.3 Interruptores de Alto Rendimiento UL 489 - Serie S800U (Curva K, hasta 50 kA poder de interrupción)
    currents_s800u = [20, 30, 40, 50, 60, 70, 80, 90, 100]
    for c in currents_s800u:
        # 1P
        items.append((
            brand, line_dist, "Interruptores de Alto Rendimiento UL 489", "System pro M compact S800U", f"S801U-K{c}",
            f"Interruptor Automático Alto Rendimiento S801U-K{c} 1P {c}A 30kA/50kA",
            f"Interruptor termomagnético modular de alta capacidad de corte (hasta 50 kA) según UL 489 e IEC 60947-2",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "K", "Tension": "240V AC", "PoderCorte": "30 kA a 240V AC (UL 489) / 50 kA (IEC 60947-2)", "Montaje": "Riel DIN 35mm"}),
            "Protección de cabeceras de tableros de distribución en ambientes industriales severos con alta corriente de cortocircuito"
        ))
        # 3P
        items.append((
            brand, line_dist, "Interruptores de Alto Rendimiento UL 489", "System pro M compact S800U", f"S803U-K{c}",
            f"Interruptor Automático Alto Rendimiento S803U-K{c} 3P {c}A 50kA",
            f"Interruptor tripolar industrial de alta capacidad de ruptura de 50 kA para distribución principal en riel DIN",
            json.dumps({"Polos": "3P", "Corriente": f"{c}A", "Curva": "K", "Tension": "240V AC", "PoderCorte": "50 kA a 240V AC", "Certificacion": "UL 489 / IEC 60947-2", "Montaje": "Riel DIN 35mm"}),
            "Acometidas principales industriales, plantas de tratamiento y tableros generales de media potencia"
        ))

    # 1.3b.4 Protectores Suplementarios Universales AC/DC UL 1077 - Serie S200MUC (Curva C)
    currents_s200muc = [6, 10, 16, 20, 25, 32, 40, 50, 63]
    for c in currents_s200muc:
        items.append((
            brand, line_dist, "Protectores Suplementarios AC/DC UL 1077", "System pro M compact S200MUC", f"S201MUC-C{c}",
            f"Protector Suplementario AC/DC S201MUC-C{c} 1P {c}A Curva C 10kA",
            f"Disyuntor suplementario universal unipolar para aplicaciones tanto en corriente alterna como continua (hasta 250V DC)",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "C", "Tension": "277V AC / 250V DC", "PoderCorte": "10 kA", "Certificacion": "UL 1077 / CSA 22.2 / IEC 60947-2"}),
            "Circuitos de control de automatización, tableros solares y fuentes conmutadas mixtas AC/DC"
        ))
        items.append((
            brand, line_dist, "Protectores Suplementarios AC/DC UL 1077", "System pro M compact S200MUC", f"S202MUC-C{c}",
            f"Protector Suplementario AC/DC S202MUC-C{c} 2P {c}A Curva C 10kA",
            f"Disyuntor suplementario bipolar universal para hasta 480Y/277V AC y 500V DC con imanes permanentes de soplado",
            json.dumps({"Polos": "2P", "Corriente": f"{c}A", "Curva": "C", "Tension": "480Y/277V AC / 500V DC", "PoderCorte": "10 kA", "Certificacion": "UL 1077 / IEC 60947-2"}),
            "Protección de circuitos auxiliares en subestaciones, plantas fotovoltaicas y accionamientos de velocidad"
        ))

    # 1.3b.5 Protectores Suplementarios de Alta Capacidad UL 1077 - Serie S300P (Curva C, 25 kA poder de interrupción)
    currents_s300p = [10, 16, 20, 25, 32, 40, 50, 63]
    for c in currents_s300p:
        # 1P
        items.append((
            brand, line_dist, "Protectores Suplementarios Alta Capacidad UL 1077", "System pro M compact S300P", f"S301P-C{c}",
            f"Protector Suplementario S301P-C{c} 1P {c}A Curva C 25kA",
            f"Disyuntor modular unipolar compacto con excepcional poder de corte de 25 kA para protección de equipos sensibles",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "25 kA a 240V AC (IEC 60947-2) / 10 kA a 277V AC (UL 1077)", "Montaje": "Riel DIN 35mm"}),
            "Equipos de control industrial, servocontroladores y fuentes industriales donde se requiera alta capacidad de ruptura"
        ))
        # 3P
        items.append((
            brand, line_dist, "Protectores Suplementarios Alta Capacidad UL 1077", "System pro M compact S300P", f"S303P-C{c}",
            f"Protector Suplementario S303P-C{c} 3P {c}A Curva C 25kA",
            f"Disyuntor modular tripolar de alta capacidad de 25 kA con terminales cilíndricos bidireccionales",
            json.dumps({"Polos": "3P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "25 kA a 415V AC", "Montaje": "Riel DIN 35mm"}),
            "Protección de variadores de frecuencia, transformadores de control y maquinaria de precisión"
        ))

    # 1.3b.6 Interruptores Combinados Termomagnético y Diferencial (RCBO) - Serie DS201 UL (1P+N, 30mA)
    currents_ds201 = [6, 10, 16, 20, 25, 32]
    for c in currents_ds201:
        items.append((
            brand, line_dist, "Disyuntores Diferenciales Combinados (RCBO)", "System pro M compact DS201", f"DS201-C{c}A30UL",
            f"Disyuntor Diferencial Combinado DS201-C{c}A30UL 1P+N {c}A 30mA Curva C 6kA",
            f"Dispositivo compacto de 2 módulos que combina protección termomagnética contra sobrecarga/cortocircuito y diferencial 30mA contra fugas a tierra",
            json.dumps({"Polos": "1P+N (2 módulos)", "Corriente": f"{c}A", "Sensibilidad": "30mA", "Tipo": "Clase A", "Curva": "C", "PoderCorte": "6 kA (UL 1053 / IEC 61009-1)", "Tension": "120-240V AC"}),
            "Protección completa en un solo dispositivo para tomas de corriente en áreas húmedas, laboratorios y cocinas industriales"
        ))

    # 1.3b.7 Portafusibles Seccionables Modulares en Riel DIN - Serie E 90 (hasta 32A, 690V AC / 1000V DC)
    items.extend([
        (brand, line_dist, "Portafusibles Seccionables Modulares", "System pro M compact E 90", "E91/32", "Portafusible Modular E 91/32 1P 32A 690V AC (10x38 mm)", "Portafusible seccionable unipolar en riel DIN para cartuchos cilíndricos 10x38 mm hasta 32A", json.dumps({"Polos": "1P", "Corriente": "32A", "Tension": "690V AC", "Cartucho": "10x38 mm", "Norma": "IEC 60947-3 / UL 4248-1", "Montaje": "Riel DIN 35mm"}), "Protección de transformadores de maniobra, instrumentos de medición y circuitos auxiliares"),
        (brand, line_dist, "Portafusibles Seccionables Modulares", "System pro M compact E 90", "E92/32", "Portafusible Modular E 92/32 2P 32A 690V AC (10x38 mm)", "Portafusible seccionable bipolar para cartuchos cilíndricos 10x38 mm", json.dumps({"Polos": "2P", "Corriente": "32A", "Tension": "690V AC", "Cartucho": "10x38 mm", "Montaje": "Riel DIN 35mm"}), "Protección de líneas bifásicas y circuitos de control de potencia"),
        (brand, line_dist, "Portafusibles Seccionables Modulares", "System pro M compact E 90", "E93/32", "Portafusible Modular E 93/32 3P 32A 690V AC (10x38 mm)", "Portafusible seccionable tripolar para protección trifásica con cartuchos 10x38 mm", json.dumps({"Polos": "3P", "Corriente": "32A", "Tension": "690V AC", "Cartucho": "10x38 mm", "Montaje": "Riel DIN 35mm"}), "Protección trifásica de condensadores, variadores y pequeños motores"),
        (brand, line_dist, "Portafusibles Seccionables Modulares", "System pro M compact E 90", "E91N/32", "Portafusible Modular E 91N/32 1P+N 32A 690V AC", "Portafusible unipolar con neutro pasante seccionable para cuadros de distribución", json.dumps({"Polos": "1P+N", "Corriente": "32A", "Tension": "690V AC", "Cartucho": "10x38 mm"}), "Cuadros de distribución terciaria y protección de circuitos de alumbrado"),
        (brand, line_dist, "Portafusibles Seccionables Modulares", "System pro M compact E 90", "E90PV/32", "Portafusible Fotovoltaico E 90 PV 1P 32A 1000V DC (10x38 mm)", "Portafusible modular especializado para sistemas solares fotovoltaicos hasta 1000V DC", json.dumps({"Polos": "1P", "Corriente": "32A", "Tension": "1000V DC", "Norma": "UL 4248-19 / IEC 60269-6 (gPV)", "Cartucho": "10x38 mm gPV"}), "Cajas de combinación de strings fotovoltaicos e inversores solares fotovoltaicos")
    ])

    # 1.3b.8 Supresores de Sobretensiones Transitorias Especializados - Series OVR T2 & OVR PV (Solar)
    items.extend([
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "OVR PV", "OVR-PV-40-1000P", "Protector de Sobretensiones Solar OVR PV 40-1000 P 40kA 1000V DC", "Descargador de sobretensiones transitorias para instalaciones solares fotovoltaicas de hasta 1000V DC con cartuchos extraíbles", json.dumps({"Polos": "2P (+/-)", "Tipo": "Tipo 2 Fotovoltaico", "Tension": "1000V DC", "Imax": "40 kA", "In": "20 kA", "Norma": "UL 1449 / EN 50539-11"}), "Protección del lado DC en inversores solares y string boxes fotovoltaicas"),
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "OVR PV", "OVR-PV-40-1500P", "Protector de Sobretensiones Solar OVR PV 40-1500 P 40kA 1500V DC", "Descargador de sobretensiones de alta tensión para granjas solares fotovoltaicas de escala utility hasta 1500V DC", json.dumps({"Polos": "2P (+/-)", "Tipo": "Tipo 2 Fotovoltaico", "Tension": "1500V DC", "Imax": "40 kA", "In": "20 kA"}), "Parques solares a gran escala e inversores centrales de 1500V DC")
    ])

    # 1.4 Cajas Moldeadas Estándar FORMULA A1 y A2 (15A a 250A)
    # Ref: BuyLog Section 6 Molded Case Circuit Breakers
    items.extend([
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A015TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 15A 10kA TMF", "Interruptor termomagnético fijo compacto para protección de pequeños alimentadores trifásicos", json.dumps({"Polos": "3P", "Corriente": "15A", "PoderCorte": "10 kA a 240V / 5 kA a 415V", "Disparador": "TMF Fijo", "Conexion": "Terminales frontales F"}), "Protección de acometidas secundarias y cargas pequeñas de fuerza"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A020TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 20A 10kA TMF", "Interruptor de caja moldeada termomagnético fijo de 20A", json.dumps({"Polos": "3P", "Corriente": "20A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Alimentadores secundarios y bombas pequeñas"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A030TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 30A 10kA TMF", "Interruptor de caja moldeada termomagnético de 30A", json.dumps({"Polos": "3P", "Corriente": "30A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Tableros de fuerza en talleres y comercios"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A040TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 40A 10kA TMF", "Interruptor de caja moldeada termomagnético de 40A", json.dumps({"Polos": "3P", "Corriente": "40A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Protección de alimentadores de climatización y fuerza"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A050TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 50A 10kA TMF", "Interruptor de caja moldeada termomagnético de 50A", json.dumps({"Polos": "3P", "Corriente": "50A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Cuadros de distribución de maquinaria y talleres"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A060TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 60A 10kA TMF", "Interruptor de caja moldeada termomagnético de 60A", json.dumps({"Polos": "3P", "Corriente": "60A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Protección principal de tableros comerciales"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A070TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 70A 10kA TMF", "Interruptor de caja moldeada termomagnético de 70A", json.dumps({"Polos": "3P", "Corriente": "70A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Alimentadores generales de subdistribución"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A080TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 80A 10kA TMF", "Interruptor de caja moldeada termomagnético de 80A", json.dumps({"Polos": "3P", "Corriente": "80A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Distribución de potencia en talleres y almacenes"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A100TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 100A 10kA TMF", "Interruptor de caja moldeada de 100A para cabecera de tableros", json.dumps({"Polos": "3P", "Corriente": "100A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Cabecera principal de tableros de distribución comercial"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A1", "A1A125TW-3", "Interruptor en Caja Moldeada FORMULA A1 3P 125A 10kA TMF", "Interruptor de caja moldeada de 125A compacto", json.dumps({"Polos": "3P", "Corriente": "125A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Cabeceras de cuadros secundarios de 125A"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A2", "A2A125TW-3", "Interruptor en Caja Moldeada FORMULA A2 3P 125A 10kA TMF", "Interruptor termomagnético de caja moldeada bastidor A2 para 125A", json.dumps({"Polos": "3P", "Corriente": "125A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Acometidas de media potencia industrial"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A2", "A2A150TW-3", "Interruptor en Caja Moldeada FORMULA A2 3P 150A 10kA TMF", "Interruptor de caja moldeada para 150A bastidor A2", json.dumps({"Polos": "3P", "Corriente": "150A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Alimentadores de planta y cuadros de climatización"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A2", "A2A175TW-3", "Interruptor en Caja Moldeada FORMULA A2 3P 175A 10kA TMF", "Interruptor de caja moldeada de 175A", json.dumps({"Polos": "3P", "Corriente": "175A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Subestaciones secundarias y bombas de proceso"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A2", "A2A200TW-3", "Interruptor en Caja Moldeada FORMULA A2 3P 200A 10kA TMF", "Interruptor de potencia en caja moldeada para 200A", json.dumps({"Polos": "3P", "Corriente": "200A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Protección principal en tableros secundarios de planta"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A2", "A2A225TW-3", "Interruptor en Caja Moldeada FORMULA A2 3P 225A 10kA TMF", "Interruptor de potencia de 225A", json.dumps({"Polos": "3P", "Corriente": "225A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Alimentadores de plantas de manufactura"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "FORMULA A2", "A2A250TW-3", "Interruptor en Caja Moldeada FORMULA A2 3P 250A 10kA TMF", "Interruptor de caja moldeada de máxima capacidad de la gama FORMULA para 250A", json.dumps({"Polos": "3P", "Corriente": "250A", "PoderCorte": "10 kA a 240V", "Disparador": "TMF Fijo"}), "Cabecera principal de tableros de fuerza industrial hasta 250A")
    ])

    # 1.5 Cajas Moldeadas de Alta Gama SACE Tmax XT (XT1 a XT7, 16A a 1600A)
    # Ref: BuyLog Section 6 Molded Case Circuit Breakers
    items.extend([
        # XT1 (hasta 160A, TMD termomagnético)
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT1", "XT1C-160-TMD-3P-40A", "Interruptor Automático SACE Tmax XT1C 3P 40A 25kA TMD", "Interruptor termomagnético en caja moldeada industrial compacto con 25kA de poder de corte", json.dumps({"Polos": "3P", "Corriente": "40A", "PoderCorte": "25 kA a 415V", "Disparador": "TMD Fijo térmico / magnético", "Tension": "690V AC"}), "Protección de acometidas de fuerza y bombas pequeñas en plantas industriales"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT1", "XT1C-160-TMD-3P-63A", "Interruptor Automático SACE Tmax XT1C 3P 63A 25kA TMD", "Interruptor en caja moldeada de 63A con alta fiabilidad operativa", json.dumps({"Polos": "3P", "Corriente": "63A", "PoderCorte": "25 kA a 415V", "Disparador": "TMD Fijo"}), "Tableros de fuerza en talleres e industrias"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT1", "XT1N-160-TMD-3P-80A", "Interruptor Automático SACE Tmax XT1N 3P 80A 36kA TMD", "Interruptor en caja moldeada con 36kA de capacidad de ruptura para 80A", json.dumps({"Polos": "3P", "Corriente": "80A", "PoderCorte": "36 kA a 415V", "Disparador": "TMD Fijo"}), "Alimentadores de climatización e instalaciones terciarias críticas"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT1", "XT1N-160-TMD-3P-100A", "Interruptor Automático SACE Tmax XT1N 3P 100A 36kA TMD", "Interruptor industrial de 100A con 36kA de corte para cabeceras", json.dumps({"Polos": "3P", "Corriente": "100A", "PoderCorte": "36 kA a 415V", "Disparador": "TMD Fijo"}), "Cabecera principal de tableros de distribución de 100A"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT1", "XT1N-160-TMD-3P-125A", "Interruptor Automático SACE Tmax XT1N 3P 125A 36kA TMD", "Interruptor en caja moldeada de 125A", json.dumps({"Polos": "3P", "Corriente": "125A", "PoderCorte": "36 kA a 415V", "Disparador": "TMD Fijo"}), "Alimentadores generales de plantas manufactureras"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT1", "XT1N-160-TMD-3P-160A", "Interruptor Automático SACE Tmax XT1N 3P 160A 36kA TMD", "Interruptor termomagnético en caja moldeada para 160A con 36kA", json.dumps({"Polos": "3P", "Corriente": "160A", "PoderCorte": "36 kA a 415V", "Disparador": "TMD Fijo"}), "Protección de cuadros principales de fuerza secundaria"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT1", "XT1N-160-TMD-4P-160A", "Interruptor Automático SACE Tmax XT1N 4P 160A 36kA TMD", "Interruptor tetrapolar con neutro protegido al 100% para transferencias de red y generador", json.dumps({"Polos": "4P (3P+N)", "Corriente": "160A", "PoderCorte": "36 kA a 415V", "Disparador": "TMD Fijo"}), "Tableros de transferencia automática de 160A y redes con neutro distribuido"),

        # XT2 (hasta 160A, TMA regulable o Ekip DIP electrónico, poderes de corte hasta 70kA / 150kA)
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT2", "XT2S-160-TMA-3P-100A", "Interruptor Automático SACE Tmax XT2S 3P 100A 50kA TMA", "Interruptor industrial de alto poder de corte (50kA) con disparador térmico regulable (70-100A)", json.dumps({"Polos": "3P", "Corriente": "100A", "PoderCorte": "50 kA a 415V", "Disparador": "TMA Térmico y Magnético Regulable"}), "Acometidas industriales principales y protección cercana a transformadores"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT2", "XT2S-160-TMA-3P-160A", "Interruptor Automático SACE Tmax XT2S 3P 160A 50kA TMA", "Interruptor de caja moldeada regulable (112-160A) con 50kA de poder de corte", json.dumps({"Polos": "3P", "Corriente": "160A", "PoderCorte": "50 kA a 415V", "Disparador": "TMA Regulable"}), "Centros de control de motores y tableros principales de fábrica"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT2", "XT2N-160-EKIP-DIP-3P-160A", "Interruptor Automático SACE Tmax XT2N 3P 160A 36kA Ekip DIP LS/I", "Interruptor industrial con relé electrónico digital Ekip DIP para protección avanzada de sobrecarga y cortocircuito", json.dumps({"Polos": "3P", "Corriente": "160A", "PoderCorte": "36 kA a 415V", "Disparador": "Ekip DIP LS/I Electrónico (64-160A)", "Proteccion": "Sobrecarga L y Cortocircuito selectivo S / instantáneo I"}), "Instalaciones críticas, centros de datos y plantas hospitalarias"),

        # XT3 (hasta 250A, TMD robusto)
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT3", "XT3N-250-TMD-3P-200A", "Interruptor Automático SACE Tmax XT3N 3P 200A 36kA TMD", "Interruptor en caja moldeada robusto para 200A con 36kA de capacidad de ruptura", json.dumps({"Polos": "3P", "Corriente": "200A", "PoderCorte": "36 kA a 415V", "Disparador": "TMD Fijo"}), "Acometidas de media industria, canteras y plantas de proceso"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT3", "XT3N-250-TMD-3P-250A", "Interruptor Automático SACE Tmax XT3N 3P 250A 36kA TMD", "Interruptor de caja moldeada de 250A con 36kA para cabecera de fuerza", json.dumps({"Polos": "3P", "Corriente": "250A", "PoderCorte": "36 kA a 415V", "Disparador": "TMD Fijo"}), "Cabecera principal de tableros industriales de 250A"),

        # XT4 (hasta 250A, TMA regulable o Ekip DIP electrónico, hasta 70kA / 100kA)
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT4", "XT4S-250-TMA-3P-250A", "Interruptor Automático SACE Tmax XT4S 3P 250A 50kA TMA", "Interruptor de potencia regulable (175-250A) con 50kA de poder de corte", json.dumps({"Polos": "3P", "Corriente": "250A", "PoderCorte": "50 kA a 415V", "Disparador": "TMA Térmico y Magnético Regulable"}), "Grandes instalaciones comerciales, alimentadores de fuerza pesada"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT4", "XT4N-250-EKIP-DIP-3P-250A", "Interruptor Automático SACE Tmax XT4N 3P 250A 36kA Ekip DIP LS/I", "Interruptor con disparador electrónico digital configurable de 250A", json.dumps({"Polos": "3P", "Corriente": "250A", "PoderCorte": "36 kA a 415V", "Disparador": "Ekip DIP LS/I (100-250A)"}), "Protección selectiva de redes de distribución secundaria"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT4", "XT4S-250-TMA-4P-250A", "Interruptor Automático SACE Tmax XT4S 4P 250A 50kA TMA", "Interruptor tetrapolar regulable de 250A con 50kA de corte para transferencias", json.dumps({"Polos": "4P (3P+N)", "Corriente": "250A", "PoderCorte": "50 kA a 415V", "Disparador": "TMA Regulable"}), "Transferencias automáticas de grupos electrógenos de 150 kVA"),

        # XT5 (hasta 630A, TMD/TMA o Ekip DIP electrónico)
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT5", "XT5N-400-EKIP-DIP-3P-400A", "Interruptor Automático SACE Tmax XT5N 3P 400A 36kA Ekip DIP LS/I", "Interruptor de potencia industrial con unidad de control electrónica Ekip DIP LS/I", json.dumps({"Polos": "3P", "Corriente": "400A", "PoderCorte": "36 kA a 415V", "Disparador": "Ekip DIP LS/I Electrónico (160-400A)", "Proteccion": "Sobrecarga L y Cortocircuito selectivo S/I"}), "Cabeceras de plantas industriales, centros comerciales y transformadores"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT5", "XT5S-400-EKIP-DIP-3P-400A", "Interruptor Automático SACE Tmax XT5S 3P 400A 50kA Ekip DIP LS/I", "Interruptor de potencia industrial con 50kA de corte para redes exigentes", json.dumps({"Polos": "3P", "Corriente": "400A", "PoderCorte": "50 kA a 415V", "Disparador": "Ekip DIP LS/I Electrónico"}), "Redes de media tensión/baja tensión con elevado nivel de cortocircuito"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT5", "XT5N-630-EKIP-DIP-3P-630A", "Interruptor Automático SACE Tmax XT5N 3P 630A 36kA Ekip DIP LS/I", "Interruptor de potencia industrial para distribución de 630A", json.dumps({"Polos": "3P", "Corriente": "630A", "PoderCorte": "36 kA a 415V", "Disparador": "Ekip DIP LS/I Electrónico (250-630A)"}), "Cabecera de tableros generales de baja tensión (TGBT)"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT5", "XT5S-630-EKIP-DIP-3P-630A", "Interruptor Automático SACE Tmax XT5S 3P 630A 50kA Ekip DIP LS/I", "Interruptor de potencia de 630A con 50kA de capacidad de corte", json.dumps({"Polos": "3P", "Corriente": "630A", "PoderCorte": "50 kA a 415V", "Disparador": "Ekip DIP LS/I Electrónico"}), "Plantas de procesamiento, acerías y subestaciones de distribución"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT5", "XT5N-400-EKIP-DIP-4P-400A", "Interruptor Automático SACE Tmax XT5N 4P 400A 36kA Ekip DIP LS/I", "Interruptor tetrapolar electrónico de 400A para transferencias de potencia", json.dumps({"Polos": "4P (3P+N)", "Corriente": "400A", "PoderCorte": "36 kA a 415V", "Disparador": "Ekip DIP LS/I"}), "Alimentadores de generadores de emergencia de 300 kVA"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SACE Tmax XT5", "XT5N-630-EKIP-DIP-4P-630A", "Interruptor Automático SACE Tmax XT5N 4P 630A 36kA Ekip DIP LS/I", "Interruptor tetrapolar electrónico de 630A para generadores de 500 kVA", json.dumps({"Polos": "4P (3P+N)", "Corriente": "630A", "PoderCorte": "36 kA a 415V", "Disparador": "Ekip DIP LS/I"}), "Transferencias automáticas de gran potencia en hospitales y centros críticos"),

        # XT6 (hasta 1000A)
        (brand, line_dist, "Interruptores de Gran Potencia", "SACE Tmax XT6", "XT6N-800-EKIP-DIP-3P-800A", "Interruptor Automático SACE Tmax XT6N 3P 800A 36kA Ekip DIP LS/I", "Interruptor de caja moldeada pesada para acometidas principales de 800A", json.dumps({"Polos": "3P", "Corriente": "800A", "PoderCorte": "36 kA a 415V", "Disparador": "Ekip DIP LS/I Electrónico (320-800A)"}), "Entradas de transformadores de 500 kVA y subestaciones industriales"),
        (brand, line_dist, "Interruptores de Gran Potencia", "SACE Tmax XT6", "XT6N-1000-EKIP-DIP-3P-1000A", "Interruptor Automático SACE Tmax XT6N 3P 1000A 36kA Ekip DIP LS/I", "Interruptor de potencia industrial para 1000A", json.dumps({"Polos": "3P", "Corriente": "1000A", "PoderCorte": "36 kA a 415V", "Disparador": "Ekip DIP LS/I Electrónico (400-1000A)"}), "Salida de transformadores de 750 kVA en industrias"),

        # XT7 y XT7 M (hasta 1600A, mando manual o motorizado)
        (brand, line_dist, "Interruptores de Gran Potencia", "SACE Tmax XT7", "XT7S-1250-EKIP-DIP-3P-1250A", "Interruptor Automático SACE Tmax XT7S 3P 1250A 50kA Ekip DIP LS/I", "Interruptor de potencia de 1250A con 50kA de corte para transformadores de 1000 kVA", json.dumps({"Polos": "3P", "Corriente": "1250A", "PoderCorte": "50 kA a 415V", "Disparador": "Ekip DIP LS/I"}), "Acometidas generales de grandes fábricas y centros logísticos"),
        (brand, line_dist, "Interruptores de Gran Potencia", "SACE Tmax XT7", "XT7S-1600-EKIP-DIP-3P-1600A", "Interruptor Automático SACE Tmax XT7S 3P 1600A 50kA Ekip DIP LS/I", "Interruptor de potencia de 1600A para transformadores de 1250 kVA", json.dumps({"Polos": "3P", "Corriente": "1600A", "PoderCorte": "50 kA a 415V", "Disparador": "Ekip DIP LS/I"}), "Cabecera principal de subestación en baja tensión"),
        (brand, line_dist, "Interruptores de Gran Potencia", "SACE Tmax XT7 M", "XT7M-S-1600-EKIP-TOUCH-3P", "Interruptor Automático Motorizable SACE Tmax XT7 M 3P 1600A 50kA Ekip Touch", "Interruptor de potencia con mecanismo de resorte motorizable para sincronización y transferencias automáticas", json.dumps({"Polos": "3P", "Corriente": "1600A", "PoderCorte": "50 kA a 415V", "Disparador": "Ekip Touch LSI con pantalla gráfica", "Mecanismo": "Mandos frontales motorizables con resorte acumulado"}), "Sistemas de sincronización de generadores y transferencias automáticas de potencia")
    ])

    # 1.6 Interruptores de Bastidor Abierto (Air Circuit Breakers - ACB SACE Emax 2)
    items.extend([
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E1.2B-08-EKIP-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E1.2B 3P 800A 42kA Ekip Touch", "Interruptor abierto inteligente para protección de subestaciones y redes eléctricas", json.dumps({"Polos": "3P", "Corriente": "800A", "PoderCorte": "42 kA a 415V", "Disparador": "Ekip Touch LSI", "Montaje": "Fijo frontal"}), "Entrada de subestaciones y transformadores de 500 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E1.2B-10-EKIP-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E1.2B 3P 1000A 42kA Ekip Touch", "Interruptor abierto de 1000A con unidad de control táctil", json.dumps({"Polos": "3P", "Corriente": "1000A", "PoderCorte": "42 kA", "Disparador": "Ekip Touch LSI"}), "Subestaciones de 750 kVA en plantas industriales"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E1.2B-12-EKIP-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E1.2B 3P 1250A 42kA Ekip Touch", "Interruptor abierto de 1250A para centros de datos y plantas fabriles", json.dumps({"Polos": "3P", "Corriente": "1250A", "PoderCorte": "42 kA", "Disparador": "Ekip Touch LSI"}), "Protección de transformadores de 1000 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E1.2B-16-EKIP-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E1.2B 3P 1600A 42kA Ekip Touch", "Interruptor abierto de 1600A de bastidor compacto E1.2", json.dumps({"Polos": "3P", "Corriente": "1600A", "PoderCorte": "42 kA", "Disparador": "Ekip Touch LSI"}), "Grandes plantas industriales y complejos comerciales"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E2.2N-20-EKIP-HI-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E2.2N 3P 2000A 66kA Ekip Hi-Touch", "Interruptor abierto de 2000A con 66kA de corte, analizador de redes integrado y medición Clase 1", json.dumps({"Polos": "3P", "Corriente": "2000A", "PoderCorte": "66 kA", "Disparador": "Ekip Hi-Touch LSIG con display táctil a color", "Comunicacion": "Modbus TCP / PROFINET integrada"}), "Cabeceras de subestación con transformadores de 1500 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E2.2N-25-EKIP-HI-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E2.2N 3P 2500A 66kA Ekip Hi-Touch", "Interruptor abierto de 2500A para transformadores de 2000 kVA", json.dumps({"Polos": "3P", "Corriente": "2500A", "PoderCorte": "66 kA", "Disparador": "Ekip Hi-Touch LSIG"}), "Complejos industriales, acerías y puertos marítimos"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E4.2N-32-EKIP-HI-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E4.2N 3P 3200A 66kA Ekip Hi-Touch", "Interruptor abierto de 3200A para distribución primaria de alta energía", json.dumps({"Polos": "3P", "Corriente": "3200A", "PoderCorte": "66 kA", "Disparador": "Ekip Hi-Touch LSIG"}), "Subestaciones de 2500 kVA y plantas de procesos químicos"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E4.2H-40-EKIP-HI-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E4.2H 3P 4000A 85kA Ekip Hi-Touch", "Interruptor de gran bastidor de 4000A con 85kA de capacidad de ruptura", json.dumps({"Polos": "3P", "Corriente": "4000A", "PoderCorte": "85 kA", "Disparador": "Ekip Hi-Touch LSIG"}), "Grandes centrales eléctricas, minería y refinerías"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SACE Emax 2", "E6.2H-63-EKIP-HI-TOUCH-3P", "Interruptor Abierto SACE Emax 2 E6.2H 3P 6300A 100kA Ekip Hi-Touch", "Interruptor abierto de máxima potencia de 6300A con 100kA de poder de corte", json.dumps({"Polos": "3P", "Corriente": "6300A", "PoderCorte": "100 kA", "Disparador": "Ekip Hi-Touch LSIG con protección de tierra avanzada"}), "Subestaciones maestras y centrales de generación hidroeléctrica/termoeléctrica")
    ])

    # 1.7 Conmutadores y Transferencias Automáticas TruONE
    items.extend([
        (brand, line_dist, "Transferencias Automáticas de Red", "TruONE ATS", "OXA100U3S3QT", "Conmutador de Transferencia Automática TruONE 3P 100A", "Sistema integrado de transferencia automática red-generador con controlador y sensado de tensión en un solo bloque", json.dumps({"Polos": "3P", "Corriente": "100A", "Tension": "200-480V AC", "TiempoConmutacion": "<50ms", "Controlador": "Nivel 3 con pantalla táctil LCD"}), "Respaldo de emergencia en estaciones de servicio, comercios y clínicas"),
        (brand, line_dist, "Transferencias Automáticas de Red", "TruONE ATS", "OXA160U3S3QT", "Conmutador de Transferencia Automática TruONE 3P 160A", "Transferencia automática monobloc para 160A", json.dumps({"Polos": "3P", "Corriente": "160A", "Tension": "200-480V AC"}), "Sistemas de bombeo municipal y centros comerciales"),
        (brand, line_dist, "Transferencias Automáticas de Red", "TruONE ATS", "OXA250U3S3QT", "Conmutador de Transferencia Automática TruONE 3P 250A", "Transferencia automática industrial compacta de 250A", json.dumps({"Polos": "3P", "Corriente": "250A", "Tension": "200-480V AC"}), "Líneas de producción de plantas y almacenes frigoríficos"),
        (brand, line_dist, "Transferencias Automáticas de Red", "TruONE ATS", "OXA400U3S3QT", "Conmutador de Transferencia Automática TruONE 3P 400A", "Transferencia automática de potencia para generadores de 300 kVA", json.dumps({"Polos": "3P", "Corriente": "400A", "Tension": "200-480V AC"}), "Hospitales, centros de datos y plantas procesadoras"),
        (brand, line_dist, "Transferencias Automáticas de Red", "TruONE ATS", "OXA630U3S3QT", "Conmutador de Transferencia Automática TruONE 3P 630A", "Transferencia automática de alta potencia para generadores de 500 kVA", json.dumps({"Polos": "3P", "Corriente": "630A", "Tension": "200-480V AC"}), "Grandes industrias de manufactura y subestaciones de emergencia"),
        (brand, line_dist, "Enclavamientos para Transferencia", "SACE Tmax XT", "XT1-XT3-MIR-H", "Kit de Enclavamiento Mecánico Horizontal para SACE Tmax XT1-XT3", "Mecanismo de interbloqueo mecánico que impide el cierre simultáneo de dos interruptores", json.dumps({"Compatible": "SACE Tmax XT1 y XT3", "Tipo": "Varilla horizontal mecánica"}), "Montaje de transferencias manuales y de emergencia entre dos interruptores"),
        (brand, line_dist, "Enclavamientos para Transferencia", "SACE Tmax XT", "XT4-MIR-H", "Kit de Enclavamiento Mecánico Horizontal para SACE Tmax XT4", "Enclavamiento mecánico para dos interruptores XT4 de hasta 250A", json.dumps({"Compatible": "SACE Tmax XT4", "Tipo": "Varilla horizontal"}), "Construcción de tableros de transferencia red-generador de 250A"),
        (brand, line_dist, "Enclavamientos para Transferencia", "SACE Tmax XT", "XT5-MIR-H", "Kit de Enclavamiento Mecánico Horizontal para SACE Tmax XT5", "Placa base con balancín mecánico de interbloqueo para XT5", json.dumps({"Compatible": "SACE Tmax XT5 (400A/630A)", "Tipo": "Placa de interbloqueo"}), "Tableros de conmutación de potencia para transformador-generador de 400A/630A")
    ])

    # =========================================================================
    # 2. LÍNEA: CONTROL Y MANIOBRA DE MOTORES (AUTOMATIZACIÓN DE PROCESOS)
    # =========================================================================
    line_auto = "Automatización de Procesos"

    # 2.1 Contactores de Potencia Serie AF (Bobina Universal 100-250V AC/DC [-13])
    # Ref: Main Catalog Motor protection and control 1SBC100214C0202
    contactors_af = [
        # Tipo, Corriente AC-3, Potencia 400V, HP, Auxiliar, CodigoPedido
        ("AF09-30-10-13", "9A", "4.0 kW", "5.5 HP", "1 NA", "1SBL137001R1310"),
        ("AF09-30-01-13", "9A", "4.0 kW", "5.5 HP", "1 NC", "1SBL137001R1301"),
        ("AF12-30-10-13", "12A", "5.5 kW", "7.5 HP", "1 NA", "1SBL157001R1310"),
        ("AF12-30-01-13", "12A", "5.5 kW", "7.5 HP", "1 NC", "1SBL157001R1301"),
        ("AF16-30-10-13", "16A", "7.5 kW", "10 HP", "1 NA", "1SBL177001R1310"),
        ("AF16-30-01-13", "16A", "7.5 kW", "10 HP", "1 NC", "1SBL177001R1301"),
        ("AF26-30-00-13", "26A (25A)", "11.0 kW", "15 HP", "Sin aux", "1SBL237001R1300"),
        ("AF30-30-00-13", "30A", "15.0 kW", "20 HP", "Sin aux", "1SBL277001R1300"),
        ("AF38-30-00-13", "38A (32A)", "18.5 kW", "25 HP", "Sin aux", "1SBL297001R1300"),
        ("AF40-30-00-13", "40A", "18.5 kW", "25 HP", "Sin aux", "1SBL347001R1300"),
        ("AF52-30-00-13", "52A", "22.0 kW", "30 HP", "Sin aux", "1SBL367001R1300"),
        ("AF65-30-00-13", "65A", "30.0 kW", "40 HP", "Sin aux", "1SBL387001R1300"),
        ("AF80-30-00-13", "80A", "37.0 kW", "50 HP", "Sin aux", "1SBL397001R1300"),
        ("AF96-30-00-13", "96A", "45.0 kW", "60 HP", "Sin aux", "1SBL407001R1300")
    ]
    for code, cur, pwr, hp, aux, order_code in contactors_af:
        items.append((
            brand, line_auto, "Contactores de Potencia", "Serie AF", code,
            f"Contactor Tripolar AF {cur} {pwr} ({hp}) Bobina 100-250V AC/DC ({aux})",
            f"Contactor electromagnético tripolar de {cur} con tecnología de bobina electrónica de amplio rango 100-250V AC/DC, adecuado para motores de {pwr} ({hp}) a 400V y limitador de sobretensión integrado",
            json.dumps({"Polos": "3P", "Corriente": cur, "Potencia": f"{pwr} ({hp})", "TensionBobina": "100-250V AC/DC (50/60Hz)", "ContactosAuxiliares": aux, "CodigoPedido": order_code, "Montaje": "Riel DIN 35mm / Tornillo"}),
            f"Control y maniobra directa de motores eléctricos trifásicos hasta {pwr} ({hp}) o 25A/26A en bombas, ventiladores y compresores"
        ))

    # Contactores Serie AF con Bobina 24-60V AC / 20-60V DC [-11] (para control por PLC / 24V)
    contactors_af_24v = [
        ("AF09-30-10-11", "9A", "4.0 kW", "5.5 HP", "1 NA", "1SBL137001R1110"),
        ("AF12-30-10-11", "12A", "5.5 kW", "7.5 HP", "1 NA", "1SBL157001R1110"),
        ("AF16-30-10-11", "16A", "7.5 kW", "10 HP", "1 NA", "1SBL177001R1110"),
        ("AF26-30-00-11", "26A (25A)", "11.0 kW", "15 HP", "Sin aux", "1SBL237001R1100"),
        ("AF30-30-00-11", "30A", "15.0 kW", "20 HP", "Sin aux", "1SBL277001R1100"),
        ("AF38-30-00-11", "38A (32A)", "18.5 kW", "25 HP", "Sin aux", "1SBL297001R1100")
    ]
    for code, cur, pwr, hp, aux, order_code in contactors_af_24v:
        items.append((
            brand, line_auto, "Contactores de Potencia", "Serie AF", code,
            f"Contactor Tripolar AF {cur} {pwr} ({hp}) Bobina 24-60V AC/DC ({aux})",
            f"Contactor industrial con bobina de baja tensión compatible con salidas a transistor de PLC de 24V DC para motores de {pwr} ({hp})",
            json.dumps({"Polos": "3P", "Corriente": cur, "Potencia": f"{pwr} ({hp})", "TensionBobina": "24-60V AC / 20-60V DC", "ContactosAuxiliares": aux, "CodigoPedido": order_code}),
            f"Automatización industrial y tableros con circuito de mando en 24V DC para motores de {pwr} ({hp})"
        ))

    # Contactores de Gran Potencia AF116 a AF750 (55 kW a 400 kW)
    contactors_af_large = [
        ("AF116-30-11-13", "116A", "55.0 kW", "1SFL427001R1311"),
        ("AF140-30-11-13", "140A", "75.0 kW", "1SFL447001R1311"),
        ("AF146-30-11-13", "146A", "75.0 kW", "1SFL467001R1311"),
        ("AF190-30-11-13", "190A", "90.0 kW", "1SFL487002R1311"),
        ("AF205-30-11-13", "205A", "110.0 kW", "1SFL527002R1311"),
        ("AF265-30-11-13", "265A", "132.0 kW", "1SFL537002R1311"),
        ("AF305-30-11-13", "305A", "160.0 kW", "1SFL587002R1311"),
        ("AF370-30-11-13", "370A", "200.0 kW", "1SFL607002R1311"),
        ("AF400-30-11-70", "400A", "200.0 kW", "1SFL577001R7011"),
        ("AF460-30-11-70", "460A", "250.0 kW", "1SFL597001R7011"),
        ("AF580-30-11-70", "580A", "315.0 kW", "1SFL617001R7011"),
        ("AF750-30-11-70", "750A", "400.0 kW", "1SFL637001R7011")
    ]
    for code, cur, pwr, order_code in contactors_af_large:
        items.append((
            brand, line_auto, "Contactores de Gran Potencia", "Serie AF", code,
            f"Contactor de Potencia AF {cur} {pwr} Bobina 100-250V AC/DC (1NA+1NC)",
            f"Contactor tripolar de alta energía con control de bobina asistido electrónicamente y bornes traseros para pletinas",
            json.dumps({"Polos": "3P", "Corriente": cur, "Potencia": pwr, "TensionBobina": "100-250V AC/DC", "ContactosAuxiliares": "1 NA + 1 NC", "CodigoPedido": order_code}),
            f"Arranque y maniobra de motores industriales pesados de {pwr} en molinos, sopladores y bombeo principal"
        ))

    # Mini Contactores Serie B (B6 / B7)
    items.extend([
        (brand, line_auto, "Contactores Miniatura", "Serie B", "B6-30-10-230V", "Mini Contactor B6 3P 9A AC-1 / 6A AC-3 2.2kW Bobina 230V AC", "Contactor ultra compacto para cuadros de control con espacio reducido", json.dumps({"Polos": "3P", "Corriente": "6A (AC-3) / 9A (AC-1)", "Potencia": "2.2 kW", "Bobina": "230V AC", "ContactosAuxiliares": "1 NA"}), "Máquinas de envasado, hornos pequeños y automatismos comerciales"),
        (brand, line_auto, "Contactores Miniatura", "Serie B", "B6-30-10-24VDC", "Mini Contactor B6 3P 6A AC-3 2.2kW Bobina 24V DC", "Mini contactor tripolar accionado a 24V corriente continua", json.dumps({"Polos": "3P", "Corriente": "6A", "Potencia": "2.2 kW", "Bobina": "24V DC", "ContactosAuxiliares": "1 NA"}), "Cuadros de automatización con control en 24V DC"),
        (brand, line_auto, "Contactores Miniatura", "Serie B", "B7-30-10-230V", "Mini Contactor B7 3P 12A AC-1 / 9A AC-3 4.0kW Bobina 230V AC", "Mini contactor industrial para motores de hasta 4.0 kW", json.dumps({"Polos": "3P", "Corriente": "9A (AC-3)", "Potencia": "4.0 kW", "Bobina": "230V AC", "ContactosAuxiliares": "1 NA"}), "Sistemas de ventilación y automatismos de maquinaria"),
        (brand, line_auto, "Contactores Miniatura", "Serie B", "B7-30-10-24VDC", "Mini Contactor B7 3P 9A AC-3 4.0kW Bobina 24V DC", "Mini contactor para maniobra a 24V DC", json.dumps({"Polos": "3P", "Corriente": "9A", "Potencia": "4.0 kW", "Bobina": "24V DC", "ContactosAuxiliares": "1 NA"}), "Tableros de control con PLCs")
    ])

    # Contactores Auxiliares / Relés Contactor Serie NF
    items.extend([
        (brand, line_auto, "Bloques Auxiliares", "Serie NF", "NF22E-13", "Relé Contactor Auxiliar NF 2NA+2NC Bobina 100-250V AC/DC", "Contactor de mando de 4 polos para maniobra de circuitos auxiliares y señalización", json.dumps({"Polos": "4 Polos de mando", "Contactos": "2 NA + 2 NC", "TensionBobina": "100-250V AC/DC", "Ith": "16A"}), "Lógica de enclavamiento, mando y multiplicación de contactos en tableros"),
        (brand, line_auto, "Bloques Auxiliares", "Serie NF", "NF31E-13", "Relé Contactor Auxiliar NF 3NA+1NC Bobina 100-250V AC/DC", "Contactor auxiliar de mando con 3 contactos normalmente abiertos y 1 cerrado", json.dumps({"Polos": "4 Polos", "Contactos": "3 NA + 1 NC", "TensionBobina": "100-250V AC/DC"}), "Maniobras de automatización y seguridad eléctrica"),
        (brand, line_auto, "Bloques Auxiliares", "Serie NF", "NF40E-13", "Relé Contactor Auxiliar NF 4NA Bobina 100-250V AC/DC", "Contactor auxiliar con 4 contactos normalmente abiertos", json.dumps({"Polos": "4 Polos", "Contactos": "4 NA", "TensionBobina": "100-250V AC/DC"}), "Circuitos de señalización simultánea y control de marcha"),
        (brand, line_auto, "Bloques Auxiliares", "Serie NF", "NF22E-11", "Relé Contactor Auxiliar NF 2NA+2NC Bobina 24-60V AC/DC", "Relé contactor de mando para control directo a 24V DC de PLC", json.dumps({"Polos": "4 Polos", "Contactos": "2 NA + 2 NC", "TensionBobina": "24-60V AC/DC"}), "Integración con salidas digitales de autómatas programables")
    ])

    # 2.2 Accesorios para Contactores (Bloques Auxiliares y Enclavamientos)
    items.extend([
        (brand, line_auto, "Bloques Auxiliares", "Serie AF", "CA4-10", "Bloque de Contacto Auxiliar Frontal CA4-10 (1 NA)", "Contacto auxiliar instantáneo de montaje frontal para contactores AF09 a AF96", json.dumps({"Montaje": "Frontal a presión", "Contactos": "1 NA", "Compatible": "AF09 a AF96"}), "Adición de contacto de retención en arrancadores de motor"),
        (brand, line_auto, "Bloques Auxiliares", "Serie AF", "CA4-01", "Bloque de Contacto Auxiliar Frontal CA4-01 (1 NC)", "Contacto auxiliar de montaje frontal normalmente cerrado", json.dumps({"Montaje": "Frontal", "Contactos": "1 NC", "Compatible": "AF09 a AF96"}), "Enclavamiento eléctrico y señalización de paro"),
        (brand, line_auto, "Bloques Auxiliares", "Serie AF", "CA4-22M", "Bloque de Contacto Auxiliar Frontal CA4-22M (2 NA + 2 NC)", "Bloque de 4 contactos auxiliares frontales para contactores AF", json.dumps({"Montaje": "Frontal", "Contactos": "2 NA + 2 NC", "Compatible": "AF09 a AF96"}), "Maniobras complejas con múltiples señales de estado"),
        (brand, line_auto, "Bloques Auxiliares", "Serie AF", "CAL4-11", "Bloque de Contacto Auxiliar Lateral CAL4-11 (1 NA + 1 NC)", "Bloque auxiliar de montaje lateral para contactores AF09 a AF96", json.dumps({"Montaje": "Lateral", "Contactos": "1 NA + 1 NC", "Compatible": "AF09 a AF96"}), "Señalización lateral sin aumentar la profundidad del tablero"),
        (brand, line_auto, "Bloques Auxiliares", "Serie AF", "CAL19-11", "Bloque de Contacto Auxiliar Lateral CAL19-11 (1 NA + 1 NC)", "Bloque auxiliar lateral para contactores de potencia AF116 a AF370", json.dumps({"Montaje": "Lateral", "Contactos": "1 NA + 1 NC", "Compatible": "AF116 a AF370"}), "Circuitos de control de contactores de gran potencia"),
        (brand, line_auto, "Enclavamientos de Inversor", "Serie AF", "VM4", "Enclavamiento Mecánico VM4 para AF09..AF38", "Kit de interbloqueo mecánico que impide el cierre simultáneo de dos contactores en inversores", json.dumps({"Compatible": "AF09 a AF38", "Tipo": "Mecánico snap-on"}), "Montaje de inversores de giro y arrancadores estrella-triángulo"),
        (brand, line_auto, "Enclavamientos de Inversor", "Serie AF", "VM96-4", "Enclavamiento Mecánico VM96-4 para AF40..AF96", "Kit de enclavamiento mecánico para contactores medianos", json.dumps({"Compatible": "AF40 a AF96", "Tipo": "Mecánico"}), "Inversores de giro de motores de hasta 45 kW"),
        (brand, line_auto, "Enclavamientos de Inversor", "Serie AF", "BER16-4", "Juego de Conexión de Inversor BER16-4 para AF09..AF16", "Puentes de conexión de fuerza aislados para inversor de giro", json.dumps({"Compatible": "AF09 a AF16", "Tipo": "Puentes de potencia trifásicos"}), "Cableado rápido y seguro de inversores sin error de fases"),
        (brand, line_auto, "Enclavamientos de Inversor", "Serie AF", "BER38-4", "Juego de Conexión de Inversor BER38-4 para AF26..AF38", "Juego de barras de fuerza preformadas para inversores de giro de hasta 18.5 kW", json.dumps({"Compatible": "AF26 a AF38", "Tipo": "Barras rígidas aisladas"}), "Ensamblaje rápido de inversores de 11 a 18.5 kW")
    ])

    # 2.3 Guardamotores Magnetotérmicos (Manual Motor Starters MS116, MS132, MS165)
    # Ref: Main Catalog Section 02
    mms_ms116 = [
        ("MS116-0.16", "0.10 - 0.16 A", "50 kA", "1SAM250000R1001"),
        ("MS116-0.25", "0.16 - 0.25 A", "50 kA", "1SAM250000R1002"),
        ("MS116-0.4",  "0.25 - 0.40 A", "50 kA", "1SAM250000R1003"),
        ("MS116-0.63", "0.40 - 0.63 A", "50 kA", "1SAM250000R1004"),
        ("MS116-1.0",  "0.63 - 1.00 A", "50 kA", "1SAM250000R1005"),
        ("MS116-1.6",  "1.00 - 1.60 A", "50 kA", "1SAM250000R1006"),
        ("MS116-2.5",  "1.60 - 2.50 A", "50 kA", "1SAM250000R1007"),
        ("MS116-4.0",  "2.50 - 4.00 A", "50 kA", "1SAM250000R1008"),
        ("MS116-6.3",  "4.00 - 6.30 A", "50 kA", "1SAM250000R1009"),
        ("MS116-10",   "6.30 - 10.0 A", "50 kA", "1SAM250000R1010"),
        ("MS116-12",   "8.00 - 12.0 A", "25 kA", "1SAM250000R1012"),
        ("MS116-16",   "10.0 - 16.0 A", "16 kA", "1SAM250000R1011"),
        ("MS116-20",   "16.0 - 20.0 A", "10 kA", "1SAM250000R1013"),
        ("MS116-25",   "20.0 - 25.0 A", "10 kA", "1SAM250000R1014"),
        ("MS116-32",   "25.0 - 32.0 A", "10 kA", "1SAM250000R1015")
    ]
    for code, rng, icu, order_code in mms_ms116:
        items.append((
            brand, line_auto, "Guardamotores Magnetotérmicos", "Serie MS116", code,
            f"Guardamotor Magnetotérmico MS116 ({rng}) {icu}",
            f"Interruptor guardamotor tripolar para protección de motores contra sobrecargas, cortocircuitos y fallo de fase con compensación de temperatura",
            json.dumps({"Polos": "3P", "RangoAjuste": rng, "PoderCorte": f"{icu} a 400V AC", "ClaseDisparo": "Clase 10A", "CodigoPedido": order_code, "SensibilidadFase": "Sí", "Montaje": "Riel DIN 35mm"}),
            f"Protección integral de motores trifásicos con corriente nominal en el rango {rng}"
        ))

    mms_ms132 = [
        ("MS132-0.63", "0.40 - 0.63 A", "100 kA", "1SAM350000R1004"),
        ("MS132-1.0",  "0.63 - 1.00 A", "100 kA", "1SAM350000R1005"),
        ("MS132-1.6",  "1.00 - 1.60 A", "100 kA", "1SAM350000R1006"),
        ("MS132-2.5",  "1.60 - 2.50 A", "100 kA", "1SAM350000R1007"),
        ("MS132-4.0",  "2.50 - 4.00 A", "100 kA", "1SAM350000R1008"),
        ("MS132-6.3",  "4.00 - 6.30 A", "100 kA", "1SAM350000R1009"),
        ("MS132-10",   "6.30 - 10.0 A", "100 kA", "1SAM350000R1010"),
        ("MS132-16",   "10.0 - 16.0 A", "100 kA", "1SAM350000R1011"),
        ("MS132-20",   "16.0 - 20.0 A", "100 kA", "1SAM350000R1013"),
        ("MS132-25",   "20.0 - 25.0 A", "50 kA",  "1SAM350000R1014"),
        ("MS132-32",   "25.0 - 32.0 A", "50 kA",  "1SAM350000R1015")
    ]
    for code, rng, icu, order_code in mms_ms132:
        items.append((
            brand, line_auto, "Guardamotores Magnetotérmicos", "Serie MS132", code,
            f"Guardamotor de Alto Rendimiento MS132 ({rng}) {icu}",
            f"Guardamotor de alto poder de corte con perilla giratoria ergonómica, indicación clara de disparo TRIP y función seccionadora",
            json.dumps({"Polos": "3P", "RangoAjuste": rng, "PoderCorte": f"{icu} a 400V", "ClaseDisparo": "Clase 10", "CodigoPedido": order_code, "IndicadorDisparo": "TRIP óptico"}),
            "Instalaciones industriales de alto cortocircuito que demandan continuidad de servicio"
        ))

    mms_ms165 = [
        ("MS165-16", "10.0 - 16.0 A", "100 kA", "1SAM450000R1011"),
        ("MS165-20", "14.0 - 20.0 A", "100 kA", "1SAM450000R1012"),
        ("MS165-25", "18.0 - 25.0 A", "100 kA", "1SAM450000R1013"),
        ("MS165-32", "23.0 - 32.0 A", "100 kA", "1SAM450000R1014"),
        ("MS165-42", "30.0 - 42.0 A", "50 kA",  "1SAM450000R1015"),
        ("MS165-54", "40.0 - 54.0 A", "50 kA",  "1SAM450000R1016"),
        ("MS165-65", "52.0 - 65.0 A", "50 kA",  "1SAM450000R1017"),
        ("MS165-80", "67.0 - 80.0 A", "30 kA",  "1SAM450000R1018")
    ]
    for code, rng, icu, order_code in mms_ms165:
        items.append((
            brand, line_auto, "Guardamotores Magnetotérmicos", "Serie MS165", code,
            f"Guardamotor de Gran Potencia MS165 ({rng}) {icu}",
            f"Guardamotor de 55 mm de ancho para motores de alta potencia hasta 45 kW (80A)",
            json.dumps({"Polos": "3P", "RangoAjuste": rng, "PoderCorte": f"{icu} a 400V", "ClaseDisparo": "Clase 10", "CodigoPedido": order_code}),
            "Protección de motores pesados en transportadores, bombas principales y trituradoras"
        ))

    # Accesorios para Guardamotores
    items.extend([
        (brand, line_auto, "Bloques Auxiliares", "Serie MS", "HKF1-11", "Contacto Auxiliar Frontal para Guardamotor HKF1-11 (1 NA + 1 NC)", "Contacto auxiliar frontal que no ocupa espacio adicional de ancho en el riel DIN", json.dumps({"Montaje": "Frontal a presión", "Contactos": "1 NA + 1 NC", "Compatible": "MS116, MS132, MS165"}), "Señalización de encendido/apagado del guardamotor"),
        (brand, line_auto, "Bloques Auxiliares", "Serie MS", "HK1-11", "Contacto Auxiliar Lateral para Guardamotor HK1-11 (1 NA + 1 NC)", "Contacto auxiliar lateral de 9 mm de ancho", json.dumps({"Montaje": "Lateral izquierdo", "Contactos": "1 NA + 1 NC", "Compatible": "MS116, MS132, MS165"}), "Señalización remota y enclavamiento con PLC"),
        (brand, line_auto, "Bloques Auxiliares", "Serie MS", "SK1-11", "Contacto de Señalización de Disparo SK1-11 (1 NA + 1 NC)", "Contacto auxiliar que conmuta únicamente cuando ocurre un disparo por sobrecarga o cortocircuito", json.dumps({"Montaje": "Lateral", "Contactos": "1 NA + 1 NC", "Funcion": "Diferenciación de fallo térmico/magnético"}), "Alarma de avería a sistema SCADA o PLC"),
        (brand, line_auto, "Enclavamientos de Inversor", "Serie MS", "BEA16-4", "Adaptador de Conexión Guardamotor-Contactor BEA16-4", "Pieza de conexión eléctrica y mecánica directa entre guardamotor MS116/132 y contactor AF09..AF16", json.dumps({"Compatible": "MS116/132 a AF09..AF16", "Tipo": "Conexión directa sin cables"}), "Armado de arrancadores compactos de motor sin cableado intermedio")
    ])

    # 2.4 Relés Térmicos de Sobrecarga (TF42, TF65, TF96, TF140)
    # Ref: Main Catalog Section 06
    thermal_tf42 = [
        ("TF42-0.16", "0.10 - 0.16 A", "1SAZ721201R1001"),
        ("TF42-0.23", "0.16 - 0.23 A", "1SAZ721201R1009"),
        ("TF42-0.41", "0.28 - 0.41 A", "1SAZ721201R1014"),
        ("TF42-0.74", "0.55 - 0.74 A", "1SAZ721201R1021"),
        ("TF42-1.0",  "0.74 - 1.00 A", "1SAZ721201R1023"),
        ("TF42-1.7",  "1.30 - 1.70 A", "1SAZ721201R1028"),
        ("TF42-2.3",  "1.70 - 2.30 A", "1SAZ721201R1031"),
        ("TF42-3.1",  "2.30 - 3.10 A", "1SAZ721201R1033"),
        ("TF42-4.2",  "3.10 - 4.20 A", "1SAZ721201R1035"),
        ("TF42-5.7",  "4.20 - 5.70 A", "1SAZ721201R1038"),
        ("TF42-7.6",  "5.70 - 7.60 A", "1SAZ721201R1040"),
        ("TF42-10",   "7.60 - 10.0 A", "1SAZ721201R1043"),
        ("TF42-13",   "10.0 - 13.0 A", "1SAZ721201R1045"),
        ("TF42-16",   "13.0 - 16.0 A", "1SAZ721201R1047"),
        ("TF42-20",   "16.0 - 20.0 A", "1SAZ721201R1049"),
        ("TF42-24",   "20.0 - 24.0 A", "1SAZ721201R1051"),
        ("TF42-29",   "24.0 - 29.0 A", "1SAZ721201R1052"),
        ("TF42-35",   "29.0 - 35.0 A", "1SAZ721201R1053"),
        ("TF42-38",   "35.0 - 38.0 A", "1SAZ721201R1055")
    ]
    for code, rng, order_code in thermal_tf42:
        items.append((
            brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie TF42", code,
            f"Relé Térmico de Sobrecarga TF42 ({rng}) para AF09..AF38",
            f"Relé de protección térmica bimetálico con sensibilidad de falta de fase, compensación de temperatura ambiente y botón de rearme Manual/Automático",
            json.dumps({"RangoAjuste": rng, "ClaseDisparo": "Clase 10", "ContactosAuxiliares": "1 NA + 1 NC", "Compatible": "AF09 a AF38", "CodigoPedido": order_code, "Rearme": "Manual/Automático seleccionable"}),
            f"Protección contra sobrecargas continuas de motores con corriente nominal entre {rng}"
        ))

    # TF65 y TF96
    items.extend([
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie TF65", "TF65-40", "Relé Térmico TF65 (28-40 A) para AF40..AF65", "Relé de sobrecarga para motores de hasta 18.5 kW montado directamente al contactor", json.dumps({"RangoAjuste": "28 - 40 A", "ClaseDisparo": "Clase 10", "Compatible": "AF40 a AF65"}), "Protección de bombas y compresores medianos"),
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie TF65", "TF65-53", "Relé Térmico TF65 (40-53 A) para AF40..AF65", "Relé de sobrecarga para motores de hasta 25 kW", json.dumps({"RangoAjuste": "40 - 53 A", "ClaseDisparo": "Clase 10", "Compatible": "AF40 a AF65"}), "Protección de motores trifásicos de 22 kW"),
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie TF65", "TF65-67", "Relé Térmico TF65 (53-67 A) para AF40..AF65", "Relé de sobrecarga para motores de hasta 30 kW", json.dumps({"RangoAjuste": "53 - 67 A", "ClaseDisparo": "Clase 10", "Compatible": "AF40 a AF65"}), "Protección de motores de 30 kW en machacadoras y bombas"),
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie TF96", "TF96-78", "Relé Térmico TF96 (65-78 A) para AF80..AF96", "Relé de sobrecarga pesado para motores de 37 kW", json.dumps({"RangoAjuste": "65 - 78 A", "ClaseDisparo": "Clase 10", "Compatible": "AF80 a AF96"}), "Motores de gran inercia y ventilación pesada"),
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie TF96", "TF96-96", "Relé Térmico TF96 (75-96 A) para AF80..AF96", "Relé de sobrecarga para motores de hasta 45 kW", json.dumps({"RangoAjuste": "75 - 96 A", "ClaseDisparo": "Clase 10", "Compatible": "AF80 a AF96"}), "Protección térmica de motores principales en plantas industriales")
    ])

    # 2.5 Relés Electrónicos de Sobrecarga (EF19, EF45, EF65, EF96)
    items.extend([
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie EF", "EF19-2.7", "Relé Electrónico de Sobrecarga EF19 (0.8-2.7 A)", "Relé electrónico con clase de disparo seleccionable 10E, 20E y 30E para alta precisión y amplio rango", json.dumps({"RangoAjuste": "0.8 - 2.7 A", "ClaseDisparo": "10E, 20E, 30E seleccionable", "Compatible": "AF09 a AF38", "Tecnologia": "Sensado electrónico"}), "Motores con arranques prolongados y cargas pesadas"),
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie EF", "EF19-18.9", "Relé Electrónico de Sobrecarga EF19 (6.3-18.9 A)", "Relé electrónico de sobrecarga de alta precisión para motores de hasta 7.5 kW", json.dumps({"RangoAjuste": "6.3 - 18.9 A", "ClaseDisparo": "10E, 20E, 30E", "Compatible": "AF09 a AF38"}), "Bombas sumergibles y motores con curvas térmicas exigentes"),
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie EF", "EF45-45", "Relé Electrónico de Sobrecarga EF45 (15-45 A)", "Relé electrónico para contactores AF26 a AF38", json.dumps({"RangoAjuste": "15 - 45 A", "ClaseDisparo": "10E, 20E, 30E", "Compatible": "AF26 a AF38"}), "Sistemas de bombeo y aireación"),
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie EF", "EF65-70", "Relé Electrónico de Sobrecarga EF65 (25-70 A)", "Relé electrónico para motores de hasta 30 kW", json.dumps({"RangoAjuste": "25 - 70 A", "ClaseDisparo": "10E, 20E, 30E", "Compatible": "AF40 a AF65"}), "Líneas de manufactura y cintas transportadoras pesadas"),
        (brand, line_auto, "Relés Térmicos de Sobrecarga", "Serie EF", "EF96-100", "Relé Electrónico de Sobrecarga EF96 (36-100 A)", "Relé electrónico de máxima precisión hasta 100A", json.dumps({"RangoAjuste": "36 - 100 A", "ClaseDisparo": "10E, 20E, 30E", "Compatible": "AF80 a AF96"}), "Grandes compresores centrífugos y molinos")
    ])

    # 2.6 Arrancadores Suaves (Softstarters PSR, PSE, PSTX)
    # Ref: Softstarter Catalog 1SFC132012C0201
    # PSR: Gama Compacta (3 a 105 A) con bypass integrado
    softstarters_psr = [
        ("PSR3-600-70", "3.9A", "1.5 kW", "1SFA896103R7000"),
        ("PSR6-600-70", "6.8A", "3.0 kW", "1SFA896104R7000"),
        ("PSR9-600-70", "9.0A", "4.0 kW", "1SFA896105R7000"),
        ("PSR12-600-70", "12.0A", "5.5 kW", "1SFA896106R7000"),
        ("PSR16-600-70", "16.0A", "7.5 kW", "1SFA896107R7000"),
        ("PSR25-600-70", "25.0A", "11.0 kW", "1SFA896108R7000"),
        ("PSR30-600-70", "30.0A", "15.0 kW", "1SFA896109R7000"),
        ("PSR37-600-70", "37.0A", "18.5 kW", "1SFA896110R7000"),
        ("PSR45-600-70", "45.0A", "22.0 kW", "1SFA896111R7000"),
        ("PSR60-600-70", "60.0A", "30.0 kW", "1SFA896112R7000"),
        ("PSR72-600-70", "72.0A", "37.0 kW", "1SFA896113R7000"),
        ("PSR85-600-70", "85.0A", "45.0 kW", "1SFA896114R7000"),
        ("PSR105-600-70", "105.0A", "55.0 kW", "1SFA896115R7000")
    ]
    for code, cur, pwr, order_code in softstarters_psr:
        items.append((
            brand, line_auto, "Arrancadores Suaves", "Serie PSR", code,
            f"Arrancador Suave PSR {cur} {pwr} (208-600V) Bypass Integrado",
            f"Arrancador electrónico suave compacto bifásico con bypass de tiristores incorporado para arranque y parada suave de motores trifásicos",
            json.dumps({"Corriente": cur, "Potencia": pwr, "TensionRed": "208-600V AC", "TensionControl": "100-240V AC", "Bypass": "Integrado", "Montaje": "Riel DIN (hasta 45A) / Placa", "CodigoPedido": order_code}),
            f"Arranque suave de bombas, ventiladores y cintas transportadoras hasta {pwr} evitando picos mecánicos y eléctricos"
        ))

    # PSE: Gama Eficiente (18 a 370 A) con control de par y protección integrada
    softstarters_pse = [
        ("PSE18-600-70", "18A", "7.5 kW", "1SFA897101R7000"),
        ("PSE25-600-70", "25A", "11.0 kW", "1SFA897102R7000"),
        ("PSE30-600-70", "30A", "15.0 kW", "1SFA897103R7000"),
        ("PSE37-600-70", "37A", "18.5 kW", "1SFA897104R7000"),
        ("PSE45-600-70", "45A", "22.0 kW", "1SFA897105R7000"),
        ("PSE60-600-70", "60A", "30.0 kW", "1SFA897106R7000"),
        ("PSE72-600-70", "72A", "37.0 kW", "1SFA897107R7000"),
        ("PSE85-600-70", "85A", "45.0 kW", "1SFA897108R7000"),
        ("PSE105-600-70", "105A", "55.0 kW", "1SFA897109R7000"),
        ("PSE142-600-70", "143A", "75.0 kW", "1SFA897110R7000"),
        ("PSE170-600-70", "171A", "90.0 kW", "1SFA897111R7000"),
        ("PSE210-600-70-1", "210A", "110.0 kW", "1SFA897112R7001"),
        ("PSE250-600-70-1", "250A", "132.0 kW", "1SFA897113R7001"),
        ("PSE300-600-70-1", "300A", "160.0 kW", "1SFA897114R7001"),
        ("PSE370-600-70-1", "370A", "200.0 kW", "1SFA897115R7001")
    ]
    for code, cur, pwr, order_code in softstarters_pse:
        items.append((
            brand, line_auto, "Arrancadores Suaves", "Serie PSE", code,
            f"Arrancador Suave Eficiente PSE {cur} {pwr} Control de Par (Torque Control)",
            f"Arrancador suave de alto rendimiento con función patentada de control de par para eliminar el golpe de ariete en paradas de bombas, bypass integrado, display retroiluminado y relé electrónico de sobrecarga",
            json.dumps({"Corriente": cur, "Potencia": pwr, "TensionRed": "208-600V AC", "TensionControl": "100-250V AC", "Bypass": "Integrado", "ControlPar": "Sí (Anti-Water Hammer)", "ProteccionSobrecarga": "Electrónica incorporada", "CodigoPedido": order_code}),
            f"Sistemas de bombeo de agua potable, plantas de tratamiento de aguas residuales, ventilación industrial y compresores de {pwr}"
        ))

    # PSTX: Gama Avanzada (30 a 1250 A) control trifásico total
    softstarters_pstx = [
        ("PSTX30-600-70", "30A", "15.0 kW", "1SFA898103R7000"),
        ("PSTX45-600-70", "45A", "22.0 kW", "1SFA898105R7000"),
        ("PSTX60-600-70", "60A", "30.0 kW", "1SFA898106R7000"),
        ("PSTX72-600-70", "72A", "37.0 kW", "1SFA898107R7000"),
        ("PSTX85-600-70", "85A", "45.0 kW", "1SFA898108R7000"),
        ("PSTX105-600-70", "105A", "55.0 kW", "1SFA898109R7000"),
        ("PSTX142-600-70", "142A", "75.0 kW", "1SFA898110R7000"),
        ("PSTX170-600-70", "170A", "90.0 kW", "1SFA898111R7000"),
        ("PSTX210-600-70", "210A", "110.0 kW", "1SFA898112R7000"),
        ("PSTX250-600-70", "250A", "132.0 kW", "1SFA898113R7000"),
        ("PSTX300-600-70", "300A", "160.0 kW", "1SFA898114R7000"),
        ("PSTX370-600-70", "370A", "200.0 kW", "1SFA898115R7000"),
        ("PSTX470-600-70", "470A", "250.0 kW", "1SFA898116R7000"),
        ("PSTX570-600-70", "570A", "315.0 kW", "1SFA898117R7000"),
        ("PSTX720-600-70", "720A", "400.0 kW", "1SFA898118R7000"),
        ("PSTX840-600-70", "840A", "450.0 kW", "1SFA898119R7000"),
        ("PSTX1050-600-70", "1050A", "560.0 kW", "1SFA898120R7000"),
        ("PSTX1250-600-70", "1250A", "710.0 kW", "1SFA898121R7000")
    ]
    for code, cur, pwr, order_code in softstarters_pstx:
        items.append((
            brand, line_auto, "Arrancadores Suaves", "Serie PSTX", code,
            f"Arrancador Suave Avanzado PSTX {cur} {pwr} Trifásico Display IP66 Modbus",
            f"Arrancador suave avanzado con control en las tres fases, display gráfico desmontable IP66, comunicación Modbus RTU integrada, función Jog a baja velocidad y limpieza de bombas",
            json.dumps({"Corriente": cur, "Potencia": pwr, "TensionRed": "208-600V AC", "Control": "Trifásico completo", "Bypass": "Integrado", "Comunicacion": "Modbus RTU integrada", "Display": "Gráfico desmontable IP66", "CodigoPedido": order_code}),
            f"Aplicaciones de servicio pesado en minería, papeleras, bombeo crítico y molinos de {pwr}"
        ))

    # =========================================================================
    # 3. LÍNEA: ACCIONAMIENTOS Y CONVERTIDORES DE FRECUENCIA (DRIVES)
    # =========================================================================
    line_drives = "Drives"

    # 3.1 Variadores Industriales ACS880-01 (Mural 380-500V, Direct Torque Control - DTC)
    # Ref: ACS880 Single Drives Catalog 3AUA0000098111
    drives_acs880_400v = [
        # Código, In, Pn (kW), HP, Frame
        ("ACS880-01-02A4-3", "2.4A", "0.75 kW", "1.0 HP", "R1"),
        ("ACS880-01-03A3-3", "3.3A", "1.1 kW", "1.5 HP", "R1"),
        ("ACS880-01-04A0-3", "4.0A", "1.5 kW", "2.0 HP", "R1"),
        ("ACS880-01-05A6-3", "5.6A", "2.2 kW", "3.0 HP", "R1"),
        ("ACS880-01-07A2-3", "7.2A", "3.0 kW", "4.0 HP", "R1"),
        ("ACS880-01-09A4-3", "9.4A", "4.0 kW", "5.0 HP", "R1"),
        ("ACS880-01-12A6-3", "12.6A", "5.5 kW", "7.5 HP", "R1"),
        ("ACS880-01-017A-3", "17.0A", "7.5 kW", "10 HP", "R2"),
        ("ACS880-01-025A-3", "25.0A", "11.0 kW", "15 HP", "R2"),
        ("ACS880-01-032A-3", "32.0A", "15.0 kW", "20 HP", "R3"),
        ("ACS880-01-038A-3", "38.0A", "18.5 kW", "25 HP", "R3"),
        ("ACS880-01-045A-3", "45.0A", "22.0 kW", "30 HP", "R4"),
        ("ACS880-01-061A-3", "61.0A", "30.0 kW", "40 HP", "R4"),
        ("ACS880-01-072A-3", "72.0A", "37.0 kW", "50 HP", "R5"),
        ("ACS880-01-087A-3", "87.0A", "45.0 kW", "60 HP", "R5"),
        ("ACS880-01-105A-3", "105.0A", "55.0 kW", "75 HP", "R6"),
        ("ACS880-01-145A-3", "145.0A", "75.0 kW", "100 HP", "R6"),
        ("ACS880-01-169A-3", "169.0A", "90.0 kW", "125 HP", "R7"),
        ("ACS880-01-206A-3", "206.0A", "110.0 kW", "150 HP", "R7"),
        ("ACS880-01-246A-3", "246.0A", "132.0 kW", "175 HP", "R8"),
        ("ACS880-01-293A-3", "293.0A", "160.0 kW", "215 HP", "R8"),
        ("ACS880-01-363A-3", "363.0A", "200.0 kW", "270 HP", "R9"),
        ("ACS880-01-430A-3", "430.0A", "250.0 kW", "350 HP", "R9")
    ]
    for code, cur, pwr, hp, frame in drives_acs880_400v:
        items.append((
            brand, line_drives, "Variadores de Proceso", "Serie ACS880", code,
            f"Variador de Frecuencia Industrial ACS880-01 {pwr} ({hp} / {cur}) 380-415V DTC {frame}",
            f"Convertidor de frecuencia para montaje mural de {pwr} ({hp}) con tecnología Direct Torque Control (DTC) de máximo control dinámico de velocidad y par sin encoder, filtro de armónicos y Safe Torque Off (STO) SIL 3 integrados",
            json.dumps({"Potencia": f"{pwr} ({hp})", "Corriente": cur, "Tension": "380-415V AC Trifásico", "Control": "Direct Torque Control (DTC)", "Seguridad": "Safe Torque Off (STO) SIL 3 / PLe", "Proteccion": "IP21 (Opcional IP55)", "TamanoBastidor": frame}),
            f"Procesos industriales de alta exigencia: grúas, extrusoras, calandras, bobinadoras y bombas de {pwr} ({hp})"
        ))

    # Variadores ACS880-01 para red 230V Trifásica (0.75 a 75 kW)
    drives_acs880_230v = [
        ("ACS880-01-04A6-2", "4.6A", "0.75 kW", "R1"),
        ("ACS880-01-07A5-2", "7.5A", "1.5 kW", "R1"),
        ("ACS880-01-10A6-2", "10.6A", "2.2 kW", "R1"),
        ("ACS880-01-16A8-2", "16.8A", "4.0 kW", "R2"),
        ("ACS880-01-24A3-2", "24.3A", "5.5 kW", "R2"),
        ("ACS880-01-031A-2", "31.0A", "7.5 kW", "R3"),
        ("ACS880-01-046A-2", "46.0A", "11.0 kW", "R4"),
        ("ACS880-01-061A-2", "61.0A", "15.0 kW", "R4")
    ]
    for code, cur, pwr, frame in drives_acs880_230v:
        items.append((
            brand, line_drives, "Variadores de Proceso", "Serie ACS880", code,
            f"Variador de Frecuencia ACS880-01 {pwr} ({cur}) 208-240V Trifásico DTC",
            f"Variador industrial para redes de 230V con control de par directo DTC",
            json.dumps({"Potencia": pwr, "Corriente": cur, "Tension": "208-240V AC Trifásico", "Control": "DTC", "TamanoBastidor": frame}),
            f"Maquinaria pesada alimentada en 220V trifásicos de {pwr}"
        ))

    # 3.2 Variadores de Propósito General ACS580 (400V)
    drives_acs580 = [
        ("ACS580-01-02A7-4", "2.6A", "0.75 kW"),
        ("ACS580-01-04A1-4", "4.0A", "1.5 kW"),
        ("ACS580-01-05A7-4", "5.6A", "2.2 kW"),
        ("ACS580-01-09A5-4", "9.4A", "4.0 kW"),
        ("ACS580-01-12A7-4", "12.6A", "5.5 kW"),
        ("ACS580-01-018A-4", "17.0A", "7.5 kW"),
        ("ACS580-01-026A-4", "25.0A", "11.0 kW"),
        ("ACS580-01-033A-4", "32.0A", "15.0 kW"),
        ("ACS580-01-039A-4", "38.0A", "18.5 kW"),
        ("ACS580-01-046A-4", "45.0A", "22.0 kW"),
        ("ACS580-01-062A-4", "62.0A", "30.0 kW"),
        ("ACS580-01-073A-4", "73.0A", "37.0 kW"),
        ("ACS580-01-088A-4", "88.0A", "45.0 kW")
    ]
    for code, cur, pwr in drives_acs580:
        items.append((
            brand, line_drives, "Variadores Estándar", "Serie ACS580", code,
            f"Variador de Frecuencia de Propósito General ACS580 {pwr} ({cur}) 380-480V",
            f"Variador versátil todo en uno con reactancia de armónicos integrada, chopper de frenado y panel de control asistente con menú intuitivo en español",
            json.dumps({"Potencia": pwr, "Corriente": cur, "Tension": "380-480V AC Trifásico", "Panel": "Asistente con gráficos y USB", "Eficiencia": "IE2 / Regulación Eco"}),
            f"Control de velocidad energéticamente eficiente en bombas centrífugas, ventiladores y cintas de {pwr}"
        ))

    # 3.3 Variadores Compactos para Maquinaria ACS380
    drives_acs380 = [
        ("ACS380-040S-02A6-4", "2.6A", "0.75 kW"),
        ("ACS380-040S-04A0-4", "4.0A", "1.5 kW"),
        ("ACS380-040S-07A2-4", "7.2A", "3.0 kW"),
        ("ACS380-040S-09A4-4", "9.4A", "4.0 kW"),
        ("ACS380-040S-12A6-4", "12.6A", "5.5 kW"),
        ("ACS380-040S-017A-4", "17.0A", "7.5 kW"),
        ("ACS380-040S-025A-4", "25.0A", "11.0 kW")
    ]
    for code, cur, pwr in drives_acs380:
        items.append((
            brand, line_drives, "Variadores de Velocidad", "Serie ACS380", code,
            f"Variador para Maquinaria ACS380 {pwr} ({cur}) 380-480V STO",
            f"Variador de diseño estrecho en formato libro para constructores de maquinaria (OEM), con capacidad de programación por bloques e interfaz de bus de campo",
            json.dumps({"Potencia": pwr, "Corriente": cur, "Tension": "380-480V AC", "Formato": "Montaje en libro / riel DIN", "Seguridad": "STO SIL 3 integrado"}),
            f"Maquinaria de embalaje, procesamiento de alimentos, etiquetadoras y mezcladores de {pwr}"
        ))

    # =========================================================================
    # 4. LÍNEA: UNIDADES DE MANDO Y SEÑALIZACIÓN (PILOT DEVICES 22MM)
    # =========================================================================
    # Ref: Modular Way Metal Range Catalog 1SFC151013C0201
    line_mando = "Unidades de Mando y Señalización"

    # 4.1 Pulsadores Metálicos Ø22mm No Iluminados WAP
    items.extend([
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NR", "Pulsador Metálico Rasante Rojo Ø22mm (Sin marcar)", "Cabeza de pulsador metálico momentáneo rasante color rojo IP65", json.dumps({"Color": "Rojo", "Tipo": "Rasante Momentáneo", "Material": "Bisel metálico cromado", "Diametro": "22 mm", "Proteccion": "IP65", "CodigoPedido": "2TFC570100R1004"}), "Mando de paro y desconexión en tableros"),
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NG", "Pulsador Metálico Rasante Verde Ø22mm (Sin marcar)", "Cabeza de pulsador metálico momentáneo rasante color verde IP65", json.dumps({"Color": "Verde", "Tipo": "Rasante Momentáneo", "Material": "Metálico", "Diametro": "22 mm", "Proteccion": "IP65", "CodigoPedido": "2TFC570100R1003"}), "Mando de marcha y puesta en servicio"),
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NB", "Pulsador Metálico Rasante Negro Ø22mm", "Cabeza de pulsador rasante negro metálico", json.dumps({"Color": "Negro", "Tipo": "Rasante", "Material": "Metálico", "CodigoPedido": "2TFC570100R1002"}), "Rearme de sobrecargas y accionamiento general"),
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NW", "Pulsador Metálico Rasante Blanco Ø22mm", "Cabeza de pulsador rasante blanco metálico", json.dumps({"Color": "Blanco", "Material": "Metálico", "CodigoPedido": "2TFC570100R1001"}), "Marcha y funciones especiales"),
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NY", "Pulsador Metálico Rasante Amarillo Ø22mm", "Cabeza de pulsador rasante amarillo metálico", json.dumps({"Color": "Amarillo", "Material": "Metálico", "CodigoPedido": "2TFC570100R1005"}), "Intervención de operador y avisos"),
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NL", "Pulsador Metálico Rasante Azul Ø22mm", "Cabeza de pulsador rasante azul metálico", json.dumps({"Color": "Azul", "Material": "Metálico", "CodigoPedido": "2TFC570100R1006"}), "Rearme de fallas y reset en paneles")
    ])

    # Pulsadores Metálicos Grabados ("START", "STOP", "I", "O")
    items.extend([
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NG-START", "Pulsador Metálico Rasante Verde Grabado 'START' Ø22mm", "Pulsador metálico con serigrafía de texto 'START' en blanco indeleble", json.dumps({"Color": "Verde", "Grabado": "START", "Material": "Metálico", "CodigoPedido": "2TFC570138R1013"}), "Puesto de mando de arranque local y en pupitres"),
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NR-STOP", "Pulsador Metálico Rasante Rojo Grabado 'STOP' Ø22mm", "Pulsador metálico con grabado 'STOP'", json.dumps({"Color": "Rojo", "Grabado": "STOP", "Material": "Metálico", "CodigoPedido": "2TFC570135R1014"}), "Puestos de parada normal de motores"),
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NG-I", "Pulsador Metálico Rasante Verde Grabado 'I' Ø22mm", "Pulsador con símbolo internacional 'I' (Marcha)", json.dumps({"Color": "Verde", "Grabado": "I", "CodigoPedido": "2TFC570137R1013"}), "Tableros de exportación y normas internacionales"),
        (brand, line_mando, "Pulsadores Metálicos", "Modular Way", "WAP-11NR-O", "Pulsador Metálico Rasante Rojo Grabado 'O' Ø22mm", "Pulsador con símbolo internacional 'O' (Paro)", json.dumps({"Color": "Rojo", "Grabado": "O", "CodigoPedido": "2TFC570134R1014"}), "Consolas de control industrial")
    ])

    # 4.2 Paradas de Emergencia WAE Ø22mm
    items.extend([
        (brand, line_mando, "Paradas de Emergencia", "Modular Way", "WAE-11TR", "Pulsador de Parada de Emergencia Seta Ø40mm Desapriete por Giro (Twist Release)", "Cabeza de parada de emergencia roja tipo hongo de 40mm con enclavamiento mecánico y desenclavamiento por giro conforme a ISO 13850", json.dumps({"Color": "Rojo", "Diametro": "40 mm", "Accion": "Desenclavamiento por giro (Twist-release)", "Norma": "EN/ISO 13850", "Proteccion": "IP65", "Material": "Cuerpo metálico robusto"}), "Circuito de seguridad de paro de emergencia en máquinas y cuadros"),
        (brand, line_mando, "Paradas de Emergencia", "Modular Way", "WAE-11PR", "Pulsador de Parada de Emergencia Seta Ø40mm Tirar para Desenclavar (Pull Release)", "Parada de emergencia con desenclavamiento tirando de la seta", json.dumps({"Color": "Rojo", "Diametro": "40 mm", "Accion": "Tirar (Pull-release)", "Norma": "EN/ISO 13850"}), "Líneas de empaque y maquinaria de producción"),
        (brand, line_mando, "Paradas de Emergencia", "Modular Way", "WAE-11KR", "Pulsador de Parada de Emergencia Seta Ø40mm con Llave (Key Release)", "Parada de emergencia con desenclavamiento mediante cerradura de llave de seguridad", json.dumps({"Color": "Rojo", "Diametro": "40 mm", "Accion": "Desenclavamiento por llave Ronis", "Seguridad": "Restricción de rearme no autorizado"}), "Plantas industriales críticas y máquinas donde se requiere autorización para rearme"),
        (brand, line_mando, "Paradas de Emergencia", "Modular Way", "WAE-11TR-60", "Pulsador de Parada de Emergencia Seta Grande Ø60mm Giro", "Parada de emergencia de gran tamaño de 60mm para alta visibilidad y fácil accionamiento", json.dumps({"Color": "Rojo", "Diametro": "60 mm", "Accion": "Giro (Twist-release)"}), "Puestos de trabajo pesado y áreas de alto riesgo")
    ])

    # 4.3 Selectores Metálicos WAS Ø22mm
    items.extend([
        (brand, line_mando, "Selectores Metálicos", "Modular Way", "WAS-310NB", "Selector Metálico Maneta Corta 2 Posiciones Mantenidas 90°", "Mando selector rotativo metálico negro de 2 posiciones estables (0 - 1)", json.dumps({"Posiciones": "2 posiciones fijas 90°", "Maneta": "Corta negra", "Material": "Bisel metálico", "Proteccion": "IP65"}), "Encendido general, selección Marcha/Paro y selección de modo"),
        (brand, line_mando, "Selectores Metálicos", "Modular Way", "WAS-510NB", "Selector Metálico Maneta Corta 3 Posiciones Mantenidas (1 - 0 - 2)", "Selector rotativo metálico de 3 posiciones estables con reposo central", json.dumps({"Posiciones": "3 posiciones mantenidas (45°-0-45°)", "Maneta": "Corta negra", "Esquema": "Manual - 0 - Automático"}), "Selección de operación Manual / Fuera / Automático en bombas y motores"),
        (brand, line_mando, "Selectores Metálicos", "Modular Way", "WAS-610NB", "Selector Metálico 3 Posiciones con Retorno al Centro por Resorte", "Selector con retorno elástico momentáneo desde ambos lados al centro", json.dumps({"Posiciones": "3 posiciones con retorno por muelle a cero", "Maneta": "Corta negra"}), "Control de apertura y cierre momentáneo en válvulas o compuertas"),
        (brand, line_mando, "Selectores Metálicos", "Modular Way", "WAK-510NB", "Selector con Llave de 3 Posiciones Mantenidas Ø22mm", "Selector accionado por llave extraíble en posición cero para control de acceso", json.dumps({"Posiciones": "3 posiciones fijas", "ExtraccionLlave": "En posición cero", "Material": "Metálico"}), "Selección Local/Remoto restringida a supervisores")
    ])

    # 4.4 Pilotos Luminosos LED Integrados WBL / CL Ø22mm
    items.extend([
        (brand, line_mando, "Pilotos Luminosos LED", "Modular Way", "CL-502G", "Piloto LED Compacto Verde 24V AC/DC Ø22mm", "Indicador luminoso monobloc con tecnología LED integrada de larga duración (>50.000 h) color verde", json.dumps({"Color": "Verde", "Tension": "24V AC/DC", "Tecnologia": "LED integrado", "Proteccion": "IP66/IP67/IP69K"}), "Señalización de motor en marcha o máquina lista"),
        (brand, line_mando, "Pilotos Luminosos LED", "Modular Way", "CL-502R", "Piloto LED Compacto Rojo 24V AC/DC Ø22mm", "Indicador luminoso LED integrado color rojo a 24V", json.dumps({"Color": "Rojo", "Tension": "24V AC/DC", "Tecnologia": "LED integrado"}), "Señalización de fallo térmico, alarma o máquina detenida"),
        (brand, line_mando, "Pilotos Luminosos LED", "Modular Way", "CL-502Y", "Piloto LED Compacto Amarillo 24V AC/DC Ø22mm", "Indicador luminoso LED integrado color amarillo a 24V", json.dumps({"Color": "Amarillo", "Tension": "24V AC/DC"}), "Aviso de advertencia, nivel bajo o ciclo en proceso"),
        (brand, line_mando, "Pilotos Luminosos LED", "Modular Way", "CL-523G", "Piloto LED Compacto Verde 230V AC Ø22mm", "Piloto LED para conexión directa a red 230V AC", json.dumps({"Color": "Verde", "Tension": "230V AC", "Tecnologia": "LED"}), "Presencia de red y confirmación de maniobra en 230V"),
        (brand, line_mando, "Pilotos Luminosos LED", "Modular Way", "CL-523R", "Piloto LED Compacto Rojo 230V AC Ø22mm", "Piloto LED rojo para red 230V AC", json.dumps({"Color": "Rojo", "Tension": "230V AC"}), "Alarma general de cuadro eléctrico en 230V"),
        (brand, line_mando, "Pilotos Luminosos LED", "Modular Way", "CL-523W", "Piloto LED Compacto Blanco 230V AC Ø22mm", "Piloto LED blanco de alta luminosidad", json.dumps({"Color": "Blanco", "Tension": "230V AC"}), "Indicación de cuadro con tensión de acometida")
    ])

    # 4.5 Bloques de Contacto, Portalámparas y Bridas (WBC, MCB, MCBH)
    items.extend([
        (brand, line_mando, "Bloques Auxiliares", "Modular Way", "MCB-10", "Bloque de Contacto 1 NA para Pulsadores Ø22mm", "Bloque de contacto simple normalmente abierto para montaje en brida trasera", json.dumps({"Contactos": "1 NA (Normalmente Abierto)", "Ith": "10A", "Ui": "690V", "CodigoPedido": "1SFA611610R1001"}), "Circuito de marcha y arranque"),
        (brand, line_mando, "Bloques Auxiliares", "Modular Way", "MCB-01", "Bloque de Contacto 1 NC para Pulsadores Ø22mm", "Bloque de contacto normalmente cerrado con ruptura positiva para seguridad", json.dumps({"Contactos": "1 NC (Normalmente Cerrado)", "AperturaPositiva": "Sí", "CodigoPedido": "1SFA611610R1010"}), "Circuitos de parada y paradas de emergencia"),
        (brand, line_mando, "Bloques Auxiliares", "Modular Way", "MCBH-00", "Brida Portabloques de 3 Posiciones Ø22mm", "Brida adaptadora para fijar hasta 3 bloques de contacto o LED al cabezal", json.dumps({"Capacidad": "3 bloques", "Material": "Metálico / Polímero reforzado", "CodigoPedido": "1SFA611605R1100"}), "Fijación entre cabezal frontal y bloques de contacto"),
        (brand, line_mando, "Bloques Auxiliares", "Modular Way", "WBC-10", "Bloque de Contacto 1 NA Modular Way Metal", "Bloque de contacto 1 NA plataforma Modular Way", json.dumps({"Contactos": "1 NA", "Plataforma": "Modular Way"}), "Accionamiento en cabezas WAP/WAS"),
        (brand, line_mando, "Bloques Auxiliares", "Modular Way", "WBC-01", "Bloque de Contacto 1 NC Modular Way Metal", "Bloque de contacto 1 NC plataforma Modular Way con contacto de seguridad", json.dumps({"Contactos": "1 NC", "Plataforma": "Modular Way"}), "Accionamiento de corte en paradas de emergencia WAE")
    ])

    # 4.6 Cajas Botoneras (Enclosures)
    items.extend([
        (brand, line_mando, "Cajas Botoneras", "Modular Way", "MEP1-0", "Caja Botonera Vacía 1 Taladro Gris/Negro Ø22mm", "Caja de policarbonato reforzado para 1 unidad de mando IP66", json.dumps({"Taladros": "1 taladro 22mm", "Proteccion": "IP66", "Material": "Policarbonato resistente a rayos UV", "CodigoPedido": "1SFA611811R1000"}), "Puestos de mando locales y pulsadores de marcha simple"),
        (brand, line_mando, "Cajas Botoneras", "Modular Way", "MEP2-0", "Caja Botonera Vacía 2 Taladros Gris/Negro Ø22mm", "Caja para 2 elementos de mando IP66", json.dumps({"Taladros": "2 taladros 22mm", "Proteccion": "IP66", "CodigoPedido": "1SFA611812R1000"}), "Estaciones locales Marcha-Paro de motores"),
        (brand, line_mando, "Cajas Botoneras", "Modular Way", "MEPY1-0", "Caja Botonera Vacía 1 Taladro Amarilla para Parada de Emergencia", "Caja de seguridad amarilla de alta visibilidad para botón tipo seta", json.dumps({"Taladros": "1 taladro 22mm", "Color": "Amarillo seguridad", "Proteccion": "IP66", "CodigoPedido": "1SFA611821R1000"}), "Estaciones de parada de emergencia en pasillos y transportadores")
    ])

    # =========================================================================
    # 5. LÍNEA: RELÉS DE TIEMPO, MEDIDA Y VIGILANCIA ELECTRÓNICA
    # =========================================================================
    line_reles = "Relés de Control"

    items.extend([
        (brand, line_reles, "Relés Temporizadores", "Serie CT-S", "CT-MVS.21S", "Relé Temporizador Multifunción Electrónico 24-240V AC/DC 2 C/O", "Relé de tiempo multifunción con 11 funciones (retardo a la conexión, desconexión, generador de pulsos, intermitencia) y rango de 0.05 segundos hasta 300 horas", json.dumps({"Tension": "24-240V AC/DC Universal", "Contactos": "2 C/O (conmutados independientes 4A)", "RangoTiempo": "0.05s a 300h en 10 rangos", "Funciones": "11 funciones configurables", "Montaje": "Riel DIN 35mm"}), "Secuencias de arranque de motores estrella-triángulo, sistemas de bombeo, iluminación y automatismos"),
        (brand, line_reles, "Relés Temporizadores", "Serie CT-S", "CT-ERS.21S", "Relé Temporizador Retardo a la Conexión (ON-Delay) 24-240V AC/DC 2 C/O", "Temporizador simple de alta precisión con retardo a la activación de contactos", json.dumps({"Tension": "24-240V AC/DC", "Contactos": "2 C/O", "RangoTiempo": "0.05s a 300h"}), "Retardo de arranque escalonado para evitar picos simultáneos de corriente"),
        (brand, line_reles, "Relés de Vigilancia de Red", "Serie CM-S", "CM-PVS.41S", "Relé de Vigilancia de Red Trifásica Multifunción 300-500V AC", "Relé electrónico para monitorización de sobretensión, subtensión, asimetría de fases y fallo de fase con retardo de disparo regulable", json.dumps({"TensionSupervisada": "300 a 500V AC Trifásico", "Salidas": "2 C/O", "Deteccion": "Sobretensión, Subtensión, Pérdida de fase, Asimetría", "RetardoDisparo": "0 o 0.1 a 30s ajustable"}), "Protección avanzada de compresores, bombas y centros de control de motores contra mala calidad de red"),
        (brand, line_reles, "Relés de Vigilancia de Red", "Serie CM-S", "CM-PAS.31S", "Relé de Control de Fases y Secuencia de Giro 160-300V AC", "Relé para detección de orden de fases y fallo de una fase", json.dumps({"Tension": "160 a 300V AC", "Salida": "1 C/O", "Deteccion": "Secuencia de giro incorrecta y fallo de fase"}), "Evita que motores trifásicos giren en sentido inverso en bombas, ventiladores y ascensores"),
        (brand, line_reles, "Relés de Protección Térmica", "Serie CM-S", "CM-MSE", "Relé de Protección de Motor por Sonda Termistor PTC 110-240V AC", "Dispositivo de vigilancia de temperatura mediante sensores PTC embebidos directamente en los bobinados del estator", json.dumps({"Alimentacion": "110-240V AC", "Sensores": "Sondas PTC", "Salida": "1 NA"}), "Protección contra sobretemperatura en motores sumergibles, ventilación forzada y servicio pesado")
    ])

    # =========================================================================
    # 6. LÍNEA: FUENTES DE ALIMENTACIÓN INDUSTRIAL (CP-E / CP-C.1)
    # =========================================================================
    line_fuentes = "Fuentes de Alimentación"

    items.extend([
        (brand, line_fuentes, "Fuentes de Alimentación", "Serie CP-E", "CP-E 24/0.75", "Fuente de Alimentación Conmutada 24V DC 0.75A (18W)", "Fuente modular compacta para alimentación de circuitos de control e instrumentación", json.dumps({"Entrada": "90-264V AC / 120-375V DC", "Salida": "24V DC", "Corriente": "0.75A", "Potencia": "18W", "Montaje": "Riel DIN 35mm"}), "Alimentación de transmisores, sensores y pequeños relés"),
        (brand, line_fuentes, "Fuentes de Alimentación", "Serie CP-E", "CP-E 24/1.25", "Fuente de Alimentación Conmutada 24V DC 1.25A (30W)", "Fuente de alimentación industrial de 30W en 24V", json.dumps({"Entrada": "90-264V AC", "Salida": "24V DC regulable (24-28V)", "Corriente": "1.25A", "Potencia": "30W"}), "Cuadros de control pequeños y actuadores"),
        (brand, line_fuentes, "Fuentes de Alimentación", "Serie CP-E", "CP-E 24/2.5", "Fuente de Alimentación Conmutada 24V DC 2.5A (60W)", "Fuente de 60W para controladores lógicos y periféricos", json.dumps({"Entrada": "90-264V AC", "Salida": "24V DC", "Corriente": "2.5A", "Potencia": "60W", "Eficiencia": "89%"}), "Alimentación de PLCs compactos y módulos de E/S"),
        (brand, line_fuentes, "Fuentes de Alimentación", "Serie CP-E", "CP-E 24/5.0", "Fuente de Alimentación Conmutada 24V DC 5A (120W)", "Fuente conmutada industrial de 120W de alta estabilidad", json.dumps({"Entrada": "115/230V AC seleccionable", "Salida": "24V DC (ajustable 24-28V)", "Corriente": "5.0A", "Potencia": "120W", "Eficiencia": "89%"}), "Tableros de control con pantallas HMI, PLCs y relés"),
        (brand, line_fuentes, "Fuentes de Alimentación", "Serie CP-E", "CP-E 24/10.0", "Fuente de Alimentación Conmutada 24V DC 10A (240W) con PFC", "Fuente de potencia industrial con corrección activa de factor de potencia (PFC)", json.dumps({"Entrada": "90-264V AC Universal", "Salida": "24V DC", "Corriente": "10.0A", "Potencia": "240W", "PFC": "Activo"}), "Centros de control de motores, líneas automáticas y salas de control"),
        (brand, line_fuentes, "Fuentes de Alimentación", "Serie CP-E", "CP-E 24/20.0", "Fuente de Alimentación Conmutada 24V DC 20A (480W) con PFC", "Fuente de máxima potencia monofásica para 20A continuos", json.dumps({"Entrada": "90-264V AC", "Salida": "24V DC", "Corriente": "20.0A", "Potencia": "480W"}), "Grandes cuadros de automatización industrial y servidores"),
        (brand, line_fuentes, "Fuentes de Alimentación", "Serie CP-C.1", "CP-C.1 24/20.0", "Fuente de Alta Gama CP-C.1 24V DC 20A con Power Boost 150%", "Fuente premium de alta resistencia con reserva de potencia del 50% para arrancar cargas difíciles", json.dumps({"Entrada": "85-264V AC / 90-300V DC", "Salida": "24V DC", "Corriente": "20A (30A Power Boost)", "Eficiencia": "94%", "Temperatura": "-25 a +70 °C"}), "Plantas industriales críticas y procesos continuos")
    ])

    # =========================================================================
    # 7. LÍNEA: GESTIÓN Y MEDICIÓN DE ENERGÍA (M4M / CTMAX)
    # =========================================================================
    line_medida = "Medición y Calidad de Energía"

    items.extend([
        (brand, line_medida, "Centrales de Medida Multímetro", "Serie M4M", "M4M-20-MODBUS", "Analizador de Redes Eléctricas M4M 20 Modbus RTU Pantalla Gráfica", "Multímetro digital de medida de parámetros eléctricos (V, I, P, Q, S, FP, F, THD) para montaje empotrado en puerta 96x96 mm con puerto serie RS485 Modbus RTU", json.dumps({"Parametros": "Tensión, Corriente, Potencia activa/reactiva, Energía kWh Clase 0.5S, THD hasta armónico 40", "Comunicacion": "RS485 Modbus RTU", "Montaje": "Empotrado 96x96 mm", "Pantalla": "Gráfica LCD táctil retroiluminada"}), "Monitorización de cuadros generales de baja tensión y gestión energética en fábricas"),
        (brand, line_medida, "Centrales de Medida Multímetro", "Serie M4M", "M4M-20-ETHERNET", "Analizador de Redes Eléctricas M4M 20 Ethernet Modbus TCP", "Analizador con puerto Ethernet RJ45 nativo para conexión directa a redes LAN y servidores SCADA", json.dumps({"Parametros": "Parámetros eléctricos completos y calidad de red", "Comunicacion": "Ethernet Modbus TCP / Webserver integrado", "Precision": "Clase 0.5S"}), "Sistemas de gestión energética ISO 50001 e integración en plantas inteligentes"),
        (brand, line_medida, "Centrales de Medida Multímetro", "Serie M4M", "M4M-30-MODBUS", "Analizador de Redes y Calidad de Onda M4M 30 con Registro de Eventos", "Analizador avanzado con medición de armónicos individuales hasta orden 40, detección de huecos/sobretensiones y memoria interna de eventos", json.dumps({"Parametros": "Calidad de onda completa, armónicos individuales, transitorios, eventos", "Memoria": "Registro interno de curvas de carga", "Comunicacion": "Modbus RTU"}), "Auditorías energéticas y subestaciones de distribución exigentes"),
        (brand, line_medida, "Transformadores de Corriente (TC)", "Serie CTMAX", "CTMAX-1-100/5", "Transformador de Corriente de Núcleo Cerrado CTMAX 1 100/5A", "Transformador de medida para barras y cables de hasta 30 mm", json.dumps({"Relacion": "100/5 A", "Clase": "Clase 0.5 (1.5 VA) / Clase 1 (2.5 VA)", "Ventana": "Cable Ø30 mm o barra 30x10 mm"}), "Conexión a centrales de medida en alimentadores de 100A"),
        (brand, line_medida, "Transformadores de Corriente (TC)", "Serie CTMAX", "CTMAX-1-200/5", "Transformador de Corriente CTMAX 1 200/5A", "Transformador de medida para 200A", json.dumps({"Relacion": "200/5 A", "Clase": "Clase 0.5 (2.5 VA)", "Ventana": "Ø30 mm / 30x10 mm"}), "Alimentadores de 200A en cuadros de fuerza"),
        (brand, line_medida, "Transformadores de Corriente (TC)", "Serie CTMAX", "CTMAX-2-400/5", "Transformador de Corriente CTMAX 2 400/5A", "Transformador de medida para barras de 40x10 mm", json.dumps({"Relacion": "400/5 A", "Clase": "Clase 0.5 (5 VA)", "Ventana": "Barra 40x10 mm"}), "Cabeceras de cuadros secundarios de 400A"),
        (brand, line_medida, "Transformadores de Corriente (TC)", "Serie CTMAX", "CTMAX-2-600/5", "Transformador de Corriente CTMAX 2 600/5A", "Transformador de medida para 600A", json.dumps({"Relacion": "600/5 A", "Clase": "Clase 0.5 (5 VA)", "Ventana": "Barra 40x10 mm"}), "Entradas principales de tableros de 600A"),
        (brand, line_medida, "Transformadores de Corriente (TC)", "Serie CTMAX", "CTMAX-3-1000/5", "Transformador de Corriente CTMAX 3 1000/5A", "Transformador de medida para pletinas de gran tamaño", json.dumps({"Relacion": "1000/5 A", "Clase": "Clase 0.5 (10 VA)", "Ventana": "Barra 60x20 mm"}), "Salida de transformadores de 750 kVA"),
        (brand, line_medida, "Transformadores de Corriente (TC)", "Serie CTMAX", "CTMAX-3-1500/5", "Transformador de Corriente CTMAX 3 1500/5A", "Transformador para acometidas de hasta 1500A", json.dumps({"Relacion": "1500/5 A", "Clase": "Clase 0.5 (15 VA)"}), "Cabecera principal de subestaciones de distribución")
    ])

    # =========================================================================
    # 8. LÍNEA: CONTROLADORES Y AUTOMATIZACIÓN (PLCs AC500 / PANTALLAS CP600)
    # =========================================================================
    line_plc = "Controladores y HMI"

    items.extend([
        (brand, line_plc, "Controladores Lógicos (PLCs)", "AC500-eCo", "PM554-T-ETH", "Controlador Lógico Modular AC500-eCo CPU 8DI/6DO Transistor Ethernet", "CPU compacta escalable con puerto Ethernet integrado (soporte Modbus TCP y servidor web), 128 kB de memoria de programa y slot para tarjeta SD", json.dumps({"EntradasDigitales": "8 DI 24V DC", "SalidasDigitales": "6 DO transistor 24V DC", "Comunicacion": "Ethernet (Modbus TCP) + RS485 (Modbus RTU)", "Memoria": "128 kB", "Alimentacion": "24V DC"}), "Automatización de maquinaria, control de bombas, HVAC y plantas de envasado"),
        (brand, line_plc, "Controladores Lógicos (PLCs)", "AC500-eCo", "PM554-R-AC", "Controlador Lógico Modular AC500-eCo CPU 8DI/6DO Relé 230V AC", "CPU con alimentación directa a 100-240V AC y salidas a relé conmutadas", json.dumps({"EntradasDigitales": "8 DI 24V DC", "SalidasDigitales": "6 DO relé libres de potencial (2A)", "Alimentacion": "100-240V AC", "Comunicacion": "RS485 Modbus RTU"}), "Cuadros de control autónomos en instalaciones terciarias e iluminación"),
        (brand, line_plc, "Controladores Lógicos (PLCs)", "AC500-eCo", "PM564-R-ETH", "Controlador Lógico AC500-eCo CPU 6DI/6DO Relé + 2AI/1AO Ethernet", "CPU compacta con entradas y salidas analógicas integradas en el equipo", json.dumps({"EntradasDigitales": "6 DI", "SalidasDigitales": "6 DO relé", "EntradasAnalogicas": "2 AI (0-10V / 4-20mA)", "SalidasAnalogicas": "1 AO", "Comunicacion": "Ethernet"}), "Control en bucle cerrado PID de presión, temperatura o nivel"),
        (brand, line_plc, "Módulos de Expansión", "Serie S500", "DI524", "Módulo de Expansión Digital S500 32 Entradas Digitales 24V DC", "Módulo de alta densidad con 32 entradas digitales en 24V DC", json.dumps({"EntradasDigitales": "32 DI 24V DC", "Aislamiento": "Por grupos", "Compatible": "Familia AC500 y AC500-eCo"}), "Captación masiva de estados de pulsadores, finales de carrera y sensores"),
        (brand, line_plc, "Módulos de Expansión", "Serie S500", "DO524", "Módulo de Expansión Digital S500 32 Salidas Transistor 24V DC", "Módulo de 32 salidas digitales a transistor de 0.5A", json.dumps({"SalidasDigitales": "32 DO transistor 24V DC 0.5A", "Compatible": "AC500"}), "Accionamiento directo de relés y válvulas"),
        (brand, line_plc, "Módulos de Expansión", "Serie S500", "AX522", "Módulo de Expansión Analógico S500 4 Entradas / 4 Salidas Analógicas", "Módulo mixto de alta resolución (12 bits) configurable para tensión y corriente", json.dumps({"EntradasAnalogicas": "4 AI configurables (0-10V, +/-10V, 0/4-20mA)", "SalidasAnalogicas": "4 AO configurables", "Resolucion": "12 bits + signo"}), "Control de variadores de velocidad y registro de variables de proceso"),
        (brand, line_plc, "Pantallas Táctiles HMI", "Serie CP600-eCo", "CP604", "Pantalla Táctil HMI CP604 4.3\" Color TFT Táctil Ethernet", "Panel de operador táctil compacto de 4.3 pulgadas en color con puerto Ethernet y programación intuitiva PB610", json.dumps({"Pantalla": "4.3 pulgadas TFT color (480x272 px)", "Colores": "64k colores", "Comunicacion": "1x Ethernet 10/100, 1x USB host", "ProteccionFrontal": "IP66"}), "Interfaz de operador en puestos de mando locales y máquinas compactas"),
        (brand, line_plc, "Pantallas Táctiles HMI", "Serie CP600-eCo", "CP607", "Pantalla Táctil HMI CP607 7.0\" Color TFT Panorámica Ethernet", "Panel HMI de 7 pulgadas de alta definición panorámica 16:9 con funciones de recetas, alarmas y tendencias", json.dumps({"Pantalla": "7.0 pulgadas panorámica (800x480 px)", "Comunicacion": "Ethernet Modbus TCP, USB, RS485", "ProteccionFrontal": "IP66"}), "Puesto de supervisión principal en líneas de manufactura y tratamiento de aguas"),
        (brand, line_plc, "Pantallas Táctiles HMI", "Serie CP600-eCo", "CP610", "Pantalla Táctil HMI CP610 10.1\" Color TFT Táctil Ethernet", "Panel HMI de gran formato de 10.1 pulgadas", json.dumps({"Pantalla": "10.1 pulgadas (1024x600 px)", "Comunicacion": "Ethernet, USB, serie", "Proteccion": "IP66"}), "Salas de control de procesos continuos y maquinaria compleja")
    ])

    return items

def populate_database():
    items = get_abb_catalog_data()
    print(f"Total de productos preparados para ABB: {len(items)}")

    # Verify no duplicate codes
    codes = [it[4] for it in items]
    unique_codes = set(codes)
    if len(codes) != len(unique_codes):
        print(f"ALERTA: Existen {len(codes) - len(unique_codes)} códigos duplicados:")
        from collections import Counter
        counts = Counter(codes)
        for c, cnt in counts.items():
            if cnt > 1:
                print(f"  Duplicado: {c} ({cnt} veces)")
        return

    paths = get_db_paths()
    for db_path in paths:
        print(f"\nSincronizando base de datos en: {db_path}")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.executemany("""
            INSERT OR REPLACE INTO ProductsCatalog (
                Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application, Status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Disponible');
        """, items)
        conn.commit()

        # Rebuild FTS5
        try:
            cur.execute("INSERT INTO Products_FTS(Products_FTS) VALUES('rebuild');")
            conn.commit()
            print("  FTS5 reconstruido exitosamente.")
        except Exception as e:
            print(f"  Aviso al reconstruir FTS5: {e}")

        cur.execute("SELECT COUNT(1) FROM ProductsCatalog WHERE Brand = 'ABB';")
        count_abb = cur.fetchone()[0]
        cur.execute("SELECT COUNT(1) FROM Products_FTS;")
        fts_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT Brand) FROM ProductsCatalog;")
        brands_count = cur.fetchone()[0]
        print(f"-> Productos ABB en ProductsCatalog: {count_abb}")
        print(f"-> Total productos indexados en Products_FTS: {fts_count}")
        print(f"-> Marcas activas en catálogo: {brands_count}")

        conn.close()

    # Synchronize release directory if present
    rel_dir = os.path.abspath("AgentePower/bin/Release/net8.0")
    if os.path.exists(rel_dir):
        shutil.copy2(os.path.abspath("agente_ventas.db"), os.path.join(rel_dir, "agente_ventas.db"))
        print(f"-> Sincronizado a Release: {os.path.join(rel_dir, 'agente_ventas.db')}")

if __name__ == "__main__":
    populate_database()
