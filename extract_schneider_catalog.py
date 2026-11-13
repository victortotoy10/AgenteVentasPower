import os
import sqlite3
import json

def get_db_paths():
    paths = [
        os.path.abspath("AgentePower/agente_ventas.db"),
        os.path.abspath("AgentePower/bin/Debug/net8.0/agente_ventas.db"),
        os.path.abspath("agente_ventas.db")
    ]
    return [p for p in paths if os.path.exists(os.path.dirname(p))]

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("PRAGMA synchronous = NORMAL;")
    cur.execute("PRAGMA cache_size = -64000;")
    cur.execute("PRAGMA temp_store = MEMORY;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS ProductsCatalog (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Brand TEXT NOT NULL,
            BusinessLine TEXT NOT NULL,
            Family TEXT NOT NULL,
            Series TEXT,
            Code TEXT NOT NULL UNIQUE,
            Name TEXT NOT NULL,
            Description TEXT,
            TechnicalSpecs TEXT,
            Application TEXT,
            Status TEXT DEFAULT 'Disponible',
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_brand ON ProductsCatalog (Brand);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_line ON ProductsCatalog (BusinessLine);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_series ON ProductsCatalog (Series);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_products_code ON ProductsCatalog (Code);")

    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS Products_FTS USING fts5(
            Code,
            Name,
            Brand,
            BusinessLine,
            Family,
            Series,
            Description,
            TechnicalSpecs,
            Application,
            content='ProductsCatalog',
            content_rowid='Id'
        );
    """)

    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_products_insert AFTER INSERT ON ProductsCatalog BEGIN
            INSERT INTO Products_FTS (rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
            VALUES (new.Id, new.Code, new.Name, new.Brand, new.BusinessLine, new.Family, new.Series, new.Description, new.TechnicalSpecs, new.Application);
        END;
    """)

    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_products_delete AFTER DELETE ON ProductsCatalog BEGIN
            INSERT INTO Products_FTS (Products_FTS, rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
            VALUES ('delete', old.Id, old.Code, old.Name, old.Brand, old.BusinessLine, old.Family, old.Series, old.Description, old.TechnicalSpecs, old.Application);
        END;
    """)

    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_products_update AFTER UPDATE ON ProductsCatalog BEGIN
            INSERT INTO Products_FTS (Products_FTS, rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
            VALUES ('delete', old.Id, old.Code, old.Name, old.Brand, old.BusinessLine, old.Family, old.Series, old.Description, old.TechnicalSpecs, old.Application);
            INSERT INTO Products_FTS (rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
            VALUES (new.Id, new.Code, new.Name, new.Brand, new.BusinessLine, new.Family, new.Series, new.Description, new.TechnicalSpecs, new.Application);
        END;
    """)

    conn.commit()
    return conn

