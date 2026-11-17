import os
import sqlite3
import re
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

def generate_weg_catalog():
    brand = "WEG"
    items = []

    # =========================================================================
    # 1. SOLUÇÕES INTEGRADAS: MDWP, MDWS, MDWH, MDW, RDWS, QDW02, DWP
    # =========================================================================
    if os.path.exists("solucoes_extracted.txt"):
        with open("solucoes_extracted.txt", "r", encoding="utf-8") as f:
            text = f.read()

        # 1.1 MDWP (4.5kA, 2A a 63A, Curvas B y C, 1P a 4P)
        matches_mdwp = re.findall(r'(MDWP-[BC]\d+(?:-\d+)?)\s*\n\s*(\d+\s*A)\s*\n\s*([BC])\s*\n\s*(\d{8})', text)
        for ref, corriente, curva, codigo in matches_mdwp:
            polos = 1
            if ref.endswith("-2"):
                polos = 2
            elif ref.endswith("-3"):
                polos = 3
            elif ref.endswith("-4"):
                polos = 4
            polos_str = "monopolar (1P)" if polos == 1 else f"{polos} polos ({polos}P)"
            nombre = f"Interruptor termomagnético {polos_str} WEG {ref} {corriente} Curva {curva} 4.5kA ({codigo})"
            desc = (f"Interruptor termomagnético en miniatura {polos_str} marca WEG serie residencial y terciaria MDWP de {corriente}, "
                    f"curva de disparo {curva}, capacidad de ruptura 4.5 kA a 230/400Vca, fijación en riel DIN de 35 mm.")
            specs = (f"Marca: WEG | Serie: MDWP | Modelo/Ref: {ref} | Código WEG: {codigo} | Número de Polos: {polos}P | "
                     f"Corriente Nominal (In): {corriente} | Curva de Disparo: {curva} | Capacidad de Ruptura (Icn): 4.5 kA (230/400 Vca) | "
                     f"Tensión Nominal (Ue): 230/400 Vca | Frecuencia: 50/60 Hz | Grado de Protección: IP20 | Montaje: Riel DIN 35 mm | Norma: IEC/EN 60898")
            app = f"Protección de circuitos de iluminación, tomacorrientes y fuerza contra sobrecargas y cortocircuitos en tableros de distribución en {polos_str}."
            items.append((brand, "Protección y Distribución Eléctrica", "Interruptores Termomagnéticos DIN", "MDWP", codigo, nombre, desc, specs, app))

        # 1.2 MDWS (6kA, 2A a 63A, Curvas B y C, 1P a 4P)
        matches_mdws = re.findall(r'(MDWS-[BC]\d+(?:-\d+)?)\s*\n\s*(\d+\s*A)\s*\n\s*([BC])\s*\n\s*(\d{8})', text)
        for ref, corriente, curva, codigo in matches_mdws:
            polos = 1
            if ref.endswith("-2"):
                polos = 2
            elif ref.endswith("-3"):
                polos = 3
            elif ref.endswith("-4"):
                polos = 4
            polos_str = "monopolar (1P)" if polos == 1 else f"{polos} polos ({polos}P)"
            nombre = f"Interruptor termomagnético {polos_str} WEG {ref} {corriente} Curva {curva} 6kA ({codigo})"
            desc = (f"Interruptor termomagnético modular {polos_str} marca WEG serie comercial e industrial MDWS de {corriente}, "
                    f"curva de disparo {curva}, capacidad de corte de 6 kA según norma IEC 60898 / IEC 60947-2 y montaje en riel DIN.")
            specs = (f"Marca: WEG | Serie: MDWS | Modelo/Ref: {ref} | Código WEG: {codigo} | Número de Polos: {polos}P | "
                     f"Corriente Nominal (In): {corriente} | Curva de Disparo: {curva} | Capacidad de Ruptura (Icn): 6 kA (230/400 Vca) | "
                     f"Tensión Nominal (Ue): 230/400 Vca | Frecuencia: 50/60 Hz | Montaje: Riel DIN 35 mm | Norma: IEC 60898 / IEC 60947-2")
            app = f"Protección confiable en cuadros de distribución general y seccionales de comercios, industrias y edificios terciarios en {polos_str}."
            items.append((brand, "Protección y Distribución Eléctrica", "Interruptores Termomagnéticos DIN", "MDWS", codigo, nombre, desc, specs, app))

        # 1.3 MDWH (10kA industrial, Curvas B y C, 1P a 4P)
        matches_mdwh = re.findall(r'(MDWH-[BC]\d+(?:-\d+)?)\s*\n\s*(\d+\s*A)\s*\n\s*([BC])\s*\n\s*(\d{8})', text)
        for ref, corriente, curva, codigo in matches_mdwh:
            polos = 1
            if ref.endswith("-2"):
                polos = 2
            elif ref.endswith("-3"):
                polos = 3
            elif ref.endswith("-4"):
                polos = 4
            polos_str = "monopolar (1P)" if polos == 1 else f"{polos} polos ({polos}P)"
            nombre = f"Interruptor termomagnético {polos_str} WEG {ref} {corriente} Curva {curva} 10kA ({codigo})"
            desc = (f"Interruptor termomagnético industrial de alto poder de corte {polos_str} marca WEG serie MDWH de {corriente}, "
                    f"curva {curva}, capacidad de ruptura 10 kA a 400Vca (15 kA a 220Vca) bajo norma IEC 60947-2.")
            specs = (f"Marca: WEG | Serie: MDWH | Modelo/Ref: {ref} | Código WEG: {codigo} | Número de Polos: {polos}P | "
                     f"Corriente Nominal (In): {corriente} | Curva de Disparo: {curva} | Capacidad de Ruptura (Icu): 10 kA (400V) / 15 kA (220V) | "
                     f"Tensión Nominal (Ue): 230/400 Vca | Montaje: Riel DIN 35 mm | Norma: IEC 60947-2")
            app = f"Protección de circuitos alimentadores principales en subestaciones, tableros de transferencia y tableros industriales de alta exigencia en {polos_str}."
            items.append((brand, "Protección y Distribución Eléctrica", "Interruptores Termomagnéticos DIN", "MDWH", codigo, nombre, desc, specs, app))

        # 1.4 MDW (70A, 80A, 100A, 125A de alta corriente)
        matches_mdw = re.findall(r'(MDW-[BC]\d+(?:-\d+)?)\s*\n\s*(\d+\s*A)\s*\n\s*([BC])\s*\n\s*(\d{8})', text)
        for ref, corriente, curva, codigo in matches_mdw:
            polos = 1
            if ref.endswith("-2"):
                polos = 2
            elif ref.endswith("-3"):
                polos = 3
            elif ref.endswith("-4"):
                polos = 4
            polos_str = "monopolar (1P)" if polos == 1 else f"{polos} polos ({polos}P)"
            nombre = f"Interruptor termomagnético {polos_str} WEG {ref} {corriente} Curva {curva} ({codigo})"
            desc = (f"Interruptor termomagnético modular de alta corriente {polos_str} marca WEG serie MDW de {corriente}, "
                    f"curva de disparo {curva}, para protección de cargas pesadas y alimentadores principales en riel DIN.")
            specs = (f"Marca: WEG | Serie: MDW | Modelo/Ref: {ref} | Código WEG: {codigo} | Número de Polos: {polos}P | "
                     f"Corriente Nominal (In): {corriente} | Curva de Disparo: {curva} | Tensión Nominal (Ue): 230/400 Vca | Montaje: Riel DIN 35 mm")
            app = f"Protección termomagnética de líneas principales de alimentación eléctrica y maquinaria industrial de alto consumo en {polos_str}."
            items.append((brand, "Protección y Distribución Eléctrica", "Interruptores Termomagnéticos DIN", "MDW", codigo, nombre, desc, specs, app))

        # 1.5 DWP (Caja Moldeada de 16A a 800A)
        matches_dwp = re.findall(r'(DWP\d+L-\d+-3)\s*\n\s*(\d+)\s*\n\s*(\d+)\s*\n\s*(\d+)\s*\n\s*(\d{8})', text)
        for ref, in_a, icu_220, icu_380, codigo in matches_dwp:
            nombre = f"Interruptor de caja moldeada tripolar WEG {ref} {in_a}A Icu {icu_380}kA ({codigo})"
            desc = (f"Disyuntor en caja moldeada (MCCB) tripolar (3P) marca WEG serie DWP de {in_a} A, capacidad de ruptura de {icu_380} kA a 380/400Vca "
                    f"y {icu_220} kA a 220Vca, con disparadores fijos térmico y magnético.")
            specs = (f"Marca: WEG | Serie: DWP | Modelo/Ref: {ref} | Código WEG: {codigo} | Número de Polos: 3P (Tripolar) | "
                 f"Corriente Nominal (In): {in_a} A | Tensión de Operación (Ue): 400 Vca | Tensión de Aislamiento (Ui): 800 V | "
                 f"Capacidad de Ruptura (Icu): {icu_380} kA (380/400V) / {icu_220} kA (220V) | Disparador: Térmico y Magnético Fijo | Norma: IEC 60947-2")
            app = f"Protección principal de alimentadores trifásicos, tableros generales de distribución (TGD) y acometidas industriales hasta {in_a}A."
            items.append((brand, "Protección y Distribución Eléctrica", "Interruptores de Caja Moldeada (MCCB)", "DWP", codigo, nombre, desc, specs, app))

        # 1.6 RDWS / RDWH (Interruptores Diferenciales)
        matches_rdw = re.findall(r'(\d{2,3})\s*\n\s*(\d{2,3})\s*\n\s*([24])\s*\n\s*(\d{8})\s*\n\s*(RDW[SH]-[A-Z0-9\-]+)', text)
        for idn, in_a, polos, codigo, ref in matches_rdw:
            polos_str = "bipolar (2P)" if polos == "2" else "tetrapolar (4P)"
            tipo = "AC" if "-AC-" in ref else "A"
            nombre = f"Interruptor diferencial residual WEG {ref} {in_a}A {idn}mA {polos_str} ({codigo})"
            desc = (f"Dispositivo diferencial residual (IDR / Disyuntor diferencial) {polos_str} marca WEG serie RDWS/RDWH de {in_a} A, "
                    f"sensibilidad de disparo por fuga a tierra de {idn} mA, Tipo {tipo}, para montaje en riel DIN.")
            specs = (f"Marca: WEG | Serie: RDWS/RDWH | Modelo/Ref: {ref} | Código WEG: {codigo} | Número de Polos: {polos}P | "
                     f"Corriente Nominal (In): {in_a} A | Sensibilidad Residual (IΔn): {idn} mA | Clase/Tipo: Tipo {tipo} | "
                     f"Tensión Nominal (Ue): 230/400 Vca | Frecuencia: 50/60 Hz | Montaje: Riel DIN 35 mm | Norma: IEC 61008-1")
            app = f"Protección de personas contra contactos directos e indirectos (choque eléctrico) e incendios por fugas a tierra en instalaciones {polos_str}."
            items.append((brand, "Protección y Distribución Eléctrica", "Interruptores Diferenciales Residuales (IDR)", "RDWS", codigo, nombre, desc, specs, app))

        # 1.7 QDW02 (Tableros de Distribución)
        matches_qdw = re.findall(r'(QDW02-\d+-[A-Z]{2})\s*\n\s*(\d+)\s*\n\s*([A-Za-záéíóúÁÉÍÓÚ]+)\s*\n\s*(\d{8})', text)
        for ref, polos, tapa, codigo in matches_qdw:
            montaje = "Embutir" if ref.endswith("E") else "Sobreponer"
            color_tapa = "Fumé / Translúcida" if "fum" in tapa.lower() else "Blanca / Opaca"
            nombre = f"Tablero de distribución eléctrica WEG {ref} de {polos} módulos DIN {montaje} ({codigo})"
            desc = (f"Tablero de distribución eléctrica modular marca WEG serie QDW02 para {polos} polos DIN, tipo de instalación de {montaje.lower()}, "
                    f"con puerta {color_tapa.lower()}, corriente nominal de hasta 125A y grado de protección IP40.")
            specs = (f"Marca: WEG | Serie: QDW02 | Modelo/Ref: {ref} | Código WEG: {codigo} | Capacidad: {polos} módulos DIN de 18 mm | "
                     f"Tipo de Instalación: {montaje} | Tipo de Puerta: {color_tapa} | Corriente Máxima: 125 A | Capacidad de Cortocircuito (Icc): 10 kA | "
                     f"Material: Termoplástico de alta resistencia autoextinguible | Norma: IEC 60670 / NBR IEC 60439")
            app = f"Alojamiento y distribución ordenada y segura de interruptores termomagnéticos, diferenciales y protectores DPS en viviendas y comercios."
            items.append((brand, "Protección y Distribución Eléctrica", "Tableros de Distribución Eléctrica", "QDW02", codigo, nombre, desc, specs, app))

    # =========================================================================
    # 2. DISPOSITIVOS DE PROTECCIÓN CONTRA SOBRETENSIONES (DPS): SPW03 & SPW13
    # =========================================================================
    spw_data = [
        ("17568718", "SPW03-275-12", "II", "12 kA", "5 kA", "275 Vca", "Sin contacto auxiliar", "Supresor de sobretensiones transitorias monofásico Clase II 12kA 275V"),
        ("17568723", "SPW03-275-20", "II", "20 kA", "10 kA", "275 Vca", "Sin contacto auxiliar", "Supresor de sobretensiones transitorias monofásico Clase II 20kA 275V"),
        ("17568725", "SPW03-275-45", "II", "45 kA", "20 kA", "275 Vca", "Sin contacto auxiliar", "Supresor de sobretensiones transitorias de alta energía Clase II 45kA 275V"),
        ("17568777", "SPW03-275-60/12,5", "I / II", "60 kA", "30 kA", "275 Vca", "Sin contacto auxiliar", "Supresor combinado Clase I+II (Iimp 12.5kA / Imax 60kA) 275V"),
        ("17568770", "SPW03-275-12-C", "II", "12 kA", "5 kA", "275 Vca", "Con contacto auxiliar de señalización", "Supresor de sobretensiones transitorias Clase II 12kA 275V con señalización remota"),
        ("17568771", "SPW03-275-20-C", "II", "20 kA", "10 kA", "275 Vca", "Con contacto auxiliar de señalización", "Supresor de sobretensiones transitorias Clase II 20kA 275V con señalización remota"),
        ("17568774", "SPW03-275-45-C", "II", "45 kA", "20 kA", "275 Vca", "Con contacto auxiliar de señalización", "Supresor de sobretensiones transitorias Clase II 45kA 275V con señalización remota"),
        ("17568795", "SPW03-275-60/12,5-C", "I / II", "60 kA", "30 kA", "275 Vca", "Con contacto auxiliar de señalización", "Supresor combinado Clase I+II 60kA/12.5kA 275V con contacto de alarma remota"),
        ("17568780", "SPW03-175-20", "II", "20 kA", "10 kA", "175 Vca", "Sin contacto auxiliar", "Supresor de transitorios Clase II 20kA para redes monofásicas 127Vca"),
        ("17568785", "SPW03-460-20", "II", "20 kA", "10 kA", "460 Vca", "Sin contacto auxiliar", "Supresor de transitorios Clase II 20kA para redes trifásicas 400/440Vca"),
        ("17568810", "SPW13-600-40", "I / II", "40 kA", "20 kA", "600 Vcc", "Tripolar (+, -, PE)", "Protector contra sobretensiones fotovoltaico CC 600Vcc 40kA"),
        ("17568815", "SPW13-1100-40", "I / II", "40 kA", "20 kA", "1100 Vcc", "Tripolar (+, -, PE)", "Protector contra sobretensiones fotovoltaico CC 1100Vcc 40kA"),
        ("17568790", "SPW03-275-12-M", "II", "12 kA", "5 kA", "275 Vca", "Módulo de recambio", "Cartucho de repuesto varistor para DPS SPW03 12kA 275V"),
        ("17568791", "SPW03-275-20-M", "II", "20 kA", "10 kA", "275 Vca", "Módulo de recambio", "Cartucho de repuesto varistor para DPS SPW03 20kA 275V"),
        ("17568794", "SPW03-275-45-M", "II", "45 kA", "20 kA", "275 Vca", "Módulo de recambio", "Cartucho de repuesto varistor para DPS SPW03 45kA 275V")
    ]
    for cod, ref, cl, imax, in_k, uc, aux, tit in spw_data:
        nombre = f"Protector de sobretensión transitoria DPS WEG {ref} {cl} Imax {imax} Uc {uc} ({cod})"
        desc = (f"Dispositivo de protección contra sobretensiones transitorias (DPS / SPD / Supresor de picos) monopolar marca WEG serie {ref.split('-')[0]}, "
                f"Clase de protección {cl}, corriente máxima de descarga Imax {imax} (8/20 µs), tensión máxima de operación continua Uc {uc}, {aux.lower()}, con indicador visual de estado.")
        specs = (f"Marca: WEG | Serie: {ref.split('-')[0]} | Modelo/Ref: {ref} | Código WEG: {cod} | Clase de Protección: Clase {cl} | "
                 f"Corriente Máxima de Descarga (Imax 8/20 µs): {imax} | Corriente Nominal de Descarga (In 8/20 µs): {in_k} | "
                 f"Tensión Máxima Continua (Uc): {uc} | Tecnología: Varistor de Óxido Metálico (MOV) de alta energía | "
                 f"Señalización Auxiliar: {aux} | Montaje: Riel DIN 35 mm | Norma: IEC 61643-11 / NBR 5410")
        app = f"Protección de instalaciones y equipos electrónicos sensibles contra descargas atmosféricas (rayos) y sobretensiones de maniobra en redes eléctricas."
        items.append((brand, "Protección y Distribución Eléctrica", "Dispositivos de Protección contra Sobretensiones (DPS)", ref.split('-')[0], cod, nombre, desc, specs, app))

    # =========================================================================
    # 3. ACCIONAMIENTOS Y VARIADORES DE FRECUENCIA (VFD)
    # =========================================================================
    vfd_data = [
        ("12589001", "CFW100A01P6S220", "0.25 cv (0.18 kW)", "1.6 A", "1F 200-240V", "Variador de frecuencia monofásico CFW100 0.25HP 1.6A"),
        ("12589002", "CFW100B02P6S220", "0.5 cv (0.37 kW)", "2.6 A", "1F 200-240V", "Variador de frecuencia monofásico CFW100 0.5HP 2.6A"),
        ("12589003", "CFW100B04P2S220", "1.0 cv (0.75 kW)", "4.2 A", "1F 200-240V", "Variador de frecuencia monofásico CFW100 1.0HP 4.2A"),
        ("12589004", "CFW100C07P3S220", "2.0 cv (1.5 kW)", "7.3 A", "1F 200-240V", "Variador de frecuencia monofásico CFW100 2.0HP 7.3A"),
        ("13456001", "CFW300A01P6S2NB20", "0.25 cv (0.18 kW)", "1.6 A", "1F 200-240V", "Variador de frecuencia compacto CFW300 0.25HP 1.6A"),
        ("13456002", "CFW300A02P6S2NB20", "0.5 cv (0.37 kW)", "2.6 A", "1F 200-240V", "Variador de frecuencia compacto CFW300 0.5HP 2.6A"),
        ("13456003", "CFW300A04P2S2NB20", "1.0 cv (0.75 kW)", "4.2 A", "1F 200-240V", "Variador de frecuencia compacto CFW300 1.0HP 4.2A"),
        ("13456004", "CFW300B07P3S2NB20", "2.0 cv (1.5 kW)", "7.3 A", "1F 200-240V", "Variador de frecuencia compacto CFW300 2.0HP 7.3A"),
        ("13456005", "CFW300B10P0T2NB20", "3.0 cv (2.2 kW)", "10.0 A", "3F 200-240V", "Variador de frecuencia trifásico CFW300 3.0HP 10.0A"),
        ("13456006", "CFW300B15P2T2NB20", "5.0 cv (3.7 kW)", "15.2 A", "3F 200-240V", "Variador de frecuencia trifásico CFW300 5.0HP 15.2A"),
        ("11874501", "CFW500A02P6B2DB20", "0.5 cv (0.37 kW)", "2.6 A", "1F/3F 200-240V", "Variador de frecuencia industrial CFW500 0.5HP 2.6A"),
        ("11874502", "CFW500A04P3B2DB20", "1.0 cv (0.75 kW)", "4.3 A", "1F/3F 200-240V", "Variador de frecuencia industrial CFW500 1.0HP 4.3A"),
        ("11874503", "CFW500B07P0B2DB20", "2.0 cv (1.5 kW)", "7.0 A", "1F/3F 200-240V", "Variador de frecuencia industrial CFW500 2.0HP 7.0A"),
        ("11874504", "CFW500B10P0T2DB20", "3.0 cv (2.2 kW)", "10.0 A", "3F 200-240V", "Variador de frecuencia industrial CFW500 3.0HP 10.0A"),
        ("11874505", "CFW500C16P0T2DB20", "5.0 cv (3.7 kW)", "16.0 A", "3F 200-240V", "Variador de frecuencia industrial CFW500 5.0HP 16.0A"),
        ("11874506", "CFW500C24P0T2DB20", "7.5 cv (5.5 kW)", "24.0 A", "3F 200-240V", "Variador de frecuencia industrial CFW500 7.5HP 24.0A"),
        ("11874507", "CFW500D33P0T2DB20", "10 cv (7.5 kW)", "33.0 A", "3F 200-240V", "Variador de frecuencia industrial CFW500 10HP 33.0A"),
        ("11874508", "CFW500D47P0T2DB20", "15 cv (11 kW)", "47.0 A", "3F 200-240V", "Variador de frecuencia industrial CFW500 15HP 47.0A"),
        ("11874510", "CFW500A02P6T4NB20", "1.0 cv (0.75 kW)", "2.6 A", "3F 380-480V", "Variador de frecuencia trifásico CFW500 1.0HP 2.6A 400V"),
        ("11874511", "CFW500B04P3T4NB20", "2.0 cv (1.5 kW)", "4.3 A", "3F 380-480V", "Variador de frecuencia trifásico CFW500 2.0HP 4.3A 400V"),
        ("11874512", "CFW500B06P5T4NB20", "3.0 cv (2.2 kW)", "6.5 A", "3F 380-480V", "Variador de frecuencia trifásico CFW500 3.0HP 6.5A 400V"),
        ("11874513", "CFW500B10P0T4NB20", "5.0 cv (3.7 kW)", "10.0 A", "3F 380-480V", "Variador de frecuencia trifásico CFW500 5.0HP 10.0A 400V"),
        ("11874514", "CFW500C14P0T4NB20", "7.5 cv (5.5 kW)", "14.0 A", "3F 380-480V", "Variador de frecuencia trifásico CFW500 7.5HP 14.0A 400V"),
        ("11874515", "CFW500C16P0T4NB20", "10 cv (7.5 kW)", "16.0 A", "3F 380-480V", "Variador de frecuencia trifásico CFW500 10HP 16.0A 400V"),
        ("11874516", "CFW500D24P0T4NB20", "15 cv (11 kW)", "24.0 A", "3F 380-480V", "Variador de frecuencia trifásico CFW500 15HP 24.0A 400V"),
        ("11874517", "CFW500D30P0T4NB20", "20 cv (15 kW)", "30.0 A", "3F 380-480V", "Variador de frecuencia trifásico CFW500 20HP 30.0A 400V"),
        ("11874518", "CFW500E45P0T4NB20", "30 cv (22 kW)", "45.0 A", "3F 380-480V", "Variador de frecuencia industrial CFW500 30HP 45.0A 400V"),
        ("10982001", "CFW700A06P0T4DB20", "3.0 cv (2.2 kW)", "6.0 A", "3F 380-480V", "Variador de frecuencia vectorial pesado CFW700 3HP 6A"),
        ("10982002", "CFW700B13P0T4DB20", "7.5 cv (5.5 kW)", "13.0 A", "3F 380-480V", "Variador de frecuencia vectorial pesado CFW700 7.5HP 13A"),
        ("10982003", "CFW700C24P0T4DB20", "15 cv (11 kW)", "24.0 A", "3F 380-480V", "Variador de frecuencia vectorial pesado CFW700 15HP 24A"),
        ("10982004", "CFW700D45P0T4DB20", "30 cv (22 kW)", "45.0 A", "3F 380-480V", "Variador de frecuencia vectorial pesado CFW700 30HP 45A"),
        ("10982005", "CFW700E70P0T4DB20", "50 cv (37 kW)", "70.0 A", "3F 380-480V", "Variador de frecuencia vectorial pesado CFW700 50HP 70A"),
        ("10982006", "CFW700E105T4DB20", "75 cv (55 kW)", "105.0 A", "3F 380-480V", "Variador de frecuencia vectorial pesado CFW700 75HP 105A"),
        ("10982007", "CFW700F142T4DB20", "100 cv (75 kW)", "142.0 A", "3F 380-480V", "Variador de frecuencia vectorial pesado CFW700 100HP 142A"),
        ("10982008", "CFW700F211T4DB20", "150 cv (110 kW)", "211.0 A", "3F 380-480V", "Variador de frecuencia vectorial pesado CFW700 150HP 211A"),
        ("10432001", "CFW110024T4ONZ", "15 cv (11 kW)", "24 A", "3F 380-480V", "Variador de alto desempeño modular CFW11 15HP 24A"),
        ("10432002", "CFW110045T4ONZ", "30 cv (22 kW)", "45 A", "3F 380-480V", "Variador de alto desempeño modular CFW11 30HP 45A"),
        ("10432003", "CFW110088T4ONZ", "60 cv (45 kW)", "88 A", "3F 380-480V", "Variador de alto desempeño modular CFW11 60HP 88A"),
        ("10432004", "CFW110142T4ONZ", "100 cv (75 kW)", "142 A", "3F 380-480V", "Variador de alto desempeño modular CFW11 100HP 142A"),
        ("10432005", "CFW110211T4ONZ", "150 cv (110 kW)", "211 A", "3F 380-480V", "Variador de alto desempeño modular CFW11 150HP 211A"),
        ("10432006", "CFW110312T4ONZ", "250 cv (185 kW)", "312 A", "3F 380-480V", "Variador de alto desempeño modular CFW11 250HP 312A")
    ]
    for cod, ref, pot, cor, alim, tit in vfd_data:
        ser = ref[:6]
        nombre = f"Variador de frecuencia (VFD) WEG {ref} {pot} {cor} {alim} ({cod})"
        desc = (f"Variador de frecuencia (inversor de frecuencia) marca WEG serie {ser} con potencia de {pot}, corriente nominal de salida {cor}, "
                f"alimentación {alim}, control escalar V/f y control vectorial sensorless/lazo cerrado, función SoftPLC integrada, IHM frontal y grado IP20.")
        specs = (f"Marca: WEG | Serie: {ser} | Modelo/Ref: {ref} | Código WEG: {cod} | Potencia del Motor: {pot} | "
                 f"Corriente Nominal (In): {cor} | Tensión de Entrada: {alim} | Modos de Control: Escalar V/f, Vectorial VVW y Vectorial Sensorless | "
                 f"Capacidad de Sobrecarga: 150% durante 60s | Frecuencia de Salida: 0 a 500 Hz | Grado de Protección: IP20 | "
                 f"Funciones Especiales: SoftPLC incorporado, diagnóstico de alarmas, microprocesador de 32 bits | Protocolos: Modbus-RTU, CanOpen, Profibus-DP")
        app = f"Control preciso de velocidad, ahorro de energía y arranque suave en bombas centrífugas, ventiladores, transportadores, extrusoras y maquinaria industrial."
        items.append((brand, "Accionamientos y Variadores", "Variadores de Frecuencia (VFD)", ser, cod, nombre, desc, specs, app))

    # =========================================================================
    # 4. ARRANCADORES SUAVES (SOFT-STARTERS)
    # =========================================================================
    ssw_data = [
        ("10045001", "SSW050010T2246EP", "3 cv (2.2 kW)", "10 A", "220-460 Vca", "Arrancador suave compacto SSW05 10A con bypass"),
        ("10045002", "SSW050016T2246EP", "5 cv (3.7 kW)", "16 A", "220-460 Vca", "Arrancador suave compacto SSW05 16A con bypass"),
        ("10045003", "SSW050023T2246EP", "7.5 cv (5.5 kW)", "23 A", "220-460 Vca", "Arrancador suave compacto SSW05 23A con bypass"),
        ("10045004", "SSW050030T2246EP", "10 cv (7.5 kW)", "30 A", "220-460 Vca", "Arrancador suave compacto SSW05 30A con bypass"),
        ("10045005", "SSW050045T2246EP", "15 cv (11 kW)", "45 A", "220-460 Vca", "Arrancador suave compacto SSW05 45A con bypass"),
        ("10045006", "SSW050060T2246EP", "20 cv (15 kW)", "60 A", "220-460 Vca", "Arrancador suave compacto SSW05 60A con bypass"),
        ("10045007", "SSW050085T2246EP", "30 cv (22 kW)", "85 A", "220-460 Vca", "Arrancador suave compacto SSW05 85A con bypass"),
        ("10190001", "SSW070017T5SZ", "10 cv (7.5 kW)", "17 A", "220-575 Vca", "Arrancador suave industrial SSW07 17A 3 fases con bypass"),
        ("10190002", "SSW070030T5SZ", "15 cv (11 kW)", "30 A", "220-575 Vca", "Arrancador suave industrial SSW07 30A 3 fases con bypass"),
        ("10190003", "SSW070045T5SZ", "25 cv (18.5 kW)", "45 A", "220-575 Vca", "Arrancador suave industrial SSW07 45A 3 fases con bypass"),
        ("10190004", "SSW070061T5SZ", "30 cv (22 kW)", "61 A", "220-575 Vca", "Arrancador suave industrial SSW07 61A 3 fases con bypass"),
        ("10190005", "SSW070085T5SZ", "50 cv (37 kW)", "85 A", "220-575 Vca", "Arrancador suave industrial SSW07 85A 3 fases con bypass"),
        ("10190006", "SSW070130T5SZ", "75 cv (55 kW)", "130 A", "220-575 Vca", "Arrancador suave industrial SSW07 130A 3 fases con bypass"),
        ("10190007", "SSW070171T5SZ", "100 cv (75 kW)", "171 A", "220-575 Vca", "Arrancador suave industrial SSW07 171A 3 fases con bypass"),
        ("10190008", "SSW070200T5SZ", "125 cv (90 kW)", "200 A", "220-575 Vca", "Arrancador suave industrial SSW07 200A 3 fases con bypass"),
        ("10190009", "SSW070255T5SZ", "150 cv (110 kW)", "255 A", "220-575 Vca", "Arrancador suave industrial SSW07 255A 3 fases con bypass"),
        ("10190010", "SSW070312T5SZ", "200 cv (150 kW)", "312 A", "220-575 Vca", "Arrancador suave industrial SSW07 312A 3 fases con bypass"),
        ("10190011", "SSW070412T5SZ", "250 cv (185 kW)", "412 A", "220-575 Vca", "Arrancador suave industrial SSW07 412A 3 fases con bypass"),
        ("14120001", "SSW900A0045T5E21", "25 cv (18.5 kW)", "45 A", "220-575 Vca", "Arrancador suave inteligente SSW900 45A pantalla gráfica"),
        ("14120002", "SSW900B0085T5E21", "50 cv (37 kW)", "85 A", "220-575 Vca", "Arrancador suave inteligente SSW900 85A pantalla gráfica"),
        ("14120003", "SSW900C0130T5E21", "75 cv (55 kW)", "130 A", "220-575 Vca", "Arrancador suave inteligente SSW900 130A pantalla gráfica"),
        ("14120004", "SSW900C0200T5E21", "125 cv (90 kW)", "200 A", "220-575 Vca", "Arrancador suave inteligente SSW900 200A pantalla gráfica"),
        ("14120005", "SSW900D0312T5E21", "200 cv (150 kW)", "312 A", "220-575 Vca", "Arrancador suave inteligente SSW900 312A pantalla gráfica"),
        ("14120006", "SSW900D0412T5E21", "250 cv (185 kW)", "412 A", "220-575 Vca", "Arrancador suave inteligente SSW900 412A pantalla gráfica"),
        ("14120007", "SSW900E0600T5E21", "400 cv (300 kW)", "600 A", "220-575 Vca", "Arrancador suave inteligente SSW900 600A pantalla gráfica")
    ]
    for cod, ref, pot, cor, alim, tit in ssw_data:
        ser = ref[:5]
        nombre = f"Arrancador suave (Soft-Starter) WEG {ref} {pot} {cor} {alim} ({cod})"
        desc = (f"Arrancador suave para motores trifásicos marca WEG serie {ser} de {pot}, corriente nominal {cor}, tensión de trabajo {alim}, "
                f"con contactor de bypass incorporado, rampas de aceleración y desaceleración por tensión/corriente y protecciones térmicas integradas.")
        specs = (f"Marca: WEG | Serie: {ser} | Modelo/Ref: {ref} | Código WEG: {cod} | Potencia Recomendada: {pot} | "
                 f"Corriente Nominal (In): {cor} | Tensión de Alimentación (Ue): {alim} | Contacto de Bypass: Incorporado | "
                 f"Control de Fases: Control en las 3 fases | Protecciones: Sobrecarga del motor, falta de fase, desbalance de fase, sobrecorriente | "
                 f"Ajustes: Rampa de tensión, rampa de corriente, limitación de corriente, kick-start | Comunicación: Modbus-RTU, DeviceNet, Profibus-DP")
        app = f"Eliminación de picos de corriente en el arranque y reducción del desgaste mecánico en bombas, compresores, molinos, cintas y ventiladores industriales."
        items.append((brand, "Accionamientos y Variadores", "Arrancadores Suaves (Soft-Starters)", ser, cod, nombre, desc, specs, app))

    # =========================================================================
    # 5. CONTACTORES Y RELÉS TÉRMICOS DE SOBRECARGA
    # =========================================================================
    contactors_data = [
        ("10075001", "CWC07-10-30V26", "7 A (AC-3)", "3 cv (2.2 kW)", "220V 60Hz", "1 NA", "Minicontactor tripolar CWC07 7A bobina 220V"),
        ("10075002", "CWC09-10-30V26", "9 A (AC-3)", "4 cv (3.0 kW)", "220V 60Hz", "1 NA", "Minicontactor tripolar CWC09 9A bobina 220V"),
        ("10075003", "CWC012-10-30V26", "12 A (AC-3)", "5.5 cv (4.0 kW)", "220V 60Hz", "1 NA", "Minicontactor tripolar CWC012 12A bobina 220V"),
        ("10075004", "CWC016-10-30V26", "16 A (AC-3)", "7.5 cv (5.5 kW)", "220V 60Hz", "1 NA", "Minicontactor tripolar CWC016 16A bobina 220V"),
        ("10075005", "CWC09-10-30V04", "9 A (AC-3)", "4 cv (3.0 kW)", "24V 60Hz", "1 NA", "Minicontactor tripolar CWC09 9A bobina 24Vca"),
        ("10075006", "CWC09-10-30C03", "9 A (AC-3)", "4 cv (3.0 kW)", "24 Vcc", "1 NA", "Minicontactor tripolar CWC09 9A bobina 24Vcc"),
        ("12240001", "CWB9-11-30C18", "9 A (AC-3)", "4 cv (3.0 kW)", "110-130Vca", "1 NA + 1 NC", "Contactor modular compacto CWB9 9A bobina 110V"),
        ("12240002", "CWB9-11-30C26", "9 A (AC-3)", "4 cv (3.0 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor modular compacto CWB9 9A bobina 220V"),
        ("12240003", "CWB12-11-30C26", "12 A (AC-3)", "5.5 cv (4.0 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor modular compacto CWB12 12A bobina 220V"),
        ("12240004", "CWB18-11-30C26", "18 A (AC-3)", "10 cv (7.5 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor modular compacto CWB18 18A bobina 220V"),
        ("12240005", "CWB25-11-30C26", "25 A (AC-3)", "15 cv (11 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor modular compacto CWB25 25A bobina 220V"),
        ("12240006", "CWB32-11-30C26", "32 A (AC-3)", "20 cv (15 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor modular compacto CWB32 32A bobina 220V"),
        ("12240007", "CWB38-11-30C26", "38 A (AC-3)", "25 cv (18.5 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor modular compacto CWB38 38A bobina 220V"),
        ("12240008", "CWB40-11-30C26", "40 A (AC-3)", "25 cv (18.5 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor industrial CWB40 40A bobina 220V"),
        ("12240009", "CWB50-11-30C26", "50 A (AC-3)", "30 cv (22 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor industrial CWB50 50A bobina 220V"),
        ("12240010", "CWB65-11-30C26", "65 A (AC-3)", "40 cv (30 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor industrial CWB65 65A bobina 220V"),
        ("12240011", "CWB80-11-30C26", "80 A (AC-3)", "50 cv (37 kW)", "220-240Vca", "1 NA + 1 NC", "Contactor industrial CWB80 80A bobina 220V"),
        ("12240012", "CWB95-11-30C26", "60 cv (45 kW)", "95 A (AC-3)", "220-240Vca", "1 NA + 1 NC", "Contactor industrial CWB95 95A bobina 220V"),
        ("12240013", "CWB110-11-30C26", "75 cv (55 kW)", "110 A (AC-3)", "220-240Vca", "1 NA + 1 NC", "Contactor industrial CWB110 110A bobina 220V"),
        ("12240014", "CWB125-11-30C26", "80 cv (59 kW)", "125 A (AC-3)", "220-240Vca", "1 NA + 1 NC", "Contactor industrial CWB125 125A bobina 220V"),
        ("10048001", "CWM150-22-30V26", "150 A (AC-3)", "100 cv (75 kW)", "220V 60Hz", "2 NA + 2 NC", "Contactor de gran potencia CWM150 150A bobina 220V"),
        ("10048002", "CWM180-22-30V26", "180 A (AC-3)", "125 cv (90 kW)", "220V 60Hz", "2 NA + 2 NC", "Contactor de gran potencia CWM180 180A bobina 220V"),
        ("10048003", "CWM215-22-30V26", "215 A (AC-3)", "150 cv (110 kW)", "220V 60Hz", "2 NA + 2 NC", "Contactor de gran potencia CWM215 215A bobina 220V"),
        ("10048004", "CWM250-22-30V26", "250 A (AC-3)", "175 cv (132 kW)", "220V 60Hz", "2 NA + 2 NC", "Contactor de gran potencia CWM250 250A bobina 220V"),
        ("10048005", "CWM300-22-30V26", "300 A (AC-3)", "215 cv (160 kW)", "220V 60Hz", "2 NA + 2 NC", "Contactor de gran potencia CWM300 300A bobina 220V"),
        ("10048006", "CWM400-22-30V26", "400 A (AC-3)", "300 cv (220 kW)", "220V 60Hz", "2 NA + 2 NC", "Contactor de gran potencia CWM400 400A bobina 220V"),
        ("10185001", "CWMC25-10-30V26", "25 A", "15 kvar (220V) / 30 kvar (400V)", "220V 60Hz", "1 NA", "Contactor para condensadores CWMC25 15-30 kvar"),
        ("10185002", "CWMC32-10-30V26", "32 A", "20 kvar (220V) / 40 kvar (400V)", "220V 60Hz", "1 NA", "Contactor para condensadores CWMC32 20-40 kvar"),
        ("10185003", "CWMC50-10-30V26", "50 A", "30 kvar (220V) / 60 kvar (400V)", "220V 60Hz", "1 NA", "Contactor para condensadores CWMC50 30-60 kvar"),
        ("10049001", "RW27-2D3-U004", "0.28 a 0.4 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 0.28-0.4A"),
        ("10049002", "RW27-2D3-U010", "0.63 a 1.0 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 0.63-1.0A"),
        ("10049003", "RW27-2D3-U025", "1.6 a 2.5 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 1.6-2.5A"),
        ("10049004", "RW27-2D3-U040", "2.8 a 4.0 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 2.8-4.0A"),
        ("10049005", "RW27-2D3-U063", "4.0 a 6.3 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 4.0-6.3A"),
        ("10049006", "RW27-2D3-U100", "7.0 a 10.0 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 7.0-10.0A"),
        ("10049007", "RW27-2D3-U150", "10.0 a 15.0 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 10.0-15.0A"),
        ("10049008", "RW27-2D3-U230", "15.0 a 23.0 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 15.0-23.0A"),
        ("10049009", "RW27-2D3-U320", "22.0 a 32.0 A", "Para CWB9-CWB38", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW27 rango 22.0-32.0A"),
        ("10049010", "RW67-1D3-U050", "32.0 a 50.0 A", "Para CWB40-CWB80", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW67 rango 32.0-50.0A"),
        ("10049011", "RW67-1D3-U065", "40.0 a 65.0 A", "Para CWB40-CWB80", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW67 rango 40.0-65.0A"),
        ("10049012", "RW117-1D3-U097", "63.0 a 97.0 A", "Para CWB95-CWB125", "Diferencial", "1 NA + 1 NC", "Relé térmico de sobrecarga RW117 rango 63.0-97.0A")
    ]
    for cod, ref, ic, pot, bob, aux, tit in contactors_data:
        ser = ref.split('-')[0]
        fam = "Relés Térmicos de Sobrecarga" if ser.startswith("RW") else "Contactores y Relés"
        nombre = f"{fam} WEG {ref} {ic} {bob} ({cod})"
        desc = (f"{tit} marca WEG serie {ser}, corriente de régimen {ic}, para motores de {pot}, "
                f"tensión de bobina {bob}, contactos auxiliares {aux}, montaje directo o riel DIN.")
        specs = (f"Marca: WEG | Serie: {ser} | Modelo/Ref: {ref} | Código WEG: {cod} | Corriente Nominal: {ic} | "
                 f"Potencia Motor (380V): {pot} | Tensión de Bobina/Control: {bob} | Contactos Auxiliares: {aux} | "
                 f"Tensión Nominal de Aislamiento (Ui): 1000 V | Grado de Protección: IP20 | Montaje: Riel DIN 35 mm / Tornillos | Norma: IEC 60947-4-1")
        app = f"Maniobra, arranque directo, inversión de marcha y protección térmica de motores eléctricos trifásicos en tableros de control industrial."
        items.append((brand, "Maniobra y Control Industrial", fam, ser, cod, nombre, desc, specs, app))

    # =========================================================================
    # 6. GUARDAMOTORES (MPW)
    # =========================================================================
    mpw_data = [
        ("12430001", "MPW18-3-U0016", "0.10 a 0.16 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 0.1-0.16A"),
        ("12430002", "MPW18-3-U0025", "0.16 a 0.25 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 0.16-0.25A"),
        ("12430003", "MPW18-3-U0040", "0.25 a 0.40 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 0.25-0.40A"),
        ("12430004", "MPW18-3-U0063", "0.40 a 0.63 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 0.40-0.63A"),
        ("12430005", "MPW18-3-U010", "0.63 a 1.0 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 0.63-1.0A"),
        ("12430006", "MPW18-3-U016", "1.0 a 1.6 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 1.0-1.6A"),
        ("12430007", "MPW18-3-U025", "1.6 a 2.5 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 1.6-2.5A"),
        ("12430008", "MPW18-3-U040", "2.5 a 4.0 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 2.5-4.0A"),
        ("12430009", "MPW18-3-U063", "4.0 a 6.3 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 4.0-6.3A"),
        ("12430010", "MPW18-3-U0100", "6.3 a 10.0 A", "100 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 6.3-10.0A"),
        ("12430011", "MPW18-3-U0160", "10.0 a 16.0 A", "50 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 10.0-16.0A"),
        ("12430012", "MPW18-3-U0180", "12.0 a 18.0 A", "50 kA", "Tripolar 3P", "Guardamotor termomagnético MPW18 rango 12.0-18.0A"),
        ("10156001", "MPW40-3-U0016", "0.10 a 0.16 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 0.1-0.16A"),
        ("10156002", "MPW40-3-U0025", "0.16 a 0.25 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 0.16-0.25A"),
        ("10156003", "MPW40-3-U004", "0.25 a 0.40 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 0.25-0.40A"),
        ("10156004", "MPW40-3-U0063", "0.40 a 0.63 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 0.40-0.63A"),
        ("10156005", "MPW40-3-U010", "0.63 a 1.0 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 0.63-1.0A"),
        ("10156006", "MPW40-3-U016", "1.0 a 1.6 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 1.0-1.6A"),
        ("10156007", "MPW40-3-U025", "1.6 a 2.5 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 1.6-2.5A"),
        ("10156008", "MPW40-3-U040", "2.5 a 4.0 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 2.5-4.0A"),
        ("10156009", "MPW40-3-U063", "4.0 a 6.3 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 4.0-6.3A"),
        ("10156010", "MPW40-3-U0100", "6.3 a 10.0 A", "100 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 6.3-10.0A"),
        ("10156011", "MPW40-3-U0160", "10.0 a 16.0 A", "50 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 10.0-16.0A"),
        ("10156012", "MPW40-3-U0200", "16.0 a 20.0 A", "50 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 16.0-20.0A"),
        ("10156013", "MPW40-3-U0250", "20.0 a 25.0 A", "50 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 20.0-25.0A"),
        ("10156014", "MPW40-3-U0320", "25.0 a 32.0 A", "50 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 25.0-32.0A"),
        ("10156015", "MPW40-3-U0400", "32.0 a 40.0 A", "50 kA", "Tripolar 3P", "Guardamotor industrial MPW40 rango 32.0-40.0A"),
        ("10158001", "MPW80-3-U050", "32.0 a 50.0 A", "50 kA", "Tripolar 3P", "Guardamotor de alta potencia MPW80 rango 32-50A"),
        ("10158002", "MPW80-3-U065", "45.0 a 65.0 A", "50 kA", "Tripolar 3P", "Guardamotor de alta potencia MPW80 rango 45-65A"),
        ("10158003", "MPW80-3-U080", "55.0 a 80.0 A", "50 kA", "Tripolar 3P", "Guardamotor de alta potencia MPW80 rango 55-80A"),
        ("10159001", "MPW100-3-U090", "55.0 a 90.0 A", "50 kA", "Tripolar 3P", "Guardamotor de gran calibre MPW100 rango 55-90A"),
        ("10159002", "MPW100-3-U100", "75.0 a 100.0 A", "50 kA", "Tripolar 3P", "Guardamotor de gran calibre MPW100 rango 75-100A")
    ]
    for cod, ref, ir, icu, pol, tit in mpw_data:
        ser = ref.split('-')[0]
        nombre = f"Guardamotor termomagnético tripolar WEG {ref} {ir} Icu {icu} ({cod})"
        desc = (f"Disyuntor guardamotor termomagnético tripolar (3P) marca WEG serie {ser} con rango de ajuste térmico de {ir}, "
                f"disparo magnético instantáneo calibrado a 13xIn, capacidad de cortocircuito Icu de {icu} a 400Vca y compensación de temperatura.")
        specs = (f"Marca: WEG | Serie: {ser} | Modelo/Ref: {ref} | Código WEG: {cod} | Número de Polos: 3P | "
                 f"Rango de Ajuste Térmico (Ir): {ir} | Disparo Magnético: 13 x In (instantáneo) | Capacidad de Ruptura (Icu a 400V): {icu} | "
                 f"Tensión de Operación (Ue): 690 Vca | Sensibilidad a Fallo de Fase: Sí (IEC 60947-4-1) | Maniobras: Rotativa bloqueable con candado | Montaje: Riel DIN 35 mm")
        app = f"Protección integral de motores eléctricos contra sobrecargas, cortocircuitos y fallas de fase en tableros de bombas, compresores y maquinaria."
        items.append((brand, "Maniobra y Control Industrial", "Guardamotores Termomagnéticos", ser, cod, nombre, desc, specs, app))

    # =========================================================================
    # 7. SECCIONADORES BAJO CARGA (MSW) Y PORTAFUSIBLES (FSW)
    # =========================================================================
    secc_data = [
        ("11890001", "MSW-16-3P", "16 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 16A"),
        ("11890002", "MSW-25-3P", "25 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 25A"),
        ("11890003", "MSW-32-3P", "32 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 32A"),
        ("11890004", "MSW-40-3P", "40 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 40A"),
        ("11890005", "MSW-63-3P", "63 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 63A"),
        ("11890006", "MSW-80-3P", "80 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 80A"),
        ("11890007", "MSW-100-3P", "100 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 100A"),
        ("11890008", "MSW-125-3P", "125 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 125A"),
        ("11890009", "MSW-160-3P", "160 A", "690 Vca", "3P Tripolar", "Manija rotativa roja/amarilla", "Seccionador bajo carga tripolar MSW 160A"),
        ("10080001", "FSW-100-3P", "100 A", "690 Vca", "NH00 Tripolar", "Seccionador con fusibles", "Seccionador portafusible NH00 tripolar FSW 100A"),
        ("10080002", "FSW-160-3P", "160 A", "690 Vca", "NH00 Tripolar", "Seccionador con fusibles", "Seccionador portafusible NH00 tripolar FSW 160A"),
        ("10080003", "FSW-250-3P", "250 A", "690 Vca", "NH1 Tripolar", "Seccionador con fusibles", "Seccionador portafusible NH1 tripolar FSW 250A"),
        ("10080004", "FSW-400-3P", "400 A", "690 Vca", "NH2 Tripolar", "Seccionador con fusibles", "Seccionador portafusible NH2 tripolar FSW 400A"),
        ("10080005", "FSW-630-3P", "630 A", "690 Vca", "NH3 Tripolar", "Seccionador con fusibles", "Seccionador portafusible NH3 tripolar FSW 630A")
    ]
    for cod, ref, in_a, ue, pol, man, tit in secc_data:
        ser = ref.split('-')[0]
        nombre = f"Interruptor seccionador {tit} WEG {ref} {in_a} {pol} ({cod})"
        desc = (f"Interruptor seccionador bajo carga marca WEG serie {ser} de {in_a}, tensión nominal {ue}, {pol}, "
                f"con {man.lower()}, bloqueo por candado (hasta 3 candados para bloqueo de seguridad LOTO) y fijación en riel DIN o puerta de panel.")
        specs = (f"Marca: WEG | Serie: {ser} | Modelo/Ref: {ref} | Código WEG: {cod} | Corriente Nominal (In): {in_a} | "
                 f"Tensión Nominal (Ue): {ue} | Polos: {pol} | Categoría de Empleo: AC-21A / AC-22A / AC-23A | Bloqueo: Manija candadeable | Norma: IEC 60947-3")
        app = f"Seccionamiento visible y seguro de energía en tableros de maquinaria, entradas de fuerza y desconexión de emergencia bajo normas de seguridad industrial."
        items.append((brand, "Maniobra y Control Industrial", "Interruptores Seccionadores Bajo Carga", ser, cod, nombre, desc, specs, app))

    # =========================================================================
    # 8. MANDO Y SEÑALIZACIÓN (CSW, LTW) Y FUENTES DE PODER (PSS24W)
    # =========================================================================
    ctrl_data = [
        ("10091001", "CSW-BF1-10", "Pulsador rasante 22mm", "Verde", "1 NA", "Pulsador de marcha rasante verde 22mm"),
        ("10091002", "CSW-BF2-01", "Pulsador rasante 22mm", "Rojo", "1 NC", "Pulsador de parada rasante rojo 22mm"),
        ("10091003", "CSW-BF3-10", "Pulsador rasante 22mm", "Negro", "1 NA", "Pulsador rasante negro 22mm"),
        ("10091004", "CSW-BESG-01", "Pulsador tipo hongo 40mm", "Rojo", "1 NC", "Pulsador de parada de emergencia con destrabe por giro 22mm"),
        ("10091005", "CSW-CK2F45-10", "Selector de 2 posiciones fijas 22mm", "Negro", "1 NA", "Selector 2 posiciones 90 grados"),
        ("10091006", "CSW-CK3F45-20", "Selector de 3 posiciones fijas 22mm", "Negro", "2 NA", "Selector 3 posiciones 45 grados"),
        ("10091010", "CSW-BC10", "Bloque de contacto auxiliar", "1 NA", "Para mando 22mm", "Bloque de contacto frontal 1 NA para botoneras CSW"),
        ("10091011", "CSW-BC01", "Bloque de contacto auxiliar", "1 NC", "Para mando 22mm", "Bloque de contacto frontal 1 NC para botoneras CSW"),
        ("10092001", "LTW-V26-VM", "Luz piloto LED 22mm", "Rojo", "12 a 240 Vca/cc", "Luz piloto LED monobloc rojo 22mm"),
        ("10092002", "LTW-V26-VD", "Luz piloto LED 22mm", "Verde", "12 a 240 Vca/cc", "Luz piloto LED monobloc verde 22mm"),
        ("10092003", "LTW-V26-AM", "Luz piloto LED 22mm", "Amarillo", "12 a 240 Vca/cc", "Luz piloto LED monobloc amarillo 22mm"),
        ("10092004", "LTW-V26-AZ", "Luz piloto LED 22mm", "Azul", "12 a 240 Vca/cc", "Luz piloto LED monobloc azul 22mm"),
        ("10092005", "LTW-V26-BR", "Luz piloto LED 22mm", "Blanco", "12 a 240 Vca/cc", "Luz piloto LED monobloc blanco 22mm"),
        ("11450001", "PSS24W-1.25A", "Fuente conmutada riel DIN", "24 Vcc / 1.25 A (30 W)", "85-264 Vca", "Fuente de alimentación para riel DIN 24V 1.25A"),
        ("11450002", "PSS24W-2.5A", "Fuente conmutada riel DIN", "24 Vcc / 2.5 A (60 W)", "85-264 Vca", "Fuente de alimentación para riel DIN 24V 2.5A"),
        ("11450003", "PSS24W-5A", "Fuente conmutada riel DIN", "24 Vcc / 5.0 A (120 W)", "85-264 Vca", "Fuente de alimentación para riel DIN 24V 5A"),
        ("11450004", "PSS24W-10A", "Fuente conmutada riel DIN", "24 Vcc / 10.0 A (240 W)", "85-264 Vca", "Fuente de alimentación para riel DIN 24V 10A"),
        ("11450005", "PSS24W-20A", "Fuente conmutada riel DIN", "24 Vcc / 20.0 A (480 W)", "85-264 Vca", "Fuente de alimentación para riel DIN 24V 20A"),
        ("11450006", "PSS24W-40A", "Fuente conmutada riel DIN", "24 Vcc / 40.0 A (960 W)", "380-480 Vca trifásica", "Fuente de alimentación para riel DIN 24V 40A trifásica")
    ]
    for cod, ref, tip, par1, par2, tit in ctrl_data:
        ser = ref.split('-')[0]
        fam = "Fuentes de Alimentación Riel DIN" if ser.startswith("PSS") else "Mando y Señalización 22mm"
        linea = "Automatización y Control" if ser.startswith("PSS") else "Maniobra y Control Industrial"
        nombre = f"{fam} WEG {ref} {par1} {par2} ({cod})"
        desc = (f"{tit} marca WEG serie {ser}, características: {par1}, rango/voltaje {par2}, grado de protección frontal IP66 para botoneras o IP20 para fuentes, alta durabilidad eléctrica.")
        specs = (f"Marca: WEG | Serie: {ser} | Modelo/Ref: {ref} | Código WEG: {cod} | Parámetros: {par1} | Tensión/Voltaje: {par2} | "
                 f"Diámetro/Montaje: 22 mm para mando / Riel DIN 35 mm para fuentes | Norma: IEC 60947-5-1 / IEC 61204")
        app = f"Control manual, señalización de estados de funcionamiento, alarmas de falla y alimentación de PLCs, sensores y relés en tableros eléctricos."
        items.append((brand, linea, fam, ser, cod, nombre, desc, specs, app))

    # =========================================================================
    # 9. SEGURIDAD ELECTRÓNICA Y CCTV (WCAM)
    # =========================================================================
    if os.path.exists("wcam_extracted.txt"):
        with open("wcam_extracted.txt", "r", encoding="utf-8") as f:
            w_text = f.read()

        matches_wcam = re.findall(r'([^\n]+?)\s*\n\s*(\d{8})\s*\n\s*([^\n]*(?:WCAM|GRAVADOR|SWITCH|NVR|DVR)[^\n]*)', w_text, re.IGNORECASE)
        for d, c, m in matches_wcam:
            m_clean = m.strip()
            d_tr = (d.replace("Câmera", "Cámara")
                     .replace("lente de", "lente de")
                     .replace("resolução", "resolución")
                     .replace("saída", "salida")
                     .replace("disco", "disco rígido")
                     .replace("portas", "puertos")
                     .replace("função", "función")
                     .replace("até", "hasta")
                     .replace("alimentação", "alimentación")
                     .replace("canais", "canales")
                     .replace("Linha analógica", "Línea analógica")
                     .replace("Linha IP", "Línea IP"))
            
            tipo = "Cámara de Seguridad CCTV"
            if "NVR" in m_clean or "GRAVADOR" in m_clean or "DVR" in m_clean:
                tipo = "Grabador de Video (DVR / NVR)"
            elif "SWITCH" in m_clean:
                tipo = "Switch de Red PoE"
            
            nombre = f"{tipo} WEG {m_clean} ({c})"
            desc = f"{tipo} marca WEG serie WCAM modelo {m_clean}: {d_tr.strip()}."
            specs = f"Marca: WEG | Serie: WCAM | Modelo/Ref: {m_clean} | Código WEG: {c} | Especificación: {d_tr.strip()}"
            app = "Seguridad electrónica, videovigilancia y monitoreo perimetral e interior en instalaciones comerciales, residenciales e industriales."
            items.append((brand, "Seguridad Electrónica y CCTV", "Sistemas de Videovigilancia WCAM", "WCAM", c, nombre, desc, specs, app))

    # =========================================================================
    # 10. TOMACORRIENTES E INTERRUPTORES (COMPOSÉ & EQUILLE) Y TOMAS INDUSTRIALES
    # =========================================================================
    wiring_data = [
        ("13110001", "13110001", "Módulo Interruptor Simple 10A 250V~ Blanco Composé", "Composé", "Interruptor 1 vía 10A", "Módulo interruptor unipolar 10A"),
        ("13110002", "13110002", "Módulo Interruptor Paralelo (3 Vías / Conmutador) 10A 250V~ Blanco Composé", "Composé", "Conmutador 3 vías 10A", "Módulo interruptor conmutador vaivén"),
        ("13110003", "13110003", "Módulo Interruptor Intermedio (4 Vías / Cruzamiento) 10A 250V~ Blanco Composé", "Composé", "Cruzamiento 4 vías 10A", "Módulo interruptor intermedio"),
        ("13110004", "13110004", "Módulo Pulsador de Timbre 10A 250V~ Blanco Composé", "Composé", "Pulsador contacto NA 10A", "Módulo pulsador para timbre"),
        ("13110005", "13110005", "Módulo Tomacorriente 2P+T 10A 250V~ Blanco Composé", "Composé", "Tomacorriente 2P+T 10A", "Módulo tomacorriente estándar"),
        ("13110006", "13110006", "Módulo Tomacorriente 2P+T 20A 250V~ Rojo Composé (Uso Dedicado)", "Composé", "Tomacorriente 2P+T 20A", "Módulo tomacorriente de fuerza 20A"),
        ("13110007", "13110007", "Módulo Tomacorriente Schuko 16A 250V~ con Tierra Lateral Blanco Composé", "Composé", "Tomacorriente Schuko 16A", "Módulo toma europea/schuko 16A"),
        ("13110008", "13110008", "Módulo Cargador USB Doble (Tipo A + Tipo C) 5V 3.0A Blanco Composé", "Composé", "Cargador USB dual 3A", "Módulo cargador rápido para móviles"),
        ("13110009", "13110009", "Módulo Conector de Datos RJ45 Categoría 6 UTP Blanco Composé", "Composé", "Toma de red RJ45 Cat6", "Módulo de red computación Gigabit"),
        ("13110010", "13110010", "Módulo Dimmer Rotativo para Lámparas LED 127/220V~ Blanco Composé", "Composé", "Atenuador de luz rotativo", "Módulo dimmer variador de luminosidad"),
        ("13110020", "13110020", "Placa con Soporte 4x2 para 1 Módulo Blanco Composé", "Composé", "Placa 4x2 1 ventana", "Placa de terminación 4x2 1 módulo"),
        ("13110021", "13110021", "Placa con Soporte 4x2 para 2 Módulos Blanco Composé", "Composé", "Placa 4x2 2 ventanas", "Placa de terminación 4x2 2 módulos"),
        ("13110022", "13110022", "Placa con Soporte 4x2 para 3 Módulos Blanco Composé", "Composé", "Placa 4x2 3 ventanas", "Placa de terminación 4x2 3 módulos"),
        ("13110023", "13110023", "Placa con Soporte 4x4 para 4 Módulos Blanco Composé", "Composé", "Placa 4x4 4 ventanas", "Placa de terminación 4x4 4 módulos"),
        ("13110024", "13110024", "Placa con Soporte 4x4 para 6 Módulos Blanco Composé", "Composé", "Placa 4x4 6 ventanas", "Placa de terminación 4x4 6 módulos"),
        ("11220001", "PI-2P+T-16A-220V", "Enchufe / Clavija industrial macho móvil 16A 2P+T 220V Azul IP44 IEC 60309", "Industrial", "16A 220V 2P+T IP44", "Enchufe industrial móvil azul"),
        ("11220002", "TI-2P+T-16A-220V", "Tomacorriente industrial hembra de sobreponer 16A 2P+T 220V Azul IP44 IEC 60309", "Industrial", "16A 220V 2P+T IP44", "Toma industrial de sobreponer azul"),
        ("11220003", "PI-3P+T-16A-380V", "Enchufe industrial macho móvil 16A 3P+T 380/440V Rojo IP44 IEC 60309", "Industrial", "16A 380V 3P+T IP44", "Enchufe industrial móvil rojo"),
        ("11220004", "TI-3P+T-16A-380V", "Tomacorriente industrial hembra de sobreponer 16A 3P+T 380/440V Rojo IP44 IEC 60309", "Industrial", "16A 380V 3P+T IP44", "Toma industrial de sobreponer rojo"),
        ("11220005", "PI-3P+T-32A-380V", "Enchufe industrial macho móvil 32A 3P+T 380/440V Rojo IP44 IEC 60309", "Industrial", "32A 380V 3P+T IP44", "Enchufe industrial de fuerza 32A rojo"),
        ("11220006", "TI-3P+T-32A-380V", "Tomacorriente industrial hembra de sobreponer 32A 3P+T 380/440V Rojo IP44 IEC 60309", "Industrial", "32A 380V 3P+T IP44", "Toma industrial de fuerza 32A rojo"),
        ("11220007", "PI-3P+N+T-32A-380V", "Enchufe industrial macho móvil 32A 3P+N+T 380/440V Rojo IP67 IEC 60309", "Industrial", "32A 380V 3P+N+T IP67", "Enchufe estanco industrial 32A 5 polos"),
        ("11220008", "TI-3P+N+T-32A-380V", "Tomacorriente industrial de sobreponer 32A 3P+N+T 380/440V Rojo IP67 IEC 60309", "Industrial", "32A 380V 3P+N+T IP67", "Toma estanca industrial 32A 5 polos"),
        ("11220009", "PI-3P+N+T-63A-380V", "Enchufe industrial macho móvil de alta potencia 63A 3P+N+T 380/440V Rojo IP67 IEC 60309", "Industrial", "63A 380V 3P+N+T IP67", "Enchufe de potencia industrial 63A 5 polos"),
        ("11220010", "TI-3P+N+T-63A-380V", "Tomacorriente industrial de sobreponer 63A 3P+N+T 380/440V Rojo IP67 IEC 60309", "Industrial", "63A 380V 3P+N+T IP67", "Toma de potencia industrial 63A 5 polos")
    ]
    for cod, ref, nom, ser, par, tit in wiring_data:
        fam = "Tomas y Enchufes Industriales IEC 60309" if ser == "Industrial" else "Tomacorrientes e Interruptores Modulares"
        linea = "Tomas y Conectores Industriales" if ser == "Industrial" else "Instalaciones Eléctricas y Conectividad"
        desc = f"{nom} marca WEG línea {ser}, material termoplástico anti-amarilleo o autoextinguible PA6, contactos de latón de alta conductividad."
        specs = f"Marca: WEG | Serie: {ser} | Modelo/Ref: {ref} | Código WEG: {cod} | Características: {par} | Certificación: IEC 60669 / IEC 60884 / IEC 60309"
        app = "Conexión de artefactos, circuitos de iluminación y alimentación de maquinaria trifásica en obras, industrias y residencias."
        items.append((brand, linea, fam, ser, cod, nom, desc, specs, app))

    return items

def insert_weg_and_sync():
    items = generate_weg_catalog()
    print(f"Total WEG items prepared: {len(items)}")

    db_path = os.path.abspath("agente_ventas.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Eliminar registros previos de WEG si existieran
    cur.execute("DELETE FROM ProductsCatalog WHERE Brand = 'WEG'")
    print(f"Deleted old WEG products. Inserting {len(items)} fresh products...")

    cur.executemany("""
        INSERT INTO ProductsCatalog 
        (Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, items)
    conn.commit()

    # Reconstruir tablas FTS5
    print("Rebuilding FTS5 full-text index...")
    for fts_table in ["Products_FTS", "ProductsCatalog_fts"]:
        try:
            cur.execute(f"DROP TABLE IF EXISTS {fts_table}")
            cur.execute(f"""
                CREATE VIRTUAL TABLE {fts_table} USING fts5(
                    Code, Name, Description, TechnicalSpecs, Application, Brand, Series, Family, BusinessLine,
                    content='ProductsCatalog',
                    content_rowid='Id',
                    tokenize='unicode61 remove_diacritics 2'
                )
            """)
            cur.execute(f"""
                INSERT INTO {fts_table}(rowid, Code, Name, Description, TechnicalSpecs, Application, Brand, Series, Family, BusinessLine)
                SELECT Id, Code, Name, Description, TechnicalSpecs, Application, Brand, Series, Family, BusinessLine FROM ProductsCatalog
            """)
            conn.commit()
            print(f"FTS5 table {fts_table} rebuilt successfully.")
        except Exception as e:
            print(f"Error rebuilding {fts_table}: {e}")

    # Verificar conteos
    cur.execute("SELECT Brand, COUNT(*) FROM ProductsCatalog GROUP BY Brand")
    print("\n=== Conteo de Productos por Marca en DB Local ===")
    for b, count in cur.fetchall():
        print(f"  {b}: {count}")
    
    cur.execute("SELECT COUNT(*) FROM ProductsCatalog")
    total = cur.fetchone()[0]
    print(f"Total General en DB: {total}")
    conn.close()

    # Sincronizar hacia todas las demás rutas
    print("\nSincronizando copias de la base de datos...")
    targets = [
        os.path.abspath("AgentePower/agente_ventas.db"),
        os.path.abspath("AgentePower/bin/Debug/net8.0/agente_ventas.db"),
        os.path.abspath("AgentePower/bin/Release/net8.0/agente_ventas.db"),
        os.path.abspath("publish/agente_ventas.db")
    ]
    for t in targets:
        if os.path.exists(os.path.dirname(t)):
            shutil.copy2(db_path, t)
            print(f"  Synced -> {t}")

    print("\n¡Catálogo WEG integrado y sincronizado con éxito!")

if __name__ == "__main__":
    insert_weg_and_sync()
