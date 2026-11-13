import os
import sqlite3
import json

def get_db_paths():
    paths = [
        os.path.abspath("AgentePower/agente_ventas.db"),
        os.path.abspath("AgentePower/bin/Debug/net8.0/agente_ventas.db"),
        os.path.abspath("AgentePower/bin/Release/net8.0/agente_ventas.db"),
        os.path.abspath("publish/agente_ventas.db"),
        os.path.abspath("agente_ventas.db")
    ]
    return [p for p in paths if os.path.exists(os.path.dirname(p))]

def get_siemens_catalog_data():
    brand = "Siemens"
    items = []

    # =========================================================================
    # 1. LÍNEA: DISTRIBUCIÓN ELÉCTRICA EN BAJA TENSIÓN (SENTRON)
    # =========================================================================
    line_dist = "Distribución Eléctrica"

    # Termomagnéticos Modulares SENTRON 5SL4 (Poder de corte 10 kA)
    currents_5sl4 = [6, 10, 16, 20, 25, 32, 40, 50, 63]
    for c in currents_5sl4:
        # 1P
        code_1p = f"5SL41{c:02d}-7"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "SENTRON 5SL4", code_1p,
            f"Interruptor Automático SENTRON 5SL4 1P {c}A Curva C 10kA",
            f"Interruptor magnetotérmico unipolar para protección industrial y terciaria de circuitos derivados",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "10 kA (IEC 60898-1)", "Tension": "230/400V AC", "Montaje": "Riel DIN 35mm"}),
            "Protección de circuitos monofásicos de fuerza, iluminación y tomas industriales"
        ))
        # 2P
        code_2p = f"5SL42{c:02d}-7"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "SENTRON 5SL4", code_2p,
            f"Interruptor Automático SENTRON 5SL4 2P {c}A Curva C 10kA",
            f"Interruptor bipolar industrial magnetotérmico con alta capacidad de ruptura",
            json.dumps({"Polos": "2P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "10 kA", "Tension": "400V AC"}),
            "Circuitos bifásicos, compresores, aires acondicionados y acometidas secundarias"
        ))
        # 3P
        code_3p = f"5SL43{c:02d}-7"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "SENTRON 5SL4", code_3p,
            f"Interruptor Automático SENTRON 5SL4 3P {c}A Curva C 10kA",
            f"Interruptor tripolar industrial para protección de alimentadores y motores trifásicos",
            json.dumps({"Polos": "3P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "10 kA", "Tension": "400V AC"}),
            "Distribución trifásica en tableros de control de motores, climatización y plantas industriales"
        ))

    # Interruptores Diferenciales SENTRON 5SV
    items.extend([
        (brand, line_dist, "Interruptores Diferenciales", "SENTRON 5SV", "5SV3312-6", "Interruptor Diferencial SENTRON 5SV 2P 25A 30mA", "Dispositivo de corriente residual bipolar para protección de personas", json.dumps({"Polos": "2P", "Corriente": "25A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC"}), "Protección humana contra descargas eléctricas en circuitos monofásicos"),
        (brand, line_dist, "Interruptores Diferenciales", "SENTRON 5SV", "5SV3314-6", "Interruptor Diferencial SENTRON 5SV 2P 40A 30mA", "Diferencial bipolar de 40A para cuadros generales residenciales y comerciales", json.dumps({"Polos": "2P", "Corriente": "40A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC"}), "Cabecera de tableros de distribución monofásicos"),
        (brand, line_dist, "Interruptores Diferenciales", "SENTRON 5SV", "5SV3316-6", "Interruptor Diferencial SENTRON 5SV 2P 63A 30mA", "Diferencial de alta capacidad para 63A monofásicos", json.dumps({"Polos": "2P", "Corriente": "63A", "Sensibilidad": "30mA", "Tipo": "AC"}), "Tableros con alta demanda monofásica"),
        (brand, line_dist, "Interruptores Diferenciales", "SENTRON 5SV", "5SV3342-6", "Interruptor Diferencial SENTRON 5SV 4P 25A 30mA", "Diferencial tetrapolar para circuitos trifásicos con neutro", json.dumps({"Polos": "4P", "Corriente": "25A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Líneas de alimentación a talleres y pequeños obradores"),
        (brand, line_dist, "Interruptores Diferenciales", "SENTRON 5SV", "5SV3344-6", "Interruptor Diferencial SENTRON 5SV 4P 40A 30mA", "Diferencial tetrapolar industrial de 40A clase AC", json.dumps({"Polos": "4P", "Corriente": "40A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Tableros generales comerciales y plantas terciarias"),
        (brand, line_dist, "Interruptores Diferenciales", "SENTRON 5SV", "5SV3346-6", "Interruptor Diferencial SENTRON 5SV 4P 63A 30mA", "Diferencial tetrapolar de potencia para 63A", json.dumps({"Polos": "4P", "Corriente": "63A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Cabeceras de cuadros de fuerza industrial")
    ])

    # Protectores contra Sobretensiones Transitorias SENTRON 5SD7 (DPS / SPD)
    items.extend([
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "SENTRON 5SD7", "5SD7461-1", "Protector de Sobretensiones SENTRON 5SD7 Tipo 2 1P+N 40kA", "Descargador de sobretensiones transitorias para redes monofásicas con contacto remoto", json.dumps({"Polos": "1P+N", "Imax": "40 kA", "In": "20 kA", "Up": "1.5 kV", "Tension": "230V AC", "ContactoRemoto": "Sí"}), "Protección de equipos electrónicos sensibles y servidores monofásicos"),
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "SENTRON 5SD7", "5SD7464-1", "Protector de Sobretensiones SENTRON 5SD7 Tipo 2 3P+N 40kA", "Descargador tetrapolar industrial para protección de tableros trifásicos", json.dumps({"Polos": "3P+N", "Imax": "40 kA", "In": "20 kA", "Up": "1.5 kV", "Tension": "230/400V AC", "Cartuchos": "Recambiables"}), "Cabecera de cuadros de distribución en industrias y comercios"),
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "SENTRON 5SD7", "5SD7484-1", "Protector de Sobretensiones Combinado SENTRON 5SD7 Tipo 1+2 100kA", "Descargador de corrientes de rayo y sobretensiones de máxima capacidad", json.dumps({"Polos": "3P+N", "Iimp": "25 kA por polo", "Imax": "100 kA", "Norma": "IEC 61643-11"}), "Acometidas de edificios con pararrayos y subestaciones eléctricas")
    ])

    # Cajas Moldeadas SENTRON 3VA1 (Termomagnéticos hasta 250A)
    items.extend([
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1140-3ED36-0AA0", "Interruptor Automático SENTRON 3VA1 3P 40A 25kA TM210", "Interruptor en caja moldeada termomagnético compacto de 40A", json.dumps({"Polos": "3P", "Corriente": "40A", "PoderCorte": "25 kA a 415V", "Disparador": "TM210 Fijo"}), "Acometidas de fuerza y tableros de bombas pequeñas"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1150-3ED36-0AA0", "Interruptor Automático SENTRON 3VA1 3P 50A 25kA TM210", "Interruptor en caja moldeada compacto de 50A", json.dumps({"Polos": "3P", "Corriente": "50A", "PoderCorte": "25 kA a 415V", "Disparador": "TM210 Fijo"}), "Protección de alimentadores industriales secundarios"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1163-3ED36-0AA0", "Interruptor Automático SENTRON 3VA1 3P 63A 25kA TM210", "Interruptor en caja moldeada de 63A", json.dumps({"Polos": "3P", "Corriente": "63A", "PoderCorte": "25 kA a 415V", "Disparador": "TM210 Fijo"}), "Tableros de fuerza en talleres y locales"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1180-3ED36-0AA0", "Interruptor Automático SENTRON 3VA1 3P 80A 25kA TM210", "Interruptor en caja moldeada de 80A", json.dumps({"Polos": "3P", "Corriente": "80A", "PoderCorte": "25 kA", "Disparador": "TM210 Fijo"}), "Alimentadores de planta y climatización"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1110-3ED36-0AA0", "Interruptor Automático SENTRON 3VA1 3P 100A 25kA TM210", "Interruptor en caja moldeada para cabeceras de cuadros de 100A", json.dumps({"Polos": "3P", "Corriente": "100A", "PoderCorte": "25 kA a 415V", "Disparador": "TM210 Fijo"}), "Cabecera de tableros de distribución comercial"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1112-3ED36-0AA0", "Interruptor Automático SENTRON 3VA1 3P 125A 25kA TM210", "Interruptor en caja moldeada de 125A", json.dumps({"Polos": "3P", "Corriente": "125A", "PoderCorte": "25 kA", "Disparador": "TM210 Fijo"}), "Alimentadores generales de subdistribución"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1116-3ED36-0AA0", "Interruptor Automático SENTRON 3VA1 3P 160A 25kA TM210", "Interruptor termomagnético en caja moldeada para 160A", json.dumps({"Polos": "3P", "Corriente": "160A", "PoderCorte": "25 kA a 415V", "Disparador": "TM210 Fijo"}), "Protección principal en cuadros secundarios de fábrica"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1220-4EF32-0AA0", "Interruptor Automático SENTRON 3VA1 3P 200A 36kA TM240", "Interruptor termomagnético regulable para 200A con 36kA de corte", json.dumps({"Polos": "3P", "Corriente": "200A", "PoderCorte": "36 kA a 415V", "Disparador": "TM240 Térmico Regulable (140-200A)"}), "Acometidas de media industria y centros de bombeo"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1225-4EF32-0AA0", "Interruptor Automático SENTRON 3VA1 3P 250A 36kA TM240", "Interruptor en caja moldeada regulable de 250A con 36kA", json.dumps({"Polos": "3P", "Corriente": "250A", "PoderCorte": "36 kA a 415V", "Disparador": "TM240 Regulable (175-250A)"}), "Cabecera principal de tableros industriales de 250A"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1116-3EE46-0AA0", "Interruptor Automático SENTRON 3VA1 4P 160A 25kA TM220", "Interruptor tetrapolar con neutro protegido al 100% para transferencias", json.dumps({"Polos": "4P (3P+N)", "Corriente": "160A", "PoderCorte": "25 kA", "Disparador": "TM220"}), "Sistemas de transferencia red-generador de 160A"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA1", "3VA1225-4EF42-0AA0", "Interruptor Automático SENTRON 3VA1 4P 250A 36kA TM240", "Interruptor tetrapolar regulable de 250A para generadores", json.dumps({"Polos": "4P (3P+N)", "Corriente": "250A", "PoderCorte": "36 kA", "Disparador": "TM240 Regulable"}), "Transferencias automáticas de grupos electrógenos de 150 kVA")
    ])

    # Cajas Moldeadas Electrónicas SENTRON 3VA2 (400A a 1000A)
    items.extend([
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA2", "3VA2340-5HN32-0AA0", "Interruptor Automático SENTRON 3VA2 3P 400A 55kA ETU320", "Interruptor de potencia industrial con unidad de control electrónica ETU320", json.dumps({"Polos": "3P", "Corriente": "400A", "PoderCorte": "55 kA a 415V", "Disparador": "ETU320 Electrónico LI (160-400A)", "Proteccion": "Sobrecarga L y Cortocircuito I regulables"}), "Cabeceras de distribución en plantas industriales y centros comerciales"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA2", "3VA2463-5HN32-0AA0", "Interruptor Automático SENTRON 3VA2 3P 630A 55kA ETU320", "Interruptor de potencia industrial para distribución de 630A con 55kA", json.dumps({"Polos": "3P", "Corriente": "630A", "PoderCorte": "55 kA a 415V", "Disparador": "ETU320 Electrónico LI (250-630A)"}), "Cabecera de tableros generales de baja tensión (TGBT)"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA2", "3VA2580-5HN32-0AA0", "Interruptor Automático SENTRON 3VA2 3P 800A 55kA ETU320", "Interruptor de caja moldeada pesada para 800A", json.dumps({"Polos": "3P", "Corriente": "800A", "PoderCorte": "55 kA a 415V", "Disparador": "ETU320 Electrónico"}), "Entrada de transformadores de 500 kVA"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA2", "3VA2510-5HN32-0AA0", "Interruptor Automático SENTRON 3VA2 3P 1000A 55kA ETU320", "Interruptor de potencia de 1000A con protección electrónica", json.dumps({"Polos": "3P", "Corriente": "1000A", "PoderCorte": "55 kA", "Disparador": "ETU320 Electrónico"}), "Salida de transformadores de 750 kVA"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA2", "3VA2340-5HN42-0AA0", "Interruptor Automático SENTRON 3VA2 4P 400A 55kA ETU320", "Interruptor tetrapolar electrónico de 400A para transferencias de potencia", json.dumps({"Polos": "4P (3P+N)", "Corriente": "400A", "PoderCorte": "55 kA", "Disparador": "ETU320"}), "Alimentadores de generadores de 300 kVA con neutro"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "SENTRON 3VA2", "3VA2463-5HN42-0AA0", "Interruptor Automático SENTRON 3VA2 4P 630A 55kA ETU320", "Interruptor tetrapolar electrónico de 630A para generadores de 500 kVA", json.dumps({"Polos": "4P (3P+N)", "Corriente": "630A", "PoderCorte": "55 kA", "Disparador": "ETU320"}), "Transferencias automáticas de hospitales y plantas críticas")
    ])

    # Interruptores de Bastidor Abierto SENTRON 3WA (ACB 800A a 6300A)
    items.extend([
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1108-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 800A 55kA ETU300", "Interruptor abierto inteligente para protección de redes y subestaciones", json.dumps({"Polos": "3P", "Corriente": "800A", "PoderCorte": "55 kA a 500V", "Disparador": "ETU300 Electrónico", "Montaje": "Fijo frontal"}), "Entrada de subestaciones y transformadores de 500 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1110-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 1000A 55kA ETU300", "Interruptor abierto de potencia de 1000A", json.dumps({"Polos": "3P", "Corriente": "1000A", "PoderCorte": "55 kA", "Disparador": "ETU300"}), "Subestaciones de 750 kVA en industrias"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1112-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 1250A 55kA ETU300", "Interruptor abierto de potencia de 1250A", json.dumps({"Polos": "3P", "Corriente": "1250A", "PoderCorte": "55 kA", "Disparador": "ETU300"}), "Protección de transformadores de 1000 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1116-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 1600A 55kA ETU300", "Interruptor abierto de potencia de 1600A", json.dumps({"Polos": "3P", "Corriente": "1600A", "PoderCorte": "55 kA", "Disparador": "ETU300"}), "Grandes plantas industriales y complejos comerciales"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1120-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 2000A 66kA ETU600", "Interruptor abierto de 2000A con unidad de control avanzada ETU600 y display", json.dumps({"Polos": "3P", "Corriente": "2000A", "PoderCorte": "66 kA", "Disparador": "ETU600 LSI con pantalla gráfica", "Comunicacion": "PROFINET / Modbus TCP"}), "Cabeceras de subestación con transformador de 1500 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1225-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 2500A 66kA ETU600", "Interruptor abierto de 2500A con 66kA de corte", json.dumps({"Polos": "3P", "Corriente": "2500A", "PoderCorte": "66 kA", "Disparador": "ETU600"}), "Complejos industriales, acerías y puertos"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1232-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 3200A 66kA ETU600", "Interruptor abierto de 3200A para distribución primaria", json.dumps({"Polos": "3P", "Corriente": "3200A", "PoderCorte": "66 kA", "Disparador": "ETU600"}), "Subestaciones de 2500 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1340-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 4000A 85kA ETU600", "Interruptor de gran bastidor de 4000A con 85kA", json.dumps({"Polos": "3P", "Corriente": "4000A", "PoderCorte": "85 kA", "Disparador": "ETU600"}), "Grandes centrales eléctricas y minería"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "SENTRON 3WA", "3WA1363-2AE01-0AA0", "Interruptor Abierto SENTRON 3WA1 3P 6300A 100kA ETU600", "Interruptor de máxima potencia de 6300A con 100kA de capacidad de ruptura", json.dumps({"Polos": "3P", "Corriente": "6300A", "PoderCorte": "100 kA", "Disparador": "ETU600 LSIG"}), "Subestaciones maestras y centrales de generación eléctrica")
    ])

    # =========================================================================
    # 2. LÍNEA: CONTROL Y MANIOBRA DE MOTORES (SIRIUS)
    # =========================================================================
    line_sirius = "Automatización de Procesos"

    # Contactores SIRIUS 3RT20 (Tamaños S00, S0, S2, S3)
    contactores_sirius = [
        # S00
        ("3RT2015-1AP01", "7A", "3.0 kW", "230V AC", "1NA"),
        ("3RT2016-1AP01", "9A", "4.0 kW", "230V AC", "1NA"),
        ("3RT2017-1AP01", "12A", "5.5 kW", "230V AC", "1NA"),
        ("3RT2018-1AP01", "16A", "7.5 kW", "230V AC", "1NA"),
        ("3RT2016-1AK61", "9A", "4.0 kW", "110V AC", "1NA"),
        ("3RT2017-1AK61", "12A", "5.5 kW", "110V AC", "1NA"),
        ("3RT2016-1BB41", "9A", "4.0 kW", "24V DC", "1NA"),
        ("3RT2017-1BB41", "12A", "5.5 kW", "24V DC", "1NA"),
        # S0
        ("3RT2024-1AP00", "12A", "5.5 kW", "230V AC", "1NA+1NC"),
        ("3RT2025-1AP00", "17A", "7.5 kW", "230V AC", "1NA+1NC"),
        ("3RT2026-1AP00", "25A", "11.0 kW", "230V AC", "1NA+1NC"),
        ("3RT2027-1AP00", "32A", "15.0 kW", "230V AC", "1NA+1NC"),
        ("3RT2028-1AP00", "38A", "18.5 kW", "230V AC", "1NA+1NC"),
        ("3RT2026-1AK60", "25A", "11.0 kW", "110V AC", "1NA+1NC"),
        ("3RT2027-1AK60", "32A", "15.0 kW", "110V AC", "1NA+1NC"),
        ("3RT2026-1BB40", "25A", "11.0 kW", "24V DC", "1NA+1NC"),
        ("3RT2027-1BB40", "32A", "15.0 kW", "24V DC", "1NA+1NC"),
        # S2
        ("3RT2035-1AP00", "40A", "18.5 kW", "230V AC", "1NA+1NC"),
        ("3RT2036-1AP00", "50A", "22.0 kW", "230V AC", "1NA+1NC"),
        ("3RT2037-1AP00", "65A", "30.0 kW", "230V AC", "1NA+1NC"),
        ("3RT2038-1AP00", "80A", "37.0 kW", "230V AC", "1NA+1NC"),
        # S3
        ("3RT2046-1AP00", "95A", "45.0 kW", "230V AC", "1NA+1NC"),
        ("3RT2047-1AP00", "110A", "55.0 kW", "230V AC", "1NA+1NC")
    ]
    for code, curr, kw, bobina, aux in contactores_sirius:
        tam = "S00" if "3RT201" in code else ("S0" if "3RT202" in code else ("S2" if "3RT203" in code else "S3"))
        items.append((
            brand, line_sirius, "Contactores de Potencia", "SIRIUS 3RT2", code,
            f"Contactor de Potencia SIRIUS 3RT20 {curr} {tam} Bobina {bobina}",
            f"Contactor tripolar electromagnético para mando de motores categoría AC-3 con contactos auxiliares integrados",
            json.dumps({"Tamaño": tam, "CorrienteAC3": curr, "PotenciaMotor": f"{kw} a 400V", "TensionBobina": bobina, "ContactosAuxiliares": aux, "VidaMecanica": "30 millones de maniobras"}),
            "Arranque directo y control de motores trifásicos, bombas, ventiladores y compresores"
        ))

    # Contactores de Gran Potencia SIRIUS 3RT10 (Tamaños S6 a S12 de 115A a 500A)
    contactores_sirius_potencia = [
        ("3RT1054-1AP36", "115A", "55 kW", "S6", "230V AC"),
        ("3RT1055-6AP36", "150A", "75 kW", "S6", "230V AC"),
        ("3RT1056-6AP36", "185A", "90 kW", "S6", "230V AC"),
        ("3RT1064-6AP36", "225A", "110 kW", "S10", "230V AC"),
        ("3RT1065-6AP36", "265A", "132 kW", "S10", "230V AC"),
        ("3RT1066-6AP36", "300A", "160 kW", "S10", "230V AC"),
        ("3RT1075-6AP36", "400A", "200 kW", "S12", "230V AC"),
        ("3RT1076-6AP36", "500A", "250 kW", "S12", "230V AC")
    ]
    for code, curr, kw, tam, bobina in contactores_sirius_potencia:
        items.append((
            brand, line_sirius, "Contactores de Gran Potencia", "SIRIUS 3RT1", code,
            f"Contactor Industrial SIRIUS 3RT10 {curr} Tamaño {tam} Bobina {bobina}",
            f"Contactor de potencia pesada con accionamiento asistido para motores de alta potencia",
            json.dumps({"Tamaño": tam, "CorrienteAC3": curr, "PotenciaMotor": f"{kw} a 400V", "Bobina": bobina, "Polos": "3P + 2NA + 2NC"}),
            "Arranque de grandes molinos, trituradoras, bombas de draga y compresores industriales"
        ))

    # Guardamotores SIRIUS 3RV20 (0.16A a 40A / 80A)
    guardamotores_sirius = [
        ("3RV2011-0AA10", "0.11 - 0.16 A", "S00", "0.04 kW"),
        ("3RV2011-0BA10", "0.14 - 0.20 A", "S00", "0.06 kW"),
        ("3RV2011-0CA10", "0.18 - 0.25 A", "S00", "0.06 kW"),
        ("3RV2011-0DA10", "0.22 - 0.32 A", "S00", "0.09 kW"),
        ("3RV2011-0EA10", "0.28 - 0.40 A", "S00", "0.09 kW"),
        ("3RV2011-0FA10", "0.35 - 0.50 A", "S00", "0.12 kW"),
        ("3RV2011-0GA10", "0.45 - 0.63 A", "S00", "0.18 kW"),
        ("3RV2011-0HA10", "0.55 - 0.80 A", "S00", "0.25 kW"),
        ("3RV2011-0JA10", "0.70 - 1.00 A", "S00", "0.25 kW"),
        ("3RV2011-0KA10", "0.90 - 1.25 A", "S00", "0.37 kW"),
        ("3RV2011-1AA10", "1.10 - 1.60 A", "S00", "0.55 kW"),
        ("3RV2011-1BA10", "1.40 - 2.00 A", "S00", "0.75 kW"),
        ("3RV2011-1CA10", "1.80 - 2.50 A", "S00", "0.75 kW"),
        ("3RV2011-1DA10", "2.20 - 3.20 A", "S00", "1.10 kW"),
        ("3RV2011-1EA10", "2.80 - 4.00 A", "S00", "1.50 kW"),
        ("3RV2011-1FA10", "3.50 - 5.00 A", "S00", "1.50 kW"),
        ("3RV2011-1GA10", "4.50 - 6.30 A", "S00", "2.20 kW"),
        ("3RV2011-1HA10", "5.50 - 8.00 A", "S00", "3.00 kW"),
        ("3RV2011-1JA10", "7.00 - 10.00 A", "S00", "4.00 kW"),
        ("3RV2011-1KA10", "9.00 - 12.50 A", "S00", "5.50 kW"),
        ("3RV2011-4AA10", "10.00 - 16.00 A", "S00", "7.50 kW"),
        ("3RV2021-4BA10", "13.00 - 20.00 A", "S0", "9.00 kW"),
        ("3RV2021-4CA10", "16.00 - 22.00 A", "S0", "11.00 kW"),
        ("3RV2021-4DA10", "18.00 - 25.00 A", "S0", "11.00 kW"),
        ("3RV2021-4EA10", "23.00 - 28.00 A", "S0", "15.00 kW"),
        ("3RV2021-4PA10", "30.00 - 36.00 A", "S0", "18.50 kW"),
        ("3RV2021-4FA10", "34.00 - 40.00 A", "S0", "18.50 kW"),
        ("3RV2031-4WA10", "36.00 - 45.00 A", "S2", "22.00 kW"),
        ("3RV2031-4XA10", "42.00 - 52.00 A", "S2", "22.00 kW"),
        ("3RV2031-4JA10", "54.00 - 65.00 A", "S2", "30.00 kW"),
        ("3RV2031-4KA10", "62.00 - 73.00 A", "S2", "37.00 kW"),
        ("3RV2031-4RA10", "70.00 - 80.00 A", "S2", "37.00 kW")
    ]
    for code, rango, tam, kw in guardamotores_sirius:
        items.append((
            brand, line_sirius, "Guardamotores Magnetotérmicos", "SIRIUS 3RV2", code,
            f"Guardamotor Magnetotérmico SIRIUS 3RV20 {rango} Tamaño {tam}",
            f"Disyuntor protector de motor con disparador térmico y magnético de clase 10 para protección completa de motor",
            json.dumps({"Tamaño": tam, "RangoAjuste": rango, "PotenciaMotor": f"Hasta {kw} a 400V", "Accionamiento": "Maneta Rotativa", "CapacidadCorte": "Hasta 100 kA", "Montaje": "Riel DIN 35mm"}),
            "Protección contra cortocircuito, sobrecarga y asimetría de fases en motores eléctricos industriales"
        ))

    # Relés Térmicos de Sobrecarga SIRIUS 3RU21 y Accesorios
    reles_sirius = [
        ("3RU2116-0AB0", "0.11 - 0.16 A", "S00"),
        ("3RU2116-0BB0", "0.14 - 0.20 A", "S00"),
        ("3RU2116-0CB0", "0.18 - 0.25 A", "S00"),
        ("3RU2116-0DB0", "0.22 - 0.32 A", "S00"),
        ("3RU2116-0EB0", "0.28 - 0.40 A", "S00"),
        ("3RU2116-0FB0", "0.35 - 0.50 A", "S00"),
        ("3RU2116-0GB0", "0.45 - 0.63 A", "S00"),
        ("3RU2116-0HB0", "0.55 - 0.80 A", "S00"),
        ("3RU2116-0JB0", "0.70 - 1.00 A", "S00"),
        ("3RU2116-0KB0", "0.90 - 1.25 A", "S00"),
        ("3RU2116-1AB0", "1.10 - 1.60 A", "S00"),
        ("3RU2116-1BB0", "1.40 - 2.00 A", "S00"),
        ("3RU2116-1CB0", "1.80 - 2.50 A", "S00"),
        ("3RU2116-1DB0", "2.20 - 3.20 A", "S00"),
        ("3RU2116-1EB0", "2.80 - 4.00 A", "S00"),
        ("3RU2116-1FB0", "3.50 - 5.00 A", "S00"),
        ("3RU2116-1GB0", "4.50 - 6.30 A", "S00"),
        ("3RU2116-1HB0", "5.50 - 8.00 A", "S00"),
        ("3RU2116-1JB0", "7.00 - 10.00 A", "S00"),
        ("3RU2116-1KB0", "9.00 - 12.50 A", "S00"),
        ("3RU2116-4AB0", "11.00 - 16.00 A", "S00"),
        ("3RU2126-4BB0", "14.00 - 20.00 A", "S0"),
        ("3RU2126-4CB0", "17.00 - 22.00 A", "S0"),
        ("3RU2126-4DB0", "20.00 - 25.00 A", "S0"),
        ("3RU2126-4EB0", "27.00 - 32.00 A", "S0"),
        ("3RU2126-4FB0", "34.00 - 40.00 A", "S0")
    ]
    for code, rango, tam in reles_sirius:
        items.append((
            brand, line_sirius, "Relés Térmicos de Sobrecarga", "SIRIUS 3RU2", code,
            f"Relé Térmico Diferencial SIRIUS 3RU21 {rango} Tamaño {tam}",
            f"Relé térmico bimetálico para montaje directo bajo contactor 3RT20",
            json.dumps({"Tamaño": tam, "RangoAjuste": rango, "ContactosAuxiliares": "1NA + 1NC", "ClaseDisparo": "Clase 10", "Rearme": "Manual / Automático"}),
            "Protección contra sobrecarga prolongada y desequilibrio de fase en motores"
        ))

    items.extend([
        (brand, line_sirius, "Bloques Auxiliares", "SIRIUS 3RH29", "3RH2911-1HA11", "Bloque Auxiliar SIRIUS 1NA + 1NC Frontal", "Bloque auxiliar a presión frontal para contactores 3RT2", json.dumps({"Contactos": "1 NA + 1 NC", "Montaje": "Frontal"}), "Señalización y enclavamientos"),
        (brand, line_sirius, "Bloques Auxiliares", "SIRIUS 3RH29", "3RH2911-1HA22", "Bloque Auxiliar SIRIUS 2NA + 2NC Frontal", "Bloque auxiliar frontal de 4 contactos para contactores 3RT2", json.dumps({"Contactos": "2 NA + 2 NC"}), "Cuadros de control automático"),
        (brand, line_sirius, "Bloques Auxiliares", "SIRIUS 3RH29", "3RH2921-1DA11", "Bloque Auxiliar SIRIUS 1NA + 1NC Lateral", "Bloque auxiliar de montaje lateral para contactores 3RT202", json.dumps({"Contactos": "1 NA + 1 NC", "Montaje": "Lateral"}), "Ahorro de profundidad en tableros"),
        (brand, line_sirius, "Enclavamientos de Inversor", "SIRIUS 3RA29", "3RA2922-2H", "Kit Enclavamiento Mecánico Inversor S0", "Kit de interbloqueo mecánico para montar inversor de giro con 2 contactores 3RT202", json.dumps({"Tamaño": "S0"}), "Arrancadores inversores de giro de motores")
    ])

    # Arrancadores Suaves SIRIUS 3RW30, 3RW40 y 3RW52
    arrancadores_sirius = [
        # 3RW30
        ("3RW3013-1BB14", "3.6A", "1.5 kW", "3RW30", "S00"),
        ("3RW3014-1BB14", "6.5A", "3.0 kW", "3RW30", "S00"),
        ("3RW3016-1BB14", "9.0A", "4.0 kW", "3RW30", "S00"),
        ("3RW3017-1BB14", "12.5A", "5.5 kW", "3RW30", "S00"),
        ("3RW3026-1BB14", "25.0A", "11.0 kW", "3RW30", "S0"),
        ("3RW3027-1BB14", "32.0A", "15.0 kW", "3RW30", "S0"),
        ("3RW3028-1BB14", "38.0A", "18.5 kW", "3RW30", "S0"),
        # 3RW40
        ("3RW4026-1BB14", "25.0A", "11.0 kW", "3RW40", "S0"),
        ("3RW4027-1BB14", "32.0A", "15.0 kW", "3RW40", "S0"),
        ("3RW4028-1BB14", "38.0A", "18.5 kW", "3RW40", "S0"),
        ("3RW4036-1BB14", "45.0A", "22.0 kW", "3RW40", "S2"),
        ("3RW4037-1BB14", "63.0A", "30.0 kW", "3RW40", "S2"),
        ("3RW4038-1BB14", "72.0A", "37.0 kW", "3RW40", "S2"),
        ("3RW4046-1BB14", "80.0A", "45.0 kW", "3RW40", "S3"),
        ("3RW4047-1BB14", "106.0A", "55.0 kW", "3RW40", "S3"),
        # 3RW52
        ("3RW5214-1TC14", "18.0A", "7.5 kW", "3RW52", "S00"),
        ("3RW5215-1TC14", "25.0A", "11.0 kW", "3RW52", "S00"),
        ("3RW5216-1TC14", "32.0A", "15.0 kW", "3RW52", "S00"),
        ("3RW5224-1TC14", "47.0A", "22.0 kW", "3RW52", "S0"),
        ("3RW5225-1TC14", "63.0A", "30.0 kW", "3RW52", "S0"),
        ("3RW5226-1TC14", "77.0A", "37.0 kW", "3RW52", "S0"),
        ("3RW5227-1TC14", "93.0A", "45.0 kW", "3RW52", "S0"),
        ("3RW5234-1TC14", "113.0A", "55.0 kW", "3RW52", "S2"),
        ("3RW5235-1TC14", "143.0A", "75.0 kW", "3RW52", "S2"),
        ("3RW5236-1TC14", "171.0A", "90.0 kW", "3RW52", "S2"),
        ("3RW5244-1TC14", "210.0A", "110.0 kW", "3RW52", "S3")
    ]
    for code, curr, kw, serie, tam in arrancadores_sirius:
        items.append((
            brand, line_sirius, "Arrancadores Suaves", f"SIRIUS {serie}", code,
            f"Arrancador Suave SIRIUS {serie} {curr} {kw} a 400V Tamaño {tam}",
            f"Arrancador progresivo electrónico con bypass de contactor integrado para arranque y parada suave de motores trifásicos",
            json.dumps({"Serie": serie, "Corriente": curr, "PotenciaMotor": f"{kw} a 400V", "Tension": "200-480V AC", "Bypass": "Integrado", "Control": "Control de rampa y limitación de corriente"}),
            "Reducción de picos de arranque y protección mecánica en bombas, cintas transportadoras, compresores y ventiladores"
        ))

    # =========================================================================
    # 3. LÍNEA: VARIADORES DE VELOCIDAD (SINAMICS)
    # =========================================================================
    line_drives = "Drives"

    # SINAMICS V20 Monofásicos 200-240V
    v20_mono = [
        ("6SL3210-5BB11-2UV1", "0.12 kW / 0.16 HP", "0.9A"),
        ("6SL3210-5BB12-5UV1", "0.25 kW / 0.33 HP", "1.7A"),
        ("6SL3210-5BB13-7UV1", "0.37 kW / 0.5 HP", "2.3A"),
        ("6SL3210-5BB17-5UV1", "0.75 kW / 1.0 HP", "4.2A"),
        ("6SL3210-5BB21-5UV1", "1.5 kW / 2.0 HP", "7.8A"),
        ("6SL3210-5BB22-2UV1", "2.2 kW / 3.0 HP", "11.0A"),
        ("6SL3210-5BB23-0UV1", "3.0 kW / 4.0 HP", "13.6A")
    ]
    for code, hp, curr in v20_mono:
        items.append((
            brand, line_drives, "Variadores de Velocidad", "SINAMICS V20", code,
            f"Variador de Frecuencia SINAMICS V20 {hp} 200-240V Monofásico",
            f"Convertidor de frecuencia compacto para motores trifásicos alimentado con 220V monofásica",
            json.dumps({"Potencia": hp, "Entrada": "Monofásica 200-240V AC", "Salida": "Trifásica 0-240V", "Corriente": curr, "Comunicacion": "Modbus RTU / USS integrado", "Montaje": "Pared o Riel DIN"}),
            "Bombas centrífugas pequeñas, agitadores, extractores y cintas transportadoras"
        ))

    # SINAMICS V20 Trifásicos 380-480V
    v20_tri = [
        ("6SL3210-5BE13-7UV0", "0.37 kW / 0.5 HP", "1.3A"),
        ("6SL3210-5BE17-5UV0", "0.75 kW / 1.0 HP", "2.2A"),
        ("6SL3210-5BE21-5UV0", "1.5 kW / 2.0 HP", "4.1A"),
        ("6SL3210-5BE22-2UV0", "2.2 kW / 3.0 HP", "5.6A"),
        ("6SL3210-5BE23-0UV0", "3.0 kW / 4.0 HP", "7.3A"),
        ("6SL3210-5BE24-0UV0", "4.0 kW / 5.5 HP", "8.8A"),
        ("6SL3210-5BE25-5UV0", "5.5 kW / 7.5 HP", "12.5A"),
        ("6SL3210-5BE31-1UV0", "7.5 kW / 10.0 HP", "16.5A"),
        ("6SL3210-5BE31-5UV0", "11.0 kW / 15.0 HP", "25.0A"),
        ("6SL3210-5BE31-8UV0", "15.0 kW / 20.0 HP", "31.0A")
    ]
    for code, hp, curr in v20_tri:
        items.append((
            brand, line_drives, "Variadores de Velocidad", "SINAMICS V20", code,
            f"Variador de Frecuencia SINAMICS V20 {hp} 380-480V Trifásico",
            f"Variador robusto industrial con alta resistencia al calor y polvo gracias a su diseño de refrigeración avanzada",
            json.dumps({"Potencia": hp, "Entrada": "Trifásica 380-480V AC", "Corriente": curr, "Control": "V/f y FCC (Control de Corriente de Flujo)", "Sobrecarga": "150% durante 60s"}),
            "Industria manufacturera, plantas procesadoras de alimentos, bombeo e impulsión"
        ))

    # SINAMICS G120X (Especializado en Bombeo, Agua y Climatización)
    g120x_models = [
        ("6SL3220-1YE18-0UF0", "3.0 kW / 4.0 HP", "7.7A"),
        ("6SL3220-1YE20-0UF0", "4.0 kW / 5.5 HP", "10.2A"),
        ("6SL3220-1YE22-0UF0", "5.5 kW / 7.5 HP", "13.2A"),
        ("6SL3220-1YE24-0UF0", "7.5 kW / 10.0 HP", "18.0A"),
        ("6SL3220-1YE26-0UF0", "11.0 kW / 15.0 HP", "26.0A"),
        ("6SL3220-1YE28-0UF0", "15.0 kW / 20.0 HP", "32.0A"),
        ("6SL3220-1YE30-0UF0", "18.5 kW / 25.0 HP", "38.0A"),
        ("6SL3220-1YE32-0UF0", "22.0 kW / 30.0 HP", "45.0A"),
        ("6SL3220-1YE34-0UF0", "30.0 kW / 40.0 HP", "60.0A"),
        ("6SL3220-1YE36-0UF0", "37.0 kW / 50.0 HP", "75.0A"),
        ("6SL3220-1YE38-0UF0", "45.0 kW / 60.0 HP", "90.0A"),
        ("6SL3220-1YE40-0UF0", "55.0 kW / 75.0 HP", "110.0A"),
        ("6SL3220-1YE42-0UF0", "75.0 kW / 100.0 HP", "145.0A")
    ]
    for code, hp, curr in g120x_models:
        items.append((
            brand, line_drives, "Variadores de Infraestructura", "SINAMICS G120X", code,
            f"Variador para Bombeo y HVAC SINAMICS G120X {hp} 380-480V",
            f"Convertidor de frecuencia de alto rendimiento diseñado específicamente para agua, tratamiento residual y sistemas HVAC con PROFINET / Modbus",
            json.dumps({"Potencia": hp, "Tension": "380-480V Trifásico", "Corriente": curr, "Funciones": "Detección de cavitación, limpieza de bomba, llenado suave de tuberías", "Proteccion": "IP20 / Barnizado 3C3"}),
            "Plantas potabilizadoras, estaciones de bombeo de agua limpia, piscinas camaroneras e impulsión de aguas residuales"
        ))

    # SINAMICS G120C (Compactos Industriales con PROFINET / Safety STO)
    g120c_models = [
        ("6SL3210-1KE13-2AF2", "1.1 kW / 1.5 HP", "3.1A"),
        ("6SL3210-1KE15-8AF2", "2.2 kW / 3.0 HP", "5.6A"),
        ("6SL3210-1KE18-8AF2", "4.0 kW / 5.5 HP", "8.8A"),
        ("6SL3210-1KE21-7AF2", "7.5 kW / 10.0 HP", "16.5A"),
        ("6SL3210-1KE23-2AF2", "15.0 kW / 20.0 HP", "31.0A")
    ]
    for code, hp, curr in g120c_models:
        items.append((
            brand, line_drives, "Variadores de Automatización", "SINAMICS G120C", code,
            f"Variador Compacto SINAMICS G120C {hp} con PROFINET y Seguridad STO",
            f"Variador vectorial industrial de alta respuesta dinámica integrado en TIA Portal con función de parada segura Safe Torque Off (STO)",
            json.dumps({"Potencia": hp, "Tension": "380-480V Trifásico", "Corriente": curr, "Comunicacion": "PROFINET integrado (2 puertos)", "Seguridad": "STO SIL 2 / PL d"}),
            "Máquinas automáticas, envolvedoras, mezcladoras, líneas de ensamble y transporte de precisión"
        ))

    # =========================================================================
    # 4. LÍNEA: CONTROLADORES PROGRAMABLES (PLCS) Y PANTALLAS HMI (SIMATIC)
    # =========================================================================
    line_simatic = "Controladores y HMI"

    # Módulos Lógicos Inteligentes LOGO! 8
    items.extend([
        (brand, line_simatic, "Módulos Lógicos (Smart Relays)", "SIMATIC LOGO!", "6ED1052-1MD08-0BA1", "Módulo Lógico Inteligente LOGO! 12/24RCE con Pantalla y Ethernet", "Mini PLC programable con 8 entradas digitales (4 utilizables como analógicas 0-10V) y 4 salidas a relé de 10A con web server integrado", json.dumps({"Alimentacion": "12/24V DC", "Entradas": "8 ED (4 EA 0-10V)", "Salidas": "4 a relé 10A", "Comunicacion": "Ethernet RJ45 Modbus TCP", "Pantalla": "Display con retroiluminación configurable"}), "Control de bombeo alternado, iluminación de edificios, portones y automatismos pequeños"),
        (brand, line_simatic, "Módulos Lógicos (Smart Relays)", "SIMATIC LOGO!", "6ED1052-1FB08-0BA1", "Módulo Lógico Inteligente LOGO! 230RCE 115-230V AC/DC con Ethernet", "Controlador con alimentación directa a 115-230V AC sin necesidad de fuente externa", json.dumps({"Alimentacion": "115-230V AC/DC", "Entradas": "8 digitales AC", "Salidas": "4 a relé", "Ethernet": "RJ45 con Web Server"}), "Automatismos donde no se cuenta con fuente de 24VDC"),
        (brand, line_simatic, "Módulos Lógicos (Smart Relays)", "SIMATIC LOGO!", "6ED1052-1CC08-0BA1", "Módulo Lógico Inteligente LOGO! 24CE Salidas Transistor", "Controlador con salidas a transistor para alta frecuencia de conmutación", json.dumps({"Alimentacion": "24V DC", "Salidas": "4 a transistor 0.3A", "Entradas": "8 (4 analógicas)"}), "Control de actuadores rápidos y señalización"),
        (brand, line_simatic, "Módulos de Expansión LOGO!", "SIMATIC LOGO!", "6ED1055-1MB00-0BA2", "Módulo de Expansión Digital LOGO! DM8 12/24R", "Módulo de ampliación de 4 entradas digitales y 4 salidas a relé a 24V", json.dumps({"Entradas": "4 ED", "Salidas": "4 a relé 5A", "Alimentacion": "12/24V DC"}), "Ampliación de capacidad en proyectos LOGO!"),
        (brand, line_simatic, "Módulos de Expansión LOGO!", "SIMATIC LOGO!", "6ED1055-1FB00-0BA2", "Módulo de Expansión Digital LOGO! DM8 230R", "Módulo de ampliación de 4 entradas y 4 salidas relé a 230V AC", json.dumps({"Entradas": "4 ED AC", "Salidas": "4 a relé", "Alimentacion": "115-230V AC"}), "Ampliación en tableros de iluminación y climatización"),
        (brand, line_simatic, "Módulos de Expansión LOGO!", "SIMATIC LOGO!", "6ED1055-1MA00-0BA2", "Módulo de Expansión Analógica LOGO! AM2 2 Entradas", "Módulo para lectura de señales de instrumentación analógica", json.dumps({"Entradas": "2 entradas analógicas (0-10V o 0/4-20mA)", "Resolucion": "10 bits"}), "Lectura de transmisores de presión, nivel y temperatura"),
        (brand, line_simatic, "Módulos de Expansión LOGO!", "SIMATIC LOGO!", "6ED1055-1MM00-0BA2", "Módulo de Expansión Analógica LOGO! AM2 AQ 2 Salidas", "Módulo de salidas analógicas para control proporcional", json.dumps({"Salidas": "2 salidas analógicas (0-10V o 0/4-20mA)", "Resolucion": "10 bits"}), "Control analógico de velocidad de variadores y válvulas modulantes"),
        (brand, line_simatic, "Pantallas de Texto LOGO!", "SIMATIC LOGO!", "6ED1055-4MH08-0BA1", "Pantalla de Texto Externa LOGO! TDE con Doble Ethernet", "Panel de operador para montaje en puerta de tablero IP65 con 6 líneas de texto", json.dumps({"Lineas": "6 líneas de 20 caracteres", "Puertos": "2 puertos Ethernet RJ45", "Teclas": "4 teclas de función"}), "Interfaz de operador para visualización y ajuste de consignas sin abrir el tablero")
    ])

    # Controladores Lógicos Programables SIMATIC S7-1200
    items.extend([
        (brand, line_simatic, "Controladores Lógicos (PLCs)", "SIMATIC S7-1200", "6ES7212-1BD40-0XB0", "PLC SIMATIC S7-1200 CPU 1212C AC/DC/Relé", "Controlador modular compacto programable en TIA Portal con puerto PROFINET", json.dumps({"Alimentacion": "120-230V AC", "Entradas": "8 ED 24V DC / 2 EA 0-10V", "Salidas": "6 a relé 2A", "Memoria": "75 KB de trabajo", "Comunicacion": "PROFINET RJ45"}), "Automatización de maquinaria estándar, empacadoras y control de procesos"),
        (brand, line_simatic, "Controladores Lógicos (PLCs)", "SIMATIC S7-1200", "6ES7214-1BG40-0XB0", "PLC SIMATIC S7-1200 CPU 1214C DC/DC/Relé", "El PLC industrial más utilizado en Ecuador con 14 entradas y 10 salidas a relé", json.dumps({"Alimentacion": "24V DC", "Entradas": "14 ED 24V DC / 2 EA 0-10V", "Salidas": "10 a relé 2A", "Memoria": "100 KB de trabajo", "Expansion": "Hasta 8 Signal Modules"}), "Automatización integral de líneas de producción, plantas embotelladoras y ensilaje"),
        (brand, line_simatic, "Controladores Lógicos (PLCs)", "SIMATIC S7-1200", "6ES7214-1AG40-0XB0", "PLC SIMATIC S7-1200 CPU 1214C DC/DC/DC Transistor", "PLC con salidas a transistor de alta velocidad aptas para tren de pulsos PTO/PWM", json.dumps({"Alimentacion": "24V DC", "Entradas": "14 ED 24V DC", "Salidas": "10 a transistor (hasta 100 kHz para control de servomotores y paso a paso)"}), "Control de movimiento, posicionamiento de ejes y etiquetadoras rápidas"),
        (brand, line_simatic, "Controladores Lógicos (PLCs)", "SIMATIC S7-1200", "6ES7215-1BG40-0XB0", "PLC SIMATIC S7-1200 CPU 1215C DC/DC/Relé Doble Ethernet", "PLC de alta gama con doble puerto PROFINET conmutado y 2 salidas analógicas integradas", json.dumps({"Alimentacion": "24V DC", "Entradas": "14 ED / 2 EA (0-10V)", "Salidas": "10 a relé / 2 SA (0-20mA)", "Puertos": "2 puertos PROFINET RJ45 integrados", "Memoria": "125 KB"}), "Sistemas con topología en anillo Ethernet, pantallas HMI y variadores de frecuencia"),
        (brand, line_simatic, "Módulos de Expansión S7-1200", "SIMATIC S7-1200", "6ES7221-1BF32-0XB0", "Módulo de Expansión Digital SM 1221 8 Entradas 24V DC", "Módulo de 8 entradas digitales discretas para S7-1200", json.dumps({"Entradas": "8 ED 24V DC"}), "Ampliación de pulsadores y sensores"),
        (brand, line_simatic, "Módulos de Expansión S7-1200", "SIMATIC S7-1200", "6ES7222-1HF32-0XB0", "Módulo de Expansión Digital SM 1222 8 Salidas a Relé 2A", "Módulo de 8 salidas de contacto seco a relé", json.dumps({"Salidas": "8 a relé 2A"}), "Mando de contactores y válvulas"),
        (brand, line_simatic, "Módulos de Expansión S7-1200", "SIMATIC S7-1200", "6ES7223-1PH32-0XB0", "Módulo de Expansión Digital SM 1223 16 Entradas / 16 Salidas Relé", "Módulo de alta densidad con 32 canales de control", json.dumps({"Entradas": "16 ED 24V DC", "Salidas": "16 a relé 2A"}), "Tableros de control con gran número de señales de campo"),
        (brand, line_simatic, "Módulos de Expansión S7-1200", "SIMATIC S7-1200", "6ES7231-4HD32-0XB0", "Módulo Analógico SM 1231 4 Entradas Analógicas 13 Bits", "Módulo de 4 entradas analógicas configurables para corriente o tensión", json.dumps({"Entradas": "4 EA (0-10V / ±10V / 0-20mA / 4-20mA)", "Resolucion": "13 bits"}), "Adquisición de datos de transmisores de presión, caudal y nivel"),
        (brand, line_simatic, "Módulos de Expansión S7-1200", "SIMATIC S7-1200", "6ES7232-4HD32-0XB0", "Módulo Analógico SM 1232 4 Salidas Analógicas", "Módulo de 4 canales de salida analógica", json.dumps({"Salidas": "4 SA (0-10V o 4-20mA)", "Resolucion": "14 bits"}), "Control modulante de válvulas y consignas de velocidad"),
        (brand, line_simatic, "Módulos de Expansión S7-1200", "SIMATIC S7-1200", "6ES7231-5PD32-0XB0", "Módulo de Temperatura RTD SM 1231 4 Canales Pt100", "Módulo de precisión para lectura directa de termorresistencias", json.dumps({"Canales": "4 entradas para Pt100, Pt1000, Ni100", "Resolucion": "15 bits + signo"}), "Control de temperatura en autoclaves, cuartos fríos y silos")
    ])

    # Pantallas Táctiles HMI SIMATIC Basic Panels (2nd Generation)
    items.extend([
        (brand, line_simatic, "Pantallas Táctiles HMI", "SIMATIC HMI", "6AV2123-2DB03-0AX0", "Pantalla Táctil SIMATIC HMI KTP400 Basic 4.3 Pulgadas", "Panel de operador táctil widescreen TFT de 65,000 colores con puerto PROFINET", json.dumps({"Tamaño": "4.3 Pulgadas Widescreen", "Resolución": "480 x 272", "Teclas": "4 teclas de función", "Interfaz": "PROFINET RJ45", "Software": "WinCC Basic (TIA Portal)"}), "Monitoreo compacto de máquinas individuales"),
        (brand, line_simatic, "Pantallas Táctiles HMI", "SIMATIC HMI", "6AV2123-2GB03-0AX0", "Pantalla Táctil SIMATIC HMI KTP700 Basic 7.0 Pulgadas", "El panel HMI industrial más vendido en Ecuador con pantalla táctil de 7 pulgadas a color", json.dumps({"Tamaño": "7.0 Pulgadas Widescreen", "Resolución": "800 x 480", "Teclas": "8 teclas de función", "Interfaz": "PROFINET RJ45", "Proteccion": "IP65 frontal"}), "Frentes de tablero de control de bombas, líneas de producción y máquinas de proceso"),
        (brand, line_simatic, "Pantallas Táctiles HMI", "SIMATIC HMI", "6AV2123-2JB03-0AX0", "Pantalla Táctil SIMATIC HMI KTP900 Basic 9.0 Pulgadas", "Panel de operador de formato intermedio de 9 pulgadas para supervisión gráfica detallada", json.dumps({"Tamaño": "9.0 Pulgadas", "Resolución": "800 x 480", "Teclas": "8 teclas", "Interfaz": "PROFINET"}), "Líneas de empaque y pupitres de mando con múltiples sinópticos"),
        (brand, line_simatic, "Pantallas Táctiles HMI", "SIMATIC HMI", "6AV2123-2MB03-0AX0", "Pantalla Táctil SIMATIC HMI KTP1200 Basic 12.0 Pulgadas", "Panel HMI de gran formato de 12 pulgadas para supervisión de plantas completas", json.dumps({"Tamaño": "12.0 Pulgadas", "Resolución": "1280 x 800 Widescreen", "Teclas": "10 teclas de función", "Interfaz": "PROFINET"}), "Salas de control de plantas de alimentos, tratamiento de agua y CCMs")
    ])

    # =========================================================================
    # 5. LÍNEA: FUENTES DE ALIMENTACIÓN INDUSTRIAL (SITOP)
    # =========================================================================
    line_sitop = "Fuentes de Alimentación"

    sitop_models = [
        ("6EP1331-5BA00", "24V DC 0.6A 15W", "PSU100C", "0.6A", "15W"),
        ("6EP1331-5BA10", "24V DC 1.3A 30W", "PSU100C", "1.3A", "30W"),
        ("6EP1332-5BA00", "24V DC 2.5A 60W", "PSU100C", "2.5A", "60W"),
        ("6EP1332-5BA10", "24V DC 4.0A 100W", "PSU100C", "4.0A", "100W"),
        ("6EP1333-1LB00", "24V DC 5.0A 120W", "SITOP Lite", "5.0A", "120W"),
        ("6EP1334-1LB00", "24V DC 10.0A 240W", "SITOP Lite", "10.0A", "240W"),
        ("6EP1336-1LB00", "24V DC 20.0A 480W", "SITOP Lite", "20.0A", "480W"),
        ("6EP1333-2BA20", "24V DC 5.0A 120W Smart", "SITOP Smart", "5.0A", "120W"),
        ("6EP1334-2BA20", "24V DC 10.0A 240W Smart", "SITOP Smart", "10.0A", "240W"),
        ("6EP3437-8SB00-0AY0", "24V DC 40.0A 960W Trifásica", "SITOP PSU8200", "40.0A", "960W")
    ]
    for code, desc, serie, curr, watts in sitop_models:
        items.append((
            brand, line_sitop, "Fuentes de Alimentación", f"SITOP {serie}", code,
            f"Fuente de Poder Regulada SITOP {serie} {desc} Riel DIN",
            f"Fuente de alimentación conmutada regulada de alta fiabilidad industrial con protección contra sobrecargas y cortocircuitos continuos",
            json.dumps({"Serie": serie, "TensionEntrada": "120-230V AC Monofásica (o 400V 3F para PSU8200)", "TensionSalida": "24V DC Regulada", "Corriente": curr, "Potencia": watts, "Montaje": "Riel DIN 35mm"}),
            "Alimentación fiable de PLCs S7-1200, pantallas HMI, módulos de E/S y sensores industriales"
        ))

    # =========================================================================
    # 6. LÍNEA: MEDICIÓN Y GESTIÓN ENERGÉTICA (SENTRON PAC)
    # =========================================================================
    line_medicion = "Medición y Calidad de Energía"

    items.extend([
        (brand, line_medicion, "Centrales de Medida Multímetro", "SENTRON PAC", "7KM2200-2EA30-1EA1", "Medidor de Energía Multifunción SENTRON PAC2200 Ethernet", "Central de medida compacta con pantalla LCD y puerto Modbus TCP integrado", json.dumps({"Clase": "Clase 1 (IEC 61557-12)", "Medición": "V, I, F, FP, kW, kVA, kWh", "Comunicacion": "Modbus TCP Ethernet RJ45 y servidor web", "Montaje": "Riel DIN"}), "Medición de consumo y reparto de costos en tableros secundarios de subdistribución"),
        (brand, line_medicion, "Centrales de Medida Multímetro", "SENTRON PAC", "7KM3133-0BA00-3AA0", "Medidor de Potencia y Energía SENTRON PAC3100 Modbus RTU", "Central de medida para montaje en puerta de tablero 96x96mm con RS485", json.dumps({"Tamaño": "96 x 96 mm", "Clase": "Clase 0.5", "Comunicacion": "Modbus RTU RS485 integrada", "Pantalla": "LCD gráfica iluminada"}), "Frente de tablero de acometidas industriales y CCM"),
        (brand, line_medicion, "Centrales de Medida Multímetro", "SENTRON PAC", "7KM3220-0BA01-1DA0", "Medidor de Redes Avanzado SENTRON PAC3200 PROFINET", "Analizador de redes de precisión para integración en TIA Portal", json.dumps({"Clase": "Clase 0.5S de alta precisión", "Comunicacion": "PROFINET / Modbus TCP", "Armónicos": "THD de tensión y corriente", "Tarifas": "Multitarifa"}), "Sistemas de gestión energética SCADA y cumplimiento de código de red"),
        (brand, line_medicion, "Centrales de Medida Multímetro", "SENTRON PAC", "7KM4212-0BA00-3AA0", "Analizador de Calidad de Energía SENTRON PAC4200", "Analizador de calidad de suministro eléctrico con memoria de eventos de perturbación", json.dumps({"Clase": "Clase 0.2", "Armónicos": "Hasta orden 64", "Memoria": "Registro histórico y oscilografía", "Comunicacion": "Doble Ethernet"}), "Subestaciones maestras, hospitales y salas de cómputo críticas"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "SENTRON 4NC", "4NC5112-2CB21", "Transformador de Corriente TC SENTRON 100/5A Diámetro 21mm", "Transformador de medida toroidal para cable hasta 100A", json.dumps({"Relacion": "100/5A", "Ventana": "21mm", "Clase": "Clase 1"}), "Medición de alimentadores de 100A"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "SENTRON 4NC", "4NC5115-2CB21", "Transformador de Corriente TC SENTRON 200/5A Diámetro 21mm", "Transformador de corriente para cable hasta 200A", json.dumps({"Relacion": "200/5A", "Ventana": "21mm", "Clase": "Clase 0.5"}), "Medición en tableros de bombas"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "SENTRON 4NC", "4NC5223-2CE21", "Transformador de Corriente TC SENTRON 400/5A Barra 30x10mm", "Transformador para barra plana de 400A", json.dumps({"Relacion": "400/5A", "VentanaBarra": "30x10mm", "Clase": "Clase 0.5"}), "Salidas de interruptores 3VA de 400A"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "SENTRON 4NC", "4NC5327-2CH21", "Transformador de Corriente TC SENTRON 800/5A Barra 50x12mm", "Transformador para barras de 800A", json.dumps({"Relacion": "800/5A", "VentanaBarra": "50x12mm", "Clase": "Clase 0.5"}), "Acometidas principales de transformadores de 500 kVA"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "SENTRON 4NC", "4NC5431-2CH21", "Transformador de Corriente TC SENTRON 1000/5A Barra 60x12mm", "Transformador de corriente para barras de 1000A", json.dumps({"Relacion": "1000/5A", "VentanaBarra": "60x12mm", "Clase": "Clase 0.5"}), "Medición de subestaciones de 750 kVA"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "SENTRON 4NC", "4NC5435-2CH21", "Transformador de Corriente TC SENTRON 1600/5A Barra 80x12mm", "Transformador para barras de 1600A", json.dumps({"Relacion": "1600/5A", "VentanaBarra": "80x12mm", "Clase": "Clase 0.5"}), "Medición de transformadores de 1000 a 1250 kVA")
    ])

    # =========================================================================
    # 7. LÍNEA: MANDO Y SEÑALIZACIÓN (SIRIUS ACT Ø22mm)
    # =========================================================================
    line_mando = "Unidades de Mando y Señalización"

    # SIRIUS ACT Metálicos 3SU1 (IP69K de máxima resistencia)
    items.extend([
        (brand, line_mando, "Pulsadores Metálicos", "SIRIUS ACT", "3SU1150-0AB10-1BA0", "Pulsador Metálico Rasante Negro 1NA Ø22mm", "Pulsador metálico cromado brillante con grado de protección IP69K", json.dumps({"Diametro": "22mm", "Color": "Negro", "Contactos": "1 NA", "Proteccion": "IP69K resistente a lavado a alta presión"}), "Pupitres de mando y tableros industriales"),
        (brand, line_mando, "Pulsadores Metálicos", "SIRIUS ACT", "3SU1150-0AB40-1BA0", "Pulsador Metálico Rasante Verde 1NA Ø22mm (Marcha)", "Pulsador verde para orden de encendido y marcha", json.dumps({"Diametro": "22mm", "Color": "Verde", "Contactos": "1 NA", "Proteccion": "IP69K"}), "Arranque de motores y maquinaria"),
        (brand, line_mando, "Pulsadores Metálicos", "SIRIUS ACT", "3SU1150-0AB20-1CA0", "Pulsador Metálico Rasante Rojo 1NC Ø22mm (Parada)", "Pulsador rojo con contacto normalmente cerrado para paro de ciclo", json.dumps({"Diametro": "22mm", "Color": "Rojo", "Contactos": "1 NC", "Proteccion": "IP69K"}), "Parada operativa de máquinas"),
        (brand, line_mando, "Selectores Metálicos", "SIRIUS ACT", "3SU1150-2BF60-1BA0", "Selector Metálico 2 Posiciones Fijas 1NA Ø22mm", "Interruptor selector con maneta corta negra de 2 posiciones a 90°", json.dumps({"Diametro": "22mm", "Posiciones": "2 fijas", "Contactos": "1 NA"}), "Conmutación de modo Manual / Automático"),
        (brand, line_mando, "Selectores Metálicos", "SIRIUS ACT", "3SU1150-2BL60-1NA0", "Selector Metálico 3 Posiciones Fijas 2NA Ø22mm", "Selector de 3 posiciones fijas (I - O - II) con 2 contactos normalmente abiertos", json.dumps({"Diametro": "22mm", "Posiciones": "3 fijas", "Contactos": "2 NA"}), "Alternancia de bombas y selección de velocidad"),
        (brand, line_mando, "Paradas de Emergencia", "SIRIUS ACT", "3SU1150-1HB20-1CG0", "Parada de Emergencia Seta 40mm Desenganche Giro 1NC Metálica", "Pulsador de seguridad tipo hongo con apertura positiva según ISO 13850", json.dumps({"Diametro": "Seta 40mm / Montaje 22mm", "Color": "Rojo", "Contactos": "1 NC apertura positiva", "Norma": "ISO 13850 / EN 60947-5-5"}), "Parada de emergencia en maquinaria y transportadores"),
        (brand, line_mando, "Pilotos Luminosos LED", "SIRIUS ACT", "3SU1152-6AA40-1AA0", "Piloto LED Metálico Verde 24V AC/DC Ø22mm", "Indicador luminoso LED verde de alta brillantez para 24V", json.dumps({"Color": "Verde", "Tension": "24V AC/DC", "Proteccion": "IP69K"}), "Indicación de marcha o estado OK"),
        (brand, line_mando, "Pilotos Luminosos LED", "SIRIUS ACT", "3SU1152-6AA20-1AA0", "Piloto LED Metálico Rojo 24V AC/DC Ø22mm", "Indicador luminoso LED rojo para 24V", json.dumps({"Color": "Rojo", "Tension": "24V AC/DC"}), "Alarma o fallo térmico"),
        (brand, line_mando, "Pilotos Luminosos LED", "SIRIUS ACT", "3SU1156-6AA40-1AA0", "Piloto LED Metálico Verde 230V AC Ø22mm", "Piloto luminoso LED para conexión directa a red 230VAC", json.dumps({"Color": "Verde", "Tension": "230V AC"}), "Presencia de red en tableros"),
        (brand, line_mando, "Pilotos Luminosos LED", "SIRIUS ACT", "3SU1156-6AA20-1AA0", "Piloto LED Metálico Rojo 230V AC Ø22mm", "Piloto luminoso LED rojo para red 230VAC", json.dumps({"Color": "Rojo", "Tension": "230V AC"}), "Alarma general de cuadro eléctrico"),
        (brand, line_mando, "Cajas Botoneras", "SIRIUS ACT", "3SU1801-0AA00-0AA2", "Caja Botonera Vacía 1 Taladro Gris/Negro Ø22mm", "Caja de plástico reforzado para 1 unidad de mando IP66/IP69K", json.dumps({"Taladros": "1 taladro 22mm", "Material": "Plástico resistente a rayos UV", "Proteccion": "IP69K"}), "Puestos de mando locales y pulsadores de marcha"),
        (brand, line_mando, "Cajas Botoneras", "SIRIUS ACT", "3SU1802-0AA00-0AA2", "Caja Botonera Vacía 2 Taladros Gris/Negro Ø22mm", "Caja para 2 elementos de mando (Marcha/Paro)", json.dumps({"Taladros": "2 taladros 22mm", "Proteccion": "IP69K"}), "Estaciones locales Marcha-Paro de motores"),
        (brand, line_mando, "Cajas Botoneras", "SIRIUS ACT", "3SU1801-0NA00-2AA2", "Estación de Parada de Emergencia Completa Amarilla", "Caja amarilla de seguridad completa con pulsador tipo seta y contacto 1NC", json.dumps({"Color": "Amarillo seguridad", "Seta": "40mm con enclavamiento", "Contactos": "1 NC", "Norma": "ISO 13850"}), "Dispositivo de parada de emergencia en líneas de envasado y fábricas")
    ])

    # =========================================================================
    # 8. LÍNEA: RELÉS DE TIEMPO Y VIGILANCIA (SIRIUS 3RP / 3UG)
    # =========================================================================
    line_reles = "Relés de Control"

    items.extend([
        (brand, line_reles, "Relés Temporizadores", "SIRIUS 3RP", "3RP2505-1AW30", "Temporizador Electrónico Multifunción SIRIUS 12-240V AC/DC 1 C/O", "Relé de tiempo multifunción con 27 funciones (retardo a la conexión, desconexión, intermitencia, pulso) y rango de tiempo desde 0.05 segundos hasta 100 horas", json.dumps({"Tension": "12-240V AC/DC Universal", "Contacto": "1 C/O (conmutado 3A)", "RangoTiempo": "0.05s a 100h en 7 rangos", "Montaje": "Riel DIN 35mm"}), "Secuencias de arranque de motores estrella-triángulo, bombas, luces y ventilación"),
        (brand, line_reles, "Relés Temporizadores", "SIRIUS 3RP", "3RP2505-1BW30", "Temporizador Electrónico Multifunción SIRIUS 12-240V AC/DC 2 C/O", "Temporizador multifunción con 2 contactos conmutados independientes", json.dumps({"Tension": "12-240V AC/DC", "Contactos": "2 C/O"}), "Maniobras conmutadas dobles"),
        (brand, line_reles, "Relés de Vigilancia de Red", "SIRIUS 3UG", "3UG4614-1BR20", "Relé de Vigilancia de Red Trifásica SIRIUS 160-690V AC", "Relé de supervisión multifuncional con pantalla LCD digital para subtensión, sobretensión, asimetría de fases y fallo de neutro", json.dumps({"Tension": "160 a 690V AC Trifásico", "Salidas": "2 C/O", "Display": "LCD digital para lectura en tiempo real", "Ajuste": "Tiempo de retardo de disparo configurable"}), "Protección avanzada de motores y compresores contra mala calidad del suministro eléctrico"),
        (brand, line_reles, "Relés de Vigilancia de Red", "SIRIUS 3UG", "3UG4511-1AP20", "Relé de Control de Fases y Secuencia SIRIUS 160-690V AC", "Relé analógico compacto para detección de secuencia correcta de giro y caída de fase", json.dumps({"Tension": "160 a 690V AC", "Salida": "1 C/O (conmutado)", "Deteccion": "Fallo de fase y orden de fases"}), "Evita el giro inverso en bombas, ascensores y compresores"),
        (brand, line_reles, "Relés de Protección Térmica", "SIRIUS 3RN", "3RN2000-1AA30", "Relé de Termistor PTC para Protección de Motor 24-240V AC/DC", "Dispositivo de vigilancia de temperatura mediante sondas PTC embebidas en los bobinados del motor", json.dumps({"Alimentacion": "24-240V AC/DC", "Sondas": "Sensores PTC", "Salida": "1 C/O"}), "Protección térmica absoluta contra sobrecalentamiento en motores sumergibles y servicio pesado")
    ])

    return items

def populate_database():
    items = get_siemens_catalog_data()
    print(f"Total de productos preparados para Siemens: {len(items)}")

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

        cur.execute("SELECT COUNT(1) FROM ProductsCatalog WHERE Brand = 'Siemens';")
        count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(1) FROM Products_FTS;")
        fts_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT Brand) FROM ProductsCatalog;")
        brands_count = cur.fetchone()[0]
        print(f"-> Productos Siemens en ProductsCatalog: {count}")
        print(f"-> Total productos indexados en Products_FTS: {fts_count}")
        print(f"-> Marcas activas en catálogo: {brands_count}")

        conn.close()

if __name__ == "__main__":
    populate_database()