def get_schneider_catalog_data():
    brand = "Schneider Electric"
    items = []

    # =========================================================================
    # 1. LÍNEA: DISTRIBUCIÓN ELÉCTRICA
    # =========================================================================
    line_dist = "Distribución Eléctrica"
    
    # Easy9 Termomagnéticos 1P, 2P, 3P
    currents_easy9 = [6, 10, 16, 20, 25, 32, 40, 50, 63]
    for c in currents_easy9:
        # 1P
        code_1p = f"EZ9F341{c:02d}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "Easy9", code_1p,
            f"Interruptor Termomagnético Easy9 1P {c}A Curva C",
            f"Interruptor unipolar magnetotérmico para protección contra sobrecargas y cortocircuitos",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "4.5 kA (IEC 60898-1)", "Tension": "230V AC", "Montaje": "Riel DIN"}),
            "Protección de circuitos de alumbrado y tomas monofásicas en instalaciones residenciales y comerciales"
        ))
        # 2P
        code_2p = f"EZ9F342{c:02d}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "Easy9", code_2p,
            f"Interruptor Termomagnético Easy9 2P {c}A Curva C",
            f"Interruptor bipolar magnetotérmico para protección de circuitos monofásicos bifilares y bifásicos",
            json.dumps({"Polos": "2P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "4.5 kA (IEC 60898-1)", "Tension": "230/400V AC", "Montaje": "Riel DIN"}),
            "Protección de aires acondicionados, cocinas eléctricas y tableros residenciales"
        ))
        # 3P
        code_3p = f"EZ9F343{c:02d}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "Easy9", code_3p,
            f"Interruptor Termomagnético Easy9 3P {c}A Curva C",
            f"Interruptor tripolar magnetotérmico para protección de cargas trifásicas en baja tensión",
            json.dumps({"Polos": "3P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "4.5 kA (IEC 60898-1)", "Tension": "400V AC", "Montaje": "Riel DIN"}),
            "Protección de maquinaria trifásica, bombas y alimentadores de tableros comerciales"
        ))

    # Acti9 iC60N Industriales 1P, 2P, 3P
    currents_acti9 = [6, 10, 16, 20, 25, 32, 40, 50, 63]
    for c in currents_acti9:
        # 1P
        code = f"A9F741{c:02d}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "Acti9", code,
            f"Interruptor Automático Acti9 iC60N 1P {c}A Curva C",
            f"Disyuntor magnetotérmico de alta continuidad de servicio para entornos industriales",
            json.dumps({"Polos": "1P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "6 kA (IEC 60898-1) / 10 kA (IEC 60947-2)", "Tension": "220-240V AC", "VisiSafe": "Sí", "VisiTrip": "Sí"}),
            "Instalaciones industriales, hospitales y edificios terciarios críticos"
        ))
        # 2P
        code_2p = f"A9F742{c:02d}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "Acti9", code_2p,
            f"Interruptor Automático Acti9 iC60N 2P {c}A Curva C",
            f"Disyuntor bipolar industrial de máxima seguridad con ventana de disparo VisiTrip",
            json.dumps({"Polos": "2P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "6 kA / 10 kA", "Tension": "230-400V AC", "VisiSafe": "Sí", "VisiTrip": "Sí"}),
            "Distribución eléctrica industrial y terciaria con aislamiento galvánico garantizado"
        ))
        # 3P
        code_3p = f"A9F743{c:02d}"
        items.append((
            brand, line_dist, "Interruptores Termomagnéticos", "Acti9", code_3p,
            f"Interruptor Automático Acti9 iC60N 3P {c}A Curva C",
            f"Disyuntor tripolar industrial de potencia para protección de alimentadores trifásicos",
            json.dumps({"Polos": "3P", "Corriente": f"{c}A", "Curva": "C", "PoderCorte": "6 kA / 10 kA", "Tension": "400V AC", "VisiSafe": "Sí", "VisiTrip": "Sí"}),
            "Tableros de fuerza industrial, centros de datos y plantas manufactureras"
        ))

    # Interruptores Diferenciales Easy9 e iID
    items.extend([
        (brand, line_dist, "Interruptores Diferenciales", "Easy9", "EZ9R34225", "Interruptor Diferencial Easy9 2P 25A 30mA", "Dispositivo de protección diferencial contra fugas a tierra para viviendas", json.dumps({"Polos": "2P", "Corriente": "25A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC"}), "Protección humana contra contactos directos e indirectos"),
        (brand, line_dist, "Interruptores Diferenciales", "Easy9", "EZ9R34240", "Interruptor Diferencial Easy9 2P 40A 30mA", "Dispositivo diferencial de cabecera para cuadros de distribución residencial", json.dumps({"Polos": "2P", "Corriente": "40A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC"}), "Protección general de fugas en tableros residenciales de 40A"),
        (brand, line_dist, "Interruptores Diferenciales", "Easy9", "EZ9R34440", "Interruptor Diferencial Easy9 4P 40A 30mA", "Dispositivo diferencial tetrapolar para tableros trifásicos comerciales", json.dumps({"Polos": "4P", "Corriente": "40A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Protección diferencial de circuitos trifásicos con neutro"),
        (brand, line_dist, "Interruptores Diferenciales", "Acti9", "A9R63625", "Interruptor Diferencial Acti9 iID40 1P+N 25A 30mA Tipo AC", "Diferencial modular industrial de alta inmunidad", json.dumps({"Polos": "1P+N", "Corriente": "25A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC"}), "Protección diferencial en cuadros industriales y centros de control"),
        (brand, line_dist, "Interruptores Diferenciales", "Acti9", "A9R63640", "Interruptor Diferencial Acti9 iID40 1P+N 40A 30mA Tipo AC", "Diferencial modular industrial de 40A clase AC", json.dumps({"Polos": "1P+N", "Corriente": "40A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "230V AC"}), "Salidas de fuerza en entornos industriales"),
        (brand, line_dist, "Interruptores Diferenciales", "Acti9", "A9R63740", "Interruptor Diferencial Acti9 iID40 3P+N 40A 30mA Tipo AC", "Diferencial tetrapolar industrial para circuitos de fuerza", json.dumps({"Polos": "3P+N", "Corriente": "40A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Líneas de alimentación trifásica en talleres e industrias"),
        (brand, line_dist, "Interruptores Diferenciales", "Acti9", "A9R63763", "Interruptor Diferencial Acti9 iID40 3P+N 63A 30mA Tipo AC", "Diferencial tetrapolar industrial de 63A para cabecera de grupo", json.dumps({"Polos": "3P+N", "Corriente": "63A", "Sensibilidad": "30mA", "Tipo": "AC", "Tension": "400V AC"}), "Cabecera de grupos de fuerza en cuadros generales")
    ])

    # Cajas Moldeadas ComPact NSXm y ComPact NSX
    items.extend([
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426100", "Interruptor Automático ComPact NSXm 3P 50A 16kA", "Interruptor termomagnético en caja moldeada compacto para acometidas", json.dumps({"Polos": "3P", "Corriente": "50A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo", "Conexion": "Bornes EverLink"}), "Protección de acometidas de fuerza en baja tensión"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426101", "Interruptor Automático ComPact NSXm 3P 63A 16kA", "Interruptor en caja moldeada para cabeceras de cuadros secundarios", json.dumps({"Polos": "3P", "Corriente": "63A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Tableros de distribución de fuerza en talleres y comercios"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426102", "Interruptor Automático ComPact NSXm 3P 80A 16kA", "Interruptor en caja moldeada para distribución de potencia hasta 80A", json.dumps({"Polos": "3P", "Corriente": "80A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Alimentadores de plantas industriales y edificios"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426103", "Interruptor Automático ComPact NSXm 3P 100A 16kA", "Interruptor en caja moldeada para protección de cuadros generales de 100A", json.dumps({"Polos": "3P", "Corriente": "100A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Cabecera de tableros de bombas, climatización e industria"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426104", "Interruptor Automático ComPact NSXm 3P 125A 16kA", "Interruptor en caja moldeada de 125A con protección termomagnética", json.dumps({"Polos": "3P", "Corriente": "125A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Alimentadores generales de subdistribución industrial"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426105", "Interruptor Automático ComPact NSXm 3P 160A 16kA", "Interruptor de potencia en caja moldeada ultracompacto para 160A", json.dumps({"Polos": "3P", "Corriente": "160A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Protección principal en tableros de potencia baja tensión"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV429630", "Interruptor Automático ComPact NSX100F 3P 100A 36kA", "Interruptor de potencia industrial con alta capacidad de corte", json.dumps({"Polos": "3P", "Corriente": "100A", "PoderCorte": "36 kA (380-415V)", "Disparador": "TMD Regulable (70-100A)"}), "Acometidas industriales principales y protección de transformadores"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV430630", "Interruptor Automático ComPact NSX160F 3P 160A 36kA", "Interruptor de caja moldeada regulable para distribución general", json.dumps({"Polos": "3P", "Corriente": "160A", "PoderCorte": "36 kA (380-415V)", "Disparador": "TMD Regulable (112-160A)"}), "Centros de control de motores y tableros principales de fábrica"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV431630", "Interruptor Automático ComPact NSX250F 3P 250A 36kA", "Interruptor de caja moldeada de 250A para grandes instalaciones", json.dumps({"Polos": "3P", "Corriente": "250A", "PoderCorte": "36 kA (380-415V)", "Disparador": "TMD Regulable (175-250A)"}), "Cabecera principal de plantas industriales y grandes centros comerciales")
    ])

    # =========================================================================
    # 2. LÍNEA: AUTOMATIZACIÓN DE PROCESOS
    # =========================================================================
    line_auto = "Automatización de Procesos"

    # Contactores TeSys D Bobina 220V AC (M7) y 110V AC (F7)
    contactors_tesys_d = [
        ("LC1D09M7", "9A", "4 kW", "220V AC"),
        ("LC1D12M7", "12A", "5.5 kW", "220V AC"),
        ("LC1D18M7", "18A", "7.5 kW", "220V AC"),
        ("LC1D25M7", "25A", "11 kW", "220V AC"),
        ("LC1D32M7", "32A", "15 kW", "220V AC"),
        ("LC1D38M7", "38A", "18.5 kW", "220V AC"),
        ("LC1D40AM7", "40A", "18.5 kW", "220V AC"),
        ("LC1D50AM7", "50A", "22 kW", "220V AC"),
        ("LC1D65AM7", "65A", "30 kW", "220V AC"),
        ("LC1D80M7", "80A", "37 kW", "220V AC"),
        ("LC1D95M7", "95A", "45 kW", "220V AC"),
        ("LC1D115M7", "115A", "55 kW", "220V AC"),
        ("LC1D150M7", "150A", "75 kW", "220V AC"),
        ("LC1D09F7", "9A", "4 kW", "110V AC"),
        ("LC1D12F7", "12A", "5.5 kW", "110V AC"),
        ("LC1D18F7", "18A", "7.5 kW", "110V AC"),
        ("LC1D25F7", "25A", "11 kW", "110V AC"),
        ("LC1D32F7", "32A", "15 kW", "110V AC")
    ]
    for code, curr, kw, bobina in contactors_tesys_d:
        items.append((
            brand, line_auto, "Contactores de Potencia", "TeSys D", code,
            f"Contactor TeSys D {curr} 3P Bobina {bobina}",
            f"Contactor electromagnético tripolar para control y maniobra de motores categoría AC-3",
            json.dumps({"Polos": "3P + 1NA + 1NC", "CorrienteAC3": curr, "PotenciaMotor": f"{kw} a 380-400V", "TensionBobina": bobina, "VidaMecanica": "15 millones de ciclos"}),
            "Arranque de motores trifásicos, bombas, compresores y sistemas de ventilación"
        ))

    # Contactores Miniatura TeSys K
    items.extend([
        (brand, line_auto, "Contactores Miniatura", "TeSys K", "LC1K0610M7", "Contactor Miniatura TeSys K 6A 3P 1NA 220V AC", "Contactor compacto para espacio reducido en riel DIN", json.dumps({"Polos": "3P + 1NA", "CorrienteAC3": "6A", "PotenciaMotor": "2.2 kW a 400V", "Bobina": "220V AC"}), "Pequeña maquinaria y armarios de control compactos"),
        (brand, line_auto, "Contactores Miniatura", "TeSys K", "LC1K0910M7", "Contactor Miniatura TeSys K 9A 3P 1NA 220V AC", "Contactor compacto de 9A para arranque de motores ligeros", json.dumps({"Polos": "3P + 1NA", "CorrienteAC3": "9A", "PotenciaMotor": "4 kW a 400V", "Bobina": "220V AC"}), "Sistemas de bombeo residencial e industrial ligero"),
        (brand, line_auto, "Contactores Miniatura", "TeSys K", "LC1K1210M7", "Contactor Miniatura TeSys K 12A 3P 1NA 220V AC", "Contactor compacto de 12A de alto rendimiento", json.dumps({"Polos": "3P + 1NA", "CorrienteAC3": "12A", "PotenciaMotor": "5.5 kW a 400V", "Bobina": "220V AC"}), "Automatización de empaquetadoras y cintas")
    ])

    # Guardamotores TeSys Deca GV2ME (Pulsadores) y GV2P (Rotativo)
    guardamotores = [
        ("GV2ME04", "0.4 - 0.63 A", "0.18 kW"),
        ("GV2ME05", "0.63 - 1.0 A", "0.25 kW"),
        ("GV2ME06", "1.0 - 1.6 A", "0.37 kW"),
        ("GV2ME07", "1.6 - 2.5 A", "0.75 kW"),
        ("GV2ME08", "2.5 - 4.0 A", "1.5 kW"),
        ("GV2ME10", "4.0 - 6.3 A", "2.2 kW"),
        ("GV2ME14", "6.0 - 10.0 A", "4.0 kW"),
        ("GV2ME16", "9.0 - 14.0 A", "5.5 kW"),
        ("GV2ME20", "13.0 - 18.0 A", "7.5 kW"),
        ("GV2ME21", "17.0 - 23.0 A", "9.0 kW"),
        ("GV2ME22", "20.0 - 25.0 A", "11.0 kW"),
        ("GV2ME32", "24.0 - 32.0 A", "15.0 kW"),
        ("GV2P10", "4.0 - 6.3 A", "2.2 kW"),
        ("GV2P14", "6.0 - 10.0 A", "4.0 kW"),
        ("GV2P16", "9.0 - 14.0 A", "5.5 kW"),
        ("GV2P20", "13.0 - 18.0 A", "7.5 kW"),
        ("GV2P22", "20.0 - 25.0 A", "11.0 kW")
    ]
    for code, rango, kw in guardamotores:
        tipo = "Maneta Rotativa" if code.startswith("GV2P") else "Pulsadores I/O"
        items.append((
            brand, line_auto, "Guardamotores", "TeSys Deca", code,
            f"Guardamotor Magnetotérmico TeSys {code[:4]} {rango}",
            f"Dispositivo integral de protección de motor contra cortocircuitos, sobrecargas y desequilibrio de fases",
            json.dumps({"Polos": "3P", "RangoRegulacion": rango, "PotenciaMotor": f"Hasta {kw} a 400V", "Accionamiento": tipo, "Montaje": "Riel DIN 35mm"}),
            "Protección individualizada de motores eléctricos en cuadros de maniobra y CCM"
        ))

    # Arrancadores Suaves Altistart
    items.extend([
        (brand, line_auto, "Arrancadores Suaves", "Altistart 01", "ATS01N103FT", "Arrancador Suave Altistart 01 3A 1.1kW 110-480V", "Arrancador progresivo compacto para arranque suave de motores monofásicos y trifásicos", json.dumps({"Corriente": "3A", "Potencia": "1.1 kW a 400V", "Tension": "110-480V AC", "Bypass": "Integrado"}), "Reducción de golpe de ariete en pequeñas bombas y cintas"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 01", "ATS01N106FT", "Arrancador Suave Altistart 01 6A 2.2kW 110-480V", "Arrancador suave compacto con ajuste de rampa de aceleración y deceleración", json.dumps({"Corriente": "6A", "Potencia": "2.2 kW a 400V", "Tension": "110-480V AC"}), "Sistemas mecánicos que requieren arranque sin sacudidas"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 01", "ATS01N112FT", "Arrancador Suave Altistart 01 12A 5.5kW 110-480V", "Arrancador suave de 12A con bypass integrado", json.dumps({"Corriente": "12A", "Potencia": "5.5 kW a 400V", "Tension": "110-480V AC"}), "Bombas sumergibles, ventiladores y compresores"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22D17Q", "Arrancador Progresivo Altistart 22 17A 7.5kW 230-440V", "Arrancador suave industrial para bombas y ventiladores con bypass integrado", json.dumps({"Corriente": "17A", "Potencia": "7.5 kW a 400V", "Tension": "230-440V AC", "Protocolo": "Modbus integrado"}), "Eliminación de sobretensiones y picos de corriente en arranque de bombas"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22D32Q", "Arrancador Progresivo Altistart 22 32A 15kW 230-440V", "Arrancador suave industrial con control trifásico de par", json.dumps({"Corriente": "32A", "Potencia": "15 kW a 400V", "Tension": "230-440V AC"}), "Grandes ventiladores y bombas de plantas industriales")
    ])

    # =========================================================================
    # 3. LÍNEA: RELÉS DE CONTROL
    # =========================================================================
    line_reles = "Relés de Control"

    # Relés Térmicos TeSys LRD
    reles_termicos = [
        ("LRD04", "0.4 - 0.63 A"), ("LRD05", "0.63 - 1.0 A"), ("LRD06", "1.0 - 1.6 A"),
        ("LRD07", "1.6 - 2.5 A"), ("LRD08", "2.5 - 4.0 A"), ("LRD10", "4.0 - 6.0 A"),
        ("LRD12", "5.5 - 8.0 A"), ("LRD14", "7.0 - 10.0 A"), ("LRD16", "9.0 - 13.0 A"),
        ("LRD21", "12.0 - 18.0 A"), ("LRD22", "16.0 - 24.0 A"), ("LRD32", "23.0 - 32.0 A"),
        ("LRD35", "30.0 - 38.0 A"), ("LRD3353", "23.0 - 32.0 A"), ("LRD3355", "30.0 - 40.0 A")
    ]
    for code, rango in reles_termicos:
        items.append((
            brand, line_reles, "Relés Térmicos de Sobrecarga", "TeSys Deca", code,
            f"Relé Térmico Diferencial TeSys LRD {rango}",
            f"Relé térmico bimetálico de protección contra sobrecargas y desequilibrios de fase para contactores LC1D",
            json.dumps({"RangoAjuste": rango, "ContactosAuxiliares": "1NA + 1NC", "ClaseDisparo": "Clase 10A", "Rearme": "Manual o Automático", "Montaje": "Directo bajo contactor LC1D"}),
            "Protección térmica de motores eléctricos contra calentamientos prolongados"
        ))

    # Relés Enchufables Electromecánicos Harmony RXM y Bases
    items.extend([
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXM2AB2P7", "Relé Miniatura Enchufable 2 C/O 12A Bobina 230V AC", "Relé electromecánico miniatura de 2 contactos conmutados con botón de test", json.dumps({"Contactos": "2 C/O (12A)", "Bobina": "230V AC", "Indicador": "LED mecánico y luminoso", "Base": "RXZE2M114"}), "Interfaz de mando y aislamiento en tableros de control"),
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXM2AB2BD", "Relé Miniatura Enchufable 2 C/O 12A Bobina 24V DC", "Relé miniatura de 2 contactos conmutados para circuitos de automatización a 24VDC", json.dumps({"Contactos": "2 C/O (12A)", "Bobina": "24V DC", "Base": "RXZE2M114"}), "Acoplamiento entre salidas de PLC y actuadores de potencia"),
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXM4AB2P7", "Relé Miniatura Enchufable 4 C/O 6A Bobina 230V AC", "Relé miniatura de 4 contactos conmutados multipropósito", json.dumps({"Contactos": "4 C/O (6A)", "Bobina": "230V AC", "Base": "RXZE2M114"}), "Multiplicación de señales y enclavamientos de seguridad eléctrica"),
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXM4AB2BD", "Relé Miniatura Enchufable 4 C/O 6A Bobina 24V DC", "Relé miniatura de 4 contactos conmutados para lógica de control a 24VDC", json.dumps({"Contactos": "4 C/O (6A)", "Bobina": "24V DC", "Base": "RXZE2M114"}), "Pupitres de mando, cuadros de automatización y PLC"),
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXZE2M114", "Base para Relé RXM2/RXM4 Montaje Riel DIN", "Base con bornes de tornillo para montaje en riel DIN de relés de 2 y 4 contactos", json.dumps({"Montaje": "Riel DIN 35mm", "Terminales": "Tornillos imperdibles", "Compatible": "RXM2 y RXM4"}), "Fijación y conexionado de relés enchufables en tablero"),
        (brand, line_reles, "Relés de Medida y Control", "Harmony Control", "RM22TG20", "Relé de Control de Fases RM22 183-528V AC 2 C/O", "Relé de control trifásico para detección de presencia de fase y secuencia correcta", json.dumps({"Tension": "183 a 528V AC trifásico", "Salidas": "2 C/O (8A)", "Deteccion": "Secuencia de fase y fallo de fase"}), "Protección de motores contra giro inverso y funcionamiento bifásico"),
        (brand, line_reles, "Relés de Medida y Control", "Harmony Control", "RM22TR33", "Relé de Control de Tensión Trifásica RM22 380-480V AC", "Relé multifunción para vigilancia de sobretensión, subtensión y fallo de fase", json.dumps({"RangoVigilancia": "380 a 480V AC", "Retardo": "Ajustable 0.1 a 10s", "Salidas": "2 C/O"}), "Protección de maquinaria sensible frente a fluctuaciones de la red eléctrica")
    ])

    # =========================================================================
    # 4. LÍNEA: DRIVES (VARIADORES DE FRECUENCIA)
    # =========================================================================
    line_drives = "Drives"

    # Altivar 12 Monofásicos a Trifásicos
    atv12_models = [
        ("ATV12H018M2", "0.18 kW / 0.25 HP", "1.4A"),
        ("ATV12H037M2", "0.37 kW / 0.5 HP", "2.4A"),
        ("ATV12H075M2", "0.75 kW / 1.0 HP", "4.2A"),
        ("ATV12HU15M2", "1.5 kW / 2.0 HP", "7.5A"),
        ("ATV12HU22M2", "2.2 kW / 3.0 HP", "10.0A")
    ]
    for code, hp, curr in atv12_models:
        items.append((
            brand, line_drives, "Variadores de Velocidad", "Altivar 12", code,
            f"Variador de Frecuencia Altivar 12 {hp} 200-240V Monofásico",
            f"Convertidor de frecuencia compacto para motores trifásicos asíncronos con alimentación doméstica o comercial",
            json.dumps({"Potencia": hp, "Entrada": "Monofásica 200-240V AC", "Salida": "Trifásica 0-240V", "CorrienteSalida": curr, "FiltroEMC": "Integrado", "Comunicacion": "Modbus RTU"}),
            "Control de velocidad para bombas de agua, extractores, ventiladores y cintas transportadoras pequeñas"
        ))

    # Altivar 320 Trifásicos 380-500V
    atv320_models = [
        ("ATV320U04N4B", "0.37 kW / 0.5 HP", "1.5A"),
        ("ATV320U07N4B", "0.75 kW / 1.0 HP", "2.3A"),
        ("ATV320U15N4B", "1.5 kW / 2.0 HP", "4.1A"),
        ("ATV320U22N4B", "2.2 kW / 3.0 HP", "5.5A"),
        ("ATV320U30N4B", "3.0 kW / 4.0 HP", "7.1A"),
        ("ATV320U40N4B", "4.0 kW / 5.5 HP", "9.5A"),
        ("ATV320U55N4B", "5.5 kW / 7.5 HP", "14.3A"),
        ("ATV320U75N4B", "7.5 kW / 10.0 HP", "17.0A"),
        ("ATV320D11N4B", "11.0 kW / 15.0 HP", "27.7A"),
        ("ATV320D15N4B", "15.0 kW / 20.0 HP", "33.0A")
    ]
    for code, hp, curr in atv320_models:
        items.append((
            brand, line_drives, "Variadores de Velocidad", "Altivar 320", code,
            f"Variador de Frecuencia Altivar 320 Book {hp} 380-500V Trifásico",
            f"Variador vectorial avanzado de formato libro estrecho con funciones de seguridad integradas",
            json.dumps({"Potencia": hp, "Entrada": "Trifásica 380-500V AC", "CorrienteNominal": curr, "Seguridad": "STO SIL 3 / PLe", "Comunicacion": "Modbus RTU / CANopen integrados"}),
            "Maquinaria de envasado, grúas, elevación, bombas centrífugas y procesos industriales complejos"
        ))

    # =========================================================================
    # 5. LÍNEA: UNIDADES DE MANDO Y SEÑALIZACIÓN
    # =========================================================================
    line_mando = "Unidades de Mando y Señalización"

    # Harmony XB4 Metálicos Ø22mm
    items.extend([
        (brand, line_mando, "Pulsadores Metálicos", "Harmony XB4", "XB4BA21", "Pulsador Metálico Rasante Negro 1NA Ø22mm", "Pulsador completo con cuerpo metálico cromado y retorno por resorte", json.dumps({"Diametro": "22mm", "Color": "Negro", "Contactos": "1 NA", "GradoProteccion": "IP66 / IP69K", "Bisel": "Metálico Cromado"}), "Mando de maquinaria industrial y pupitres de control"),
        (brand, line_mando, "Pulsadores Metálicos", "Harmony XB4", "XB4BA31", "Pulsador Metálico Rasante Verde 1NA Ø22mm", "Pulsador verde para marcha / arranque de sistemas eléctricos", json.dumps({"Diametro": "22mm", "Color": "Verde", "Contactos": "1 NA", "GradoProteccion": "IP66 / IP69K"}), "Orden de marcha en arrancadores y tableros de motores"),
        (brand, line_mando, "Pulsadores Metálicos", "Harmony XB4", "XB4BA42", "Pulsador Metálico Rasante Rojo 1NC Ø22mm", "Pulsador rojo de parada de proceso con contacto normalmente cerrado", json.dumps({"Diametro": "22mm", "Color": "Rojo", "Contactos": "1 NC", "GradoProteccion": "IP66 / IP69K"}), "Orden de parada operativa en paneles de control"),
        (brand, line_mando, "Selectores Metálicos", "Harmony XB4", "XB4BD21", "Selector Metálico 2 Posiciones Fijas 1NA Ø22mm", "Interruptor selector con maneta estándar de 2 posiciones a 90°", json.dumps({"Diametro": "22mm", "Posiciones": "2 fijas", "Contactos": "1 NA", "Maneta": "Negra estándar"}), "Selección de modo Manual / Automático en tableros"),
        (brand, line_mando, "Selectores Metálicos", "Harmony XB4", "XB4BD33", "Selector Metálico 3 Posiciones Fijas 2NA Ø22mm", "Selector de 3 posiciones mantenidas con 2 contactos abiertos", json.dumps({"Diametro": "22mm", "Posiciones": "3 fijas (I - O - II)", "Contactos": "2 NA"}), "Conmutación de bombas 1 - 0 - 2 y selección de canal"),
        (brand, line_mando, "Paradas de Emergencia", "Harmony XB4", "XB4BS542", "Parada de Emergencia Seta Ø40mm Desenganche por Giro 1NC", "Pulsador de seguridad tipo hongo con enclavamiento mecánico de apertura positiva", json.dumps({"Diametro": "Seta 40mm / Montaje 22mm", "Color": "Rojo", "Contactos": "1 NC apertura garantizada", "Norma": "ISO 13850"}), "Parada de emergencia de seguridad obligatoria en máquinas"),
        (brand, line_mando, "Pilotos Luminosos LED", "Harmony XB4", "XB4BVB3", "Piloto LED Monobloc Verde 24V AC/DC Ø22mm", "Indicador luminoso verde LED de alta visibilidad para 24V", json.dumps({"Diametro": "22mm", "Color": "Verde", "Tension": "24V AC/DC", "Consumo": "<18 mA", "Proteccion": "IP66"}), "Señalización de máquina en funcionamiento o estado OK"),
        (brand, line_mando, "Pilotos Luminosos LED", "Harmony XB4", "XB4BVB4", "Piloto LED Monobloc Rojo 24V AC/DC Ø22mm", "Indicador luminoso rojo LED de fallo o alarma", json.dumps({"Diametro": "22mm", "Color": "Rojo", "Tension": "24V AC/DC", "Consumo": "<18 mA"}), "Señalización de paro, sobrecarga térmica o falla"),
        (brand, line_mando, "Pilotos Luminosos LED", "Harmony XB4", "XB4BVM3", "Piloto LED Monobloc Verde 230V AC Ø22mm", "Indicador luminoso verde LED para conexión directa a 220-240VAC", json.dumps({"Diametro": "22mm", "Color": "Verde", "Tension": "230-240V AC", "VidaUtil": "100,000 horas"}), "Indicación de presencia de tensión de red en tablero general"),
        (brand, line_mando, "Pilotos Luminosos LED", "Harmony XB4", "XB4BVM4", "Piloto LED Monobloc Rojo 230V AC Ø22mm", "Indicador luminoso rojo LED para red 220-240VAC", json.dumps({"Diametro": "22mm", "Color": "Rojo", "Tension": "230-240V AC"}), "Indicador de alarma general en cuadros de bombas"),
        (brand, line_mando, "Cajas Botoneras", "Harmony XALD", "XALD01", "Caja Botonera Vacía 1 Taladro Gris/Gris Ø22mm", "Caja estanca de policarbonato para alojar 1 unidad de mando de 22mm", json.dumps({"Taladros": "1 taladro 22mm", "Proteccion": "IP66 / IP69K", "Material": "Policarbonato"}), "Estación de mando local para parada de emergencia o pulsador de marcha"),
        (brand, line_mando, "Cajas Botoneras", "Harmony XALD", "XALD02", "Caja Botonera Vacía 2 Taladros Gris/Gris Ø22mm", "Caja estanca para 2 unidades de mando (Marcha / Paro)", json.dumps({"Taladros": "2 taladros 22mm", "Proteccion": "IP66"}), "Puesto de operador local Marcha-Paro junto al motor"),
        (brand, line_mando, "Cajas Botoneras", "Harmony XALK", "XALK178", "Estación de Parada de Emergencia Completa Seta 40mm", "Caja amarilla de seguridad completa con seta roja y contacto 1NC + 1NA", json.dumps({"ColorBase": "Amarillo seguridad", "Seta": "40mm desenganche por giro", "Contactos": "1NC + 1NA", "Proteccion": "IP66"}), "Punto de seguridad de emergencia visible en líneas de producción")
    ])

    # =========================================================================
    # 6. LÍNEA: CELDAS DE PROTECCIÓN Y ENVOLVENTES
    # =========================================================================
    line_celdas = "Celdas de Protección"

    # Armarios Metálicos Estancos Spacial CRN (IP66, IK10)
    armarios_spacial = [
        ("NSYCRN325150", "300 x 250 x 150 mm"),
        ("NSYCRN43200", "400 x 300 x 200 mm"),
        ("NSYCRN54200", "500 x 400 x 200 mm"),
        ("NSYCRN64200", "600 x 400 x 200 mm"),
        ("NSYCRN65200", "600 x 500 x 200 mm"),
        ("NSYCRN75250", "700 x 500 x 250 mm"),
        ("NSYCRN86250", "800 x 600 x 250 mm"),
        ("NSYCRN108300", "1000 x 800 x 300 mm"),
        ("NSYCRN128300", "1200 x 800 x 300 mm")
    ]
    for code, dims in armarios_spacial:
        items.append((
            brand, line_celdas, "Cajas y Armarios Metálicos", "Spacial CRN", code,
            f"Armario Metálico Spacial CRN {dims} IP66",
            f"Envolvente industrial de chapa de acero soldado con puerta ciega y placa de montaje lisa incluida",
            json.dumps({"Dimensiones": dims, "GradoProteccion": "IP66 / IK10", "Acabado": "Pintura epoxi-poliéster gris RAL 7035", "Cierre": "Doble barra de 3mm"}),
            "Alojamiento y protección de tableros de fuerza, variadores y control en naves industriales y exteriores"
        ))

    # Cuadros Modulares de Distribución Pragma y Mini Pragma
    items.extend([
        (brand, line_celdas, "Cuadros Modulares", "Mini Pragma", "MIP12112", "Cofre Empotrar Mini Pragma 1 Fila 12 Módulos Puerta Fumé", "Cuadro estético para aparamenta modular con puerta abatible", json.dumps({"Modulos": "12 módulos", "Montaje": "Empotrado", "Proteccion": "IP40 / IK07", "Material": "Tecnoplástico autoextinguible"}), "Distribución eléctrica en oficinas, comercios y viviendas"),
        (brand, line_celdas, "Cuadros Modulares", "Mini Pragma", "MIP12218", "Cofre Empotrar Mini Pragma 2 Filas 24 Módulos Puerta Fumé", "Cuadro modular de 24 módulos para media distribución", json.dumps({"Modulos": "24 módulos (2x12)", "Montaje": "Empotrado", "Proteccion": "IP40"}), "Tablero secundario en plantas de oficinas o locales comerciales"),
        (brand, line_celdas, "Cuadros Modulares", "Pragma", "PRA10218", "Cuadro de Distribución Pragma Superficie 2 Filas 36 Módulos", "Cofre industrial de superficie con chasis extraíble y rieles regulables", json.dumps({"Modulos": "36 módulos (2x18)", "Montaje": "Superficie", "Proteccion": "IP40 / IK08", "Corriente": "Hasta 125A"}), "Tableros de distribución técnica en locales comerciales y centros médicos"),
        (brand, line_celdas, "Cuadros Modulares", "Pragma", "PRA10324", "Cuadro de Distribución Pragma Superficie 3 Filas 72 Módulos", "Cuadro de gran capacidad para distribución modular", json.dumps({"Modulos": "72 módulos (3x24)", "Montaje": "Superficie", "Proteccion": "IP40", "Corriente": "Hasta 160A"}), "Distribución eléctrica principal en edificios y talleres"),
        (brand, line_celdas, "Repartidores de Carga", "Linergy", "LGY412560", "Bloque Repartidor Escalonado Linergy 4P 125A 60 Salidas", "Repartidor tetrapolar escalonado para montaje en riel DIN o placa", json.dumps({"Polos": "4P (Tetrapolar)", "Corriente": "125A", "TensionAislamiento": "500V", "Montaje": "Riel DIN 35mm"}), "Distribución equitativa y ordenada de fases y neutro en tableros de potencia"),
        (brand, line_celdas, "Repartidores de Carga", "Linergy", "LGY416048", "Bloque Repartidor Escalonado Linergy 4P 160A 48 Salidas", "Repartidor tetrapolar de alta intensidad para tableros generales", json.dumps({"Polos": "4P (Tetrapolar)", "Corriente": "160A", "PoderCortoCircuito": "Icw 8.4kA"}), "Distribución de acometidas en tableros generales de baja tensión")
    ])

    return items

def populate_database():
    items = get_schneider_catalog_data()
    print(f"Total de productos preparados para Schneider Electric: {len(items)}")

    paths = get_db_paths()
    for db_path in paths:
        print(f"\nSincronizando base de datos en: {db_path}")
        conn = init_db(db_path)
        cur = conn.cursor()

        # Insertar con INSERT OR REPLACE para actualizar specs sin duplicar
        cur.executemany("""
            INSERT OR REPLACE INTO ProductsCatalog (
                Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application, Status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Disponible');
        """, items)
        conn.commit()

        # Comprobar conteo
        cur.execute("SELECT COUNT(1) FROM ProductsCatalog WHERE Brand = 'Schneider Electric';")
        count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(1) FROM Products_FTS;")
        fts_count = cur.fetchone()[0]
        print(f"-> Productos en ProductsCatalog: {count}")
        print(f"-> Productos indexados en Products_FTS: {fts_count}")

        conn.close()

if __name__ == "__main__":
    populate_database()

