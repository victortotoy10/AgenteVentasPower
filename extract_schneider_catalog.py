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

    # Protectores contra Sobretensiones Transitorias (DPS / Surge Protective Devices) Acti9 iPRD
    items.extend([
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "Acti9", "A9L16292", "Protector de Sobretensiones Acti9 iPRD40r 1P+N 40kA", "Descargador de sobretensiones transitorias Tipo 2 con contacto de señalización remota", json.dumps({"Polos": "1P+N", "Imax": "40 kA", "In": "15 kA", "Up": "1.4 kV", "Tension": "230V AC", "ContactoRemoto": "Sí"}), "Protección de equipos electrónicos y centros de cómputo monofásicos contra descargas atmosféricas"),
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "Acti9", "A9L16294", "Protector de Sobretensiones Acti9 iPRD40r 3P+N 40kA", "Descargador tetrapolar Tipo 2 para protección de tableros trifásicos comerciales e industriales", json.dumps({"Polos": "3P+N", "Imax": "40 kA", "In": "15 kA", "Up": "1.4 kV", "Tension": "230/400V AC", "Cartuchos": "Enchufables recambiables"}), "Cabecera de tableros de fuerza en industrias, edificios y clínicas"),
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "Acti9", "A9L16297", "Protector de Sobretensiones Acti9 iPRD65r 3P+N 65kA", "Descargador industrial de máxima capacidad de absorción de transitorios", json.dumps({"Polos": "3P+N", "Imax": "65 kA", "In": "20 kA", "Up": "1.5 kV", "Tension": "230/400V AC"}), "Zonas de alta exposición a rayos y tormentas en subestaciones y plantas"),
        (brand, line_dist, "Protectores contra Sobretensiones (DPS)", "Acti9", "A9L16301", "Protector de Sobretensiones Acti9 iPRD-DC 40r 1000V DC Solar", "Descargador de sobretensión específico para cadenas de paneles fotovoltaicos", json.dumps({"Polos": "2P", "Ucpv": "1000V DC", "Imax": "40 kA", "Norma": "EN 50539-11"}), "Protección en cajas de combinación (combiner boxes) de proyectos de energía solar fotovoltaica")
    ])

    # Cajas Moldeadas ComPact NSXm y ComPact NSX (50A a 630A)
    items.extend([
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426100", "Interruptor Automático ComPact NSXm 3P 50A 16kA", "Interruptor termomagnético en caja moldeada compacto para acometidas", json.dumps({"Polos": "3P", "Corriente": "50A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo", "Conexion": "Bornes EverLink"}), "Protección de acometidas de fuerza en baja tensión"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426101", "Interruptor Automático ComPact NSXm 3P 63A 16kA", "Interruptor en caja moldeada para cabeceras de cuadros secundarios", json.dumps({"Polos": "3P", "Corriente": "63A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Tableros de distribución de fuerza en talleres y comercios"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426102", "Interruptor Automático ComPact NSXm 3P 80A 16kA", "Interruptor en caja moldeada para distribución de potencia hasta 80A", json.dumps({"Polos": "3P", "Corriente": "80A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Alimentadores de plantas industriales y edificios"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426103", "Interruptor Automático ComPact NSXm 3P 100A 16kA", "Interruptor en caja moldeada para protección de cuadros generales de 100A", json.dumps({"Polos": "3P", "Corriente": "100A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Cabecera de tableros de bombas, climatización e industria"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426104", "Interruptor Automático ComPact NSXm 3P 125A 16kA", "Interruptor en caja moldeada de 125A con protección termomagnética", json.dumps({"Polos": "3P", "Corriente": "125A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Alimentadores generales de subdistribución industrial"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSXm", "LV426105", "Interruptor Automático ComPact NSXm 3P 160A 16kA", "Interruptor de potencia en caja moldeada ultracompacto para 160A", json.dumps({"Polos": "3P", "Corriente": "160A", "PoderCorte": "16 kA (380-415V)", "Disparador": "TMD Fijo"}), "Protección principal en tableros de potencia baja tensión"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV429630", "Interruptor Automático ComPact NSX100F 3P 100A 36kA", "Interruptor de potencia industrial con alta capacidad de corte", json.dumps({"Polos": "3P", "Corriente": "100A", "PoderCorte": "36 kA (380-415V)", "Disparador": "TMD Regulable (70-100A)"}), "Acometidas industriales principales y protección de transformadores"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV430630", "Interruptor Automático ComPact NSX160F 3P 160A 36kA", "Interruptor de caja moldeada regulable para distribución general", json.dumps({"Polos": "3P", "Corriente": "160A", "PoderCorte": "36 kA (380-415V)", "Disparador": "TMD Regulable (112-160A)"}), "Centros de control de motores y tableros principales de fábrica"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV431630", "Interruptor Automático ComPact NSX250F 3P 250A 36kA", "Interruptor de caja moldeada de 250A para grandes instalaciones", json.dumps({"Polos": "3P", "Corriente": "250A", "PoderCorte": "36 kA (380-415V)", "Disparador": "TMD Regulable (175-250A)"}), "Cabecera principal de plantas industriales y grandes centros comerciales"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV432676", "Interruptor Automático ComPact NSX400F 3P 400A 36kA Micrologic 2.3", "Interruptor industrial de potencia con unidad de control electrónica Micrologic", json.dumps({"Polos": "3P", "Corriente": "400A", "PoderCorte": "36 kA (380-415V)", "Disparador": "Micrologic 2.3 Electrónico (160-400A)", "Proteccion": "Sobrecarga L y Cortocircuito instantáneo S/I"}), "Cabeceras de plantas industriales, centros comerciales y distribución de transformadores"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV432693", "Interruptor Automático ComPact NSX400N 3P 400A 50kA Micrologic 2.3", "Interruptor de potencia industrial con 50kA de poder de corte", json.dumps({"Polos": "3P", "Corriente": "400A", "PoderCorte": "50 kA (380-415V)", "Disparador": "Micrologic 2.3 Electrónico"}), "Redes eléctricas exigentes con alto nivel de cortocircuito"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV432876", "Interruptor Automático ComPact NSX630F 3P 630A 36kA Micrologic 2.3", "Interruptor de potencia industrial para distribución de 630A", json.dumps({"Polos": "3P", "Corriente": "630A", "PoderCorte": "36 kA (380-415V)", "Disparador": "Micrologic 2.3 Electrónico (250-630A)"}), "Cabecera de tableros generales de baja tensión (TGBT)"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV432893", "Interruptor Automático ComPact NSX630N 3P 630A 50kA Micrologic 2.3", "Interruptor de potencia de 630A con 50kA de corte para industria pesada", json.dumps({"Polos": "3P", "Corriente": "630A", "PoderCorte": "50 kA (380-415V)", "Disparador": "Micrologic 2.3 Electrónico"}), "Plantas camaroneras, acerías y subestaciones de distribución"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV430635", "Interruptor Automático ComPact NSX160F 4P 160A 36kA TMD", "Interruptor tetrapolar con neutro protegido al 100% para generadores y transferencias", json.dumps({"Polos": "4P (3P+N)", "Corriente": "160A", "PoderCorte": "36 kA", "Disparador": "TMD Regulable"}), "Sistemas de transferencia red-generador y distribución con neutro"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV431635", "Interruptor Automático ComPact NSX250F 4P 250A 36kA TMD", "Interruptor tetrapolar de 250A para conmutación de red y generador", json.dumps({"Polos": "4P (3P+N)", "Corriente": "250A", "PoderCorte": "36 kA", "Disparador": "TMD Regulable"}), "Tableros de transferencia automática y distribución tetrapolar"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV432677", "Interruptor Automático ComPact NSX400F 4P 400A 36kA Micrologic 2.3", "Interruptor tetrapolar de potencia de 400A con protección electrónica", json.dumps({"Polos": "4P (3P+N)", "Corriente": "400A", "PoderCorte": "36 kA", "Disparador": "Micrologic 2.3 Electrónico"}), "Alimentadores de generadores de emergencia de 300 kVA"),
        (brand, line_dist, "Interruptores de Caja Moldeada", "ComPact NSX", "LV432877", "Interruptor Automático ComPact NSX630F 4P 630A 36kA Micrologic 2.3", "Interruptor tetrapolar de 630A para generadores de 500 kVA", json.dumps({"Polos": "4P (3P+N)", "Corriente": "630A", "PoderCorte": "36 kA", "Disparador": "Micrologic 2.3 Electrónico"}), "Transferencias automáticas de gran potencia y hospitales")
    ])

    # Interruptores de Alta Potencia ComPact NS (800A a 1600A)
    items.extend([
        (brand, line_dist, "Interruptores de Gran Potencia", "ComPact NS", "33044", "Interruptor Automático ComPact NS800N 3P 800A 50kA Micrologic 2.0A", "Interruptor de potencia en caja moldeada pesada con amperímetro integrado", json.dumps({"Polos": "3P", "Corriente": "800A", "PoderCorte": "50 kA (380-415V)", "Disparador": "Micrologic 2.0A con display LCD"}), "Entradas de transformadores de 500 kVA y subestaciones"),
        (brand, line_dist, "Interruptores de Gran Potencia", "ComPact NS", "33064", "Interruptor Automático ComPact NS1000N 3P 1000A 50kA Micrologic 2.0A", "Interruptor de potencia industrial para acometidas principales de 1000A", json.dumps({"Polos": "3P", "Corriente": "1000A", "PoderCorte": "50 kA", "Disparador": "Micrologic 2.0A con pantalla"}), "Salida de transformadores de 750 kVA en industrias"),
        (brand, line_dist, "Interruptores de Gran Potencia", "ComPact NS", "33084", "Interruptor Automático ComPact NS1250N 3P 1250A 50kA Micrologic 2.0A", "Interruptor de potencia para transformadores de 1000 kVA", json.dumps({"Polos": "3P", "Corriente": "1250A", "PoderCorte": "50 kA", "Disparador": "Micrologic 2.0A"}), "Acometidas generales de grandes fábricas y centros logísticos"),
        (brand, line_dist, "Interruptores de Gran Potencia", "ComPact NS", "33104", "Interruptor Automático ComPact NS1600N 3P 1600A 50kA Micrologic 2.0A", "Interruptor de potencia máxima para transformadores de 1250 kVA", json.dumps({"Polos": "3P", "Corriente": "1600A", "PoderCorte": "50 kA", "Disparador": "Micrologic 2.0A"}), "Cabecera principal de subestación en baja tensión")
    ])

    # Interruptores de Bastidor Abierto (Air Circuit Breakers - ACB) MasterPact MTZ
    items.extend([
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV847280", "Interruptor de Potencia MasterPact MTZ1 08 H1 3P 800A 42kA", "Interruptor abierto inteligente con conectividad digital nativa y Micrologic 2.0X", json.dumps({"Polos": "3P", "Corriente": "800A", "PoderCorte": "42 kA (415V)", "Montaje": "Fijo / Opcional Seccionable", "Disparador": "Micrologic 2.0X", "ClasePrecision": "Medición Clase 1"}), "Interruptor de entrada de subestaciones y plantas industriales críticas"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV847281", "Interruptor de Potencia MasterPact MTZ1 10 H1 3P 1000A 42kA", "Interruptor abierto de 1000A con unidad de control avanzada", json.dumps({"Polos": "3P", "Corriente": "1000A", "PoderCorte": "42 kA", "Disparador": "Micrologic 2.0X"}), "Acometidas de transformadores de 750 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV847282", "Interruptor de Potencia MasterPact MTZ1 12 H1 3P 1250A 42kA", "Interruptor abierto de 1250A para tableros principales de subestación", json.dumps({"Polos": "3P", "Corriente": "1250A", "PoderCorte": "42 kA", "Disparador": "Micrologic 2.0X"}), "Subestaciones de 1000 kVA en centros de datos e industrias"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV847283", "Interruptor de Potencia MasterPact MTZ1 16 H1 3P 1600A 42kA", "Interruptor abierto de 1600A para distribución de alta energía", json.dumps({"Polos": "3P", "Corriente": "1600A", "PoderCorte": "42 kA", "Disparador": "Micrologic 2.0X"}), "Grandes plantas de manufactura y distribución eléctrica"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV848140", "Interruptor de Potencia MasterPact MTZ2 20 H1 3P 2000A 66kA", "Interruptor abierto de 2000A con 66kA de corte y protección selectiva Micrologic 5.0X", json.dumps({"Polos": "3P", "Corriente": "2000A", "PoderCorte": "66 kA", "Disparador": "Micrologic 5.0X (LSI con retardo selectivo)"}), "Cabeceras de subestaciones con transformadores de 1500 kVA"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV848141", "Interruptor de Potencia MasterPact MTZ2 25 H1 3P 2500A 66kA", "Interruptor abierto de 2500A para transformadores de 2000 kVA", json.dumps({"Polos": "3P", "Corriente": "2500A", "PoderCorte": "66 kA", "Disparador": "Micrologic 5.0X"}), "Infraestructuras portuarias, refinerías y acerías"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV848142", "Interruptor de Potencia MasterPact MTZ2 32 H1 3P 3200A 66kA", "Interruptor de bastidor abierto de 3200A para distribución primaria", json.dumps({"Polos": "3P", "Corriente": "3200A", "PoderCorte": "66 kA", "Disparador": "Micrologic 5.0X"}), "Subestaciones de 2500 kVA y grandes complejos petroquímicos"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV848143", "Interruptor de Potencia MasterPact MTZ3 40 H1 3P 4000A 66kA", "Interruptor de gran bastidor de 4000A para distribución masiva", json.dumps({"Polos": "3P", "Corriente": "4000A", "PoderCorte": "66 kA", "Disparador": "Micrologic 5.0X"}), "Grandes centrales de generación eléctrica y distribución industrial"),
        (brand, line_dist, "Interruptores de Potencia en Bastidor Abierto", "MasterPact MTZ", "LV848144", "Interruptor de Potencia MasterPact MTZ3 63 H1 3P 6300A 100kA", "Interruptor de máxima potencia de 6300A con 100kA de capacidad de ruptura", json.dumps({"Polos": "3P", "Corriente": "6300A", "PoderCorte": "100 kA", "Disparador": "Micrologic 6.0X (Protección a tierra LSIG)"}), "Subestaciones maestras y centrales hidroeléctricas/termoeléctricas")
    ])

    # Sistemas de Transferencia Automática TransferPact y Enclavamientos
    items.extend([
        (brand, line_dist, "Transferencias Automáticas de Red", "TransferPact", "TPC1003P", "Conmutador de Transferencia Automática TransferPact 3P 100A", "Equipo integrado de transferencia automática red-generador con controlador electrónico", json.dumps({"Polos": "3P", "Corriente": "100A", "Tension": "415V AC", "TiempoConmutacion": "<500ms", "Controlador": "Integrado con pantalla"}), "Respaldo de emergencia en gasolineras, edificios comerciales y centros médicos"),
        (brand, line_dist, "Transferencias Automáticas de Red", "TransferPact", "TPC1603P", "Conmutador de Transferencia Automática TransferPact 3P 160A", "Sistema monobloc compacto de conmutación automática para 160A", json.dumps({"Polos": "3P", "Corriente": "160A", "Tension": "415V AC"}), "Sistemas de bombeo municipal y centros comerciales"),
        (brand, line_dist, "Transferencias Automáticas de Red", "TransferPact", "TPC2503P", "Conmutador de Transferencia Automática TransferPact 3P 250A", "Transferencia automática industrial con enclavamiento mecánico integrado", json.dumps({"Polos": "3P", "Corriente": "250A", "Tension": "415V AC"}), "Líneas de producción de fábricas y almacenes frigoríficos"),
        (brand, line_dist, "Transferencias Automáticas de Red", "TransferPact", "TPC4003P", "Conmutador de Transferencia Automática TransferPact 3P 400A", "Transferencia automática de potencia para generadores de 300 kVA", json.dumps({"Polos": "3P", "Corriente": "400A", "Tension": "415V AC"}), "Hospitales, centros de datos y plantas procesadoras"),
        (brand, line_dist, "Transferencias Automáticas de Red", "TransferPact", "TPC6303P", "Conmutador de Transferencia Automática TransferPact 3P 630A", "Transferencia automática de alta capacidad para generadores de 500 kVA", json.dumps({"Polos": "3P", "Corriente": "630A", "Tension": "415V AC"}), "Grandes industrias de exportación y subestaciones de emergencia"),
        (brand, line_dist, "Enclavamientos para Transferencia", "ComPact NSX", "TRV00210", "Kit de Enclavamiento Mecánico por Varillas para NSX100-250", "Mecanismo de interbloqueo que impide el cierre simultáneo de dos interruptores", json.dumps({"Compatible": "ComPact NSX100 a NSX250", "Tipo": "Varillas mecánicas"}), "Montaje de transferencias manuales o automáticas entre dos breakers NSX"),
        (brand, line_dist, "Enclavamientos para Transferencia", "ComPact NSX", "LV432598", "Kit de Enclavamiento Mecánico con Placa Base para NSX400-630", "Placa base con enclavamiento mecánico para dos interruptores de 400A o 630A", json.dumps({"Compatible": "ComPact NSX400 y NSX630", "Tipo": "Placa con balancín mecánico"}), "Construcción de tableros de transferencia red-red o red-generador")
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

    # Contactores de Gran Potencia TeSys F (185A a 630A)
    contactors_tesys_f = [
        ("LC1F185M7", "185A", "90 kW", "220V AC"),
        ("LC1F225M7", "225A", "110 kW", "220V AC"),
        ("LC1F265M7", "265A", "132 kW", "220V AC"),
        ("LC1F330M7", "330A", "160 kW", "220V AC"),
        ("LC1F400M7", "400A", "200 kW", "220V AC"),
        ("LC1F500M7", "500A", "250 kW", "220V AC"),
        ("LC1F630M7", "630A", "335 kW", "220V AC")
    ]
    for code, curr, kw, bobina in contactors_tesys_f:
        items.append((
            brand, line_auto, "Contactores de Gran Potencia", "TeSys F", code,
            f"Contactor de Potencia TeSys F {curr} 3P Bobina {bobina}",
            f"Contactor industrial robusto para cargas de motor pesadas y alta intensidad de conmutación",
            json.dumps({"Polos": "3P", "CorrienteAC3": curr, "PotenciaMotor": f"{kw} a 400V", "Bobina": bobina, "Mantenimiento": "Polos y bobina sustituibles fácilmente"}),
            "Arranque de grandes molinos, trituradoras, bombas de draga y compresores industriales"
        ))

    # Contactores Electrónicos Inteligentes TeSys Giga (115A a 500A)
    contactors_tesys_giga = [
        ("LC1G115KUEN", "115A", "55 kW"),
        ("LC1G150KUEN", "150A", "75 kW"),
        ("LC1G185KUEN", "185A", "90 kW"),
        ("LC1G225KUEN", "225A", "110 kW"),
        ("LC1G265KUEN", "265A", "132 kW"),
        ("LC1G330KUEN", "330A", "160 kW"),
        ("LC1G400KUEN", "400A", "200 kW"),
        ("LC1G500KUEN", "500A", "250 kW")
    ]
    for code, curr, kw in contactors_tesys_giga:
        items.append((
            brand, line_auto, "Contactores de Alta Eficiencia", "TeSys Giga", code,
            f"Contactor Inteligente TeSys Giga {curr} 3P Bobina Electrónica 100-250V",
            f"Contactor de última generación con bobina electrónica multivoltaje de muy bajo consumo y diagnóstico de desgaste integrado",
            json.dumps({"Polos": "3P", "CorrienteAC3": curr, "PotenciaMotor": f"{kw} a 400V", "Bobina": "100-250V AC/DC Amplio Rango", "Diagnostico": "LED indicador de vida útil de contactos"}),
            "Sistemas de bombeo continuo, industria química, alimentaria y minería con alta exigencia ecológica"
        ))

    # Contactores Miniatura TeSys K y Accesorios Auxiliares
    items.extend([
        (brand, line_auto, "Contactores Miniatura", "TeSys K", "LC1K0610M7", "Contactor Miniatura TeSys K 6A 3P 1NA 220V AC", "Contactor compacto para espacio reducido en riel DIN", json.dumps({"Polos": "3P + 1NA", "CorrienteAC3": "6A", "PotenciaMotor": "2.2 kW a 400V", "Bobina": "220V AC"}), "Pequeña maquinaria y armarios de control compactos"),
        (brand, line_auto, "Contactores Miniatura", "TeSys K", "LC1K0910M7", "Contactor Miniatura TeSys K 9A 3P 1NA 220V AC", "Contactor compacto de 9A para arranque de motores ligeros", json.dumps({"Polos": "3P + 1NA", "CorrienteAC3": "9A", "PotenciaMotor": "4 kW a 400V", "Bobina": "220V AC"}), "Sistemas de bombeo residencial e industrial ligero"),
        (brand, line_auto, "Contactores Miniatura", "TeSys K", "LC1K1210M7", "Contactor Miniatura TeSys K 12A 3P 1NA 220V AC", "Contactor compacto de 12A de alto rendimiento", json.dumps({"Polos": "3P + 1NA", "CorrienteAC3": "12A", "PotenciaMotor": "5.5 kW a 400V", "Bobina": "220V AC"}), "Automatización de empaquetadoras y cintas"),
        (brand, line_auto, "Bloques Auxiliares", "TeSys Deca", "LADN11", "Bloque de Contactos Auxiliares TeSys 1NA + 1NC Frontal", "Bloque de contactos instantáneos de montaje frontal para contactores LC1D", json.dumps({"Contactos": "1 NA + 1 NC", "Montaje": "Frontal a presión", "Tension": "Hasta 690V AC"}), "Señalización de estado y enclavamientos eléctricos"),
        (brand, line_auto, "Bloques Auxiliares", "TeSys Deca", "LADN22", "Bloque de Contactos Auxiliares TeSys 2NA + 2NC Frontal", "Bloque frontal de 4 contactos auxiliares para contactores LC1D", json.dumps({"Contactos": "2 NA + 2 NC", "Montaje": "Frontal a presión"}), "Cuadros de control con múltiples señales a PLC y pilotos"),
        (brand, line_auto, "Bloques Auxiliares", "TeSys Deca", "LADN40", "Bloque de Contactos Auxiliares TeSys 4NA Frontal", "Bloque frontal de 4 contactos normalmente abiertos para contactores LC1D", json.dumps({"Contactos": "4 NA", "Montaje": "Frontal"}), "Multiplicación de señales de marcha y confirmación"),
        (brand, line_auto, "Enclavamientos de Inversor", "TeSys Deca", "LAD9R1V", "Kit de Enclavamiento Mecánico con Conexiones para Inversor LC1D09-D38", "Kit completo para armar arrancador inversor de giro con dos contactores TeSys D", json.dumps({"Compatible": "LC1D09 a LC1D38", "Incluye": "Enclavamiento mecánico + juego de barras de potencia"}), "Armado rápido y seguro de tableros de inversión de giro para motores")
    ])

    # Guardamotores TeSys Deca GV2ME y GV2P
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

    # Arrancadores Suaves Altistart 01, Altistart 22 y Altistart 480
    items.extend([
        (brand, line_auto, "Arrancadores Suaves", "Altistart 01", "ATS01N103FT", "Arrancador Suave Altistart 01 3A 1.1kW 110-480V", "Arrancador progresivo compacto para arranque suave de motores monofásicos y trifásicos", json.dumps({"Corriente": "3A", "Potencia": "1.1 kW a 400V", "Tension": "110-480V AC", "Bypass": "Integrado"}), "Reducción de golpe de ariete en pequeñas bombas y cintas"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 01", "ATS01N106FT", "Arrancador Suave Altistart 01 6A 2.2kW 110-480V", "Arrancador suave compacto con ajuste de rampa de aceleración y deceleración", json.dumps({"Corriente": "6A", "Potencia": "2.2 kW a 400V", "Tension": "110-480V AC"}), "Sistemas mecánicos que requieren arranque sin sacudidas"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 01", "ATS01N112FT", "Arrancador Suave Altistart 01 12A 5.5kW 110-480V", "Arrancador suave de 12A con bypass integrado", json.dumps({"Corriente": "12A", "Potencia": "5.5 kW a 400V", "Tension": "110-480V AC"}), "Bombas sumergibles, ventiladores y compresores"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22D17Q", "Arrancador Progresivo Altistart 22 17A 7.5kW 230-440V", "Arrancador suave industrial para bombas y ventiladores con bypass integrado", json.dumps({"Corriente": "17A", "Potencia": "7.5 kW a 400V", "Tension": "230-440V AC", "Protocolo": "Modbus integrado"}), "Eliminación de sobretensiones y picos de corriente en arranque de bombas"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22D32Q", "Arrancador Progresivo Altistart 22 32A 15kW 230-440V", "Arrancador suave industrial con control trifásico de par", json.dumps({"Corriente": "32A", "Potencia": "15 kW a 400V", "Tension": "230-440V AC"}), "Grandes ventiladores y bombas de plantas industriales"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22D47Q", "Arrancador Progresivo Altistart 22 47A 22kW 230-440V", "Arrancador suave industrial de 47A con bypass de contactor interno", json.dumps({"Corriente": "47A", "Potencia": "22 kW / 30 HP a 400V", "Tension": "230-440V AC"}), "Sistemas de bombeo de agua potable y riego agrícola"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22D62Q", "Arrancador Progresivo Altistart 22 62A 30kW 230-440V", "Arrancador suave de 62A para bombas y compresores de tornillo", json.dumps({"Corriente": "62A", "Potencia": "30 kW / 40 HP a 400V", "Tension": "230-440V AC"}), "Salas de compresores industriales y plantas de hielo"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22D75Q", "Arrancador Progresivo Altistart 22 75A 37kW 230-440V", "Arrancador suave industrial de 75A", json.dumps({"Corriente": "75A", "Potencia": "37 kW / 50 HP a 400V", "Tension": "230-440V AC"}), "Arranque progresivo de bombas centrífugas de 50 HP"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22D88Q", "Arrancador Progresivo Altistart 22 88A 45kW 230-440V", "Arrancador suave industrial de 88A para 60 HP", json.dumps({"Corriente": "88A", "Potencia": "45 kW / 60 HP a 400V", "Tension": "230-440V AC"}), "Grandes extractores y bombas industriales"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22C11Q", "Arrancador Progresivo Altistart 22 110A 55kW 230-440V", "Arrancador suave industrial de 110A para 75 HP", json.dumps({"Corriente": "110A", "Potencia": "55 kW / 75 HP a 400V", "Tension": "230-440V AC"}), "Plantas camaroneras y estaciones de bombeo de gran caudal"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22C14Q", "Arrancador Progresivo Altistart 22 140A 75kW 230-440V", "Arrancador suave industrial de 140A para 100 HP", json.dumps({"Corriente": "140A", "Potencia": "75 kW / 100 HP a 400V", "Tension": "230-440V AC"}), "Sistemas de bombeo principal de 100 HP en camaroneras y agroindustria"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 22", "ATS22C17Q", "Arrancador Progresivo Altistart 22 170A 90kW 230-440V", "Arrancador suave de 170A para motores pesados de 125 HP", json.dumps({"Corriente": "170A", "Potencia": "90 kW / 125 HP a 400V", "Tension": "230-440V AC"}), "Plantas de harina de pescado, ingenios azucareros y bombeo"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 480", "ATS480D17Y", "Arrancador Suave Altistart 480 17A 7.5kW para Servicio Severo", "Arrancador suave de última generación con ciberseguridad integrada y control de par avanzado", json.dumps({"Corriente": "17A", "Potencia": "7.5 kW a 400V", "Tension": "208 a 690V AC", "Ciberseguridad": "Achilles Nivel 2"}), "Aplicaciones severas en minería, agua y petróleo"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 480", "ATS480D32Y", "Arrancador Suave Altistart 480 32A 15kW para Servicio Severo", "Arrancador para entornos exigentes y alta inercia", json.dumps({"Corriente": "32A", "Potencia": "15 kW a 400V", "Tension": "208-690V AC"}), "Trituradoras, molinos y bombas de alta presión"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 480", "ATS480D62Y", "Arrancador Suave Altistart 480 62A 30kW para Servicio Severo", "Arrancador pesado de 62A con bus Modbus y ranura Ethernet", json.dumps({"Corriente": "62A", "Potencia": "30 kW a 400V", "Tension": "208-690V AC"}), "Ventiladores de minas y bombas de pulpa"),
        (brand, line_auto, "Arrancadores Suaves", "Altistart 480", "ATS480C14Y", "Arrancador Suave Altistart 480 140A 75kW para Servicio Severo", "Arrancador suave para motores de 100 HP en condiciones de carga severa", json.dumps({"Corriente": "140A", "Potencia": "75 kW a 400V", "Tension": "208-690V AC"}), "Compresores de gas, bombas centrífugas de gran inercia y puertos")
    ])

    # =========================================================================
    # 3. LÍNEA: RELÉS DE CONTROL Y FUENTES DE PODER
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

    # Relés Enchufables Electromecánicos Harmony RXM, Bases y Relés de Medida
    items.extend([
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXM2AB2P7", "Relé Miniatura Enchufable 2 C/O 12A Bobina 230V AC", "Relé electromecánico miniatura de 2 contactos conmutados con botón de test", json.dumps({"Contactos": "2 C/O (12A)", "Bobina": "230V AC", "Indicador": "LED mecánico y luminoso", "Base": "RXZE2M114"}), "Interfaz de mando y aislamiento en tableros de control"),
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXM2AB2BD", "Relé Miniatura Enchufable 2 C/O 12A Bobina 24V DC", "Relé miniatura de 2 contactos conmutados para circuitos de automatización a 24VDC", json.dumps({"Contactos": "2 C/O (12A)", "Bobina": "24V DC", "Base": "RXZE2M114"}), "Acoplamiento entre salidas de PLC y actuadores de potencia"),
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXM4AB2P7", "Relé Miniatura Enchufable 4 C/O 6A Bobina 230V AC", "Relé miniatura de 4 contactos conmutados multipropósito", json.dumps({"Contactos": "4 C/O (6A)", "Bobina": "230V AC", "Base": "RXZE2M114"}), "Multiplicación de señales y enclavamientos de seguridad eléctrica"),
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXM4AB2BD", "Relé Miniatura Enchufable 4 C/O 6A Bobina 24V DC", "Relé miniatura de 4 contactos conmutados para lógica de control a 24VDC", json.dumps({"Contactos": "4 C/O (6A)", "Bobina": "24V DC", "Base": "RXZE2M114"}), "Pupitres de mando, cuadros de automatización y PLC"),
        (brand, line_reles, "Relés Enchufables", "Harmony Relay", "RXZE2M114", "Base para Relé RXM2/RXM4 Montaje Riel DIN", "Base con bornes de tornillo para montaje en riel DIN de relés de 2 y 4 contactos", json.dumps({"Montaje": "Riel DIN 35mm", "Terminales": "Tornillos imperdibles", "Compatible": "RXM2 y RXM4"}), "Fijación y conexionado de relés enchufables en tablero"),
        (brand, line_reles, "Relés de Medida y Control", "Harmony Control", "RM22TG20", "Relé de Control de Fases RM22 183-528V AC 2 C/O", "Relé de control trifásico para detección de presencia de fase y secuencia correcta", json.dumps({"Tension": "183 a 528V AC trifásico", "Salidas": "2 C/O (8A)", "Deteccion": "Secuencia de fase y fallo de fase"}), "Protección de motores contra giro inverso y funcionamiento bifásico"),
        (brand, line_reles, "Relés de Medida y Control", "Harmony Control", "RM22TR33", "Relé de Control de Tensión Trifásica RM22 380-480V AC", "Relé multifunción para vigilancia de sobretensión, subtensión y fallo de fase", json.dumps({"RangoVigilancia": "380 a 480V AC", "Retardo": "Ajustable 0.1 a 10s", "Salidas": "2 C/O"}), "Protección de maquinaria sensible frente a fluctuaciones de la red eléctrica")
    ])

    # Fuentes de Alimentación Conmutadas Modicon Power Supply (24V DC)
    fuentes_modicon = [
        ("ABLS1A24021", "2.1A", "50W"),
        ("ABLS1A24031", "3.1A", "75W"),
        ("ABLS1A24050", "5.0A", "120W"),
        ("ABLS1A24100", "10.0A", "240W"),
        ("ABLS1A24200", "20.0A", "480W")
    ]
    for code, curr, watts in fuentes_modicon:
        items.append((
            brand, line_reles, "Fuentes de Alimentación", "Modicon Power", code,
            f"Fuente de Poder Regulada Modicon 24V DC {curr} {watts} Riel DIN",
            f"Fuente conmutada compacta de alta eficiencia con protección contra sobrecargas y cortocircuitos",
            json.dumps({"TensionEntrada": "100-240V AC Monofásica", "TensionSalida": "24V DC Regulada", "Corriente": curr, "Potencia": watts, "Montaje": "Riel DIN 35mm", "Eficiencia": ">88%"}),
            "Alimentación de PLCs, pantallas HMI, relés, sensores y lazos de control de 24VDC"
        ))

    # Relés Inteligentes Zelio Logic
    items.extend([
        (brand, line_reles, "Relés Inteligentes", "Zelio Logic", "SR2B121BD", "Relé Inteligente Zelio Logic Compacto 12 E/S 24V DC con Pantalla", "Controlador lógico programable compacto con 8 entradas digitales (4 analógicas) y 4 salidas a relé", json.dumps({"Alimentacion": "24V DC", "Entradas": "8 (4 configurables 0-10V)", "Salidas": "4 a relé 8A", "Pantalla": "LCD con reloj horario", "Lenguaje": "Ladder / FBD"}), "Automatización de portones, bombas alternadas, iluminación y pequeños procesos"),
        (brand, line_reles, "Relés Inteligentes", "Zelio Logic", "SR2B201BD", "Relé Inteligente Zelio Logic Compacto 20 E/S 24V DC con Pantalla", "Controlador con 12 entradas digitales (6 analógicas) y 8 salidas a relé", json.dumps({"Alimentacion": "24V DC", "Entradas": "12", "Salidas": "8 a relé", "Pantalla": "LCD integrada"}), "Control automático de 2 a 3 bombas, ventilación y calderas"),
        (brand, line_reles, "Relés Inteligentes", "Zelio Logic", "SR2B201FU", "Relé Inteligente Zelio Logic Compacto 20 E/S 100-240V AC", "Controlador con alimentación directa a 110-220VAC sin necesidad de fuente externa", json.dumps({"Alimentacion": "100-240V AC", "Entradas": "12 digitales AC", "Salidas": "8 a relé"}), "Sistemas donde no se dispone de fuente de 24VDC"),
        (brand, line_reles, "Relés Inteligentes", "Zelio Logic", "SR3B261BD", "Relé Inteligente Zelio Logic Modular 26 E/S 24V DC Ampliable", "Controlador modular expandible hasta 40 E/S con módulos de extensión", json.dumps({"Alimentacion": "24V DC", "Entradas": "16", "Salidas": "10 a relé", "Ampliable": "Sí, mediante módulos de extensión"}), "Procesos medianos con necesidad de ampliación futura y comunicación Modbus")
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

    # Altivar Process ATV630 (Bombas, Tratamiento de Agua y Fluidos con Ethernet)
    atv630_models = [
        ("ATV630U07N4", "0.75 kW / 1.0 HP", "2.2A"),
        ("ATV630U15N4", "1.5 kW / 2.0 HP", "4.0A"),
        ("ATV630U22N4", "2.2 kW / 3.0 HP", "5.6A"),
        ("ATV630U30N4", "3.0 kW / 4.0 HP", "7.2A"),
        ("ATV630U40N4", "4.0 kW / 5.5 HP", "9.3A"),
        ("ATV630U55N4", "5.5 kW / 7.5 HP", "12.7A"),
        ("ATV630U75N4", "7.5 kW / 10.0 HP", "16.5A"),
        ("ATV630D11N4", "11.0 kW / 15.0 HP", "23.5A"),
        ("ATV630D15N4", "15.0 kW / 20.0 HP", "31.7A"),
        ("ATV630D18N4", "18.5 kW / 25.0 HP", "39.2A"),
        ("ATV630D22N4", "22.0 kW / 30.0 HP", "46.3A"),
        ("ATV630D30N4", "30.0 kW / 40.0 HP", "61.5A"),
        ("ATV630D37N4", "37.0 kW / 50.0 HP", "74.5A"),
        ("ATV630D45N4", "45.0 kW / 60.0 HP", "88.0A"),
        ("ATV630D55N4", "55.0 kW / 75.0 HP", "106.0A"),
        ("ATV630D75N4", "75.0 kW / 100.0 HP", "145.0A")
    ]
    for code, hp, curr in atv630_models:
        items.append((
            brand, line_drives, "Variadores de Proceso", "Altivar Process ATV630", code,
            f"Variador de Velocidad Altivar Process ATV630 {hp} 380-480V con Ethernet",
            f"Variador de servicios orientado a procesos con curvas de bomba integradas, servidor web y medición de energía incorporada",
            json.dumps({"Potencia": hp, "Tension": "380-480V Trifásico", "Corriente": curr, "Comunicacion": "Doble puerto Ethernet/IP y Modbus TCP", "Funciones": "Control multibomba, antiatasco, detección de fuga"}),
            "Plantas de tratamiento de agua potable y residual, bombeo en camaroneras, sistemas de riego e industrias de bebidas"
        ))

    # Easy Altivar 610 (Económico para Bombas y Ventiladores)
    atv610_models = [
        ("ATV610U07N4", "0.75 kW / 1.0 HP", "2.2A"),
        ("ATV610U15N4", "1.5 kW / 2.0 HP", "4.0A"),
        ("ATV610U22N4", "2.2 kW / 3.0 HP", "5.6A"),
        ("ATV610U30N4", "3.0 kW / 4.0 HP", "7.2A"),
        ("ATV610U40N4", "4.0 kW / 5.5 HP", "9.3A"),
        ("ATV610U55N4", "5.5 kW / 7.5 HP", "12.7A"),
        ("ATV610U75N4", "7.5 kW / 10.0 HP", "16.5A"),
        ("ATV610D11N4", "11.0 kW / 15.0 HP", "23.5A"),
        ("ATV610D15N4", "15.0 kW / 20.0 HP", "31.7A"),
        ("ATV610D18N4", "18.5 kW / 25.0 HP", "39.2A"),
        ("ATV610D22N4", "22.0 kW / 30.0 HP", "46.3A")
    ]
    for code, hp, curr in atv610_models:
        items.append((
            brand, line_drives, "Variadores Estándar", "Easy Altivar 610", code,
            f"Variador de Frecuencia Easy Altivar 610 {hp} 380-415V Trifásico",
            f"Variador robusto optimizado en costo para aplicaciones estándar de bombas y ventiladores centrífugos",
            json.dumps({"Potencia": hp, "Tension": "380-415V Trifásico", "Corriente": curr, "Protocolo": "Modbus RTU RS485 integrado", "Recubrimiento": "Placas electrónicas barnizadas Clase 3C3"}),
            "Sistemas de presurización de agua en edificios, torres de enfriamiento y aire acondicionado HVAC"
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

    # Harmony XB5 Plásticos Ø22mm (Doble Aislamiento)
    items.extend([
        (brand, line_mando, "Pulsadores Plásticos", "Harmony XB5", "XB5AA21", "Pulsador Plástico Rasante Negro 1NA Ø22mm", "Pulsador plástico de doble aislamiento para ambientes húmedos o corrosivos", json.dumps({"Diametro": "22mm", "Color": "Negro", "Contactos": "1 NA", "Proteccion": "IP66 / IP69K", "Bisel": "Plástico negro"}), "Tableros de control en plantas químicas, piscinas y camaroneras"),
        (brand, line_mando, "Pulsadores Plásticos", "Harmony XB5", "XB5AA31", "Pulsador Plástico Rasante Verde 1NA Ø22mm", "Pulsador plástico de marcha con protección IP66", json.dumps({"Diametro": "22mm", "Color": "Verde", "Contactos": "1 NA"}), "Marcha de bombas en ambientes costeros o salinos"),
        (brand, line_mando, "Pulsadores Plásticos", "Harmony XB5", "XB5AA42", "Pulsador Plástico Rasante Rojo 1NC Ø22mm", "Pulsador plástico de parada con protección reforzada", json.dumps({"Diametro": "22mm", "Color": "Rojo", "Contactos": "1 NC"}), "Parada operativa en ambientes corrosivos"),
        (brand, line_mando, "Selectores Plásticos", "Harmony XB5", "XB5AD21", "Selector Plástico 2 Posiciones Fijas 1NA Ø22mm", "Selector de maneta estándar plástica de 2 posiciones", json.dumps({"Diametro": "22mm", "Posiciones": "2 fijas", "Contactos": "1 NA"}), "Selección de régimen de funcionamiento"),
        (brand, line_mando, "Selectores Plásticos", "Harmony XB5", "XB5AD33", "Selector Plástico 3 Posiciones Fijas 2NA Ø22mm", "Selector plástico de 3 posiciones I-O-II mantenidas", json.dumps({"Diametro": "22mm", "Posiciones": "3 fijas", "Contactos": "2 NA"}), "Alternancia de bombas y equipos"),
        (brand, line_mando, "Paradas de Emergencia", "Harmony XB5", "XB5AS542", "Parada de Emergencia Plástica Seta Ø40mm 1NC", "Seta de seguridad plástica con desenganche por giro y apertura positiva", json.dumps({"Diametro": "40mm", "Color": "Rojo", "Contactos": "1 NC", "Norma": "EN/ISO 13850"}), "Seguridad en plantas procesadoras de alimentos y lavado a presión"),
        (brand, line_mando, "Pilotos Luminosos LED", "Harmony XB5", "XB5AVB3", "Piloto LED Plástico Verde 24V AC/DC Ø22mm", "Piloto monobloc plástico verde de 24V", json.dumps({"Color": "Verde", "Tension": "24V AC/DC", "Proteccion": "IP66"}), "Indicación en pupitres de mando anticorrosivos"),
        (brand, line_mando, "Pilotos Luminosos LED", "Harmony XB5", "XB5AVB4", "Piloto LED Plástico Rojo 24V AC/DC Ø22mm", "Piloto monobloc plástico rojo de 24V", json.dumps({"Color": "Rojo", "Tension": "24V AC/DC"}), "Alarma en ambientes salinos"),
        (brand, line_mando, "Pilotos Luminosos LED", "Harmony XB5", "XB5AVM3", "Piloto LED Plástico Verde 230V AC Ø22mm", "Piloto monobloc plástico para conexión a 220V", json.dumps({"Color": "Verde", "Tension": "230V AC"}), "Señalización de encendido en tableros de bombeo"),
        (brand, line_mando, "Pilotos Luminosos LED", "Harmony XB5", "XB5AVM4", "Piloto LED Plástico Rojo 230V AC Ø22mm", "Piloto monobloc plástico para alarma en 220V", json.dumps({"Color": "Rojo", "Tension": "230V AC"}), "Indicación de sobrecarga en cuadros exteriores")
    ])

    # =========================================================================
    # 6. LÍNEA: ENVOLVENTES Y CELDAS DE PROTECCIÓN
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

    # Cuadros Modulares de Distribución Pragma, Mini Pragma y Repartidores Linergy
    items.extend([
        (brand, line_celdas, "Cuadros Modulares", "Mini Pragma", "MIP12112", "Cofre Empotrar Mini Pragma 1 Fila 12 Módulos Puerta Fumé", "Cuadro estético para aparamenta modular con puerta abatible", json.dumps({"Modulos": "12 módulos", "Montaje": "Empotrado", "Proteccion": "IP40 / IK07", "Material": "Tecnoplástico autoextinguible"}), "Distribución eléctrica en oficinas, comercios y viviendas"),
        (brand, line_celdas, "Cuadros Modulares", "Mini Pragma", "MIP12218", "Cofre Empotrar Mini Pragma 2 Filas 24 Módulos Puerta Fumé", "Cuadro modular de 24 módulos para media distribución", json.dumps({"Modulos": "24 módulos (2x12)", "Montaje": "Empotrado", "Proteccion": "IP40"}), "Tablero secundario en plantas de oficinas o locales comerciales"),
        (brand, line_celdas, "Cuadros Modulares", "Pragma", "PRA10218", "Cuadro de Distribución Pragma Superficie 2 Filas 36 Módulos", "Cofre industrial de superficie con chasis extraíble y rieles regulables", json.dumps({"Modulos": "36 módulos (2x18)", "Montaje": "Superficie", "Proteccion": "IP40 / IK08", "Corriente": "Hasta 125A"}), "Tableros de distribución técnica en locales comerciales y centros médicos"),
        (brand, line_celdas, "Cuadros Modulares", "Pragma", "PRA10324", "Cuadro de Distribución Pragma Superficie 3 Filas 72 Módulos", "Cuadro de gran capacidad para distribución modular", json.dumps({"Modulos": "72 módulos (3x24)", "Montaje": "Superficie", "Proteccion": "IP40", "Corriente": "Hasta 160A"}), "Distribución eléctrica principal en edificios y talleres"),
        (brand, line_celdas, "Repartidores de Carga", "Linergy", "LGY412560", "Bloque Repartidor Escalonado Linergy 4P 125A 60 Salidas", "Repartidor tetrapolar escalonado para montaje en riel DIN o placa", json.dumps({"Polos": "4P (Tetrapolar)", "Corriente": "125A", "TensionAislamiento": "500V", "Montaje": "Riel DIN 35mm"}), "Distribución equitativa y ordenada de fases y neutro en tableros de potencia"),
        (brand, line_celdas, "Repartidores de Carga", "Linergy", "LGY416048", "Bloque Repartidor Escalonado Linergy 4P 160A 48 Salidas", "Repartidor tetrapolar de alta intensidad para tableros generales", json.dumps({"Polos": "4P (Tetrapolar)", "Corriente": "160A", "PoderCortoCircuito": "Icw 8.4kA"}), "Distribución de acometidas en tableros generales de baja tensión")
    ])

    # =========================================================================
    # 7. LÍNEA: AUTOMATIZACIÓN AVANZADA, PLCS Y PANTALLAS HMI
    # =========================================================================
    line_plc = "Controladores y HMI"

    # Controladores Modicon M221 y Expansiones TM3
    items.extend([
        (brand, line_plc, "Controladores Lógicos (PLCs)", "Modicon M221", "TM221C16R", "Controlador Lógico PLC Modicon M221 16 E/S a Relé", "PLC compacto programable con EcoStruxure Machine Expert Basic", json.dumps({"Entradas": "9 digitales 24V DC", "Salidas": "7 a relé 2A", "Alimentacion": "100-240V AC", "Puertos": "USB de programación y puerto serie RS485"}), "Automatización de máquinas compactas y líneas de empaque"),
        (brand, line_plc, "Controladores Lógicos (PLCs)", "Modicon M221", "TM221C24R", "Controlador Lógico PLC Modicon M221 24 E/S a Relé", "PLC compacto de 24 E/S con entradas rápidas de conteo", json.dumps({"Entradas": "14 digitales (4 rápidas)", "Salidas": "10 a relé", "Alimentacion": "100-240V AC"}), "Control de cintas transportadoras, dosificadoras y llenadoras"),
        (brand, line_plc, "Controladores Lógicos (PLCs)", "Modicon M221", "TM221CE24R", "Controlador Lógico PLC Modicon M221 24 E/S Relé con Ethernet", "PLC con puerto Ethernet nativo para conexión en red industrial", json.dumps({"Entradas": "14 digitales", "Salidas": "10 a relé", "Ethernet": "RJ45 Modbus TCP", "Alimentacion": "100-240V AC"}), "Sistemas con supervisión SCADA, conexión remota y pantallas HMI"),
        (brand, line_plc, "Controladores Lógicos (PLCs)", "Modicon M221", "TM221CE40R", "Controlador Lógico PLC Modicon M221 40 E/S Relé con Ethernet", "PLC de alta capacidad con 40 E/S integradas y puerto Ethernet", json.dumps({"Entradas": "24 digitales", "Salidas": "16 a relé", "Ethernet": "Modbus TCP", "Alimentacion": "100-240V AC"}), "Automatización de plantas embotelladoras, lavadoras y silos"),
        (brand, line_plc, "Módulos de Expansión", "Modicon TM3", "TM3DI16", "Módulo de Expansión Modicon TM3 16 Entradas Digitales 24V", "Módulo de ampliación de entradas discretas para PLC M221/M241", json.dumps({"Entradas": "16 digitales 24V DC", "Conexion": "Bornes de tornillo extraíbles"}), "Ampliación de sensores y finales de carrera en tableros"),
        (brand, line_plc, "Módulos de Expansión", "Modicon TM3", "TM3DQ16R", "Módulo de Expansión Modicon TM3 16 Salidas a Relé", "Módulo de ampliación de salidas a relé de 2A", json.dumps({"Salidas": "16 a relé", "CorrienteMax": "2A por salida"}), "Mando de múltiples contactores, electroválvulas y pilotos"),
        (brand, line_plc, "Módulos de Expansión", "Modicon TM3", "TM3AM6", "Módulo Analógico Modicon TM3 4 Entradas / 2 Salidas", "Módulo mixto de señales analógicas de 4-20mA y 0-10V", json.dumps({"EntradasAnalógicas": "4 (0-10V / 4-20mA)", "SalidasAnalógicas": "2 (0-10V / 4-20mA)", "Resolucion": "12 bits"}), "Control proporcional de válvulas, lectura de sensores de presión y temperatura")
    ])

    # Pantallas Táctiles HMI Harmony ST6
    hmis_st6 = [
        ("HMIST6200", "4.3 Pulgadas", "480 x 272"),
        ("HMIST6400", "7.0 Pulgadas", "800 x 480"),
        ("HMIST6500", "10.1 Pulgadas", "1024 x 600"),
        ("HMIST6600", "12.1 Pulgadas", "1280 x 800"),
        ("HMIST6700", "15.6 Pulgadas", "1366 x 768")
    ]
    for code, size, res in hmis_st6:
        items.append((
            brand, line_plc, "Pantallas Táctiles HMI", "Harmony ST6", code,
            f"Pantalla Táctil HMI Harmony ST6 {size} Color Widescreen Ethernet",
            f"Interfaz hombre-máquina de alta resolución gráfica programable con EcoStruxure Operator Terminal Expert",
            json.dumps({"Tamaño": size, "Resolución": res, "Colores": "16 millones", "Puertos": "Ethernet RJ45, USB host, RS485/RS232", "Alimentacion": "24V DC", "Proteccion": "IP65F frontal"}),
            "Visualización y control de máquinas en salas de control y frentes de tablero"
        ))

    # =========================================================================
    # 8. LÍNEA: MEDICIÓN Y GESTIÓN DE ENERGÍA (POWERLOGIC)
    # =========================================================================
    line_medicion = "Medición y Calidad de Energía"

    items.extend([
        (brand, line_medicion, "Centrales de Medida Multímetro", "PowerLogic PM5000", "METSEPM5110", "Medidor de Energía PowerLogic PM5110 Clase 0.5S con Salida de Pulsos", "Central de medida compacta para supervisión de parámetros eléctricos (V, I, F, FP, kW, kVA, kWh)", json.dumps({"ClasePrecision": "0.5S (IEC 62053-22)", "Salida": "Pulsos estática", "Pantalla": "LCD retroiluminada", "Medición": "THD y armónicos individuales hasta orden 15"}), "Submedición de energía y asignación de costos en tableros secundarios"),
        (brand, line_medicion, "Centrales de Medida Multímetro", "PowerLogic PM5000", "METSEPM5330", "Medidor de Potencia y Energía PowerLogic PM5330 Modbus RTU RS485", "Central de medida avanzada con puerto serie RS485 Modbus y 2 salidas de relé de alarma", json.dumps({"ClasePrecision": "0.5S", "Comunicacion": "Modbus RTU RS485", "SalidasRelé": "2 contactos", "Armónicos": "Hasta orden 31", "Memoria": "Registro de eventos y alarmas"}), "Integración a sistemas de gestión energética SCADA o software EcoStruxure Power"),
        (brand, line_medicion, "Centrales de Medida Multímetro", "PowerLogic PM5000", "METSEPM5560", "Analizador de Redes PowerLogic PM5560 Doble Ethernet Clase 0.2S", "Analizador de redes de máxima precisión con doble puerto Ethernet RJ45 y servidor web integrado", json.dumps({"ClasePrecision": "0.2S de alta precisión", "Comunicacion": "Doble Ethernet (Daisy Chain) Modbus TCP", "WebServer": "Páginas web embebidas", "Armónicos": "Hasta orden 63", "Memoria": "1.1 MB"}), "Acometidas principales de subestación, hospitales y cumplimiento de código de red"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "PowerLogic METSECT", "METSECT5CC010", "Transformador de Corriente TC METSECT 100/5A Diámetro 21mm", "Transformador de núcleo toroidal para cable pasante", json.dumps({"Relacion": "100/5A", "Ventana": "21mm cable", "Clase": "Clase 1 (1.5VA)"}), "Medición de alimentadores de hasta 100A"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "PowerLogic METSECT", "METSECT5CC020", "Transformador de Corriente TC METSECT 200/5A Diámetro 21mm", "Transformador de corriente para cable hasta 200A", json.dumps({"Relacion": "200/5A", "Ventana": "21mm", "Clase": "Clase 0.5 (2.5VA)"}), "Alimentadores de motores y tableros de 200A"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "PowerLogic METSECT", "METSECT5MA040", "Transformador de Corriente TC METSECT 400/5A Barra 30x10mm", "Transformador para barra plana o cable pasante", json.dumps({"Relacion": "400/5A", "VentanaBarra": "30x10mm", "Clase": "Clase 0.5 (5VA)"}), "Salidas de interruptores de 400A en tableros generales"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "PowerLogic METSECT", "METSECT5MA080", "Transformador de Corriente TC METSECT 800/5A Barra 50x12mm", "Transformador para barras de distribución de 800A", json.dumps({"Relacion": "800/5A", "VentanaBarra": "50x12mm", "Clase": "Clase 0.5 (8VA)"}), "Acometidas de transformadores y generadores de 800A"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "PowerLogic METSECT", "METSECT5MB100", "Transformador de Corriente TC METSECT 1000/5A Barra 60x12mm", "Transformador de alta capacidad para barras de 1000A", json.dumps({"Relacion": "1000/5A", "VentanaBarra": "60x12mm", "Clase": "Clase 0.5 (10VA)"}), "Medición en cabeceras de subestaciones de 1000A"),
        (brand, line_medicion, "Transformadores de Corriente (TC)", "PowerLogic METSECT", "METSECT5MC160", "Transformador de Corriente TC METSECT 1600/5A Barra 80x12mm", "Transformador para barras principales de 1600A", json.dumps({"Relacion": "1600/5A", "VentanaBarra": "80x12mm", "Clase": "Clase 0.5 (15VA)"}), "Medición de transformadores de 1000 a 1250 kVA")
    ])

    # =========================================================================
    # 9. LÍNEA: SENSORES INDUSTRIALES Y PRESOSTATOS (TELEMECANIQUE SENSORS)
    # =========================================================================
    line_sensores = "Sensores Industriales"

    items.extend([
        (brand, line_sensores, "Finales de Carrera (Limit Switches)", "OsiSense XC", "XCKM115", "Final de Carrera Metálico XCKM Palanca con Rodillo Termoplástico 1NA+1NC", "Interruptor de posición de cuerpo metálico robusto para aplicaciones industriales", json.dumps({"Accionamiento": "Palanca con rodillo giratorio", "Contactos": "1 NA + 1 NC acción brusca", "Cuerpo": "Zamak metálico", "Proteccion": "IP66 / IK05"}), "Detección de posición en compuertas, grúas, elevadores y maquinaria pesada"),
        (brand, line_sensores, "Finales de Carrera (Limit Switches)", "OsiSense XC", "XCKM121", "Final de Carrera Metálico XCKM Pulsador con Rodillo Metálico 1NA+1NC", "Interruptor de posición accionado por pulsador lineal con rodillo", json.dumps({"Accionamiento": "Pulsador con rodillo", "Contactos": "1 NA + 1 NC", "Cuerpo": "Metálico IP66"}), "Detección de paso de levas y carros en maquinaria de mecanizado"),
        (brand, line_sensores, "Finales de Carrera (Limit Switches)", "OsiSense XC", "XCKP2118P16", "Final de Carrera Termoplástico XCKP Palanca Rodillo 1NA+1NC", "Interruptor de posición compacto de plástico doble aislamiento", json.dumps({"Cuerpo": "Plástico IP66/IP67", "Contactos": "1 NA + 1 NC", "EntradaCable": "M16 x 1.5"}), "Empaquetadoras, transportadores y ambientes con riesgo de corrosión"),
        (brand, line_sensores, "Finales de Carrera (Limit Switches)", "OsiSense XC", "XCKJ10511", "Final de Carrera Metálico Servicio Pesado XCKJ Palanca Rodillo", "Interruptor de posición de servicio pesado formato CENELEC", json.dumps({"Cuerpo": "Metálico reforzado", "Contactos": "1 NA + 1 NC", "Proteccion": "IP66 / NEMA 4X"}), "Siderurgia, minería, cementeras y puertos"),
        (brand, line_sensores, "Sensores de Proximidad Inductivos", "OsiSense XS", "XS612B1PAL2", "Sensor Inductivo M12 Alcance 4mm PNP NA Cable 2m", "Sensor de proximidad cilíndrico metálico roscado M12", json.dumps({"Diametro": "M12 x 1", "Alcance": "4 mm enrasable", "Salida": "PNP normalmente abierto (NA)", "Alimentacion": "12-48V DC", "Cable": "2 metros"}), "Detección sin contacto de piezas metálicas en líneas automatizadas"),
        (brand, line_sensores, "Sensores de Proximidad Inductivos", "OsiSense XS", "XS618B1PAL2", "Sensor Inductivo M18 Alcance 8mm PNP NA Cable 2m", "Sensor cilíndrico metálico M18 de alcance extendido", json.dumps({"Diametro": "M18 x 1", "Alcance": "8 mm enrasable", "Salida": "PNP NA", "Tension": "12-48V DC"}), "Conteo de botellas, cajas con grapa metálica y posición de pistones"),
        (brand, line_sensores, "Sensores de Proximidad Inductivos", "OsiSense XS", "XS630B1PAL2", "Sensor Inductivo M30 Alcance 15mm PNP NA Cable 2m", "Sensor cilíndrico metálico M30 de gran alcance de detección", json.dumps({"Diametro": "M30 x 1.5", "Alcance": "15 mm", "Salida": "PNP NA"}), "Detección de vagones, rodillos pesados y estructuras en exteriores"),
        (brand, line_sensores, "Sensores de Proximidad Inductivos", "OsiSense XS", "XS1M18MA250", "Sensor Inductivo M18 2 Hilos 24-240V AC/DC Cable 2m", "Sensor universal a dos hilos para conexión directa a bobinas o entradas AC", json.dumps({"Diametro": "M18", "Tension": "24-240V AC/DC", "Salida": "2 hilos NA", "Alcance": "5 mm"}), "Sustitución directa de finales de carrera mecánicos sin necesidad de fuente DC"),
        (brand, line_sensores, "Presostatos Industriales", "Nautilus XMLB", "XMLB004A2S11", "Presostato Electromecánico XMLB 0.25 a 4 bar Diferencial Ajustable", "Presostato de fuelle con escala graduada y diferencial ajustable para fluidos hidráulicos y agua", json.dumps({"RangoAjuste": "0.25 a 4 bar", "Contactos": "1 C/O (conmutado)", "Fluido": "Aire, agua, aceite hidráulico hasta 160°C", "Rosca": "G 1/4 hembra"}), "Control de presión de arranque/paro en bombas y compresores neumáticos"),
        (brand, line_sensores, "Presostatos Industriales", "Nautilus XMLB", "XMLB010A2S11", "Presostato Electromecánico XMLB 0.7 a 10 bar Diferencial Ajustable", "Presostato industrial para redes de agua a presión hasta 10 bar", json.dumps({"RangoAjuste": "0.7 a 10 bar", "Contactos": "1 C/O", "Conexion": "G 1/4"}), "Sistemas hidroneumáticos en edificios, industrias y plantas de ósmosis"),
        (brand, line_sensores, "Presostatos Industriales", "Nautilus XMLB", "XMLB020A2S11", "Presostato Electromecánico XMLB 1.3 a 20 bar Diferencial Ajustable", "Presostato de alta presión para circuitos hidráulicos hasta 20 bar", json.dumps({"RangoAjuste": "1.3 a 20 bar", "Contactos": "1 C/O"}), "Prensas hidráulicas y líneas de vapor/aceite"),
        (brand, line_sensores, "Presostatos para Bombas de Agua", "Pumptrol Square D", "FSG2J24", "Presostato para Bombas Pumptrol Square D 20-40 PSI", "Interruptor de presión estándar mundial para control automático de electrobombas", json.dumps({"RangoCalibracion": "20 a 40 PSI (1.4 a 2.8 bar)", "Contactos": "2P (Bipolar corta fase y neutro/fase 2)", "Capacidad": "Hasta 2 HP en 220V / 1.5 HP en 110V", "Rosca": "1/4 NPT hembra"}), "Tanques hidroneumáticos domiciliarios, comerciales y bombas de pozo"),
        (brand, line_sensores, "Presostatos para Bombas de Agua", "Pumptrol Square D", "FYG22J24", "Presostato para Bombas Pumptrol Square D 30-50 PSI", "Interruptor de presión para sistemas que requieren mayor presión de línea", json.dumps({"RangoCalibracion": "30 a 50 PSI (2.1 a 3.5 bar)", "Contactos": "2P bipolar", "Capacidad": "Hasta 2 HP"}), "Sistemas hidroneumáticos en edificios residenciales de varios pisos")
    ])

    # =========================================================================
    # 10. LÍNEA: TOMAS INDUSTRIALES Y MECANISMOS (PRATIKA Y ORION)
    # =========================================================================
    line_conectividad = "Conectividad y Mecanismos"

    # Tomas y Clavijas Industriales PratiKa (IEC 60309)
    items.extend([
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKF16M423", "Clavija Aérea Industrial PratiKa 2P+T 16A 200-250V IP44 Azul", "Enchufe macho industrial monobloc con prensaestopas integrado", json.dumps({"Polos": "2P + T", "Corriente": "16A", "Tension": "200-250V AC", "Color": "Azul", "Proteccion": "IP44"}), "Conexión de maquinaria monofásica portátil y generadores"),
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKF16M434", "Clavija Aérea Industrial PratiKa 3P+T 16A 380-415V IP44 Rojo", "Enchufe macho industrial trifásico", json.dumps({"Polos": "3P + T", "Corriente": "16A", "Tension": "380-415V AC", "Color": "Rojo", "Proteccion": "IP44"}), "Motores trifásicos, soldadoras y bombas móviles"),
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKF16M435", "Clavija Aérea Industrial PratiKa 3P+N+T 16A 380-415V IP44 Rojo", "Enchufe macho industrial tetrapolar con neutro", json.dumps({"Polos": "3P + N + T", "Corriente": "16A", "Tension": "380-415V AC", "Color": "Rojo", "Proteccion": "IP44"}), "Alimentación de cuadros de faena y eventos"),
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKF32M423", "Clavija Aérea Industrial PratiKa 2P+T 32A 200-250V IP44 Azul", "Enchufe macho de 32A monofásico", json.dumps({"Polos": "2P + T", "Corriente": "32A", "Tension": "200-250V AC", "Color": "Azul"}), "Generadores de alta potencia monofásicos"),
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKF32M434", "Clavija Aérea Industrial PratiKa 3P+T 32A 380-415V IP44 Rojo", "Enchufe macho industrial de 32A trifásico", json.dumps({"Polos": "3P + T", "Corriente": "32A", "Tension": "380-415V AC", "Color": "Rojo"}), "Hornos industriales, soldadoras MIG/TIG y compresores"),
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKF32M435", "Clavija Aérea Industrial PratiKa 3P+N+T 32A 380-415V IP44 Rojo", "Enchufe macho de 32A trifásico con neutro", json.dumps({"Polos": "3P + N + T", "Corriente": "32A", "Tension": "380-415V AC", "Color": "Rojo"}), "Acometidas temporales de obra"),
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKY16M434", "Base Aérea Hembra Industrial PratiKa 3P+T 16A 380-415V IP44 Rojo", "Tomacorriente hembra aéreo con tapa abatible", json.dumps({"Polos": "3P + T", "Corriente": "16A", "Tension": "380-415V AC", "Color": "Rojo"}), "Prolongaciones y extensiones eléctricas de taller"),
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKY32M434", "Base Aérea Hembra Industrial PratiKa 3P+T 32A 380-415V IP44 Rojo", "Tomacorriente hembra aéreo de 32A con tapa", json.dumps({"Polos": "3P + T", "Corriente": "32A", "Tension": "380-415V AC"}), "Extensiones trifásicas de alta potencia"),
        (brand, line_conectividad, "Tomas y Clavijas Industriales", "PratiKa", "PKF16F434", "Clavija Mural Inclinada PratiKa 3P+T 16A 380-415V IP67 Rojo Estanca", "Toma mural estanca sumergible temporalmente para ambientes húmedos extremos", json.dumps({"Polos": "3P + T", "Corriente": "16A", "Proteccion": "IP67 estanco total", "Montaje": "Mural en pared o tablero"}), "Lavaderos industriales, puertos pesqueros y camaroneras")
    ])

    # Mecanismos Residenciales y Comerciales Orion (Placas e Interruptores)
    items.extend([
        (brand, line_conectividad, "Mecanismos Eléctricos", "Orion", "S73010104", "Interruptor Simple 1 Vía 10A 127/250V Orion Blanco", "Módulo de interruptor unipolar de encendido con contactos de plata", json.dumps({"Tipo": "1 Vía Simple", "Corriente": "10A", "Tension": "127/250V AC", "Color": "Blanco brillante", "Norma": "INEN"}), "Encendido de iluminación en residencias, hoteles y oficinas"),
        (brand, line_conectividad, "Mecanismos Eléctricos", "Orion", "S73010204", "Interruptor Conmutable 3 Vías 10A 127/250V Orion Blanco", "Módulo conmutable para control de luces desde dos puntos distintos", json.dumps({"Tipo": "Conmutable 3 Vías", "Corriente": "10A", "Tension": "127/250V AC"}), "Escaleras, pasillos y dormitorios"),
        (brand, line_conectividad, "Mecanismos Eléctricos", "Orion", "S73010404", "Pulsador para Timbre 10A 127/250V Orion Blanco", "Módulo pulsador con retorno por resorte y símbolo de campana", json.dumps({"Tipo": "Pulsador NA", "Corriente": "10A"}), "Timbres de entrada y apertura de puertas eléctricas"),
        (brand, line_conectividad, "Mecanismos Eléctricos", "Orion", "S73026304", "Tomacorriente Doble 2P+T 15A 127/250V NEMA 5-15R Orion Blanco", "Doble toma con polo a tierra para estándar ecuatoriano y americano", json.dumps({"Configuracion": "NEMA 5-15R", "Polos": "2P + T", "Corriente": "15A", "Tension": "127/250V AC"}), "Alimentación de electrodomésticos, cómputo y tomas generales"),
        (brand, line_conectividad, "Mecanismos Eléctricos", "Orion", "S73026404", "Tomacorriente GFCI Falla a Tierra 20A 125V NEMA 5-20R Blanco", "Tomacorriente con interruptor diferencial de falla a tierra y autodiagnóstico", json.dumps({"Configuracion": "NEMA 5-20R con GFCI", "Corriente": "20A", "Sensibilidad": "4-6 mA", "LuzIndicadora": "LED de estado"}), "Cocinas, baños, lavanderías y exteriores según norma NEC"),
        (brand, line_conectividad, "Placas y Marcos", "Orion", "S73091004", "Placa 1 Ventana 4x2 Orion Classic Blanco", "Placa estética de policarbonato para 1 módulo en caja rectangular 4x2", json.dumps({"Ventanas": "1 módulo", "Tamaño": "4x2 pulgadas", "Acabado": "Blanco Classic"}), "Terminación estética de interruptores individuales"),
        (brand, line_conectividad, "Placas y Marcos", "Orion", "S73092004", "Placa 2 Ventanas 4x2 Orion Classic Blanco", "Placa para 2 módulos en caja 4x2", json.dumps({"Ventanas": "2 módulos", "Tamaño": "4x2"}), "Combinación de dos interruptores o interruptor y toma"),
        (brand, line_conectividad, "Placas y Marcos", "Orion", "S73093004", "Placa 3 Ventanas 4x2 Orion Classic Blanco", "Placa para 3 módulos en caja 4x2", json.dumps({"Ventanas": "3 módulos", "Tamaño": "4x2"}), "Tableros de control de iluminación triple")
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
        print(f"-> Productos en ProductsCatalog (Schneider): {count}")
        print(f"-> Total productos indexados en Products_FTS: {fts_count}")

        conn.close()

if __name__ == "__main__":
    populate_database()
