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

def get_weidmuller_catalog_data():
    brand = "Weidmuller"  # Nombre estricto sin diéresis para base de datos
    items = []

    # =========================================================================
    # 1. LÍNEA: CONECTIVIDAD Y BORNERAS (KLIPPON CONNECT)
    # Ref: Catalogue 1 & 1A Terminal blocks Klippon Connect
    # =========================================================================
    line_conn = "Conectividad y Borneras"

    # 1.1 Borneras de Paso de Conexión por Tornillo Serie W (WDU)
    screw_pass = [
        ("1020000000", "WDU 2.5", "2.5 mm²", "800V", "24A", "Beige", "Bornera de paso unipolar por tornillo 2.5 mm²"),
        ("1020100000", "WDU 4", "4 mm²", "800V", "32A", "Beige", "Bornera de paso unipolar por tornillo 4 mm²"),
        ("1020200000", "WDU 6", "6 mm²", "800V", "41A", "Beige", "Bornera de paso unipolar por tornillo 6 mm²"),
        ("1020300000", "WDU 10", "10 mm²", "1000V", "57A", "Beige", "Bornera de paso unipolar por tornillo 10 mm²"),
        ("1020400000", "WDU 16", "16 mm²", "1000V", "76A", "Beige", "Bornera de paso unipolar por tornillo 16 mm²"),
        ("1020500000", "WDU 35", "35 mm²", "1000V", "125A", "Beige", "Bornera de paso industrial por tornillo 35 mm²"),
        ("1020600000", "WDU 70/95", "95 mm²", "1000V", "232A", "Beige", "Bornera de potencia para alimentadores principales 95 mm²"),
        ("1024500000", "WDU 120/150", "120 mm²", "1000V", "269A", "Beige", "Bornera de alta potencia por tornillo hasta 120 mm²"),
        # Versiones Azul (para neutro)
        ("1020080000", "WDU 2.5 BL", "2.5 mm²", "800V", "24A", "Azul", "Bornera de paso unipolar azul para identificación de neutro 2.5 mm²"),
        ("1020180000", "WDU 4 BL", "4 mm²", "800V", "32A", "Azul", "Bornera de paso unipolar azul para conductor neutro 4 mm²"),
        ("1020280000", "WDU 6 BL", "6 mm²", "800V", "41A", "Azul", "Bornera de paso unipolar azul para conductor neutro 6 mm²"),
        ("1020380000", "WDU 10 BL", "10 mm²", "1000V", "57A", "Azul", "Bornera de paso unipolar azul para conductor neutro 10 mm²")
    ]
    for code, modelo, sec, v, i, col, desc in screw_pass:
        items.append((
            brand, line_conn, "Borneras de Paso por Tornillo", "Klippon Connect Serie W", code,
            f"Bornera de Paso {modelo} {sec} {v} {i} ({code})",
            f"{desc} con tecnología de brida roscada de acero templado libre de mantenimiento Weidmüller",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "SeccionNominal": sec, "TensionNominal": v, "CorrienteNominal": i, "Color": col, "TecnologiaConexion": "Tornillo (Brida de apriete)", "Montaje": "Riel DIN TS 35", "Inflamabilidad": "V-0 Wemid"}),
            "Distribución y conexionado de cables en tableros eléctricos de control, fuerza y automatización industrial"
        ))

    # 1.2 Borneras de Tierra de Protección por Tornillo Serie W (WPE)
    pe_blocks = [
        ("1010000000", "WPE 2.5", "2.5 mm²", "Verde/Amarillo", "Bornera de tierra de 2.5 mm² con pie de contacto directo a riel DIN"),
        ("1010100000", "WPE 4", "4 mm²", "Verde/Amarillo", "Bornera de tierra de 4 mm² con fijación mecánica al riel DIN"),
        ("1010200000", "WPE 6", "6 mm²", "Verde/Amarillo", "Bornera de tierra de 6 mm² con contacto a masa"),
        ("1010300000", "WPE 10", "10 mm²", "Verde/Amarillo", "Bornera de tierra industrial de 10 mm²"),
        ("1010400000", "WPE 16", "16 mm²", "Verde/Amarillo", "Bornera de tierra de alta capacidad de 16 mm²"),
        ("1010500000", "WPE 35", "35 mm²", "Verde/Amarillo", "Bornera de tierra para puesta a tierra principal de 35 mm²")
    ]
    for code, modelo, sec, col, desc in pe_blocks:
        items.append((
            brand, line_conn, "Borneras de Tierra de Protección", "Klippon Connect Serie W", code,
            f"Bornera de Tierra {modelo} {sec} PE ({code})",
            f"{desc} con conexión eléctrica y mecánica directa al riel metálico TS 35",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "SeccionNominal": sec, "Color": col, "Funcion": "Puesta a tierra PE", "TecnologiaConexion": "Tornillo con pie a riel", "Montaje": "Riel DIN TS 35"}),
            "Puesta a tierra de seguridad de circuitos derivados y equipotencialidad en cuadros eléctricos"
        ))

    # 1.3 Borneras Seccionables y Portafusibles Serie W (WTR / WSI)
    items.extend([
        (brand, line_conn, "Borneras Seccionables por Cuchilla", "Klippon Connect Serie W", "1855610000",
         "Bornera Seccionable WTR 2.5 por Cuchilla 500V 14A (1855610000)",
         "Bornera seccionable de desconexión por cuchilla pivotante para ensayos y aislamiento rápido de lazos analógicos y de control",
         json.dumps({"Modelo": "WTR 2.5", "CodigoPedido": "1855610000", "SeccionNominal": "2.5 mm²", "TensionNominal": "500V", "CorrienteNominal": "14A", "TipoSeccionamiento": "Cuchilla basculante", "Montaje": "Riel DIN TS 35"}),
         "Aislamiento y calibración de instrumentos de medición, lazos de corriente 4-20mA y señalización"),
        (brand, line_conn, "Borneras Portafusibles", "Klippon Connect Serie W", "1011000000",
         "Bornera Portafusible WSI 6/2 GZ 250V 6.3A (1011000000)",
         "Bornera portafusible con portador basculante para cartuchos de fusible cilíndricos de 5x20 mm o 5x25 mm hasta 6.3A",
         json.dumps({"Modelo": "WSI 6/2 GZ", "CodigoPedido": "1011000000", "SeccionNominal": "6 mm²", "TensionNominal": "250V", "CorrienteNominal": "6.3A", "TipoFusible": "5x20 mm o 5x25 mm", "Montaje": "Riel DIN TS 35"}),
         "Protección selectiva de fuentes de alimentación, electroválvulas y circuitos de control contra sobrecorriente"),
        (brand, line_conn, "Borneras Portafusibles", "Klippon Connect Serie W", "1014000000",
         "Bornera Portafusible WSI 6/2 GZ/LD 250V con LED Indicador (1014000000)",
         "Bornera portafusible con indicador luminoso LED para detección instantánea de fusible fundido en 100-250V AC/DC",
         json.dumps({"Modelo": "WSI 6/2 GZ/LD 250V", "CodigoPedido": "1014000000", "SeccionNominal": "6 mm²", "TensionNominal": "250V AC/DC", "IndicadorFallo": "LED integrado 100-250V", "TipoFusible": "5x20 mm"}),
         "Tableros de control de procesos donde se requiera diagnóstico visual inmediato de fallas de fusible")
    ])

    # 1.4 Borneras de Doble Piso Serie W (WDK)
    items.extend([
        (brand, line_conn, "Borneras de Doble Piso", "Klippon Connect Serie W", "1021500000",
         "Bornera de Doble Piso WDK 2.5 400V 24A (1021500000)",
         "Bornera modular de dos niveles independientes para ahorrar el 50% de espacio en el riel DIN",
         json.dumps({"Modelo": "WDK 2.5", "CodigoPedido": "1021500000", "SeccionNominal": "2.5 mm²", "TensionNominal": "400V", "CorrienteNominal": "24A", "Niveles": 2, "Conexiones": 4}),
         "Cuadros de distribución densos, bornas de entradas/salidas de PLC y concentración de señales"),
        (brand, line_conn, "Borneras de Doble Piso", "Klippon Connect Serie W", "1021600000",
         "Bornera de Doble Piso con Tierra WDK 2.5 PE (1021600000)",
         "Bornera de dos niveles con nivel inferior conectado mecánicamente a tierra PE y nivel superior de paso",
         json.dumps({"Modelo": "WDK 2.5 PE", "CodigoPedido": "1021600000", "SeccionNominal": "2.5 mm²", "NivelSuperior": "Paso 400V 24A", "NivelInferior": "Tierra PE a riel"}),
         "Conexión de sensores, actuadores y mallas de blindaje en automatización industrial")
    ])

    # 1.5 Borneras de Conexión Rápida PUSH IN Serie A (A2C / A3C / A4C)
    push_in_blocks = [
        ("1521850000", "A2C 2.5", "2.5 mm²", "800V", "24A", 2, "Bornera de paso PUSH IN de 2 conexiones 2.5 mm² inserción directa"),
        ("1521990000", "A3C 2.5", "2.5 mm²", "800V", "24A", 3, "Bornera de paso PUSH IN de 3 conexiones 2.5 mm² para bifurcación"),
        ("1522130000", "A4C 2.5", "2.5 mm²", "800V", "24A", 4, "Bornera de paso PUSH IN de 4 conexiones 2.5 mm² para distribución"),
        ("2051180000", "A2C 4", "4 mm²", "800V", "32A", 2, "Bornera PUSH IN de 2 conexiones 4 mm²"),
        ("2051360000", "A3C 4", "4 mm²", "800V", "32A", 3, "Bornera PUSH IN de 3 conexiones 4 mm²"),
        ("2051560000", "A2C 6", "6 mm²", "800V", "41A", 2, "Bornera PUSH IN de 2 conexiones 6 mm²"),
        ("2051740000", "A2C 10", "10 mm²", "1000V", "57A", 2, "Bornera PUSH IN de 2 conexiones 10 mm²"),
        ("2051900000", "A2C 16", "16 mm²", "1000V", "76A", 2, "Bornera PUSH IN de 2 conexiones 16 mm²"),
        ("1521680000", "A2C 2.5 PE", "2.5 mm²", "PE", "PE", 2, "Bornera de tierra PUSH IN 2.5 mm² Verde/Amarillo"),
        ("2051250000", "A2C 4 PE", "4 mm²", "PE", "PE", 2, "Bornera de tierra PUSH IN 4 mm² Verde/Amarillo"),
        ("2051630000", "A2C 6 PE", "6 mm²", "PE", "PE", 2, "Bornera de tierra PUSH IN 6 mm² Verde/Amarillo")
    ]
    for code, modelo, sec, v, i, conns, desc in push_in_blocks:
        items.append((
            brand, line_conn, "Borneras PUSH IN Serie A", "Klippon Connect Serie A", code,
            f"Bornera PUSH IN {modelo} {sec} ({code})",
            f"{desc} con pulsador de accionamiento de color que previene aperturas accidentales y acelera el cableado en 50%",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "SeccionNominal": sec, "TensionNominal": v, "CorrienteNominal": i, "Conexiones": conns, "TecnologiaConexion": "PUSH IN resorte directo", "Montaje": "Riel DIN TS 35"}),
            "Tableros de control de alta vibración, maquinaria móvil y cableado de alta velocidad en líneas de producción"
        ))

    # 1.6 Borneras con Tecnología SNAP IN Serie AS (Inserción Directa de Hilos Flexibles sin Puntera)
    snap_in_blocks = [
        ("2674400000", "AS2C 2.5", "2.5 mm²", "800V", "24A", "Bornera SNAP IN unipolar 2.5 mm² lista para cablear en estado abierto"),
        ("2674430000", "AS2C 4", "4 mm²", "800V", "32A", "Bornera SNAP IN unipolar 4 mm² con disparo audible al insertar el conductor"),
        ("2674410000", "AS2C 2.5 PE", "2.5 mm²", "PE", "PE", "Bornera de tierra SNAP IN 2.5 mm² con contacto automático")
    ]
    for code, modelo, sec, v, i, desc in snap_in_blocks:
        items.append((
            brand, line_conn, "Borneras SNAP IN Serie AS", "Klippon Connect Serie AS", code,
            f"Bornera SNAP IN {modelo} {sec} ({code})",
            f"{desc} que permite conectar cables flexibles pelados sin crimpar terminales virola mediante trinquete precargado",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "SeccionNominal": sec, "TensionNominal": v, "CorrienteNominal": i, "TecnologiaConexion": "SNAP IN revolucionaria", "Certificacion": "IEC 60947-7-1"}),
            "Cableado automatizado con robots y montaje ultrarrápido sin herramientas en armarios eléctricos industriales"
        ))

    # 1.7 Accesorios Esenciales de Borneras (Tapas, Topes y Puentes ZQV)
    items.extend([
        (brand, line_conn, "Tapas Finales de Cierre", "Accesorios Klippon Connect", "1050000000",
         "Tapa Final de Cierre WAP 2.5-10 Beige (1050000000)",
         "Placa de cierre y partición para aislamiento lateral seguro de borneras serie WDU de 2.5 a 10 mm²",
         json.dumps({"Modelo": "WAP 2.5-10", "CodigoPedido": "1050000000", "Espesor": "1.5 mm", "Color": "Beige", "Compatibilidad": "WDU 2.5, WDU 4, WDU 6, WDU 10"}),
         "Aislamiento de la última bornera de una regleta y separación de niveles de tensión"),
        (brand, line_conn, "Tapas Finales de Cierre", "Accesorios Klippon Connect", "1521530000",
         "Tapa Final de Cierre AEP 2C 2.5 Serie A (1521530000)",
         "Placa de cierre de poliamida Wemid para borneras PUSH IN serie A2C 2.5",
         json.dumps({"Modelo": "AEP 2C 2.5", "CodigoPedido": "1521530000", "Espesor": "2.1 mm", "Color": "Gris oscuro", "Compatibilidad": "A2C 2.5, A2C 2.5 PE"}),
         "Cierre lateral de regletas de bornes serie A"),
        (brand, line_conn, "Topes de Fijación Final", "Accesorios Klippon Connect", "1059000000",
         "Tope de Fijación Final WEW 35/2 para Riel DIN (1059000000)",
         "Soporte extremo de retención mecánica con fijación por tornillo para inmovilizar grupos de bornas en riel TS 35",
         json.dumps({"Modelo": "WEW 35/2", "CodigoPedido": "1059000000", "Ancho": "8 mm", "Material": "Wemid aislante", "Riel": "TS 35 x 7.5 / TS 35 x 15"}),
         "Fijación en ambos extremos de regletas de bornas para evitar desplazamientos por vibración"),
        (brand, line_conn, "Topes de Fijación Final", "Accesorios Klippon Connect", "1991920000",
         "Tope de Fijación Final Sin Tornillos AEB 35 SC/1 (1991920000)",
         "Tope de sujeción rápida a presión sin tornillo para riel DIN TS 35 serie Klippon Connect",
         json.dumps({"Modelo": "AEB 35 SC/1", "CodigoPedido": "1991920000", "Montaje": "A presión sin herramientas", "Riel": "TS 35"}),
         "Montaje rápido de topes de extremo en tableros de control"),
        (brand, line_conn, "Puentes Transversales Enchufables", "Accesorios Klippon Connect", "1608860000",
         "Puente Transversal Enchufable ZQV 2.5/2 de 2 Polos (1608860000)",
         "Puente conector aislado de 2 polos para conexión transversal de bornas de 2.5 mm² hasta 24A",
         json.dumps({"Modelo": "ZQV 2.5/2", "CodigoPedido": "1608860000", "Polos": 2, "CorrienteNominal": "24A", "Paso": "5.1 mm"}),
         "Puenteo y distribución de potencial entre borneras adyacentes"),
        (brand, line_conn, "Puentes Transversales Enchufables", "Accesorios Klippon Connect", "1608940000",
         "Puente Transversal Enchufable ZQV 2.5/10 de 10 Polos (1608940000)",
         "Puente de conexión transversal de 10 polos fraccionable para distribución de polaridades y alimentación común",
         json.dumps({"Modelo": "ZQV 2.5/10", "CodigoPedido": "1608940000", "Polos": 10, "CorrienteNominal": "24A", "Paso": "5.1 mm"}),
         "Distribución de 24V DC o neutro común a lo largo de 10 bornas seguidas"),
        (brand, line_conn, "Puentes Transversales Enchufables", "Accesorios Klippon Connect", "1609140000",
         "Puente Transversal Enchufable ZQV 4/2 de 2 Polos (1609140000)",
         "Puente transversal aislado para borneras de 4 mm² hasta 32A",
         json.dumps({"Modelo": "ZQV 4/2", "CodigoPedido": "1609140000", "Polos": 2, "CorrienteNominal": "32A", "Paso": "6.1 mm"}),
         "Puenteo de bornas de 4 mm²"),
        (brand, line_conn, "Puentes Transversales Enchufables", "Accesorios Klippon Connect", "1609200000",
         "Puente Transversal Enchufable ZQV 4/10 de 10 Polos (1609200000)",
         "Puente transversal de 10 polos para borneras de 4 mm² hasta 32A",
         json.dumps({"Modelo": "ZQV 4/10", "CodigoPedido": "1609200000", "Polos": 10, "CorrienteNominal": "32A"}),
         "Distribución común de fuerza o control en bornas de 4 mm²")
    ])

    # =========================================================================
    # 2. LÍNEA: FUENTES DE PODER Y GESTIÓN DC
    # Ref: Catalogue 4.3 Power supplies Version 2024
    # =========================================================================
    line_pwr = "Fuentes de Alimentación y Gestión DC"

    # 2.1 Fuentes Conmutadas de Alta Gama PROtop (DCL Technology, 95% eficiencia)
    protop_models = [
        ("2466870000", "PRO TOP1 120W 24V 5A", "Monofásica 85-277V AC", "24V DC", "5A", "120W", "Fuente conmutada premium PROtop monofásica 24V 5A con reserva dinámica DCL"),
        ("2466880000", "PRO TOP1 240W 24V 10A", "Monofásica 85-277V AC", "24V DC", "10A", "240W", "Fuente conmutada premium PROtop monofásica 24V 10A con tecnología DCL"),
        ("2466890000", "PRO TOP1 480W 24V 20A", "Monofásica 85-277V AC", "24V DC", "20A", "480W", "Fuente conmutada premium PROtop monofásica 24V 20A de alta capacidad"),
        ("2466900000", "PRO TOP1 960W 24V 40A", "Monofásica 85-277V AC", "24V DC", "40A", "960W", "Fuente conmutada premium PROtop monofásica 24V 40A para grandes demandas"),
        ("2467000000", "PRO TOP3 240W 24V 10A", "Trifásica 3x 320-575V AC", "24V DC", "10A", "240W", "Fuente conmutada trifásica PROtop 24V 10A equilibrada"),
        ("2467010000", "PRO TOP3 480W 24V 20A", "Trifásica 3x 320-575V AC", "24V DC", "20A", "480W", "Fuente conmutada trifásica PROtop 24V 20A industrial"),
        ("2467020000", "PRO TOP3 960W 24V 40A", "Trifásica 3x 320-575V AC", "24V DC", "40A", "960W", "Fuente conmutada trifásica PROtop 24V 40A de máxima potencia industrial")
    ]
    for code, modelo, vin, vout, iout, pwr, desc in protop_models:
        items.append((
            brand, line_pwr, "Fuentes Conmutadas Premium PROtop", "Serie PROtop", code,
            f"Fuente de Poder {modelo} ({code})",
            f"{desc} con limitación dinámica de corriente DCL (300% durante 20ms o 150% durante 5s) para arranque de motores y cargas capacitivas",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "TensionEntrada": vin, "TensionSalida": vout, "CorrienteSalida": iout, "Potencia": pwr, "Eficiencia": "> 95%", "MTBF": "> 1.000.000 h", "Comunicacion": "Conectable a IO-Link / CANopen"}),
            "Alimentación ininterrumpida de plantas de proceso crítico, robots, centros de datos y sistemas SCADA"
        ))

    # 2.2 Fuentes Conmutadas de Rendimiento Industrial PROmax
    promax_models = [
        ("1478100000", "PRO MAX 72W 24V 3A", "Monofásica 85-277V AC", "24V DC", "3A", "72W"),
        ("1478110000", "PRO MAX 120W 24V 5A", "Monofásica 85-277V AC", "24V DC", "5A", "120W"),
        ("1478130000", "PRO MAX 240W 24V 10A", "Monofásica 85-277V AC", "24V DC", "10A", "240W"),
        ("1478140000", "PRO MAX 480W 24V 20A", "Monofásica 85-277V AC", "24V DC", "20A", "480W"),
        ("1478150000", "PRO MAX 960W 24V 40A", "Monofásica 85-277V AC", "24V DC", "40A", "960W"),
        ("1478180000", "PRO MAX3 480W 24V 20A", "Trifásica 3x 320-575V AC", "24V DC", "20A", "480W"),
        ("1478190000", "PRO MAX3 960W 24V 40A", "Trifásica 3x 320-575V AC", "24V DC", "40A", "960W")
    ]
    for code, modelo, vin, vout, iout, pwr in promax_models:
        items.append((
            brand, line_pwr, "Fuentes Conmutadas Industriales PROmax", "Serie PROmax", code,
            f"Fuente de Poder Industrial {modelo} ({code})",
            f"Fuente conmutada robusta en riel DIN capaz de sobrecarga continua del 120% hasta 45°C y picos de 300%",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "TensionEntrada": vin, "TensionSalida": vout, "CorrienteSalida": iout, "Potencia": pwr, "SobrecargaContinua": "120% Boost continuo", "Montaje": "Riel DIN TS 35"}),
            "Automatización de maquinaria de envasado, plantas petroquímicas y tableros de control industrial"
        ))

    # 2.3 Fuentes Estándar Compactas PRObas
    probas_models = [
        ("2612050000", "PRO BAS 60W 24V 2.5A", "Monofásica 85-264V AC", "24V DC", "2.5A", "60W"),
        ("2612060000", "PRO BAS 120W 24V 5A", "Monofásica 85-264V AC", "24V DC", "5A", "120W"),
        ("2612070000", "PRO BAS 240W 24V 10A", "Monofásica 85-264V AC", "24V DC", "10A", "240W"),
        ("2612080000", "PRO BAS 480W 24V 20A", "Monofásica 85-264V AC", "24V DC", "20A", "480W")
    ]
    for code, modelo, vin, vout, iout, pwr in probas_models:
        items.append((
            brand, line_pwr, "Fuentes Conmutadas Estándar PRObas", "Serie PRObas", code,
            f"Fuente de Poder {modelo} ({code})",
            f"Fuente conmutada compacta y económica para armarios estándar con alta eficiencia y confiabilidad Weidmüller",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "TensionEntrada": vin, "TensionSalida": vout, "CorrienteSalida": iout, "Potencia": pwr, "Montaje": "Riel DIN TS 35"}),
            "Tableros de distribución de edificios, climatización y maquinaria estándar"
        ))

    # 2.4 Sistema Electrónico de Monitorización y Reparto de Carga maxGUARD
    maxguard_items = [
        ("2081870000", "AMG FIM-0", "Módulo de Alimentación maxGUARD", "Módulo principal de entrada de 24V DC hasta 40A para alimentar la regleta maxGUARD", json.dumps({"Modelo": "AMG FIM-0", "CodigoPedido": "2081870000", "Tension": "24V DC", "CorrienteEntrada": "Hasta 40A", "SeccionCable": "16 mm² PUSH IN"})),
        ("2081880000", "AMG FIM-C", "Módulo de Alimentación con IO-Link", "Módulo de alimentación maxGUARD con puerto de comunicación digital IO-Link para monitorización remota", json.dumps({"Modelo": "AMG FIM-C", "CodigoPedido": "2081880000", "Protocolo": "IO-Link", "Monitoreo": "Tensión, corriente, estados de canal"})),
        ("2082010000", "AMG ELM-1F", "Disyuntor Electrónico 1A", "Disyuntor electrónico de 1 canal fijo de 1A con desconexión selectiva ultra-rápida ante sobrecarga", json.dumps({"Modelo": "AMG ELM-1F", "CodigoPedido": "2082010000", "CorrienteNominal": "1A Fija", "Tension": "24V DC", "Desconexion": "Electrónica selectiva"})),
        ("2082020000", "AMG ELM-2F", "Disyuntor Electrónico 2A", "Disyuntor electrónico de 1 canal fijo de 2A para protección de sensores y PLCs", json.dumps({"Modelo": "AMG ELM-2F", "CodigoPedido": "2082020000", "CorrienteNominal": "2A Fija", "Tension": "24V DC"})),
        ("2082040000", "AMG ELM-4F", "Disyuntor Electrónico 4A", "Disyuntor electrónico de 1 canal fijo de 4A para protección de electroválvulas y cargas DC", json.dumps({"Modelo": "AMG ELM-4F", "CodigoPedido": "2082040000", "CorrienteNominal": "4A Fija", "Tension": "24V DC"})),
        ("2082060000", "AMG ELM-6F", "Disyuntor Electrónico 6A", "Disyuntor electrónico de 1 canal fijo de 6A", json.dumps({"Modelo": "AMG ELM-6F", "CodigoPedido": "2082060000", "CorrienteNominal": "6A Fija", "Tension": "24V DC"})),
        ("2082100000", "AMG ELM-10F", "Disyuntor Electrónico 10A", "Disyuntor electrónico de 1 canal fijo de 10A para alimentadores de campo", json.dumps({"Modelo": "AMG ELM-10F", "CodigoPedido": "2082100000", "CorrienteNominal": "10A Fija", "Tension": "24V DC"})),
        ("2082440000", "AMG ELM-12", "Disyuntor Electrónico Regulable 1-12A", "Disyuntor electrónico multirango ajustable mediante selector rotativo de 1A a 12A", json.dumps({"Modelo": "AMG ELM-12", "CodigoPedido": "2082440000", "RangoAjuste": "1A a 12A regulable", "Tension": "24V DC"})),
        ("2122930000", "AMG DIS", "Bornera de Reparto Positivo", "Bornera repartidora de potencial positivo integrada directamente en la fila maxGUARD", json.dumps({"Modelo": "AMG DIS", "CodigoPedido": "2122930000", "Potencial": "+24V DC", "Conexion": "PUSH IN"})),
        ("2122940000", "AMG OD", "Bornera de Reparto Masa 0V", "Bornera repartidora de potencial de retorno 0V para masa común", json.dumps({"Modelo": "AMG OD", "CodigoPedido": "2122940000", "Potencial": "0V DC", "Conexion": "PUSH IN"}))
    ]
    for code, modelo, nom, desc, specs in maxguard_items:
        items.append((
            brand, line_pwr, "Distribución Electrónica maxGUARD", "Sistema maxGUARD", code,
            f"{nom} {modelo} ({code})",
            f"{desc}. Combina en una única solución compacta la bornera de distribución y el fusible electrónico ahorrando hasta 50% de espacio.",
            specs,
            "Protección selectiva de ramas de 24V DC en maquinaria industrial, evitando la caída general de la fuente ante cortocircuito en un sensor"
        ))

    # 2.5 Módulos de Redundancia y Diodos
    items.extend([
        (brand, line_pwr, "Módulos de Redundancia", "Serie PRO RM", "2467140000",
         "Módulo de Redundancia Activo PRO RM 20 (2467140000)",
         "Módulo de redundancia activo con tecnología MOSFET para desacoplamiento sin pérdidas de dos fuentes de 24V hasta 2x20A o 1x40A",
         json.dumps({"Modelo": "PRO RM 20", "CodigoPedido": "2467140000", "TensionEntrada": "24V DC (10-32V)", "CorrienteNominal": "2x 20A o 1x 40A", "Tecnologia": "MOSFETs activos (mínima caída de tensión)"}),
         "Sistemas de alta disponibilidad 24/7 donde una fuente de respaldo asume la carga si la principal falla"),
        (brand, line_pwr, "Módulos de Redundancia", "Serie PRO RM", "2467150000",
         "Módulo de Redundancia Activo PRO RM 40 (2467150000)",
         "Módulo de redundancia activo de alta potencia para dos fuentes de hasta 2x40A o 1x80A",
         json.dumps({"Modelo": "PRO RM 40", "CodigoPedido": "2467150000", "CorrienteNominal": "2x 40A o 1x 80A", "Tecnologia": "MOSFETs"}),
         "Cuadros de distribución de control en plantas químicas, centrales eléctricas y refinerías"),
        (brand, line_pwr, "Módulos de Desacoplo por Diodos", "Serie PRO DM", "1222210000",
         "Módulo de Diodos PRO DM 20 (1222210000)",
         "Módulo de diodos pasivo para desacoplo de dos fuentes de alimentación de 24V DC hasta 2x20A",
         json.dumps({"Modelo": "PRO DM 20", "CodigoPedido": "1222210000", "Tension": "24V DC", "Corriente": "2x 20A"}),
         "Redundancia básica económica para alimentación de seguridad")
    ])

    # 2.6 Sistemas SAI / DC-UPS y Módulos de Batería
    items.extend([
        (brand, line_pwr, "Sistemas UPS en Corriente Continua", "Serie DC-UPS", "1370050000",
         "Módulo de Control DC-UPS CP DC UPS 24V 20A (1370050000)",
         "Unidad de control y gestión inteligente de carga de baterías para respaldo ininterrumpido en 24V DC hasta 20A",
         json.dumps({"Modelo": "CP DC UPS 24V 20A", "CodigoPedido": "1370050000", "Tension": "24V DC", "CorrienteCarga": "20A", "GestionBaterias": "Carga compensada por temperatura y diagnóstico continuo"}),
         "Garantizar el funcionamiento continuo de PLCs, pantallas HMI y comunicaciones ante cortes de energía"),
        (brand, line_pwr, "Módulos de Baterías AGM", "Serie DC-UPS", "1406930000",
         "Módulo de Baterías AGM 24V DC 3.4Ah (1406930000)",
         "Batería recargable de plomo-ácido regulada por válvula (VRLA/AGM) en chasis para riel DIN 24V 3.4Ah",
         json.dumps({"Modelo": "BATTERY 24V DC 3.4AH", "CodigoPedido": "1406930000", "Tension": "24V DC", "Capacidad": "3.4 Ah", "Montaje": "Riel DIN TS 35"}),
         "Respaldo de energía para apagado seguro de servidores y controladores industriales"),
        (brand, line_pwr, "Módulos de Baterías AGM", "Serie DC-UPS", "1406940000",
         "Módulo de Baterías AGM 24V DC 7.2Ah (1406940000)",
         "Batería recargable industrial para riel DIN 24V 7.2Ah para mayor autonomía",
         json.dumps({"Modelo": "BATTERY 24V DC 7.2AH", "CodigoPedido": "1406940000", "Tension": "24V DC", "Capacidad": "7.2 Ah"}),
         "Autonomía prolongada de sistemas de control y telemetría remota")
    ])

    # =========================================================================
    # 3. LÍNEA: RELÉS Y OPTOACOPLADORES (KLIPPON RELAY)
    # Ref: Catalogue 4.2 Relays and solid-state relays Klippon Relay
    # =========================================================================
    line_relay = "Relés y Optoacopladores"

    # 3.1 Relés de Interface Ultradelgados TERMSERIES (Ancho 6.4 mm)
    termseries_relays = [
        ("1122770000", "TRS 24VDC 1CO", "24V DC", "1 Contacto Conmutado (1 CO / SPDT)", "6A a 250V AC", "Tornillo", "Relé ultradelgado 6.4mm bobina 24V DC conmutado 6A"),
        ("1122880000", "TRZ 24VDC 1CO", "24V DC", "1 Contacto Conmutado (1 CO / SPDT)", "6A a 250V AC", "PUSH IN", "Relé ultradelgado 6.4mm PUSH IN bobina 24V DC"),
        ("1122790000", "TRS 120VAC/DC 1CO", "120V AC/DC", "1 Contacto Conmutado (1 CO / SPDT)", "6A a 250V AC", "Tornillo", "Relé ultradelgado bobina universal 120V AC/DC"),
        ("1122820000", "TRS 230VAC 1CO", "230V AC", "1 Contacto Conmutado (1 CO / SPDT)", "6A a 250V AC", "Tornillo", "Relé ultradelgado bobina 230V AC para interface"),
        ("1122890000", "TRS 24VDC 2CO", "24V DC", "2 Contactos Conmutados (2 CO / DPDT)", "8A a 250V AC (ancho 12.8mm)", "Tornillo", "Relé compacto doble contacto conmutado 8A"),
        ("1122900000", "TRZ 24VDC 2CO", "24V DC", "2 Contactos Conmutados (2 CO / DPDT)", "8A a 250V AC", "PUSH IN", "Relé compacto doble contacto PUSH IN"),
        ("1123010000", "TRS 230VAC 2CO", "230V AC", "2 Contactos Conmutados (2 CO / DPDT)", "8A a 250V AC", "Tornillo", "Relé compacto bobina 230V AC 2 contactos"),
        ("1127170000", "TOS 24VDC/24VDC 2A", "24V DC", "Estado Sólido Transistor (Optoacoplador)", "2A a 24V DC (silencioso sin desgaste)", "Tornillo", "Relé de estado sólido ultradelgado para alta frecuencia de conmutación")
    ]
    for code, modelo, vcoil, cto, rating, term, desc in termseries_relays:
        items.append((
            brand, line_relay, "Relés de Interface TERMSERIES", "Klippon Relay TERMSERIES", code,
            f"Relé de Interface {modelo} ({code})",
            f"{desc} completo con zócalo, indicador LED de estado, diodo de protección inversa y palanca eyectora",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "Bobina": vcoil, "Contactos": cto, "PoderCorte": rating, "Conexion": term, "Ancho": "6.4 mm (1CO) / 12.8 mm (2CO)", "Montaje": "Riel DIN TS 35"}),
            "Aislamiento galvánico, multiplicación de contactos y acoplamiento de señales entre salidas de PLC y actuadores"
        ))

    # 3.2 Kits de Relés Industriales Enchufables RIDERSERIES (RCI y RCM)
    riderseries_kits = [
        ("8870180000", "RCIKIT 24VDC 2CO LD/PB", "24V DC", "2 CO (DPDT) 8A", "Tornillo", "Kit de relé industrial enchufable 24V DC 2 contactos con pulsador de prueba manual y LED"),
        ("8870230000", "RCIKIT 115VAC 2CO LD/PB", "115V AC", "2 CO (DPDT) 8A", "Tornillo", "Kit de relé industrial enchufable 115V AC 2 contactos con pulsador de prueba"),
        ("8870250000", "RCIKIT 230VAC 2CO LD/PB", "230V AC", "2 CO (DPDT) 8A", "Tornillo", "Kit de relé industrial enchufable 230V AC 2 contactos con pulsador de prueba"),
        ("8870320000", "RCIKITP 24VDC 2CO LD/PB", "24V DC", "2 CO (DPDT) 8A", "PUSH IN", "Kit de relé industrial con base de conexión rápida PUSH IN"),
        ("8921000000", "RCMKIT-I 24VDC 4CO LD", "24V DC", "4 CO (4PDT) 6A", "Tornillo", "Kit de relé industrial enchufable 4 contactos conmutados 24V DC"),
        ("8921030000", "RCMKIT-I 115VAC 4CO LD", "115V AC", "4 CO (4PDT) 6A", "Tornillo", "Kit de relé industrial enchufable 4 contactos conmutados 115V AC"),
        ("8921050000", "RCMKIT-I 230VAC 4CO LD", "230V AC", "4 CO (4PDT) 6A", "Tornillo", "Kit de relé industrial enchufable 4 contactos conmutados 230V AC con LED y diodo")
    ]
    for code, modelo, vcoil, cto, term, desc in riderseries_kits:
        items.append((
            brand, line_relay, "Relés Industriales RIDERSERIES", "Klippon Relay RIDERSERIES", code,
            f"Relé Industrial Enchufable {modelo} ({code})",
            f"{desc}. Incluye relé enchufable, zócalo con clip de retención metálico, módulo LED de protección y palanca de prueba mecánica.",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "Bobina": vcoil, "Contactos": cto, "Conexion": term, "MaterialContactos": "AgNi 90/10", "VidaMecanica": "> 30.000.000 operaciones"}),
            "Conmutación de contactores, electroválvulas pesadas, motores pequeños y circuitos de enclavamiento de seguridad"
        ))

    # =========================================================================
    # 4. LÍNEA: PROTECCIÓN CONTRA SOBRETENSIONES Y DESCARGAS (VPU)
    # Ref: Catalogue 4.4 Lightning and surge protection Version 2024
    # =========================================================================
    line_spd = "Protección contra Sobretensiones (DPS / VPU)"

    # 4.1 Descargadores de Rayos y Sobretensiones Tipo 1+2 (Serie VPU I)
    vpu_i_models = [
        ("2591070000", "VPU I 3 R 280V/25KA", "Tipo 1+2 (Clase I+II)", "3P (Trifásico sin neutro)", "280V AC", "Iimp 25 kA / Imax 100 kA", "Sí (Contacto seco remoto)", "Descargador combinado de rayos y sobretensiones Tipo 1+2 3P 25kA por polo"),
        ("2591080000", "VPU I 4 R 280V/25KA", "Tipo 1+2 (Clase I+II)", "3P+N (Trifásico con neutro)", "280V/400V AC", "Iimp 25 kA / Imax 100 kA", "Sí (Contacto seco remoto)", "Descargador combinado de rayos y sobretensiones Tipo 1+2 4P con vía de chispas N-PE")
    ]
    for code, modelo, tipo, polos, uc, cap, aux, desc in vpu_i_models:
        items.append((
            brand, line_spd, "Protectores Tipo 1+2 Contra Rayos", "Serie VPU I", code,
            f"Protector Combinado Rayos y Sobretensiones {modelo} ({code})",
            f"{desc} para entrada de acometidas en edificios con pararrayos externo según norma IEC 61643-11 y UL 1449",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "Tipo": tipo, "Polos": polos, "TensionMaximaUc": uc, "CapacidadDescarga": cap, "ContactoSenalizacion": aux, "Montaje": "Riel DIN TS 35"}),
            "Acometidas principales de subestaciones, edificios residenciales, plantas industriales y torres de telecomunicaciones"
        ))

    # 4.2 Descargadores de Sobretensiones Transitorias Tipo 2 (Serie VPU II)
    vpu_ii_models = [
        ("2564290000", "VPU II 2 R 280V/40KA", "Tipo 2 (Clase II)", "1P+N (Monofásico)", "280V AC", "Imax 40 kA / In 20 kA", "Sí", "Protector de sobretensiones transitorias monofásico 1P+N 40kA con contacto"),
        ("2564320000", "VPU II 3 280V/40KA", "Tipo 2 (Clase II)", "3P (Trifásico)", "280V AC", "Imax 40 kA / In 20 kA", "No", "Protector de sobretensiones transitorias trifásico 3P 40kA"),
        ("2564330000", "VPU II 3 R 280V/40KA", "Tipo 2 (Clase II)", "3P (Trifásico)", "280V AC", "Imax 40 kA / In 20 kA", "Sí", "Protector de sobretensiones transitorias trifásico 3P 40kA con contacto de alarma"),
        ("2564340000", "VPU II 4 280V/40KA", "Tipo 2 (Clase II)", "3P+N (Tetrapolar)", "280V/400V AC", "Imax 40 kA / In 20 kA", "No", "Protector de sobretensiones transitorias tetrapolar 3P+N 40kA"),
        ("2564350000", "VPU II 4 R 280V/40KA", "Tipo 2 (Clase II)", "3P+N (Tetrapolar)", "280V/400V AC", "Imax 40 kA / In 20 kA", "Sí", "Protector de sobretensiones transitorias tetrapolar 3P+N 40kA con contacto de alarma"),
        ("2564410000", "VPU II 0 280V/40KA", "Tipo 2 (Repuesto)", "Cartucho enchufable", "280V AC", "Imax 40 kA", "Indicador óptico", "Cartucho de varistor de repuesto enchufable para descargador VPU II 280V 40kA")
    ]
    for code, modelo, tipo, polos, uc, cap, aux, desc in vpu_ii_models:
        items.append((
            brand, line_spd, "Protectores Tipo 2 contra Sobretensiones", "Serie VPU II", code,
            f"Protector de Sobretensiones {modelo} ({code})",
            f"{desc} con varistores de óxido metálico de alta energía y desconectador térmico con visor óptico verde/rojo",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "Tipo": tipo, "Polos": polos, "TensionMaximaUc": uc, "Imax": cap, "ContactoRemoto": aux, "Cartuchos": "Enchufables sin herramientas"}),
            "Cuadros generales de distribución secundaria, protección de variadores de frecuencia, PLCs y racks de servidores"
        ))

    # 4.3 Descargadores Solares Fotovoltaicos DC (Serie VPU PV)
    vpu_pv_models = [
        ("2530590000", "VPU PV II 3 R 1000", "Tipo 2 Fotovoltaico", "2 Polos (+/- y PE)", "1000V DC", "Imax 40 kA / In 20 kA", "Sí", "Protector de sobretensiones especializado para sistemas solares fotovoltaicos hasta 1000V DC"),
        ("2530630000", "VPU PV II 3 R 1500", "Tipo 2 Fotovoltaico", "2 Polos (+/- y PE)", "1500V DC", "Imax 40 kA / In 20 kA", "Sí", "Protector de sobretensiones de alta tensión para granjas solares hasta 1500V DC")
    ]
    for code, modelo, tipo, polos, uc, cap, aux, desc in vpu_pv_models:
        items.append((
            brand, line_spd, "Protectores Solares Fotovoltaicos DC", "Serie VPU PV", code,
            f"Protector Solar Fotovoltaico {modelo} ({code})",
            f"{desc} según norma EN 50539-11 y UL 1449 con contacto de tele-señalización para monitorización SCADA",
            json.dumps({"Modelo": modelo, "CodigoPedido": code, "Tipo": tipo, "TensionMaximaDC": uc, "Imax": cap, "ContactoAuxiliar": aux, "Norma": "EN 50539-11 / UL 1449"}),
            "Cajas de combinación de strings fotovoltaicos, inversores solares y huertos fotovoltaicos utility scale"
        ))

    # 4.4 Supresores para Líneas de Datos y Ethernet (VARITECTOR)
    items.extend([
        (brand, line_spd, "Protección de Señales y Datos", "Serie VARITECTOR", "8923400000",
         "Protector de Señal Analógica VSPC 2CL 24VAC (8923400000)",
         "Módulo descargador de sobretensión enchufable para dos lazos analógicos de corriente de 4-20mA sin potencial de tierra",
         json.dumps({"Modelo": "VSPC 2CL 24VAC", "CodigoPedido": "8923400000", "TensionNominal": "24V AC/DC", "TipoSenal": "Lazo 4-20mA 2 hilos", "Norma": "IEC 61643-21"}),
         "Protección de transmisores de presión, nivel, temperatura y tarjetas analógicas de PLC"),
        (brand, line_spd, "Protección de Señales y Datos", "Serie VARITECTOR", "8923430000",
         "Base para Protector de Señal VSPC BASE 2CL (8923430000)",
         "Base de carril DIN con resorte a tierra para alojar cartuchos de protección de señal analógica VSPC",
         json.dumps({"Modelo": "VSPC BASE 2CL", "CodigoPedido": "8923430000", "Montaje": "Riel DIN TS 35"}),
         "Base fija de conexionado para módulos VSPC"),
        (brand, line_spd, "Protección de Redes Ethernet", "Serie VARITECTOR", "1348550000",
         "Protector de Red Ethernet RJ45 VPU II ENERGY RJ45 (1348550000)",
         "Descargador de sobretensiones de alta velocidad para redes Ethernet Cat.6A hasta 10 Gbps con soporte PoE+",
         json.dumps({"Modelo": "VPU II ENERGY RJ45", "CodigoPedido": "1348550000", "Velocidad": "Hasta 10 GBit/s Cat.6A", "PoE": "Compatible IEEE 802.3at (PoE+)", "Conector": "RJ45 blindado hembra/hembra"}),
         "Protección de cámaras IP exteriores, antenas de comunicación y switches industriales")
    ])

    # =========================================================================
    # 5. LÍNEA: ACONDICIONAMIENTO Y AISLAMIENTO DE SEÑALES (ACT20)
    # Ref: Catalogue 4.1 Isolating amplifiers Version 2025
    # =========================================================================
    line_signal = "Acondicionamiento y Aislamiento de Señales"

    signal_converters = [
        ("7760054114", "ACT20P-CI-CO-S", "Aislador de Bucle Pasivo 4-20mA", "Aislador galvánico de bucle analógico 4-20mA autoalimentado de 1 canal con aislamiento de 3 vías de 2 kV", json.dumps({"Modelo": "ACT20P-CI-CO-S", "CodigoPedido": "7760054114", "Entrada": "4-20 mA", "Salida": "4-20 mA", "Alimentacion": "Pasivo por bucle", "Precision": "< 0.1%", "Canales": 1})),
        ("7760054115", "ACT20P-2CI-2CO-S", "Aislador Pasivo de 2 Canales", "Aislador galvánico de bucle analógico pasivo de dos canales independientes en 12.5 mm de ancho", json.dumps({"Modelo": "ACT20P-2CI-2CO-S", "CodigoPedido": "7760054115", "Canales": 2, "Entrada": "2x 4-20 mA", "Salida": "2x 4-20 mA"})),
        ("7760054117", "ACT20P-AI-AO-S", "Convertidor Analógico Universal", "Aislador y convertidor de señal activo universal configurable por interruptores DIP (0-10V, 0-20mA, 4-20mA)", json.dumps({"Modelo": "ACT20P-AI-AO-S", "CodigoPedido": "7760054117", "EntradaConfigurable": "0..10V, 0..20mA, 4..20mA", "SalidaConfigurable": "0..10V, 0..20mA, 4..20mA", "Alimentacion": "24V AC/DC"})),
        ("1176000000", "ACT20M-CI-CO-S", "Aislador Ultradelgado 6mm", "Aislador analógico de señal ultracompacto de tan solo 6 mm de ancho con aislamiento galvánico de 2.5 kV", json.dumps({"Modelo": "ACT20M-CI-CO-S", "CodigoPedido": "1176000000", "Ancho": "6.1 mm", "Entrada": "4-20 mA", "Salida": "4-20 mA", "Canales": 1})),
        ("7760054118", "ACT20P-RTD-60-S", "Transmisor de Temperatura PT100", "Convertidor y transmisor de temperatura para sondas RTD PT100 a señal analógica normalizada 4-20mA", json.dumps({"Modelo": "ACT20P-RTD-60-S", "CodigoPedido": "7760054118", "Sensor": "PT100, PT1000 (2, 3 o 4 hilos)", "Salida": "4..20 mA o 0..10 V", "RangoAjustable": "-200°C a +850°C"})),
        ("7760054119", "ACT20P-TC-S", "Transmisor de Termocuplas", "Convertidor de temperatura universal para termopares (J, K, T, E, N, R, S, B) con compensación de unión fría", json.dumps({"Modelo": "ACT20P-TC-S", "CodigoPedido": "7760054119", "Entrada": "Termocuplas J, K, T, E, R, S", "Salida": "4-20 mA", "Compensacion": "Unión fría interna"}))
    ]
    for code, modelo, nom, desc, specs in signal_converters:
        items.append((
            brand, line_signal, "Convertidores y Aisladores Analógicos", "Serie ACT20", code,
            f"{nom} {modelo} ({code})",
            f"{desc} para eliminación de lazos de tierra, ruido eléctrico y conversión de variables de proceso",
            specs,
            "Tratamiento de señales analógicas en instrumentación de tanques, hornos, molinos y control de bombas"
        ))

    # =========================================================================
    # 6. LÍNEA: HERRAMIENTAS PROFESIONALES DE PRECISIÓN (TOOLS)
    # Ref: Catalogue 6 Tools Version 2026
    # =========================================================================
    line_tools = "Herramientas de Precisión Profesionales"

    tools_list = [
        ("9005000000", "stripax", "Pelacables Profesional stripax 0.08 a 10 mm²", "Herramienta de pelado profesional con cuchillas autoajustables para conductores flexibles y macizos de 0.08 a 10 mm² (AWG 28 a 7)", json.dumps({"Modelo": "stripax", "CodigoPedido": "9005000000", "RangoPelado": "0.08 a 10 mm²", "LongitudPelado": "Hasta 25 mm regulable", "CuchillaCorte": "Integrada hasta 6 mm²", "Peso": "175 g"}), "El estándar de oro mundial para cuadristas, electricistas industriales y ensambladores de tableros"),
        ("9005610000", "stripax 16", "Pelacables Profesional stripax 16 para 6 a 16 mm²", "Herramienta de pelado autoajustable especializada para conductores de gran sección de 6 a 16 mm² (AWG 10 a 6)", json.dumps({"Modelo": "stripax 16", "CodigoPedido": "9005610000", "RangoPelado": "6 a 16 mm²", "LongitudPelado": "Hasta 25 mm"}), "Pelado de cables de alimentación de fuerza y acometidas de potencia en cuadros eléctricos"),
        ("1304950000", "stripax ULtimate", "Pelacables de Alta Resistencia stripax ULtimate", "Pelacables con geometría de cuchilla patentada para aislamientos duros, libres de halógenos y cables de goma PUR/TPE", json.dumps({"Modelo": "stripax ULtimate", "CodigoPedido": "1304950000", "RangoPelado": "0.25 a 12 mm²", "AislamientosEspeciales": "Libres de halógenos, PUR, Teflón, Silicona"}), "Industria ferroviaria, marina, eólica y entornos exigentes"),
        ("9005700000", "AM 25", "Pelacables Circular AM 25 para Mangueras", "Herramienta de desaislado de cubiertas exteriores de cables y mangueras redondas de 4.5 a 25 mm de diámetro con corte espiral y longitudinal", json.dumps({"Modelo": "AM 25", "CodigoPedido": "9005700000", "DiametroCable": "4.5 a 25 mm", "ProfundidadCorte": "Regulable hasta 4.5 mm"}), "Desenvainado de cables multipolares y mangueras de control"),
        ("9014350000", "PZ 6 Roto", "Tenaza de Crimpar PZ 6 Roto 0.14 a 6 mm²", "Tenaza de crimpado de virolas con cabezal giratorio 360° para inserción frontal o lateral de terminales huecos", json.dumps({"Modelo": "PZ 6 Roto", "CodigoPedido": "9014350000", "RangoCrimpar": "0.14 a 6 mm² (AWG 26 a 10)", "PerfilCrimpar": "Trapezoidal profesional", "Cabezal": "Giratorio en 8 posiciones"}), "Crimpado ergonómico de terminales puntera en armarios de espacio reducido"),
        ("1444050000", "PZ 6 Roto L", "Tenaza de Crimpar PZ 6 Roto L con Bloqueo", "Tenaza de crimpar de virolas con bloqueo forzado desclavable para asegurar crimpados estandarizados según DIN 46228", json.dumps({"Modelo": "PZ 6 Roto L", "CodigoPedido": "1444050000", "RangoCrimpar": "0.14 a 6 mm²", "BloqueoSeguridad": "Integrado para ciclo completo"}), "Fabricación en serie de tableros con certificación internacional"),
        ("9012600000", "PZ 16", "Tenaza de Crimpar PZ 16 para 6 a 16 mm²", "Tenaza de crimpado para virolas con y sin aislamiento plástico de 6, 10 y 16 mm²", json.dumps({"Modelo": "PZ 16", "CodigoPedido": "9012600000", "RangoCrimpar": "6 a 16 mm²", "Perfil": "Indent"}), "Conexión de terminales de fuerza y alimentadores principales"),
        ("9005990000", "PZ 50", "Tenaza de Crimpar PZ 50 para 25 a 50 mm²", "Tenaza de gran capacidad para crimpado de terminales puntera de 25, 35 y 50 mm²", json.dumps({"Modelo": "PZ 50", "CodigoPedido": "9005990000", "RangoCrimpar": "25 a 50 mm²"}), "Crimpado de acometidas principales de tableros de potencia"),
        ("9002650000", "KT 8", "Cortacables de Precisión KT 8 hasta 8 mm", "Tijera cortacables de cuchillas especiales de acero templado para corte limpio sin aplastamiento de cables de cobre y aluminio hasta 8 mm (16 mm²)", json.dumps({"Modelo": "KT 8", "CodigoPedido": "9002650000", "DiametroMaximo": "8 mm", "SeccionMaximaCu": "16 mm²", "Longitud": "165 mm"}), "Corte exacto y sin deformación de conductores antes de pelar y crimpar"),
        ("9002660000", "KT 12", "Cortacables de Precisión KT 12 hasta 12 mm", "Cortacables profesional para conductores de cobre hasta 12 mm de diámetro exterior o 35 mm²", json.dumps({"Modelo": "KT 12", "CodigoPedido": "9002660000", "DiametroMaximo": "12 mm", "SeccionMaximaCu": "35 mm²"}), "Corte de cables de alimentación en talleres y obras eléctricas"),
        ("1157830000", "KT 22", "Cortacables a Dos Manos KT 22 hasta 22 mm", "Cortacables manual de alta palanca para cables de fuerza de cobre y aluminio hasta 22 mm de diámetro o 95 mm²", json.dumps({"Modelo": "KT 22", "CodigoPedido": "1157830000", "DiametroMaximo": "22 mm", "SeccionMaximaCu": "95 mm²", "Longitud": "220 mm"}), "Instalaciones eléctricas industriales de potencia"),
        ("9008390000", "SDI 0.6x3.5x100", "Destornillador Plano Aislado 1000V VDE", "Destornillador plano de precisión aislado a 1000V según EN/IEC 60900 para apriete seguro de borneras WDU 2.5", json.dumps({"Modelo": "SDI 0.6x3.5x100", "CodigoPedido": "9008390000", "Punta": "Plana 0.6 x 3.5 mm", "Varilla": "100 mm", "Aislamiento": "1000V VDE / GS"}), "Mantenimiento y apriete en cuadros con presencia de tensión"),
        ("9008400000", "SDI 0.8x4.0x100", "Destornillador Plano Aislado 1000V VDE", "Destornillador plano aislado para borneras WDU 4 y WDU 6", json.dumps({"Modelo": "SDI 0.8x4.0x100", "CodigoPedido": "9008400000", "Punta": "Plana 0.8 x 4.0 mm", "Varilla": "100 mm", "Aislamiento": "1000V VDE"}), "Montaje de armarios eléctricos"),
        ("9008570000", "SDIK PH1", "Destornillador Phillips PH1 Aislado 1000V", "Destornillador de cruz Phillips PH1 con aislamiento homologado a 1000V", json.dumps({"Modelo": "SDIK PH1", "CodigoPedido": "9008570000", "Punta": "Phillips PH1", "Varilla": "80 mm", "Aislamiento": "1000V VDE"}), "Apriete de relés, contactores y fuentes de alimentación"),
        ("9008580000", "SDIK PH2", "Destornillador Phillips PH2 Aislado 1000V", "Destornillador de cruz Phillips PH2 aislado a 1000V", json.dumps({"Modelo": "SDIK PH2", "CodigoPedido": "9008580000", "Punta": "Phillips PH2", "Varilla": "100 mm", "Aislamiento": "1000V VDE"}), "Apriete de disyuntores y bornas de potencia"),
        ("9918390000", "DMS 3", "Destornillador Dinamométrico Ajustable DMS 3", "Destornillador dinamométrico con escala graduada de ajuste de par de apriete de 0.5 a 1.7 Nm con disparo automático", json.dumps({"Modelo": "DMS 3", "CodigoPedido": "9918390000", "RangoPar": "0.5 a 1.7 Nm regulable", "Precision": "+/- 6%", "Portapuntas": "1/4 pulgada con bloqueo"}), "Garantizar el torque exacto exigido por los fabricantes en borneras para evitar incendios por falso contacto")
    ]
    for code, modelo, nom, desc, specs, app in tools_list:
        items.append((
            brand, line_tools, "Herramientas de Precisión", "Herramientas Weidmüller", code,
            f"{nom} ({code})",
            f"{desc} fabricada bajo los más altos estándares de ergonomía y durabilidad alemana",
            specs,
            app
        ))

    # =========================================================================
    # 7. LÍNEA: ETHERNET INDUSTRIAL Y COMUNICACIONES
    # Ref: Catalogue 9 Industrial Ethernet Version 2026
    # =========================================================================
    line_eth = "Ethernet Industrial y Comunicaciones"

    eth_switches = [
        ("1240840000", "IE-SW-BL05-5TX", "Switch Industrial No Gestionado 5 Puertos Fast Ethernet", "Switch para riel DIN con 5 puertos RJ45 10/100BaseT(X), carcasa metálica de aluminio IP30 y rango de temperatura de -10 a 60°C", json.dumps({"Modelo": "IE-SW-BL05-5TX", "CodigoPedido": "1240840000", "Puertos": "5x RJ45 10/100BaseT(X)", "TensionAlimentacion": "12/24/48V DC o 18-30V AC", "GradoProteccion": "IP30", "Montaje": "Riel DIN TS 35"}), "Redes de automatización de planta, interconexión de PLCs, pantallas HMI y módulos E/S remotos"),
        ("1240900000", "IE-SW-BL08-8TX", "Switch Industrial No Gestionado 8 Puertos Fast Ethernet", "Switch para riel DIN con 8 puertos RJ45 10/100BaseT(X) con detección automática de velocidad y cruce MDI/MDI-X", json.dumps({"Modelo": "IE-SW-BL08-8TX", "CodigoPedido": "1240900000", "Puertos": "8x RJ45 10/100BaseT(X)", "Tension": "24V DC", "GradoProteccion": "IP30"}), "Concentración de equipos de red en armarios de control principales"),
        ("1241250000", "IE-SW-BL05-5GT", "Switch Industrial No Gestionado 5 Puertos Gigabit", "Switch Gigabit para riel DIN con 5 puertos 10/100/1000BaseT(X) de alta velocidad para transmisión intensiva de datos", json.dumps({"Modelo": "IE-SW-BL05-5GT", "CodigoPedido": "1241250000", "Puertos": "5x Gigabit RJ45", "Velocidad": "10/100/1000 Mbps", "JumboFrames": "Hasta 9 KB"}), "Sistemas de visión artificial, servidores industriales y telemetría de alta velocidad"),
        ("1241270000", "IE-SW-BL08-8GT", "Switch Industrial No Gestionado 8 Puertos Gigabit", "Switch Gigabit de 8 puertos RJ45 para comunicación sin cuellos de botella", json.dumps({"Modelo": "IE-SW-BL08-8GT", "CodigoPedido": "1241270000", "Puertos": "8x Gigabit RJ45", "Tension": "12/24/48V DC"}), "Redes troncales de fábrica y cámaras de seguridad IP"),
        ("2682130000", "IE-SW-EL05-5TX", "Switch Ultracompacto EcoLine 5 Puertos", "Switch industrial ultra-delgado serie EcoLine de 5 puertos RJ45 ideal para cuadros pequeños de distribución", json.dumps({"Modelo": "IE-SW-EL05-5TX", "CodigoPedido": "2682130000", "Puertos": "5x 10/100BaseT(X)", "Ancho": "22.5 mm ultracompacto"}), "Cajas de control descentralizadas y maquinaria con espacio reducido"),
        ("2682140000", "IE-SW-EL08-8TX", "Switch Ultracompacto EcoLine 8 Puertos", "Switch industrial EcoLine de 8 puertos RJ45 para integración rápida", json.dumps({"Modelo": "IE-SW-EL08-8TX", "CodigoPedido": "2682140000", "Puertos": "8x 10/100BaseT(X)", "Ancho": "30 mm"}), "Distribución de red en maquinaria de empaque"),
        ("1241070000", "IE-SW-AL08-8TX", "Switch Gestionado AdvancedLine 8 Puertos", "Switch industrial gestionado con 8 puertos RJ45, soporte de redundancia en anillo Turbo Ring, VLANs, QoS y SNMP", json.dumps({"Modelo": "IE-SW-AL08-8TX", "CodigoPedido": "1241070000", "Gestion": "Web / SNMP / CLI", "FuncionesAvanzadas": "VLAN, QoS, IGMP Snooping, Anillo redundante < 20ms", "Puertos": "8x RJ45"}), "Redes de misión crítica donde se requiera diagnóstico avanzado y topologías en anillo redundante"),
        ("1962840000", "IE-PS-RJ45-FH-BK", "Conector RJ45 Industrial Ensamble en Campo", "Conector RJ45 apantallado Cat.6A para montaje en campo sin herramientas de crimpado (tecnología IDC de desplazamiento de aislante)", json.dumps({"Modelo": "IE-PS-RJ45-FH-BK", "CodigoPedido": "1962840000", "Categoria": "Cat.6A / 10 Gbps", "Montaje": "En campo sin herramientas (IDC)", "Blindaje": "360° metálico fundido"}), "Confección inmediata de cables Ethernet industrial de longitud exacta en obra"),
        ("8808450000", "IE-C5DB4RE0010MCSMCS-E", "Latiguillo Ethernet M12 a M12 1m", "Cable preensamblado industrial Ethernet de 1 metro con conectores circulares M12 codificación D IP67", json.dumps({"Modelo": "IE-C5DB4RE0010MCSMCS-E", "CodigoPedido": "8808450000", "Conectores": "M12 macho recto a M12 macho recto", "Longitud": "1.0 m", "GradoProteccion": "IP67"}), "Conexión de sensores y cajas de distribución descentralizadas en intemperie o lavado a presión")
    ]
    for code, modelo, nom, desc, specs, app in eth_switches:
        items.append((
            brand, line_eth, "Switches y Conectividad Ethernet", "Industrial Ethernet Weidmüller", code,
            f"{nom} ({code})",
            desc,
            specs,
            app
        ))

    # =========================================================================
    # 8. LÍNEA: AUTOMATIZACIÓN Y E/S REMOTAS (U-REMOTE)
    # Ref: Catalogue 10 Automation and Software tools Version 2026
    # =========================================================================
    line_auto = "Automatización y E/S Remotas"

    uremote_modules = [
        ("1334910000", "UR20-FBC-PN-IRT", "Acoplador de Bus u-remote Profinet IRT", "Módulo cabecera de bus de campo para redes Profinet IRT con switch integrado de 2 puertos y servidor web de diagnóstico", json.dumps({"Modelo": "UR20-FBC-PN-IRT", "CodigoPedido": "1334910000", "Protocolo": "Profinet RT/IRT", "Puertos": "2x RJ45", "CapacidadModulos": "Hasta 64 módulos de E/S", "ServidorWeb": "Integrado para pruebas en línea"}), "Integración de islas de E/S remotas con autómatas Siemens S7-1200 / S7-1500"),
        ("1334930000", "UR20-FBC-MOD-TCP", "Acoplador de Bus Modbus TCP / EtherNet/IP", "Módulo cabecera multiprotocolo para comunicación Modbus TCP y EtherNet/IP", json.dumps({"Modelo": "UR20-FBC-MOD-TCP", "CodigoPedido": "1334930000", "Protocolos": "Modbus TCP y EtherNet/IP", "Puertos": "2x RJ45"}), "Conexión con PLCs Schneider Electric, Rockwell Allen-Bradley y sistemas SCADA"),
        ("1334870000", "UR20-FBC-EC", "Acoplador de Bus EtherCAT", "Módulo cabecera de bus ultrarrápido para redes deterministas EtherCAT", json.dumps({"Modelo": "UR20-FBC-EC", "CodigoPedido": "1334870000", "Protocolo": "EtherCAT", "Velocidad": "100 Mbps determinista"}), "Control de movimiento (Motion Control) y servoaccionamientos"),
        ("1315180000", "UR20-16DI-P", "Módulo de 16 Entradas Digitales 24V DC", "Tarjeta electrónica compacta de 16 entradas digitales P-switching (lógica positiva) en ancho de 11.5 mm con LEDs de canal", json.dumps({"Modelo": "UR20-16DI-P", "CodigoPedido": "1315180000", "Entradas": "16x 24V DC", "Conexion": "PUSH IN frontal", "FiltroEntrada": "Configurable 0.1 a 20 ms"}), "Captación de señales de finales de carrera, pulsadores y sensores fotoeléctricos"),
        ("1315250000", "UR20-16DO-P", "Módulo de 16 Salidas Digitales 24V DC", "Tarjeta electrónica de 16 salidas a transistor de 24V DC 0.5A por canal con protección electrónica de cortocircuito", json.dumps({"Modelo": "UR20-16DO-P", "CodigoPedido": "1315250000", "Salidas": "16x 24V DC a transistor (0.5A c/u)", "Proteccion": "Sobrecarga y cortocircuito individual"}), "Accionamiento directo de electroválvulas neumáticas, luces piloto y relés auxiliares"),
        ("1315590000", "UR20-4AI-UI-16", "Módulo de 4 Entradas Analógicas Universales", "Módulo de 4 canales analógicos configurables individualmente para corriente (0/4-20mA) o tensión (0/10V) a 16 bits de resolución", json.dumps({"Modelo": "UR20-4AI-UI-16", "CodigoPedido": "1315590000", "Canales": "4x Analógicos", "Resolucion": "16 bits", "Precision": "0.1% a fondo de escala"}), "Adquisición de transmisores de presión, caudal, nivel y velocidad"),
        ("1315620000", "UR20-4AO-UI-16", "Módulo de 4 Salidas Analógicas Universales", "Módulo de 4 salidas analógicas aisladas de alta precisión de 16 bits configurables en tensión o corriente", json.dumps({"Modelo": "UR20-4AO-UI-16", "CodigoPedido": "1315620000", "Canales": "4x Salidas analógicas", "Resolucion": "16 bits"}), "Consigna de velocidad para variadores de frecuencia y válvulas modulantes"),
        ("1315690000", "UR20-4AI-RTD-DIAG", "Módulo de 4 Entradas de Temperatura RTD", "Módulo especializado para conexión directa de 4 sondas de temperatura PT100/PT1000/NI1000 a 2, 3 o 4 hilos", json.dumps({"Modelo": "UR20-4AI-RTD-DIAG", "CodigoPedido": "1315690000", "Sensores": "PT100, PT200, PT500, PT1000", "Canales": 4, "Diagnostico": "Rotura de hilo y cortocircuito"}), "Monitoreo de temperatura en devanados de motores, rodamientos y reactores químicos")
    ]
    for code, modelo, nom, desc, specs, app in uremote_modules:
        items.append((
            brand, line_auto, "Módulos de E/S Remotas u-remote", "Sistema u-remote UR20", code,
            f"{nom} ({code})",
            f"{desc} con tecnología modular enchufable sin herramientas y sustitución en caliente (hot-swap)",
            specs,
            app
        ))

    # =========================================================================
    # 9. LÍNEA: CONECTORES PESADOS PARA TRABAJO INDUSTRIAL (ROCKSTAR)
    # Ref: Catalogue 3 Heavy Duty Connectors Version 2024
    # =========================================================================
    line_hdc = "Conectores Pesados Industriales (RockStar)"

    hdc_items = [
        ("1200000000", "HDC HE 6 MS", "Inserto Macho RockStar HE 6 Polos", "Inserto macho de 6 polos más tierra (6P+PE) para 16A 500V con conexión por tornillo", json.dumps({"Modelo": "HDC HE 6 MS", "CodigoPedido": "1200000000", "Polos": "6 + PE", "CorrienteNominal": "16A", "TensionNominal": "500V", "Conexion": "Tornillo"})),
        ("1200200000", "HDC HE 6 FS", "Inserto Hembra RockStar HE 6 Polos", "Inserto hembra de 6 polos más tierra (6P+PE) para 16A 500V", json.dumps({"Modelo": "HDC HE 6 FS", "CodigoPedido": "1200200000", "Polos": "6 + PE", "CorrienteNominal": "16A", "TensionNominal": "500V"})),
        ("1203900000", "HDC HE 10 MS", "Inserto Macho RockStar HE 10 Polos", "Inserto macho de 10 polos más tierra para 16A 500V", json.dumps({"Modelo": "HDC HE 10 MS", "CodigoPedido": "1203900000", "Polos": "10 + PE", "CorrienteNominal": "16A", "TensionNominal": "500V"})),
        ("1204100000", "HDC HE 10 FS", "Inserto Hembra RockStar HE 10 Polos", "Inserto hembra de 10 polos más tierra para 16A 500V", json.dumps({"Modelo": "HDC HE 10 FS", "CodigoPedido": "1204100000", "Polos": "10 + PE", "CorrienteNominal": "16A", "TensionNominal": "500V"})),
        ("1207500000", "HDC HE 16 MS", "Inserto Macho RockStar HE 16 Polos", "Inserto macho industrial de 16 polos más tierra para 16A 500V", json.dumps({"Modelo": "HDC HE 16 MS", "CodigoPedido": "1207500000", "Polos": "16 + PE", "CorrienteNominal": "16A", "TensionNominal": "500V"})),
        ("1207700000", "HDC HE 16 FS", "Inserto Hembra RockStar HE 16 Polos", "Inserto hembra industrial de 16 polos más tierra para 16A 500V", json.dumps({"Modelo": "HDC HE 16 FS", "CodigoPedido": "1207700000", "Polos": "16 + PE", "CorrienteNominal": "16A", "TensionNominal": "500V"})),
        ("1211100000", "HDC HE 24 MS", "Inserto Macho RockStar HE 24 Polos", "Inserto macho industrial de 24 polos más tierra para 16A 500V", json.dumps({"Modelo": "HDC HE 24 MS", "CodigoPedido": "1211100000", "Polos": "24 + PE", "CorrienteNominal": "16A", "TensionNominal": "500V"})),
        ("1211300000", "HDC HE 24 FS", "Inserto Hembra RockStar HE 24 Polos", "Inserto hembra industrial de 24 polos más tierra para 16A 500V", json.dumps({"Modelo": "HDC HE 24 FS", "CodigoPedido": "1211300000", "Polos": "24 + PE", "CorrienteNominal": "16A", "TensionNominal": "500V"})),
        ("1205000000", "HDC 10B TSBU 1xM25G", "Capota Metálica Aérea RockStar 10B", "Carcasa aérea de aluminio inyectado IP65 con salida de cable lateral/superior roscada M25 para tamaño 4 (10 polos)", json.dumps({"Modelo": "HDC 10B TSBU 1xM25G", "CodigoPedido": "1205000000", "Tamaño": "4", "Rosca": "M25", "GradoProteccion": "IP65"})),
        ("1205300000", "HDC 10B ABU", "Base Empotrada RockStar 10B", "Base de montaje en panel de aluminio con palanca de cierre estanca IP65 para tamaño 4", json.dumps({"Modelo": "HDC 10B ABU", "CodigoPedido": "1205300000", "Tamaño": "4", "Tipo": "Base empotrada de panel con junta de estanqueidad"})),
        ("1208600000", "HDC 16B TSBU 1xM25G", "Capota Metálica Aérea RockStar 16B", "Carcasa aérea de aluminio fundido IP65 rosca M25 para tamaño 6 (16 polos)", json.dumps({"Modelo": "HDC 16B TSBU 1xM25G", "CodigoPedido": "1208600000", "Tamaño": "6", "Rosca": "M25"})),
        ("1208900000", "HDC 16B ABU", "Base Empotrada RockStar 16B", "Base de montaje en panel con palanca longitudinal para tamaño 6", json.dumps({"Modelo": "HDC 16B ABU", "CodigoPedido": "1208900000", "Tamaño": "6"})),
        ("1212400000", "HDC 24B TSBU 1xM32G", "Capota Metálica Aérea RockStar 24B", "Carcasa aérea robusta IP65 con entrada de cable M32 para tamaño 8 (24 polos)", json.dumps({"Modelo": "HDC 24B TSBU 1xM32G", "CodigoPedido": "1212400000", "Tamaño": "8", "Rosca": "M32"})),
        ("1212700000", "HDC 24B ABU", "Base Empotrada RockStar 24B", "Base empotrada de panel con palanca de cierre para tamaño 8", json.dumps({"Modelo": "HDC 24B ABU", "CodigoPedido": "1212700000", "Tamaño": "8"}))
    ]
    for code, modelo, nom, desc, specs in hdc_items:
        items.append((
            brand, line_hdc, "Conectores Pesados RockStar", "RockStar Serie HE", code,
            f"{nom} ({code})",
            f"{desc} para conexiones eléctricas seguras y estancas en maquinaria sujeta a vibraciones, polvo y humedad",
            specs,
            "Desconexión rápida de módulos de maquinaria, moldes de inyección de plástico, robots y grúas industriales"
        ))

    # =========================================================================
    # 10. LÍNEA: MEDICIÓN Y MONITOREO DE ENERGÍA (ENERGY METERS)
    # Ref: Catalogue Measuring & monitoring systems Solutions for smart machines
    # =========================================================================
    line_meter = "Medición y Monitoreo de Energía"

    meter_items = [
        ("2544200000", "Energy Meter 520", "Analizador de Redes Trifásico Energy Meter 520", "Medidor de energía multifunción en riel DIN para redes trifásicas con medición en 4 cuadrantes y puerto serie RS485 Modbus RTU", json.dumps({"Modelo": "Energy Meter 520", "CodigoPedido": "2544200000", "TensionMedicion": "Hasta 480V AC (F-F)", "CorrienteMedicion": "Transformadores ../1A o ../5A", "Comunicacion": "RS485 Modbus RTU", "Precision": "Clase 0.5S", "Montaje": "Riel DIN (4 módulos)"}), "Monitorización de consumo energético en tableros generales de distribución y centros de costos"),
        ("2544210000", "Energy Meter 700", "Central de Medida Avanzada Energy Meter 700", "Analizador de redes con interfaz Ethernet Modbus TCP, registro de armónicos hasta orden 40 y servidor web embebido", json.dumps({"Modelo": "Energy Meter 700", "CodigoPedido": "2544210000", "Comunicacion": "Ethernet Modbus TCP / Gateway RS485", "Armonicos": "THD y armónicos individuales hasta orden 40", "Memoria": "Registro interno de datos", "Precision": "Clase 0.2S"}), "Auditorías de eficiencia energética, gestión de calidad de onda en transformadores y plantas industriales"),
        ("2544240000", "Energy Meter 750", "Analizador de Calidad de Energía Energy Meter 750", "Analizador de calidad de red de alta gama para detección de transitorios, huecos de tensión (sags/swells) y eventos de red", json.dumps({"Modelo": "Energy Meter 750", "CodigoPedido": "2544240000", "NormaCalidad": "IEC 61000-4-30 Clase A", "Eventos": "Captura de transitorios y flickers"}), "Subestaciones eléctricas de distribución y centros de datos críticos"),
        ("2544300000", "KCMA-1-100-1A-0.5", "Transformador de Corriente Núcleo Partido 100/1A", "Transformador de corriente tipo toroidal abierto para montaje directo sobre cable existente sin desconectar el circuito", json.dumps({"Modelo": "KCMA-1-100-1A-0.5", "CodigoPedido": "2544300000", "Primario": "100A", "Secundario": "1A", "ClasePrecision": "0.5", "VentanaCable": "Ø 18 mm"}), "Retrofit y modernización de tableros eléctricos existentes para monitoreo de energía"),
        ("2544310000", "KCMA-1-250-1A-0.5", "Transformador de Corriente Núcleo Partido 250/1A", "Transformador de núcleo partido 250A primario y 1A secundario de clase 0.5", json.dumps({"Modelo": "KCMA-1-250-1A-0.5", "CodigoPedido": "2544310000", "Primario": "250A", "Secundario": "1A", "ClasePrecision": "0.5", "VentanaCable": "Ø 28 mm"}), "Medición de alimentadores de potencia en media industria"),
        ("2544320000", "KCMA-1-400-1A-0.5", "Transformador de Corriente Núcleo Partido 400/1A", "Transformador de núcleo partido para barras o cables gruesos hasta 400A", json.dumps({"Modelo": "KCMA-1-400-1A-0.5", "CodigoPedido": "2544320000", "Primario": "400A", "Secundario": "1A", "ClasePrecision": "0.5", "VentanaCable": "Ø 42 mm"}), "Acometidas de centros comerciales y cuadros generales de distribución")
    ]
    for code, modelo, nom, desc, specs, app in meter_items:
        items.append((
            brand, line_meter, "Centrales de Medida y Analizadores", "Energy Meters Weidmüller", code,
            f"{nom} ({code})",
            desc,
            specs,
            app
        ))

    # =========================================================================
    # 11. LÍNEA: ENVOLVENTES Y CAJAS INDUSTRIALES (KLIPPON PROTECT)
    # Ref: Catalogue 5 Enclosure systems and accessories Version Klippon Protect
    # =========================================================================
    line_enc = "Envolventes y Cajas Industriales (Klippon Protect)"

    enclosure_items = [
        ("0342000000", "KLIPPON K1", "Caja de Aluminio Klippon K1 (80x75x57 mm)", "Caja de bornas de aluminio inyectado IP66 resistente a impactos (IK09) para ambientes industriales severos", json.dumps({"Modelo": "KLIPPON K1", "CodigoPedido": "0342000000", "Dimensiones": "80 x 75 x 57 mm", "Material": "Aluminio AlSi12", "GradoProteccion": "IP66 / IP67 / IP68", "ResistenciaImpacto": "IK09"})),
        ("0342100000", "KLIPPON K2", "Caja de Aluminio Klippon K2 (125x80x57 mm)", "Caja de aluminio fundido IP66 con junta de estanqueidad de silicona o cloropreno", json.dumps({"Modelo": "KLIPPON K2", "CodigoPedido": "0342100000", "Dimensiones": "125 x 80 x 57 mm", "GradoProteccion": "IP66"})),
        ("0342200000", "KLIPPON K3", "Caja de Aluminio Klippon K3 (165x125x75 mm)", "Caja de derivación y bornas de aluminio de tamaño mediano", json.dumps({"Modelo": "KLIPPON K3", "CodigoPedido": "0342200000", "Dimensiones": "165 x 125 x 75 mm", "GradoProteccion": "IP66"})),
        ("0342300000", "KLIPPON K4", "Caja de Aluminio Klippon K4 (200x165x90 mm)", "Caja de conexión industrial para regletas de bornes y sensores", json.dumps({"Modelo": "KLIPPON K4", "CodigoPedido": "0342300000", "Dimensiones": "200 x 165 x 90 mm", "GradoProteccion": "IP66"})),
        ("0342400000", "KLIPPON K5", "Caja de Aluminio Klippon K5 (330x230x111 mm)", "Caja de aluminio de gran tamaño para cajas de combinación y botoneras", json.dumps({"Modelo": "KLIPPON K5", "CodigoPedido": "0342400000", "Dimensiones": "330 x 230 x 111 mm", "GradoProteccion": "IP66"})),
        ("1305810000", "KLIPPON POK 080806", "Caja de Poliéster Klippon POK (75x80x55 mm)", "Caja estanca de poliéster reforzado con fibra de vidrio IP66 libre de halógenos y anticorrosiva", json.dumps({"Modelo": "KLIPPON POK 080806", "CodigoPedido": "1305810000", "Dimensiones": "75 x 80 x 55 mm", "Material": "Poliéster reforzado fibra de vidrio", "GradoProteccion": "IP66"})),
        ("1305840000", "KLIPPON POK 121209", "Caja de Poliéster Klippon POK (120x122x90 mm)", "Caja anticorrosiva de poliéster IP66 para ambientes marinos y químicos", json.dumps({"Modelo": "KLIPPON POK 121209", "CodigoPedido": "1305840000", "Dimensiones": "120 x 122 x 90 mm", "GradoProteccion": "IP66"})),
        ("1305880000", "KLIPPON POK 162609", "Caja de Poliéster Klippon POK (160x260x90 mm)", "Caja de conexión de poliéster de alta resistencia química e intemperie", json.dumps({"Modelo": "KLIPPON POK 162609", "CodigoPedido": "1305880000", "Dimensiones": "160 x 260 x 90 mm", "GradoProteccion": "IP66"}))
    ]
    for code, modelo, nom, desc, specs in enclosure_items:
        items.append((
            brand, line_enc, "Cajas y Envolventes Industriales", "Klippon Protect", code,
            f"{nom} ({code})",
            f"{desc} diseñada para soportar atmósferas corrosivas, intemperie UV y choques mecánicos",
            specs,
            "Cajas de paso y conexionado en refinerías, barcos, puertos marítimos y plantas químicas de Guayaquil"
        ))

    # =========================================================================
    # 12. LÍNEA: SISTEMAS DE IDENTIFICACIÓN Y MARCADO (MARKING SYSTEMS)
    # Ref: CAT7 Marking systems Version 2025
    # =========================================================================
    line_mark = "Sistemas de Marcado y Señalización"

    markers = [
        ("0473460001", "DEK 5 FW 1-50", "Tiras Señalizadoras DEK 5 Impresas 1-50", "Señalizadores de bornera en tarjeta con impresión horizontal números del 1 al 50 para paso de 5 mm", json.dumps({"Modelo": "DEK 5 FW 1-50", "CodigoPedido": "0473460001", "Impresion": "Números 1 al 50", "Color": "Blanco con números negros", "Ancho": "5 mm"})),
        ("0473460051", "DEK 5 FW 51-100", "Tiras Señalizadoras DEK 5 Impresas 51-100", "Señalizadores de bornera en tarjeta con impresión horizontal números del 51 al 100", json.dumps({"Modelo": "DEK 5 FW 51-100", "CodigoPedido": "0473460051", "Impresion": "Números 51 al 100"})),
        ("1609801044", "WS 10/5 MC NEUTRAL", "Marcadores Neutros MultiCard WS 10/5", "Tarjetas MultiCard de señalizadores blancos vírgenes para impresión personalizada con plotter o impresora láser Weidmüller PrintJet", json.dumps({"Modelo": "WS 10/5 MC NEUTRAL", "CodigoPedido": "1609801044", "Formato": "MultiCard", "Color": "Blanco", "Dimension": "10 x 5 mm"})),
        ("1609860000", "WS 12/5 MC NEUTRAL", "Marcadores Neutros MultiCard WS 12/5", "Marcadores MultiCard de 12 x 5 mm para borneras serie W y A", json.dumps({"Modelo": "WS 12/5 MC NEUTRAL", "CodigoPedido": "1609860000", "Dimension": "12 x 5 mm", "Color": "Blanco"})),
        ("1686360001", "SlimFix SF 1/12 MC", "Señalizadores de Cable SlimFix 0.5 a 1.5 mm²", "Marcadores tubulares cerrados para conductores de 0.5 a 1.5 mm² libres de halógenos", json.dumps({"Modelo": "SlimFix SF 1/12 MC", "CodigoPedido": "1686360001", "SeccionConductor": "0.5 a 1.5 mm²", "Color": "Blanco"})),
        ("1686370001", "SlimFix SF 2/12 MC", "Señalizadores de Cable SlimFix 1.5 a 2.5 mm²", "Marcadores tubulares para conductores de 1.5 a 2.5 mm² de sección", json.dumps({"Modelo": "SlimFix SF 2/12 MC", "CodigoPedido": "1686370001", "SeccionConductor": "1.5 a 2.5 mm²", "Color": "Blanco"}))
    ]
    for code, modelo, nom, desc, specs in markers:
        items.append((
            brand, line_mark, "Señalizadores de Borneras y Cables", "Sistemas de Marcado MultiCard", code,
            f"{nom} ({code})",
            f"{desc} para rotulación clara, duradera e imborrable en cuadros eléctricos normados",
            specs,
            "Identificación unívoca de hilos, cables y regletas de borneras según planos eléctricos de ingeniería"
        ))

    return items

def populate_database():
    items = get_weidmuller_catalog_data()
    print(f"Total de productos preparados para Weidmuller: {len(items)}")

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

        cur.execute("SELECT COUNT(1) FROM ProductsCatalog WHERE Brand = 'Weidmuller';")
        count_wm = cur.fetchone()[0]
        cur.execute("SELECT COUNT(1) FROM Products_FTS;")
        fts_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT Brand) FROM ProductsCatalog;")
        brands_count = cur.fetchone()[0]
        print(f"-> Productos Weidmuller en ProductsCatalog: {count_wm}")
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
