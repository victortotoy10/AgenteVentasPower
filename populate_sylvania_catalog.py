import sqlite3
import json
import os

DB_PATHS = [
    r"c:\Users\lenovo\Desktop\AgenteVentasPower\agente_ventas.db",
    r"c:\Users\lenovo\Desktop\AgenteVentasPower\AgentePower\agente_ventas.db",
    r"c:\Users\lenovo\Desktop\AgenteVentasPower\AgentePower\bin\Debug\net8.0\agente_ventas.db",
    r"c:\Users\lenovo\Desktop\AgenteVentasPower\AgentePower\bin\Release\net8.0\agente_ventas.db",
    r"c:\Users\lenovo\Desktop\AgenteVentasPower\publish\agente_ventas.db",
]

def get_sylvania_master_catalog():
    return [
        # =========================================================================
        # 1. CAMPANAS INDUSTRIALES LED (HIGH BAY UFO & GRANDES ALTURAS)
        # =========================================================================
        {
            "Code": "P29856",
            "Name": "Campana Industrial LED High Bay GC350 3CCT 75W/110W/150W Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Campanas Industriales LED (High Bay)",
            "Series": "High Bay GC350",
            "Description": "Campana industrial LED tipo UFO multivat térmica y ópticamente optimizada. Permite seleccionar 3 niveles de potencia (75W/110W/150W) y 3 temperaturas de color (4000K/5000K/5700K 3CCT). Eficacia de 160 lm/W hasta 24.000 lúmenes, chasis de aluminio inyectado gris RAL 7042, protección IP65 e impacto IK08. Driver atenuable 0-10V multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Ajustable": "75W / 110W / 150W",
                "Flujo_Luminoso": "12.000 lm / 18.000 lm / 24.000 lm",
                "Eficacia": "160 lm/W",
                "Temperatura_Color": "4000K / 5000K / 5700K (3CCT)",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC 50/60Hz",
                "Atenuacion": "Dimerizable 0-10V",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK08",
                "Factor_Potencia": ">0.95",
                "THD": "<20%",
                "IRC": "80",
                "Vida_Util": "130.000 horas L70",
                "Montaje": "Argolla metálica de suspensión (cadena y gancho incluidos)",
                "Garantia": "7 años"
            }, ensure_ascii=False),
            "Application": "Iluminación de grandes alturas en plantas de producción, bodegas logísticas, centros de distribución, naves industriales y talleres metalmecánicos."
        },
        {
            "Code": "P29999",
            "Name": "Campana Industrial LED High Bay GC350 3CCT 100W/150W/200W Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Campanas Industriales LED (High Bay)",
            "Series": "High Bay GC350",
            "Description": "Campana industrial LED de alta potencia UFO multivat y multicolo. Potencia seleccionable de 100W, 150W y 200W con flujo luminoso de hasta 32.000 lúmenes a 160 lm/W. Ajuste de CCT a 4000K, 5000K o 5700K. Chasis robusto de aluminio fundido disipador, protección IP65, driver 0-10V 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Ajustable": "100W / 150W / 200W",
                "Flujo_Luminoso": "16.000 lm / 24.000 lm / 32.000 lm",
                "Eficacia": "160 lm/W",
                "Temperatura_Color": "4000K / 5000K / 5700K (3CCT)",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC 50/60Hz",
                "Atenuacion": "0-10V",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK08",
                "Factor_Potencia": ">0.95",
                "THD": "<20%",
                "IRC": "80",
                "Vida_Util": "130.000 horas L70",
                "Garantia": "7 años"
            }, ensure_ascii=False),
            "Application": "Plantas industriales pesadas, almacenes de estantería alta, complejos fabriles, terminales de carga e industrias de alimentos."
        },
        {
            "Code": "P29538",
            "Name": "Campana Industrial LED High Bay GC109 100W 6000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Campanas Industriales LED (High Bay)",
            "Series": "High Bay GC109",
            "Description": "Campana industrial LED suspendida tipo UFO de 100W, flujo de 13.200 lúmenes con eficacia de 130 lm/W en luz blanca fría 6000K. Chasis compacto de fundición de aluminio negro RAL 7010 con aletas disipadoras radiales, óptica simétrica de 90°, IP65 e impacto IK08.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "100W",
                "Flujo_Luminoso": "13.200 lm",
                "Eficacia": "130 lm/W",
                "Temperatura_Color": "6000K",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK08",
                "Factor_Potencia": "0.95",
                "THD": "<20%",
                "IRC": "80",
                "Vida_Util": "40.000 horas L70",
                "Garantia": "3 años"
            }, ensure_ascii=False),
            "Application": "Bodegas de almacenamiento mediano, galpones industriales, talleres y áreas de manufactura."
        },
        {
            "Code": "P29539",
            "Name": "Campana Industrial LED High Bay GC109 150W 6000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Campanas Industriales LED (High Bay)",
            "Series": "High Bay GC109",
            "Description": "Campana industrial LED UFO de 150W que entrega 20.400 lúmenes a 130 lm/W. Luz fría 6000K de alta agudeza visual. Cuerpo hermético IP65 resistente al polvo y chorros de agua con clasificación de impacto IK08. Tensión de red 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "150W",
                "Flujo_Luminoso": "20.400 lm",
                "Eficacia": "130 lm/W",
                "Temperatura_Color": "6000K",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK08",
                "Factor_Potencia": "0.95",
                "Vida_Util": "40.000 horas L70",
                "Garantia": "3 años"
            }, ensure_ascii=False),
            "Application": "Almacenes principales, centros de acopio, líneas de ensamblaje y hangares."
        },
        {
            "Code": "P29541",
            "Name": "Campana Industrial LED High Bay GC109 200W 6000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Campanas Industriales LED (High Bay)",
            "Series": "High Bay GC109",
            "Description": "Campana industrial LED UFO de alta potencia 200W con 26.600 lúmenes de salida a 130 lm/W en 6000K. Para alturas de instalación superiores a 8 metros. Chasis de aluminio fundido, IP65, IK08, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "200W",
                "Flujo_Luminoso": "26.600 lm",
                "Eficacia": "130 lm/W",
                "Temperatura_Color": "6000K",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK08",
                "Factor_Potencia": "0.95",
                "Vida_Util": "40.000 horas L70",
                "Garantia": "3 años"
            }, ensure_ascii=False),
            "Application": "Bodegas de techos altos (8 a 15 metros), astilleros, molinos, fundiciones y almacenes de acopio masivo."
        },
        {
            "Code": "P26390",
            "Name": "Luminaria LED High Bay Canopy Sobreponer 120W 6000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Campanas Industriales LED (High Bay)",
            "Series": "High Bay Canopy",
            "Description": "Luminaria profesional tipo Canopy para adosar o sobreponer en techos de estaciones de servicio (gasolineras) y áreas cubiertas. 120W, 15.000 lúmenes (125 lm/W) en 6000K, óptica simétrica de 100°, grado de hermeticidad IP65 y máxima resistencia al impacto mecánico IK10.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "120W",
                "Flujo_Luminoso": "15.000 lm",
                "Eficacia": "125 lm/W",
                "Temperatura_Color": "6000K",
                "Angulo_Apertura": "100°",
                "Tension_Operacion": "100-277V AC",
                "Atenuacion": "0-10V Dimerizable",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK10",
                "Factor_Potencia": "0.9",
                "Vida_Util": "50.000 horas L70",
                "Montaje": "Sobrepuesto en techo / dosel",
                "Garantia": "3 años"
            }, ensure_ascii=False),
            "Application": "Islas de despacho y aleros en gasolineras / estaciones de servicio, peajes de autopista y marquesinas industriales."
        },
        {
            "Code": "P29706",
            "Name": "Luminaria LED High Bay Canopy Incrustar 120W 5700K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Campanas Industriales LED (High Bay)",
            "Series": "High Bay Canopy",
            "Description": "Luminaria tipo Canopy de embutir/incrustar con marco biselado blanco RAL 9003 para plafones de estaciones de servicio y aleros comerciales. 120W, 16.800 lúmenes con alta eficacia de 140 lm/W en 5700K. Grado IP65, impacto IK06, driver multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "120W",
                "Flujo_Luminoso": "16.800 lm",
                "Eficacia": "140 lm/W",
                "Temperatura_Color": "5700K",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK06",
                "Factor_Potencia": "0.95",
                "Montaje": "Incrustado en cielo raso / cubierta",
                "Garantia": "3 años"
            }, ensure_ascii=False),
            "Application": "Techos falsos y plafones de gasolineras, áreas de carga y descarga cubiertas y parkings techados."
        },

        # =========================================================================
        # 2. REFLECTORES Y PROYECTORES LED PARA EXTERIORES
        # =========================================================================
        {
            "Code": "P27758",
            "Name": "Proyector LED Sylveo PRO RD 1000W 13° 5000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Sylveo PRO RD",
            "Description": "Proyector LED circular para grandes alturas y largas distancias con haz concentrado de 13°. Potencia de 1000W y 146.000 lúmenes a 146 lm/W en 5000K. Chasis de fundición de aluminio de alta resistencia con visera antideslumbrante, protección total IP66, impacto extremo IK10, supresor de sobretensión integrado SPD 10kV y driver atenuable 0-10V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "1000W",
                "Flujo_Luminoso": "146.000 lm",
                "Eficacia": "146 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "13° (Haz concentrado spot)",
                "Tension_Operacion": "120-277V AC (Opcional 480V)",
                "Supresor_Sobretension": "SPD 10kV integrado",
                "Atenuacion": "0-10V",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK10",
                "Factor_Potencia": "0.9",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "7 años"
            }, ensure_ascii=False),
            "Application": "Iluminación de estadios deportivos profesionales, torres de iluminación en minas a cielo abierto, puertos marítimos y plataformas petroleras."
        },
        {
            "Code": "P27759",
            "Name": "Proyector LED Sylveo PRO RD 1200W 13° 5000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Sylveo PRO RD",
            "Description": "Proyector LED circular de 1200W con óptica concentrada spot de 13° y salida de 177.000 lúmenes (148 lm/W) en 5000K. Protección IP66, IK10, supresor de picos 10kV, driver 0-10V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "1200W",
                "Flujo_Luminoso": "177.000 lm",
                "Eficacia": "148 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "13°",
                "Tension_Operacion": "120-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK10",
                "Supresor_Sobretension": "SPD 10kV",
                "Vida_Util": "100.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Mástiles de estadios olímpicos, canteras a cielo abierto y grúas pórtico portuarias."
        },
        {
            "Code": "P27760",
            "Name": "Proyector LED Sylveo PRO RD 1000W 30° 5000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Sylveo PRO RD",
            "Description": "Proyector LED de mástil de 1000W con haz medio de 30° que genera 150.000 lúmenes a 150 lm/W. Diseñado para montaje en torres y mástiles elevados. Chasis antivibración de aluminio inyectado, grado IP66, resistencia a impactos IK10, SPD 10kV y control 0-10V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "1000W",
                "Flujo_Luminoso": "150.000 lm",
                "Eficacia": "150 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "30° (Haz medio flood)",
                "Tension_Operacion": "120-277V AC",
                "Supresor_Sobretension": "SPD 10kV",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK10",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "7 años"
            }, ensure_ascii=False),
            "Application": "Patios de maniobras ferroviarias y portuarias, canchas de fútbol, canteras y terminales logísticos."
        },
        {
            "Code": "P27761",
            "Name": "Proyector LED Sylveo PRO RD 1200W 30° 5000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Sylveo PRO RD",
            "Description": "Proyector LED de máxima potencia en la gama Sylveo con 1200W de consumo y 182.000 lúmenes de rendimiento fotométrico (152 lm/W). Óptica de 30°, protección IP66, IK10 y SPD 10kV. Diseñado para sustituir luminarias de vapor de sodio y halogenuros metálicos de 2000W.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "1200W",
                "Flujo_Luminoso": "182.000 lm",
                "Eficacia": "152 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "30°",
                "Tension_Operacion": "120-277V AC",
                "Supresor_Sobretension": "SPD 10kV",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK10",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "7 años"
            }, ensure_ascii=False),
            "Application": "Grandes recintos deportivos, minería pesada, puertos de contenedores, presas y canteras."
        },
        {
            "Code": "P23581",
            "Name": "Proyector LED Sylveo PRO 200W-400W 5000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Sylveo PRO",
            "Description": "Proyector modular para exteriores con driver configurable que permite regular la potencia entre 200W y 400W (flujo luminoso de 24.000 lm a 48.000 lm a 120 lm/W). Ángulo de haz 30°, IP66, impacto IK08, soporte de montaje orientable en lira.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "200W ~ 400W",
                "Flujo_Luminoso": "24.000 lm ~ 48.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "30°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "7 años"
            }, ensure_ascii=False),
            "Application": "Campos de petróleo, puertos, aeropuertos, estacionamientos y fachadas monumentales."
        },
        {
            "Code": "P23582",
            "Name": "Proyector LED Sylveo PRO 300W-600W 5000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Sylveo PRO",
            "Description": "Proyector modular de gran alcance con driver configurable entre 300W y 600W (flujo de 36.000 lm a 72.000 lm a 120 lm/W). Óptica simétrica 30°, cuerpo hermético IP66, IK08, disipación de aluminio extruido anodizado.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "300W ~ 600W",
                "Flujo_Luminoso": "36.000 lm ~ 72.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "30°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "7 años"
            }, ensure_ascii=False),
            "Application": "Explotaciones mineras, complejos portuarios, terminales intermodales y campos de entrenamiento deportivo."
        },
        {
            "Code": "P23657",
            "Name": "Proyector LED Sylveo 200W Asimétrico 5000K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Sylveo",
            "Description": "Proyector LED asimétrico de 200W con 24.000 lúmenes (120 lm/W) en 5000K. Óptica asimétrica diseñada para proyectar la luz hacia adelante minimizando deslumbramiento hacia arriba. Grado IP66, impacto IK08, chasis de aluminio.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "200W",
                "Flujo_Luminoso": "24.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "5000K",
                "Distribucion_Optica": "Asimétrica",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "7 años"
            }, ensure_ascii=False),
            "Application": "Iluminación perimetral de bodegas, playas de estacionamiento, campos petroleros y fachadas."
        },
        {
            "Code": "P23679",
            "Name": "Reflector LED Jeta Pro 100W 120° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta Pro",
            "Description": "Luminaria tipo reflector para exteriores ultra delgada y liviana con driver integrado. 100W, 12.000 lúmenes (120 lm/W) en luz blanca fría 6500K. Ángulo amplio de 120°, grado IP66 contra chorros de agua y polvo, IK06, soporte metálico orientable y conector rápido.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "100W",
                "Flujo_Luminoso": "12.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "120°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK06",
                "Factor_Potencia": "0.95",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Perímetro exterior de bodegas, parqueaderos comerciales, fachadas de edificios y plazoletas."
        },
        {
            "Code": "P23680",
            "Name": "Reflector LED Jeta Pro 150W 120° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta Pro",
            "Description": "Reflector LED extra plano de alta eficiencia para exteriores. 150W, 18.000 lúmenes a 120 lm/W en 6500K. Cobertura de 120°, hermeticidad IP66, IK06, factor de potencia 0.95, tensión de operación universal 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "150W",
                "Flujo_Luminoso": "18.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "120°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK06",
                "Factor_Potencia": "0.95",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Patios de carga, parques logísticos, canchas deportivas barriales e iluminación de seguridad perimetral."
        },
        {
            "Code": "P23681",
            "Name": "Reflector LED Jeta Pro 200W 120° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta Pro",
            "Description": "Reflector LED industrial para exteriores de 200W con salida de 24.000 lúmenes a 120 lm/W en 6500K. Cuerpo robusto en aluminio extruido con tratamiento anticorrosivo, protección IP66, IK06, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "200W",
                "Flujo_Luminoso": "24.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "120°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK06",
                "Factor_Potencia": "0.95",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Áreas industriales abiertas, zonas de almacenamiento exterior, parqueaderos masivos y vallas publicitarias."
        },
        {
            "Code": "P29742",
            "Name": "Reflector LED Jeta Pro 300W 90° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta Pro",
            "Description": "Reflector LED de gran potencia 300W que emite 36.000 lúmenes a 120 lm/W en 6500K. Óptica semidispersa de 90° para mayor alcance. Grado IP66, IK06, chasis de aluminio reforzado, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "300W",
                "Flujo_Luminoso": "36.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK06",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Mástiles de altura en parkings industriales, canchas de fútbol 8 y 11, depósitos de maquinaria pesada."
        },
        {
            "Code": "P29743",
            "Name": "Reflector LED Jeta Pro 400W 90° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta Pro",
            "Description": "Reflector LED de alta potencia 400W con 48.000 lúmenes a 120 lm/W en 6500K. Chasis de aluminio extruido anticorrosión, ángulo de 90°, IP66, IK06, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "400W",
                "Flujo_Luminoso": "48.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK06",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Puertos, terminales intermodales, patios de maniobras y torres de iluminación exterior."
        },
        {
            "Code": "P29744",
            "Name": "Reflector LED Jeta Pro 500W 90° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta Pro",
            "Description": "Reflector LED para grandes superficies de 500W con 60.000 lúmenes de flujo neto (120 lm/W) en luz blanca 6500K. Ángulo de 90°, estanqueidad IP66, IK06, driver multivoltaje 100-277V de alta durabilidad.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "500W",
                "Flujo_Luminoso": "60.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "90°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK06",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Estadios deportivos, complejos logísticos, muelles y puertos marítimos, patios de ferrocarril y minas."
        },
        {
            "Code": "P29772",
            "Name": "Reflector LED Jeta High Power 100W 110° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta High Power",
            "Description": "Reflector LED plano de 100W y 10.000 lúmenes (100 lm/W) en 6500K. Ángulo 110°, IP65, IK06, válvula de respiración anticondensación, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "100W",
                "Flujo_Luminoso": "10.000 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "110°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK06",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Iluminación perimetral de fachadas, bodegas, parqueaderos y áreas comerciales."
        },
        {
            "Code": "P29774",
            "Name": "Reflector LED Jeta High Power 200W 110° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta High Power",
            "Description": "Reflector LED de 200W con 20.000 lúmenes (100 lm/W) en luz blanca 6500K. Grado IP65, válvula de alivio térmico, IK06, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "200W",
                "Flujo_Luminoso": "20.000 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK06"
            }, ensure_ascii=False),
            "Application": "Parques logísticos, patios de camiones y canchas múltiples."
        },
        {
            "Code": "P40130",
            "Name": "Reflector LED Jeta High Power 300W 110° 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta High Power",
            "Description": "Reflector LED exterior de 300W con 30.000 lúmenes en 6500K. Soporte de acero, protección IP65, disipación de calor trasera, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "300W",
                "Flujo_Luminoso": "30.000 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65"
            }, ensure_ascii=False),
            "Application": "Grandes almacenes abiertos, aparcamientos de vehículos pesados y áreas perimetrales extensas."
        },
        {
            "Code": "P29767",
            "Name": "Reflector LED Jeta 10W 110° 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta",
            "Description": "Reflector LED compacto de 10W con 1.000 lúmenes (100 lm/W) en 6500K. Grado IP65 contra agua y polvo, IK06, válvula de respiración anticondensación integrada, chasis de aluminio inyectado, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "10W",
                "Flujo_Luminoso": "1.000 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "110°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK06",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Entradas de vivienda, pasillos exteriores, jardines residenciales y señalética."
        },
        {
            "Code": "P29768",
            "Name": "Reflector LED Jeta 20W 110° 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta",
            "Description": "Reflector LED para exterior de 20W con 2.000 lúmenes (100 lm/W) en luz blanca 6500K. Grado IP65, IK06, válvula de alivio térmico/respiración, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "20W",
                "Flujo_Luminoso": "2.000 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "110°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK06",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Garajes residenciales, accesos peatonales, pequeños locales comerciales y jardineras."
        },
        {
            "Code": "P29769",
            "Name": "Reflector LED Jeta 30W 110° 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta",
            "Description": "Reflector LED de 30W con salida de 3.000 lúmenes a 100 lm/W en 6500K. Protección IP65, impacto IK06, diseño ultradelgado en aluminio con soporte en U inclinable, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "30W",
                "Flujo_Luminoso": "3.000 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "110°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK06",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Patios interiores, estacionamientos de condominios, carteles publicitarios y fachadas de tiendas."
        },
        {
            "Code": "P29770",
            "Name": "Reflector LED Jeta 50W 110° 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Reflectores y Proyectores LED Exteriores",
            "Series": "Jeta",
            "Description": "Reflector LED exterior de 50W y 5.000 lúmenes (100 lm/W) en luz fría 6500K. Chasis disipador de aluminio anodizado negro, índice de protección IP65, válvula respiradora anticondensación, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "50W",
                "Flujo_Luminoso": "5.000 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Angulo_Apertura": "110°",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK06",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Perímetros residenciales y comerciales, estacionamientos medianos, talleres y zonas de carga ligera."
        },

        # =========================================================================
        # 3. ALUMBRADO PÚBLICO LED (STREET LIGHT VIAL)
        # =========================================================================
        {
            "Code": "P29509",
            "Name": "Luminaria Alumbrado Público LED Syl-Street 36W-60W Sylvania",
            "BusinessLine": "Iluminación Pública y Vial",
            "Family": "Alumbrado Público LED",
            "Series": "Syl-Street",
            "Description": "Luminaria vial LED de alta eficiencia para postes urbanos y secundarios. Potencia configurable de 36W a 60W con flujo de 5.400 a 9.000 lúmenes (>150 lm/W) en luz neutra 4000K. Chasis de aluminio inyectado de alta disipación, compartimento óptico y eléctrico independiente, vidrio templado de protección, grado IP66 e impacto IK09. Base para fotocelda NEMA 7 pines ANSI C136.41 para telegestión IoT SylSmart City, supresor de transitorios SPD 10kV y driver atenuable 0-10V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "36W ~ 60W",
                "Flujo_Luminoso": "5.400 lm ~ 9.000 lm",
                "Eficacia": ">150 lm/W",
                "Temperatura_Color": "4000K",
                "Tension_Operacion": "100-277V AC 50/60Hz",
                "Base_Fotocelda": "NEMA 7 Pines (compatible con telegestión IoT)",
                "Supresor_Sobretension": "SPD 10kV integrado",
                "Atenuacion": "0-10V Dimerizable",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Diametro_Poste": "42-60 mm",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "10 años"
            }, ensure_ascii=False),
            "Application": "Vías secundarias, urbanizaciones, calles residenciales, ciclorrutas, parques y zonas peatonales."
        },
        {
            "Code": "P29459",
            "Name": "Luminaria Alumbrado Público LED Syl-Street 61W-80W Sylvania",
            "BusinessLine": "Iluminación Pública y Vial",
            "Family": "Alumbrado Público LED",
            "Series": "Syl-Street",
            "Description": "Luminaria vial LED para calles colectoras y avenidas urbanas. Potencia ajustable de 61W a 80W entregando 9.350 a 12.290 lúmenes (>150 lm/W) en 4000K. Grado IP66, IK09, NEMA 7 pines para fotocelda / nodo de telegestión, SPD 10kV, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "61W ~ 80W",
                "Flujo_Luminoso": "9.350 lm ~ 12.290 lm",
                "Eficacia": ">150 lm/W",
                "Temperatura_Color": "4000K",
                "Tension_Operacion": "100-277V AC",
                "Base_Fotocelda": "NEMA 7 Pines",
                "Supresor_Sobretension": "SPD 10kV",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Diametro_Poste": "42-60 mm",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "10 años"
            }, ensure_ascii=False),
            "Application": "Calles colectoras urbanas, calzadas principales de ciudadelas, avenidas comerciales y plazoletas."
        },
        {
            "Code": "P29510",
            "Name": "Luminaria Alumbrado Público LED Syl-Street 70W-100W Sylvania",
            "BusinessLine": "Iluminación Pública y Vial",
            "Family": "Alumbrado Público LED",
            "Series": "Syl-Street",
            "Description": "Luminaria para alumbrado público de vías primarias. Rango de potencia de 70W a 100W con rendimiento lumínico de 10.680 a 15.400 lúmenes (>152 lm/W) en 4000K. Chasis de aluminio inyectado, cierre hermético sin herramientas, base NEMA 7 pines, SPD 10kV, IP66, IK09.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "70W ~ 100W",
                "Flujo_Luminoso": "10.680 lm ~ 15.400 lm",
                "Eficacia": ">152 lm/W",
                "Temperatura_Color": "4000K",
                "Tension_Operacion": "100-277V AC",
                "Base_Fotocelda": "NEMA 7 Pines",
                "Supresor_Sobretension": "SPD 10kV",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "10 años"
            }, ensure_ascii=False),
            "Application": "Avenidas principales, vías colectoras pesadas, accesos a ciudades e intercambiadores de tráfico."
        },
        {
            "Code": "P29511",
            "Name": "Luminaria Alumbrado Público LED Syl-Street 90W-120W Sylvania",
            "BusinessLine": "Iluminación Pública y Vial",
            "Family": "Alumbrado Público LED",
            "Series": "Syl-Street",
            "Description": "Luminaria vial LED de alta potencia para avenidas troncales y vías de tráfico rápido. Potencia ajustable de 90W a 120W que genera 13.590 a 18.000 lúmenes (>151 lm/W) en 4000K. Óptica tipo II / tipo III para calzadas multicanal, base NEMA 7 pines, SPD 10kV, IP66, IK09.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "90W ~ 120W",
                "Flujo_Luminoso": "13.590 lm ~ 18.000 lm",
                "Eficacia": ">151 lm/W",
                "Temperatura_Color": "4000K",
                "Tension_Operacion": "100-277V AC",
                "Base_Fotocelda": "NEMA 7 Pines",
                "Supresor_Sobretension": "SPD 10kV",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "10 años"
            }, ensure_ascii=False),
            "Application": "Avenidas principales de 4 o más carriles, pasos a desnivel, vías arteriales urbanas y distribuidores de tráfico."
        },
        {
            "Code": "P29512",
            "Name": "Luminaria Alumbrado Público LED Syl-Street 110W-150W Sylvania",
            "BusinessLine": "Iluminación Pública y Vial",
            "Family": "Alumbrado Público LED",
            "Series": "Syl-Street",
            "Description": "Luminaria vial para autopistas y carreteras interurbanas. Configurable entre 110W y 150W con salida de 16.880 a 23.150 lúmenes (>153 lm/W) en 4000K. Cuerpo estanco IP66, IK09, NEMA 7 pines, SPD 10kV.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "110W ~ 150W",
                "Flujo_Luminoso": "16.880 lm ~ 23.150 lm",
                "Eficacia": ">153 lm/W",
                "Temperatura_Color": "4000K",
                "Tension_Operacion": "100-277V AC",
                "Base_Fotocelda": "NEMA 7 Pines",
                "Supresor_Sobretension": "SPD 10kV",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "10 años"
            }, ensure_ascii=False),
            "Application": "Autopistas, carreteras estatales, viaductos, puentes largos y vías de acceso a puertos y aeropuertos."
        },
        {
            "Code": "P29513",
            "Name": "Luminaria Alumbrado Público LED Syl-Street 130W-180W Sylvania",
            "BusinessLine": "Iluminación Pública y Vial",
            "Family": "Alumbrado Público LED",
            "Series": "Syl-Street",
            "Description": "Luminaria vial LED de 130W a 180W entregando 20.000 a 27.380 lúmenes (>153 lm/W) en 4000K. Protección IP66, IK09, base NEMA 7 pines, SPD 10kV, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "130W ~ 180W",
                "Flujo_Luminoso": "20.000 lm ~ 27.380 lm",
                "Eficacia": ">153 lm/W",
                "Temperatura_Color": "4000K",
                "Tension_Operacion": "100-277V AC",
                "Base_Fotocelda": "NEMA 7 Pines",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "10 años"
            }, ensure_ascii=False),
            "Application": "Vías rápidas, autopistas y accesos metropolitanos."
        },
        {
            "Code": "P29514",
            "Name": "Luminaria Alumbrado Público LED Syl-Street 150W-200W Sylvania",
            "BusinessLine": "Iluminación Pública y Vial",
            "Family": "Alumbrado Público LED",
            "Series": "Syl-Street",
            "Description": "Luminaria vial LED de máxima capacidad lumínica en la serie Syl-Street. Rango ajustable de 150W a 200W con rendimiento extraordinario de 23.210 a 30.790 lúmenes (>154 lm/W) en 4000K. Chasis reforzado de aluminio, montaje a poste 42-60 mm con regulación angular de inclinación (-10° a +20°), base NEMA 7 pines, SPD 10kV, IP66, IK09.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "150W ~ 200W",
                "Flujo_Luminoso": "23.210 lm ~ 30.790 lm",
                "Eficacia": ">154 lm/W",
                "Temperatura_Color": "4000K",
                "Tension_Operacion": "100-277V AC",
                "Base_Fotocelda": "NEMA 7 Pines",
                "Supresor_Sobretension": "SPD 10kV",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Ajuste_Inclinacion": "-10° a +20°",
                "Vida_Util": "100.000 horas L70",
                "Garantia": "10 años"
            }, ensure_ascii=False),
            "Application": "Carreteras de alta velocidad, intersecciones viales complejas, calzadas principales de puertos y estaciones de peaje."
        },

        # =========================================================================
        # 4. LUMINARIAS HERMÉTICAS ESTANCAS (ANTI POLVO Y VAPOR IP65/IP66)
        # =========================================================================
        {
            "Code": "P29942",
            "Name": "Luminaria LED Triproof Lite Anti Polvo 20W 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Triproof Lite",
            "Description": "Luminaria hermética lineal compacta estanca al polvo y agua con tecnología LED integrada. Potencia de 20W, 2.400 lúmenes (120 lm/W) en luz fría 6500K. Longitud de 670 mm, chasis y difusor resistente al impacto en policarbonato (PC), estanqueidad IP66 e impacto IK08. Tensión 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "20W",
                "Flujo_Luminoso": "2.400 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "670 mm (60 cm)",
                "Material": "Chasis y difusor en Policarbonato (PC)",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": "0.9",
                "Vida_Util": "50.000 horas L70",
                "Montaje": "Sobreponer o descolgar con grapas inoxidables"
            }, ensure_ascii=False),
            "Application": "Pasillos húmedos, parqueaderos cubiertos, lavanderías, cámaras frigoríficas ligeras y bodegas con presencia de polvo."
        },
        {
            "Code": "P27118",
            "Name": "Luminaria LED Triproof Lite Anti Polvo 50W 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Triproof Lite",
            "Description": "Luminaria hermética lineal de 1570 mm (1.5 m) para ambientes industriales hostiles. Potencia de 50W que genera 6.000 lúmenes a 120 lm/W en 6500K. Construcción 100% policarbonato de alta resistencia, índice IP66, impacto mecánico IK08, clips de montaje, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "50W",
                "Flujo_Luminoso": "6.000 lm",
                "Eficacia": "120 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "1570 mm",
                "Material": "Policarbonato (PC) anti-impacto",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": "0.9",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Naves de producción industrial, estacionamientos subterráneos, talleres automotrices y plantas embotelladoras."
        },
        {
            "Code": "P29818",
            "Name": "Luminaria LED Hermética High Flux Anti Polvo 80W 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Hermética High Flux",
            "Description": "Luminaria hermética lineal de alto flujo lumínico con 80W de potencia y 11.200 lúmenes de salida (140 lm/W) en 6500K. Longitud de 1500 mm. Cuerpo y difusor opalizado en policarbonato con máxima resistencia al impacto IK10 y hermeticidad IP65. Multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "80W",
                "Flujo_Luminoso": "11.200 lm",
                "Eficacia": "140 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "1500 mm",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK10 (Máxima resistencia mecánica)",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": ">0.9",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Plantas de procesamiento industrial continuo, bodegas de gran superficie, túneles de lavado e industrias cárnicas."
        },
        {
            "Code": "P25609",
            "Name": "Luminaria LED Hermética Módulo Anti Polvo 36W 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Hermética Módulo",
            "Description": "Luminaria estanca con módulo LED integrado de 36W y 4.500 lúmenes (125 lm/W) en luz fría 6500K. Longitud 1176 mm. Base de ABS termoplástico inyectado y difusor de policarbonato opalizado antideslumbrante, grado de protección IP65, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "36W",
                "Flujo_Luminoso": "4.500 lm",
                "Eficacia": "125 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "1176 mm (1.2 m)",
                "Chasis": "ABS de alta rigidez",
                "Difusor": "Policarbonato opalizado",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK05",
                "Tension_Operacion": "100-277V AC",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Parqueaderos techados, talleres mecánicos, cocinas industriales y áreas de empaque."
        },
        {
            "Code": "P23661",
            "Name": "Luminaria LED Hermética Módulo Anti Polvo 50W 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Hermética Módulo",
            "Description": "Luminaria estanca LED de 50W y 6.300 lúmenes (126 lm/W) en luz fría 6500K. Longitud 1476 mm. Chasis en ABS y difusor de policarbonato, grado IP65 contra polvo y humedad constante, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "50W",
                "Flujo_Luminoso": "6.300 lm",
                "Eficacia": "126 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "1476 mm (1.5 m)",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK05",
                "Tension_Operacion": "100-277V AC",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Bodegas de frío no congelado, salas de máquinas, garajes subterráneos y plantas de alimentos."
        },
        {
            "Code": "P36667",
            "Name": "Luminaria Hermética 2x18W con Tubos LED Vidrio 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Hermética 2xT8",
            "Description": "Luminaria hermética armada completa que incluye chasis estanco IP65 de 1270 mm y 2 tubos LED T8 de vidrio de 18W (potencia total 36W, 3.200 lúmenes en 6500K). Chasis de polímero ABS y difusor transparente de alta transmitancia, clips de cierre hermético, 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Configuracion": "2x18W Tubos LED T8 Vidrio incluidos",
                "Potencia_Total": "36W",
                "Flujo_Luminoso": "3.200 lm",
                "Temperatura_Color": "6500K",
                "Longitud": "1270 mm (1.2 m)",
                "Socket": "G13 para tubos T8",
                "Grado_Proteccion": "IP65",
                "Resistencia_Impacto": "IK05",
                "Tension_Operacion": "100-240V AC",
                "Montaje": "Sobreponer o descolgar en techo"
            }, ensure_ascii=False),
            "Application": "Parkings de centros comerciales, almacenes comerciales, pasillos técnicos y cuartos de bombas."
        },
        {
            "Code": "P37558",
            "Name": "Luminaria Hermética 2x9W con Tubos LED Vidrio 6500K Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Hermética 2xT8",
            "Description": "Luminaria hermética de 60 cm que incluye chasis estanco IP65 y 2 tubos LED T8 de vidrio de 9W (18W totales, 1.600 lm en 6500K). Grado IP65, 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Configuracion": "2x9W Tubos LED T8 Vidrio incluidos",
                "Potencia_Total": "18W",
                "Flujo_Luminoso": "1.600 lm",
                "Temperatura_Color": "6500K",
                "Longitud": "670 mm",
                "Grado_Proteccion": "IP65"
            }, ensure_ascii=False),
            "Application": "Pasillos estrechos, cuartos eléctricos húmedos y escaleras de servicio."
        },
        {
            "Code": "P37152",
            "Name": "Chasis Hermético 2x18W T8 IP65 sin Tubos Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Chasis Hermético",
            "Description": "Luminaria estanca vacía (chasis) para 2 tubos LED T8 de 120 cm (18W). Cuerpo en polímero ABS con empaque de estanqueidad perimetral de poliuretano inyectado, difusor de policarbonato transparente, portatubos G13 pre-cableados para conexión directa Single End, grado IP65.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "2 Tubos LED T8 de 120 cm (G13)",
                "Longitud": "1270 mm",
                "Grado_Proteccion": "IP65",
                "Material_Cuerpo": "ABS",
                "Difusor": "Poliestireno / Policarbonato de alta transparencia",
                "Cableado": "Conexión directa Single End (fase y neutro a un extremo)"
            }, ensure_ascii=False),
            "Application": "Instalación de luminarias estancas personalizables con tubos LED T8 de cualquier temperatura de color o potencia."
        },
        {
            "Code": "P37253",
            "Name": "Chasis Hermético 2x9W T8 IP65 sin Tubos Sylvania",
            "BusinessLine": "Iluminación Industrial y Profesional",
            "Family": "Luminarias Herméticas Estancas",
            "Series": "Chasis Hermético",
            "Description": "Chasis estanco IP65 vacío para 2 tubos LED T8 de 60 cm (9W). Longitud 670 mm, portatubos G13 cableados Single End, clips de cierre hermético.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "2 Tubos LED T8 de 60 cm (G13)",
                "Longitud": "670 mm",
                "Grado_Proteccion": "IP65",
                "Material_Cuerpo": "ABS"
            }, ensure_ascii=False),
            "Application": "Montaje de tubos LED T8 de 60 cm en áreas de polvo o intemperie."
        },

        # =========================================================================
        # 5. ÁREAS CLASIFICADAS Y ANTIEXPLOSIÓN (SYLSECURE / HAZLOC / EX)
        # =========================================================================
        {
            "Code": "P23736",
            "Name": "Luminaria LED Lineal SylSecure Antiexplosión 20W-40W Sylvania",
            "BusinessLine": "Iluminación para Áreas Clasificadas",
            "Family": "Áreas Clasificadas y Antiexplosión",
            "Series": "SylSecure Lineal",
            "Description": "Luminaria LED lineal a prueba de explosión certificada para atmósferas con riesgo de gases inflamables, vapores y polvos combustibles bajo norma UL844. Clasificación: Clase I Div 2 Grupos A, B, C, D (T3C); Clase II Div 1 Grupos E, F, G (T4A); Clase III. Potencia ajustable de 20W a 40W (hasta 5.480 lm a 137 lm/W) en 5000K. Chasis robusto de aleación de aluminio libre de cobre, difusor de vidrio templado termo-resistente, IP66 e impacto IK08. Multivoltaje 120-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "20W ~ 40W",
                "Flujo_Luminoso": "2.740 lm ~ 5.480 lm",
                "Eficacia": "137 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "110°",
                "Tension_Operacion": "120-277V AC",
                "Certificaciones": "UL844 (Hazardous Locations), RETILAP, NOM, CE, RoHS",
                "Clasificacion_NEC500": "Clase I Div 2 (A, B, C, D); Clase II Div 1 (E, F, G); Clase III",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Material": "Aluminio sin cobre resistente a corrosión y vidrio templado",
                "Vida_Util": "100.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Refinerías de petróleo, plantas petroquímicas, estaciones de bombeo de combustibles, depósitos de granos y plantas químicas."
        },
        {
            "Code": "P23737",
            "Name": "Luminaria LED Lineal SylSecure Antiexplosión 30W-80W Sylvania",
            "BusinessLine": "Iluminación para Áreas Clasificadas",
            "Family": "Áreas Clasificadas y Antiexplosión",
            "Series": "SylSecure Lineal",
            "Description": "Luminaria LED lineal antiexplosión de 120 cm (1200 mm) para áreas clasificadas severas. Potencia configurable de 30W a 80W generando hasta 10.960 lúmenes a 137 lm/W en 5000K. Apta para Clase I Div 2 y Clase II Div 1 según UL844. Cuerpo de fundición de aluminio marine-grade, vidrio de alta transmitancia, IP66, IK08, multivoltaje 120-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "30W ~ 80W",
                "Flujo_Luminoso": "4.110 lm ~ 10.960 lm",
                "Eficacia": "137 lm/W",
                "Temperatura_Color": "5000K",
                "Longitud": "1200 mm",
                "Certificacion": "UL844 (HazLoc) Clase I Div 2 Grupos A, B, C, D; Clase II Div 1",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Tension_Operacion": "120-277V AC",
                "Vida_Util": "100.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Plantas de procesamiento de gas natural, cabinas de pintura industrial, fábricas de solventes y destilerías."
        },
        {
            "Code": "P23951",
            "Name": "Campana LED High Bay SylSecure Antiexplosión 30W-80W Sylvania",
            "BusinessLine": "Iluminación para Áreas Clasificadas",
            "Family": "Áreas Clasificadas y Antiexplosión",
            "Series": "SylSecure High Bay",
            "Description": "Campana industrial LED de gran altura a prueba de explosión para entornos con presencia de atmósferas inflamables. Potencia configurable de 30W a 80W (hasta 12.000 lm con eficacia excepcional de 150 lm/W) en 5000K. Certificación UL844 Clase I Div 2 y Clase II Div 1. Chasis esférico aleteado de aluminio fundido pesado, vidrio templado a prueba de choque térmico, IP66, IK08, SPD 10kV.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "30W ~ 80W",
                "Flujo_Luminoso": "4.500 lm ~ 12.000 lm",
                "Eficacia": "150 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "100°",
                "Certificacion": "UL844 Clase I Div 2; Clase II Div 1; Clase III",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Supresor_Sobretension": "SPD 10kV",
                "Tension_Operacion": "100-277V AC",
                "Atenuacion": "0-10V Dimerizable",
                "Vida_Util": "100.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Grandes alturas en salas de calderas, molinos harineros, plantas de alcohol, plataformas de perforación y plantas eléctricas."
        },
        {
            "Code": "P23741",
            "Name": "Campana LED High Bay SylSecure Antiexplosión 60W-150W Sylvania",
            "BusinessLine": "Iluminación para Áreas Clasificadas",
            "Family": "Áreas Clasificadas y Antiexplosión",
            "Series": "SylSecure High Bay",
            "Description": "Campana industrial antiexplosión de alta potencia para techos elevados en zonas peligrosas. Ajustable de 60W a 150W generando hasta 22.500 lúmenes (150 lm/W) en 5000K. Certificación UL844 para Clase I Div 2 Grupos A/B/C/D y Clase II Div 1/2 Grupos E/F/G. Construcción heavy-duty hermética IP66 e impacto IK08 con SPD 10kV.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "60W ~ 150W",
                "Flujo_Luminoso": "9.000 lm ~ 22.500 lm",
                "Eficacia": "150 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "100°",
                "Certificacion": "UL844 Clase I Div 2; Clase II Div 1; Clase III",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Supresor_Sobretension": "SPD 10kV",
                "Tension_Operacion": "100-277V AC",
                "Vida_Util": "100.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Hangares petroquímicos, terminales marítimos de hidrocarburos, industrias farmacéuticas de reactivos inflamables y silos."
        },
        {
            "Code": "P23743",
            "Name": "Proyector LED Flood Light SylSecure Antiexplosión 40W-100W Sylvania",
            "BusinessLine": "Iluminación para Áreas Clasificadas",
            "Family": "Áreas Clasificadas y Antiexplosión",
            "Series": "SylSecure Flood Light",
            "Description": "Proyector LED reflector de seguridad para áreas clasificadas. Potencia ajustable de 40W a 100W entregando hasta 13.000 lúmenes a 130 lm/W en 5000K. Certificado UL844 Clase I Div 2 y Clase II Div 2. Soporte en U reforzado de acero inoxidable para montaje en pared o suelo, protección IP66, IK09 contra impactos violentos y SPD 10kV.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "40W ~ 100W",
                "Flujo_Luminoso": "5.200 lm ~ 13.000 lm",
                "Eficacia": "130 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "110°",
                "Certificacion": "UL844 Clase I Div 2; Clase II Div 2; Clase III",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Supresor_Sobretension": "SPD 10kV",
                "Tension_Operacion": "120-277V AC",
                "Vida_Util": "100.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Áreas de carga de tanqueros de gasolina, muelles petroleros, patios de reactores químicos y plantas de biogás."
        },
        {
            "Code": "P23744",
            "Name": "Proyector LED Flood Light SylSecure Antiexplosión 60W-150W Sylvania",
            "BusinessLine": "Iluminación para Áreas Clasificadas",
            "Family": "Áreas Clasificadas y Antiexplosión",
            "Series": "SylSecure Flood Light",
            "Description": "Proyector LED antiexplosión para exteriores industriales de 60W a 150W (hasta 19.500 lm a 130 lm/W) en 5000K. Apto Clase I Div 2, Clase II Div 2, chasis de aluminio marino, vidrio templado resistente a choques térmicos, IP66, IK09, 120-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Configurable": "60W ~ 150W",
                "Flujo_Luminoso": "7.800 lm ~ 19.500 lm",
                "Eficacia": "130 lm/W",
                "Temperatura_Color": "5000K",
                "Angulo_Apertura": "110°",
                "Certificacion": "UL844 Clase I Div 2; Clase II Div 2; Clase III",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK09",
                "Tension_Operacion": "120-277V AC"
            }, ensure_ascii=False),
            "Application": "Perímetros de seguridad en depósitos de hidrocarburos, refinerías y poliductos."
        },
        {
            "Code": "P26638",
            "Name": "Luminaria LED Tubular Explosion Proof Light BC5401 20W Sylvania",
            "BusinessLine": "Iluminación para Áreas Clasificadas",
            "Family": "Áreas Clasificadas y Antiexplosión",
            "Series": "Explosion Proof BC5401",
            "Description": "Luminaria tubular blindada antiexplosión Ex de 20W (2x10W) y 1.800 lúmenes (90 lm/W) en 5000K. Certificación internacional Ex para Zona 1 y Zona 2 (Clase I Div 2 Grupos A, B, C, D; Clase II Div 2 Grupos E, F, G; Clase III). Cuerpo de aluminio con recubrimiento de pintura anticorrosiva WF2, grado IP66 e impacto IK08. Permite conexión en cadena (loop in - loop out).",
            "TechnicalSpecs": json.dumps({
                "Potencia": "20W (2x10W)",
                "Flujo_Luminoso": "1.800 lm",
                "Eficacia": "90 lm/W",
                "Temperatura_Color": "5000K",
                "Longitud": "780 mm",
                "Certificacion_Ex": "Ex d e IIC T6 Gb / Ex tb IIIC T80°C Db, Clase I Div 2",
                "Proteccion_Corrosion": "WF2",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Tension_Operacion": "100-277V AC",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Plataformas petroleras offshore, salas de baterías de subestaciones, túneles de minas subterráneas y plantas de tratamiento de aguas residuales."
        },
        {
            "Code": "P26757",
            "Name": "Luminaria LED Tubular Explosion Proof Light BC5401 40W Sylvania",
            "BusinessLine": "Iluminación para Áreas Clasificadas",
            "Family": "Áreas Clasificadas y Antiexplosión",
            "Series": "Explosion Proof BC5401",
            "Description": "Luminaria tubular blindada antideflagrante Ex de 40W (2x20W) y 4.000 lúmenes en 5000K. Longitud 1390 mm. Certificación Ex Clase I Div 2, grado IP66, IK08, acabado anticorrosivo de grado naval WF2, terminales en ambos extremos para instalación lineal en serie, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "40W (2x20W)",
                "Flujo_Luminoso": "4.000 lm",
                "Eficacia": "90 lm/W",
                "Temperatura_Color": "5000K",
                "Longitud": "1390 mm",
                "Certificacion_Ex": "Clase I Div 2 Grupos A, B, C, D; Clase II Div 2",
                "Proteccion_Corrosion": "WF2",
                "Grado_Proteccion": "IP66",
                "Resistencia_Impacto": "IK08",
                "Tension_Operacion": "100-277V AC",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Túneles de cables en petroquímica, estaciones de compresión de gas y bodegas de almacenamiento de químicos volátiles."
        },

        # =========================================================================
        # 6. ILUMINACIÓN DE EMERGENCIA AUTÓNOMA Y SEÑALIZACIÓN
        # =========================================================================
        {
            "Code": "P23342",
            "Name": "Lámpara de Emergencia LED Doble Foco R1 2x1.6W 90min Sylvania",
            "BusinessLine": "Iluminación de Emergencia",
            "Family": "Iluminación de Emergencia",
            "Series": "Emergencia R1",
            "Description": "Luminaria de emergencia autónoma de sobreponer con dos cabezales rectangulares dirigibles de alta luminosidad. Potencia 2x1.6W (160 lm) en 6500K. Batería recargable integrada con 90 minutos de respaldo ante cortes de energía eléctrica. Botón de prueba (Push to Test) e indicador LED de estado de carga, carcasa termoplástica ignífuga blanca, conexión directa 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Focos": "2 x 1.6W LED orientables",
                "Flujo_Luminoso": "160 lm (2x80 lm)",
                "Temperatura_Color": "6500K",
                "Autonomia": "90 minutos garantizados",
                "Bateria": "Batería recargable de libre mantenimiento",
                "Tiempo_Recarga": "24 horas",
                "Tension_Operacion": "100-277V AC 50/60Hz",
                "Funciones": "Botón de prueba e indicador LED bicolor de carga",
                "Grado_Proteccion": "IP20",
                "Montaje": "Sobreponer en pared",
                "Normativa": "RETILAP / NFPA 101"
            }, ensure_ascii=False),
            "Application": "Rutas de evacuación en plantas de producción, oficinas, bodegas, colegios, universidades y centros comerciales."
        },
        {
            "Code": "P23344",
            "Name": "Lámpara de Emergencia LED Doble Foco R1 Mini 2x1.5W 90min Sylvania",
            "BusinessLine": "Iluminación de Emergencia",
            "Family": "Iluminación de Emergencia",
            "Series": "Emergencia R1",
            "Description": "Lámpara de emergencia compacta doble cabezal de 2x1.5W con 220 lúmenes totales (2x110 lm) en luz blanca 6500K. Autonomía de 90 minutos con batería recargable, diseño estético de bajo perfil para oficinas y comercios, botón de test, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "2 x 1.5W LED",
                "Flujo_Luminoso": "220 lm (2x110 lm)",
                "Temperatura_Color": "6500K",
                "Autonomia": "90 minutos",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP20",
                "Dimensiones": "349 x 89 x 95 mm"
            }, ensure_ascii=False),
            "Application": "Pasillos de oficinas, salas de reuniones, locales comerciales y áreas residenciales comunes."
        },
        {
            "Code": "P33718",
            "Name": "Señalizador de Emergencia LED Aviso Salida EXIT 1.8W 300min Sylvania",
            "BusinessLine": "Iluminación de Emergencia",
            "Family": "Iluminación de Emergencia",
            "Series": "Aviso Salida EXIT",
            "Description": "Letrero de señalización luminosa de emergencia tipo banderola/pared con panel de acrílico transparente y texto grabado en verde 'SALIDA'. 1.8W, modo permanente y no permanente. Batería recargable de Níquel Cadmio de alto rendimiento que proporciona una autonomía extraordinaria de 300 minutos (5 horas). Botón de test, indicador de carga, tensión 110-130V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "1.8W",
                "Leyenda": "SALIDA (Letras verdes en acrílico cristal)",
                "Autonomia": "300 minutos (5 horas continuas)",
                "Tipo_Bateria": "Níquel Cadmio (Ni-Cd) sellada",
                "Tiempo_Recarga": "24 horas",
                "Tension_Operacion": "110-130V AC",
                "Modo_Trabajo": "Permanente / Emergencia",
                "Grado_Proteccion": "IP20",
                "Factor_Potencia": "0.9",
                "Dimensiones": "290 x 45 x 180 mm"
            }, ensure_ascii=False),
            "Application": "Señalización obligatoria de puertas de salida, escaleras de escape y pasillos de emergencia en industrias y comercios."
        },

        # =========================================================================
        # 7. PANELES LED Y LUMINARIAS COMERCIALES
        # =========================================================================
        {
            "Code": "P29579",
            "Name": "Panel LED Backlit SQ 60x60 cm 36W 4000lm 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Panel Backlit SQ",
            "Description": "Panel LED cuadrado retroiluminado (Backlit) de 60x60 cm (595x595x26 mm) de alta eficacia (111 lm/W) con 4.000 lúmenes en 6500K. Luz uniforme sin zonas oscuras gracias a la tecnología Backlit. Chasis metálico blanco con difusor opalizado antideslumbrante (UGR bajo), factor de potencia 0.9, THD <20%, vida útil 50.000 horas, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "36W",
                "Flujo_Luminoso": "4.000 lm",
                "Eficacia": "111 lm/W",
                "Temperatura_Color": "6500K",
                "Formato": "60x60 cm (595 x 595 x 26 mm)",
                "Tecnologia": "Backlit (Retroiluminado directo)",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": "0.9",
                "THD": "<20%",
                "IRC": "80",
                "Grado_Proteccion": "IP20",
                "Vida_Util": "50.000 horas L70",
                "Montaje": "Incrustar en cielo raso modular (Armstrong) o descolgar"
            }, ensure_ascii=False),
            "Application": "Oficinas corporativas, bancos, aulas universitarias, hospitales, consultorios médicos y salas de conferencia."
        },
        {
            "Code": "P29562",
            "Name": "Panel LED Backlit SQ 60x60 cm 40W 3600lm 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Panel Backlit SQ",
            "Description": "Panel LED de cielo raso 60x60 cm (595x595 mm) de 40W y 3.600 lúmenes en luz blanca fría 6500K. Marco de aluminio blanco, difusor de poliestireno opalizado, ángulo amplio de 120°, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "40W",
                "Flujo_Luminoso": "3.600 lm",
                "Eficacia": "90 lm/W",
                "Temperatura_Color": "6500K",
                "Dimensiones": "595 x 595 x 26 mm",
                "Tension_Operacion": "100-277V AC",
                "Vida_Util": "35.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Cielo raso tipo baldosas en oficinas comerciales, tiendas retail, centros de estudio y farmacias."
        },
        {
            "Code": "P27916",
            "Name": "Panel LED Incrustar Slim RC 30x120 cm 40W 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Panel Slim RC",
            "Description": "Panel LED rectangular extraplano de 30x120 cm (1195x295x8.5 mm). Potencia de 40W con flujo de 3.200 lúmenes en luz blanca fría 6500K. Perfil perimetral delgado de aluminio anodizado blanco, distribución simétrica amplia de 120°, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "40W",
                "Flujo_Luminoso": "3.200 lm",
                "Eficacia": "80 lm/W",
                "Temperatura_Color": "6500K",
                "Dimensiones": "1195 x 295 x 8.5 mm (30x120 cm)",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": "0.9",
                "Grado_Proteccion": "IP20",
                "Vida_Util": "35.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Pasillos corporativos, bibliotecas, áreas de atención al cliente y salas de exhibición."
        },
        {
            "Code": "P26846",
            "Name": "Panel LED Incrustar Slim RC 60x120 cm 60W 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Panel Slim RC",
            "Description": "Panel LED rectangular de gran formato de 60x120 cm (1195x595x8.5 mm) de 60W y 4.800 lúmenes en 6500K. Marco blanco extraplano, encendido instantáneo sin parpadeo, driver externo multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "60W",
                "Flujo_Luminoso": "4.800 lm",
                "Eficacia": "80 lm/W",
                "Temperatura_Color": "6500K",
                "Dimensiones": "1195 x 595 x 8.5 mm (60x120 cm)",
                "Tension_Operacion": "100-277V AC",
                "Grado_Proteccion": "IP20",
                "Vida_Util": "35.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Espacios comerciales amplios, salas de juntas ejecutivas, vestíbulos y clínicas."
        },
        {
            "Code": "P29888",
            "Name": "Panel LED Redondo Downlight Sylvania Pro 6W 6500K",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Panel RD Pro",
            "Description": "Luminaria tipo downlight circular ultra delgada para embutir en gypsum o cielo raso. 6W de consumo, 390 lúmenes en luz blanca 6500K. Diámetro exterior Ø120 mm, resortes de sujeción integrados, marco de aluminio inyectado blanco, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "6W",
                "Flujo_Luminoso": "390 lm",
                "Eficacia": "65 lm/W",
                "Temperatura_Color": "6500K",
                "Diametro": "Ø 120 x 20 mm",
                "Corte_Techo": "Ø 105 mm",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": ">0.9",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Iluminación de baños, pasillos residenciales, balcones cubiertos y nichos decorativos."
        },
        {
            "Code": "P29891",
            "Name": "Panel LED Redondo Downlight Sylvania Pro 12W 6500K",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Panel RD Pro",
            "Description": "Downlight panel circular de embutir de 12W con 840 lúmenes (70 lm/W) en 6500K. Diámetro Ø170 mm. Difusor opalizado que suaviza la luz, factor de potencia >0.9, 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "12W",
                "Flujo_Luminoso": "840 lm",
                "Eficacia": "70 lm/W",
                "Temperatura_Color": "6500K",
                "Diametro": "Ø 170 x 25 mm",
                "Corte_Techo": "Ø 150 mm",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": ">0.9",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Habitaciones, recepciones, cafeterías, comercios y áreas de descanso."
        },
        {
            "Code": "P29894",
            "Name": "Panel LED Redondo Downlight Sylvania Pro 18W 6500K",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Panel RD Pro",
            "Description": "Panel circular downlight de incrustar de 18W con 1.350 lúmenes (75 lm/W) en 6500K. Diámetro Ø225 mm. Chasis blanco, resortes reforzados, driver multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "18W",
                "Flujo_Luminoso": "1.350 lm",
                "Eficacia": "75 lm/W",
                "Temperatura_Color": "6500K",
                "Diametro": "Ø 225 x 25 mm",
                "Corte_Techo": "Ø 205 mm",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": ">0.9",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Cocinas, salas de estar, locales comerciales, comedores y áreas de trabajo."
        },
        {
            "Code": "P29897",
            "Name": "Panel LED Redondo Downlight Sylvania Pro 24W 6500K",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Panel RD Pro",
            "Description": "Downlight panel circular de gran iluminación de 24W y 1.920 lúmenes (80 lm/W) en luz blanca 6500K. Diámetro Ø295 mm. Iluminación general potente y difusa en 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "24W",
                "Flujo_Luminoso": "1.920 lm",
                "Eficacia": "80 lm/W",
                "Temperatura_Color": "6500K",
                "Diametro": "Ø 295 x 25 mm",
                "Corte_Techo": "Ø 275 mm",
                "Tension_Operacion": "100-277V AC",
                "Factor_Potencia": ">0.9",
                "Vida_Util": "30.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Salas de reuniones, vestíbulos de hoteles, tiendas departamentales y áreas comunes."
        },
        {
            "Code": "P29802",
            "Name": "Regleta Lineal LED Batten E-lite 8W 6500K Interconectable Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Batten E-lite",
            "Description": "Luminaria lineal ultra delgada de sobreponer con sistema de interconexión directa en línea continua (hasta 6 unidades en serie sin cables adicionales). 8W, 800 lúmenes (100 lm/W) en 6500K, longitud 585 mm, cuerpo y difusor de policarbonato, 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "8W",
                "Flujo_Luminoso": "800 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "585 x 22 x 31 mm",
                "Conectividad": "Cadenas continuas hasta 6 luminarias en serie",
                "Tension_Operacion": "100-240V AC",
                "Grado_Proteccion": "IP20"
            }, ensure_ascii=False),
            "Application": "Debajo de muebles de cocina, vitrinas comerciales, gargantas de yeso decorativas y estanterías."
        },
        {
            "Code": "P26774",
            "Name": "Luminaria Lineal LED Eco Sobreponer 32W 120cm 6500K Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Paneles LED y Downlights Comerciales",
            "Series": "Lineal Eco",
            "Description": "Luminaria lineal de sobreponer con regleta LED integrada de 32W y 2.600 lúmenes en luz blanca fría 6500K. Longitud 1200 mm (1.2 m), chasis delgado con difusor curvo opalizado de 180°, tensión 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "32W",
                "Flujo_Luminoso": "2.600 lm",
                "Eficacia": "80 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "1200 x 23 x 75 mm",
                "Angulo_Apertura": "180°",
                "Tension_Operacion": "100-240V AC",
                "Vida_Util": "25.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Oficinas, bodegas pequeñas, cuartos de estudio, comercios y talleres de bricolaje."
        },

        # =========================================================================
        # 8. TUBOS LED T8 Y T5
        # =========================================================================
        {
            "Code": "P24994",
            "Name": "Tubo LED T8 Vidrio 9W 60cm 6500K Single End Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Tubos LED T8 y T5",
            "Series": "Tubo LED T8 Vidrio",
            "Description": "Tubo LED T8 de vidrio opalizado de 9W (longitud 600 mm, casquillo G13) con 800 lúmenes (89 lm/W) en luz blanca fría 6500K. Ángulo de apertura de 270°, conexión directa Single End (línea y neutro en un solo extremo, bypass directo de balastro), no requiere arrancador, tensión 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "9W",
                "Flujo_Luminoso": "800 lm",
                "Eficacia": "89 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "600 mm (60 cm)",
                "Casquillo": "G13 (T8 tradicional)",
                "Material": "Vidrio opalizado difusor",
                "Angulo_Apertura": "270°",
                "Conexion": "Single End (Fase y Neutro en un solo extremo)",
                "Tension_Operacion": "100-240V AC",
                "Factor_Potencia": ">0.5",
                "Vida_Util": "20.000 horas"
            }, ensure_ascii=False),
            "Application": "Reemplazo directo de tubos fluorescentes de 18W en luminarias comerciales de oficinas y pasillos."
        },
        {
            "Code": "P27900",
            "Name": "Tubo LED T8 Vidrio 18W 120cm 6500K Single End Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Tubos LED T8 y T5",
            "Series": "Tubo LED T8 Vidrio",
            "Description": "Tubo LED T8 de vidrio de 18W (longitud 1212 mm, base G13) que genera 1.600 lúmenes a 89 lm/W en luz blanca fría 6500K. Ángulo de haz amplio de 270°, cuerpo de vidrio térmicamente estable que no se pandea, conexión Single End directa a 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "18W",
                "Flujo_Luminoso": "1.600 lm",
                "Eficacia": "89 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "1212 mm (1.20 metros)",
                "Casquillo": "G13",
                "Material": "Vidrio opalizado",
                "Angulo_Apertura": "270°",
                "Conexion": "Single End",
                "Tension_Operacion": "100-240V AC",
                "Vida_Util": "20.000 horas"
            }, ensure_ascii=False),
            "Application": "Sustitución de tubos fluorescentes de 36W en oficinas, almacenes, instituciones educativas y comercios."
        },
        {
            "Code": "P27899",
            "Name": "Tubo LED T8 Vidrio 18W 120cm 4000K Single End Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Tubos LED T8 y T5",
            "Series": "Tubo LED T8 Vidrio",
            "Description": "Tubo LED T8 de vidrio de 18W en luz blanca neutra 4000K para espacios de trabajo continuo con descanso visual. 1.600 lúmenes, casquillo G13, conexión directa Single End, 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "18W",
                "Flujo_Luminoso": "1.600 lm",
                "Temperatura_Color": "4000K (Luz Neutra)",
                "Longitud": "1212 mm",
                "Casquillo": "G13",
                "Conexion": "Single End",
                "Tension_Operacion": "100-240V AC"
            }, ensure_ascii=False),
            "Application": "Aulas escolares, clínicas, oficinas corporativas y laboratorios."
        },
        {
            "Code": "P25161",
            "Name": "Tubo LED T8 Policarbonato PC 18W 120cm 4000K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Tubos LED T8 y T5",
            "Series": "Tubo LED T8 PC",
            "Description": "Tubo LED T8 fabricado en policarbonato irrompible (inastillable) apto para industrias de alimentos y farmacéuticas. 18W, 1.800 lúmenes (100 lm/W) en luz neutra 4000K. Ángulo de 180°, multivoltaje universal 100-277V, vida útil 40.000 horas.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "18W",
                "Flujo_Luminoso": "1.800 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "4000K",
                "Longitud": "1212 mm",
                "Material": "Policarbonato (Inastillable / Anti-rotura)",
                "Casquillo": "G13",
                "Tension_Operacion": "100-277V AC",
                "Vida_Util": "40.000 horas"
            }, ensure_ascii=False),
            "Application": "Plantas procesadoras de alimentos, cámaras de frío, farmacéuticas y talleres industriales donde no se permite vidrio."
        },
        {
            "Code": "P25125",
            "Name": "Tubo LED T8 Policarbonato PC 18W 120cm 6500K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Tubos LED T8 y T5",
            "Series": "Tubo LED T8 PC",
            "Description": "Tubo LED T8 inastillable en policarbonato de 18W con 1.800 lúmenes (100 lm/W) en 6500K. Alta resistencia al impacto mecánico, conexión Single End directa, multivoltaje 100-277V.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "18W",
                "Flujo_Luminoso": "1.800 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "1212 mm",
                "Material": "Policarbonato PC resistente",
                "Tension_Operacion": "100-277V AC",
                "Vida_Util": "40.000 horas"
            }, ensure_ascii=False),
            "Application": "Industrias de bebidas, plantas cárnicas, cocinas industriales y áreas con alta vibración."
        },
        {
            "Code": "P27608",
            "Name": "Tubo LED T5 Vidrio+PET 25W 116cm 6500K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Tubos LED T8 y T5",
            "Series": "Tubo LED T5",
            "Description": "Tubo LED formato fino T5 de alta eficacia (136 lm/W) que entrega 3.400 lúmenes con sólo 25W de consumo en luz blanca fría 6500K. Revestimiento Vidrio+PET inastillable, conexión Single End, multivoltaje 120-277V, vida útil prolongada de 50.000 horas.",
            "TechnicalSpecs": json.dumps({
                "Potencia": "25W",
                "Flujo_Luminoso": "3.400 lm",
                "Eficacia": "136 lm/W",
                "Temperatura_Color": "6500K",
                "Longitud": "1163 mm",
                "Formato": "T5 (Ø21 mm)",
                "Material": "Vidrio con película protectora PET",
                "Tension_Operacion": "120-277V AC",
                "Vida_Util": "50.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Luminarias estilizadas para oficinas modernas, pasillos corporativos, vitrinas y arquitectura interior."
        },

        # =========================================================================
        # 9. LÁMPARAS LED ALTA POTENCIA (T-BULB) Y CINTAS LED
        # =========================================================================
        {
            "Code": "P24890",
            "Name": "Bombillo LED ToLEDo High Wattage T-Bulb 20W E27 6500K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Lámparas LED Alta Potencia y Cintas",
            "Series": "ToLEDo High Wattage",
            "Description": "Lámpara LED tipo bulbo T-Bulb de 20W con 1.700 lúmenes en 6500K. Base E27, disipador de aluminio y termoplástico, ángulo 180°-220°, 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "20W",
                "Flujo_Luminoso": "1.700 lm",
                "Temperatura_Color": "6500K",
                "Base": "E27",
                "Tension_Operacion": "100-240V AC",
                "Vida_Util": "20.000 horas"
            }, ensure_ascii=False),
            "Application": "Salas de trabajo, garajes y comercios."
        },
        {
            "Code": "P24892",
            "Name": "Bombillo LED ToLEDo High Wattage T-Bulb 30W E27 6500K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Lámparas LED Alta Potencia y Cintas",
            "Series": "ToLEDo High Wattage",
            "Description": "Lámpara tipo bulbo T-Bulb de alta potencia y flujo luminoso. 30W con 2.550 lúmenes (85 lm/W) en luz blanca 6500K. Casquillo estándar E27, disipador de aluminio revestido en termoplástico, ángulo de haz amplio de 180° a 220°, tensión 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "30W",
                "Flujo_Luminoso": "2.550 lm",
                "Temperatura_Color": "6500K",
                "Base": "E27",
                "Angulo_Apertura": "180° - 220°",
                "Tension_Operacion": "100-240V AC",
                "Vida_Util": "20.000 horas",
                "Dimensiones": "Ø100 x 169 mm"
            }, ensure_ascii=False),
            "Application": "Bodegas de mediana altura, talleres, garajes y áreas de doble altura."
        },
        {
            "Code": "P24893",
            "Name": "Bombillo LED ToLEDo High Wattage T-Bulb 40W E27 6500K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Lámparas LED Alta Potencia y Cintas",
            "Series": "ToLEDo High Wattage",
            "Description": "Lámpara LED T-Bulb de 40W y 3.300 lúmenes en 6500K. Base estándar E27, disipador de calor de aletas externas para máxima disipación térmica, 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "40W",
                "Flujo_Luminoso": "3.300 lm",
                "Temperatura_Color": "6500K",
                "Base": "E27",
                "Tension_Operacion": "100-240V AC",
                "Vida_Util": "20.000 horas",
                "Dimensiones": "Ø118 x 191 mm"
            }, ensure_ascii=False),
            "Application": "Almacenes comerciales, bodegas, galpones y patios cubiertos."
        },
        {
            "Code": "P26571",
            "Name": "Bombillo LED ToLEDo High Wattage T-Bulb 50W E27 6500K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Lámparas LED Alta Potencia y Cintas",
            "Series": "ToLEDo High Wattage",
            "Description": "Lámpara LED de alta potencia 50W y 4.000 lúmenes (80 lm/W) en 6500K. Base E27 para campanas decorativas o portalámparas abiertos. Ahorro de energía del 80% frente a lámparas de mercurio y ahorro de energía compacto, 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "50W",
                "Flujo_Luminoso": "4.000 lm",
                "Temperatura_Color": "6500K",
                "Base": "E27",
                "Tension_Operacion": "100-240V AC",
                "Vida_Util": "20.000 horas",
                "Dimensiones": "Ø140 x 242 mm"
            }, ensure_ascii=False),
            "Application": "Campanas abiertas en mercados, galpones agrícolas, bodegas y locales de techos altos."
        },
        {
            "Code": "P26105",
            "Name": "Bombillo LED ToLEDo High Wattage T-Bulb 80W E27 6500K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Lámparas LED Alta Potencia y Cintas",
            "Series": "ToLEDo High Wattage",
            "Description": "Lámpara LED de alta intensidad lumínica de 80W entregando 6.400 lúmenes en 6500K. Casquillo E27, disipador de aluminio acanalado, 100-240V.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "80W",
                "Flujo_Luminoso": "6.400 lm",
                "Temperatura_Color": "6500K",
                "Base": "E27",
                "Tension_Operacion": "100-240V AC",
                "Vida_Util": "20.000 horas"
            }, ensure_ascii=False),
            "Application": "Iluminación de bodegas medianas, hangares comerciales y galpones avícolas."
        },
        {
            "Code": "P26942",
            "Name": "Bombillo LED ToLEDo High Wattage T-Bulb 100W E40 6500K Sylvania",
            "BusinessLine": "Lámparas y Tubos LED",
            "Family": "Lámparas LED Alta Potencia y Cintas",
            "Series": "ToLEDo High Wattage",
            "Description": "Lámpara LED industrial de gran formato con base Goliat E40. 100W de potencia entregando 10.000 lúmenes (100 lm/W) en luz blanca 6500K. Excelente disipación térmica, sustituye lámparas de vapor de sodio y halogenuros metálicos de 250W y 400W sin necesidad de balastro.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "100W",
                "Flujo_Luminoso": "10.000 lm",
                "Eficacia": "100 lm/W",
                "Temperatura_Color": "6500K",
                "Base": "E40 (Goliat)",
                "Tension_Operacion": "100-240V AC",
                "Vida_Util": "20.000 horas",
                "Dimensiones": "Ø140 x 258 mm"
            }, ensure_ascii=False),
            "Application": "Campanas industriales E40, luminarias viales retrofitted y grandes naves fabriles."
        },
        {
            "Code": "P29947",
            "Name": "Cinta LED 110V 9W/m 6500K Rollo 6 metros Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Lámparas LED Alta Potencia y Cintas",
            "Series": "Cinta LED 110V",
            "Description": "Cinta LED con chip integrado directamente a 110V (no requiere transformador externo a 12V). Potencia de 9W por metro, 900 lm/m (100 lm/W), densidad de 120 LED/m en luz fría 6500K. Carrete de 6 metros, protección IP20 para interiores.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "9W por metro (54W total rollo)",
                "Flujo_Luminoso": "900 lm/m",
                "Eficacia": "100 lm/W",
                "Densidad_LED": "120 LED/metro",
                "Temperatura_Color": "6500K",
                "Longitud_Rollo": "6 metros",
                "Tension_Operacion": "110V AC directo",
                "Grado_Proteccion": "IP20",
                "Vida_Util": "20.000 horas"
            }, ensure_ascii=False),
            "Application": "Iluminación arquitectónica oculta en cielos falsos, cenefas, muebles y vitrinas comerciales."
        },
        {
            "Code": "P29826",
            "Name": "Manguera LED Exterior 110V 11W/m 6500K Carrete 100m Sylvania",
            "BusinessLine": "Iluminación Comercial y Residencial",
            "Family": "Lámparas LED Alta Potencia y Cintas",
            "Series": "Manguera LED",
            "Description": "Manguera luminosa LED de exterior con recubrimiento de silicona flexible impermeable IP65. Potencia de 11W por metro con 950 lm/m en 6500K. Tensión directa a 110V, ángulo de apertura 120°, carrete continuo de 100 metros con conectores y accesorios de alimentación.",
            "TechnicalSpecs": json.dumps({
                "Consumo": "11W por metro",
                "Flujo_Luminoso": "950 lm/m",
                "Temperatura_Color": "6500K",
                "Longitud": "Carrete de 100 metros",
                "Tension_Operacion": "110V AC",
                "Grado_Proteccion": "IP65 (Impermeable exterior)",
                "Vida_Util": "15.000 horas"
            }, ensure_ascii=False),
            "Application": "Contornos arquitectónicos exteriores, fachadas de hoteles y centros comerciales, jardines y senderos."
        },

        # =========================================================================
        # 10. SISTEMAS SOLARES FOTOVOLTAICOS Y ALUMBRADO SOLAR (SYLVANIA SOLAR+)
        # =========================================================================
        {
            "Code": "P27143",
            "Name": "Inversor Solar On Grid Sylvania MUST 3kW Monofásico/Bifásico",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Inversor On-Grid MUST",
            "Description": "Inversor solar fotovoltaico interconectado a la red eléctrica (On-Grid) de 3kW de potencia nominal. Salida AC 220/230/240Vac 13A monofásico o bifásico a 50/60Hz. Entrada fotovoltaica máxima de 3.450Wp con 1 seguidor MPPT de rango extendido (100V a 550VDC). Hermeticidad IP65 para montaje exterior, monitoreo inalámbrico por WiFi/App móvil, refrigeración natural silenciosa sin ventilador y protecciones completas con anti-isla.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Nominal_AC": "3.000W (3kW / 3kVA)",
                "Tension_Salida_AC": "220V / 230V / 240V AC 50/60Hz",
                "Corriente_Salida_AC": "13A",
                "Potencia_Maxima_FV": "3.450Wp",
                "Rango_Tension_MPPT": "100V ~ 550V DC",
                "Numero_MPPT": "1",
                "Corriente_Maxima_Entrada_DC": "11A",
                "Comunicacion": "WiFi / USB / App móvil y portal web",
                "Grado_Proteccion": "IP65",
                "Garantia": "5 años"
            }, ensure_ascii=False),
            "Application": "Sistemas solares fotovoltaicos conectados a red para residencias, negocios comerciales y microempresas."
        },
        {
            "Code": "P27678",
            "Name": "Inversor Solar On Grid Sylvania MUST 6kW con 2 MPPT",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Inversor On-Grid MUST",
            "Description": "Inversor solar On-Grid de 6kW de potencia nominal para inyección a red eléctrica. Salida AC 220/230/240Vac a 26.1A. Admite hasta 7.000Wp de paneles solares con 2 seguidores MPPT independientes (100V-550VDC) permitiendo arreglos en techos con dos orientaciones distintas. Carcasa IP65, WiFi integrado.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Nominal_AC": "6.000W (6kW / 6kVA)",
                "Tension_Salida_AC": "220V / 230V / 240V AC",
                "Corriente_Salida_AC": "26.1A",
                "Potencia_Maxima_FV": "7.000Wp",
                "Rango_Tension_MPPT": "100V ~ 550V DC",
                "Numero_MPPT": "2 independientes",
                "Comunicacion": "WiFi / USB",
                "Grado_Proteccion": "IP65",
                "Garantia": "5 años"
            }, ensure_ascii=False),
            "Application": "Empresas comerciales, gasolineras, talleres y residencias con alto consumo de energía eléctrica."
        },
        {
            "Code": "P27141",
            "Name": "Inversor Solar Off Grid Sylvania MUST 2kW 24V MPPT 80A",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Inversor Off-Grid MUST",
            "Description": "Inversor cargador solar fotovoltaico autónomo (Off-Grid) de 2kW (onda sinusoidal pura) para operación aislada con baterías. Salida AC 110/115/120Vac 50/60Hz. Integra controlador solar MPPT de 80A con entrada FV máxima de 2500W (rango MPPT 30V-130VDC a 24V batería) y cargador AC inteligente de 30A. Pantalla LCD con selección de prioridades.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Nominal": "2.000W (2kW)",
                "Forma_Onda": "Onda Sinusoidal Pura",
                "Tension_Salida_AC": "110V / 115V / 120V AC 50/60Hz",
                "Tension_Banco_Baterias": "24V DC",
                "Controlador_Solar": "MPPT 80A integrado",
                "Potencia_Maxima_FV": "2.500Wp",
                "Rango_MPPT_FV": "30V ~ 130V DC",
                "Cargador_AC": "30A @24V",
                "Display": "Pantalla LCD multifunción",
                "Garantia": "5 años"
            }, ensure_ascii=False),
            "Application": "Fincas rurales, casas de campo aisladas, estaciones de telecomunicaciones y sistemas de respaldo de energía autónomos."
        },
        {
            "Code": "P27142",
            "Name": "Inversor Solar Off Grid Sylvania MUST 3kW 24V MPPT 80A",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Inversor Off-Grid MUST",
            "Description": "Inversor cargador solar aislado (Off-Grid) de 3kW a 120Vac con controlador MPPT de 80A integrado. Potencia FV máxima de 2500Wp, cargador de baterías desde red/generador de 40A @24V. Onda pura apta para motores y compresores de refrigeración hasta 1.5 HP.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Nominal": "3.000W (3kW)",
                "Onda": "Sinusoidal Pura",
                "Tension_Salida": "110/115/120Vac",
                "Banco_Baterias": "24V DC",
                "Controlador_MPPT": "80A",
                "Cargador_Baterias": "40A @24V",
                "Capacidad_Motor": "Permite arranque de motor hasta 1.5 HP",
                "Garantia": "5 años"
            }, ensure_ascii=False),
            "Application": "Electrificación rural, bombeo solar, campamentos petroleros y mineros remotos y obradores."
        },
        {
            "Code": "P25450",
            "Name": "Batería Solar Litio SylTech LiFePO4 35Ah 12.8V 448Wh Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Baterías Litio SylTech",
            "Description": "Batería solar de litio ferrofosfato (LiFePO4) de ciclo profundo para almacenamiento de energía solar. 35Ah a 12.8V (448Wh). Cuenta con sistema BMS inteligente integrado contra sobrecargas, sobredescargas y cortocircuitos. Vida útil superior a 3.000 ciclos al 75% DoD, sellado hermético IP65 para intemperie, peso ultra ligero de sólo 4.4 kg.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "35Ah",
                "Tension_Nominal": "12.8V DC",
                "Energia_Almacenada": "448Wh",
                "Tecnologia": "Litio Fosfato de Hierro (LiFePO4)",
                "Ciclos_Vida": ">3.000 ciclos al 75% DoD",
                "Sistema_BMS": "BMS inteligente integrado",
                "Grado_Proteccion": "IP65 intemperie",
                "Peso": "4.4 kg",
                "Garantia": "5 años"
            }, ensure_ascii=False),
            "Application": "Kits solares de alumbrado público, señalización vial solar y sistemas solares autónomos residenciales."
        },
        {
            "Code": "P25451",
            "Name": "Batería Solar Litio SylTech LiFePO4 50Ah 12.8V 640Wh Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Baterías Litio SylTech",
            "Description": "Batería de litio para energía solar de 50Ah a 12.8V (640Wh). BMS de control interno, resistente al calor y descarga profunda, índice IP65, más de 3.000 ciclos de vida, peso reducido de 5.8 kg.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "50Ah",
                "Tension_Nominal": "12.8V DC",
                "Energia_Almacenada": "640Wh",
                "Quimica": "LiFePO4",
                "Ciclos_Vida": ">3.000 ciclos",
                "Grado_Proteccion": "IP65",
                "Peso": "5.8 kg",
                "Garantia": "5 años"
            }, ensure_ascii=False),
            "Application": "Alumbrado público solar de alta exigencia, estaciones de monitoreo y cámaras de seguridad solar."
        },
        {
            "Code": "P29946",
            "Name": "Batería Solar Litio SylTech LiFePO4 75Ah 12.8V 960Wh Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Baterías Litio SylTech",
            "Description": "Batería solar de litio de 75Ah a 12.8V (960Wh). Máxima densidad energética para alumbrado público y almacenamiento solar autónomo, BMS integrado, IP65, peso 8.4 kg.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "75Ah",
                "Tension_Nominal": "12.8V DC",
                "Energia_Almacenada": "960Wh",
                "Quimica": "LiFePO4",
                "Grado_Proteccion": "IP65",
                "Peso": "8.4 kg",
                "Garantia": "5 años"
            }, ensure_ascii=False),
            "Application": "Proyectos solares aislados de alta autonomía y sistemas de iluminación solar intensiva."
        },
        {
            "Code": "P37577",
            "Name": "Batería Solar Gel SylTech 100Ah 12V 1200Wh Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Baterías Gel SylTech",
            "Description": "Batería solar sellada VRLA en gel de ciclo profundo. 100Ah a 12V (1.200Wh), 100% libre de mantenimiento, peso 28 kg.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "100Ah",
                "Tension_Nominal": "12V DC",
                "Energia_Almacenada": "1.200Wh",
                "Tecnologia": "Plomo-ácido Gel (VRLA GEL)",
                "Peso": "28 kg",
                "Garantia": "2 años"
            }, ensure_ascii=False),
            "Application": "Sistemas solares rurales, cercas eléctricas solares e inversores Off-Grid medianos."
        },
        {
            "Code": "P37578",
            "Name": "Batería Solar Gel SylTech 150Ah 12V 1800Wh Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Baterías Gel SylTech",
            "Description": "Batería solar sellada regulada por válvula (VRLA) con electrolito gelificado de ciclo profundo. 150Ah a 12V (1.800Wh). Libre de mantenimiento, soporta descargas profundas y temperaturas extremas (-15°C a +50°C), vida útil de diseño de 5 años, peso 41.2 kg.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "150Ah",
                "Tension_Nominal": "12V DC",
                "Energia_Almacenada": "1.800Wh",
                "Tecnologia": "Plomo-ácido con electrolito en Gel (VRLA GEL)",
                "Vida_Util": "5 años / 1.500 ciclos al 30% DoD",
                "Mantenimiento": "100% libre de mantenimiento sellada",
                "Peso": "41.2 kg",
                "Garantia": "2 años"
            }, ensure_ascii=False),
            "Application": "Bancos de baterías para inversores Off-Grid, sistemas solares aislados, iluminación perimetral solar y repetidores."
        },
        {
            "Code": "P25446",
            "Name": "Batería Solar Gel SylTech 200Ah 12V 2400Wh Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Baterías Gel SylTech",
            "Description": "Batería solar en gel de 200Ah a 12V (2.400Wh) para bancos de energía de alta capacidad en sistemas aislados de la red. Peso 57 kg.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "200Ah",
                "Tension_Nominal": "12V DC",
                "Energia_Almacenada": "2.400Wh",
                "Tecnologia": "Gel VRLA",
                "Peso": "57 kg",
                "Garantia": "2 años"
            }, ensure_ascii=False),
            "Application": "Sistemas fotovoltaicos de gran autonomía y respaldo de energía para telecomunicaciones."
        },
        {
            "Code": "P23235",
            "Name": "Batería Solar Gel SylTech 250Ah 12V 3000Wh Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Baterías Gel SylTech",
            "Description": "Batería de ciclo profundo en gel de máxima capacidad con 250Ah a 12V (3.000Wh). Peso 65.6 kg.",
            "TechnicalSpecs": json.dumps({
                "Capacidad": "250Ah",
                "Tension_Nominal": "12V DC",
                "Energia_Almacenada": "3.000Wh",
                "Tecnologia": "Gel VRLA",
                "Peso": "65.6 kg",
                "Garantia": "2 años"
            }, ensure_ascii=False),
            "Application": "Grandes bancos de almacenamiento para viviendas aisladas y microredes solares."
        },
        {
            "Code": "P38139",
            "Name": "Kit Solar Alumbrado Público Syl-Street Litio 22W-35W Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Kit Solar Syl-Street",
            "Description": "Sistema autónomo integral de alumbrado público solar. Incluye luminaria LED Syl-Street de 22W~35W (hasta 5.300 lm a 151 lm/W en 4000K), panel solar monocristalino de 165W, batería de litio LiFePO4 de 50Ah con BMS, controlador solar MPPT y soporte metálico para poste. Entrega programada de fábrica de 12 horas al 100% de luminosidad con control remoto inalámbrico. Luminaria IP66 e impacto IK08.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Luminaria": "22W ~ 35W",
                "Flujo_Luminoso": "3.314 ~ 5.300 lm",
                "Eficacia": "151 lm/W",
                "Temperatura_Color": "4000K",
                "Panel_Solar": "165W Monocristalino",
                "Bateria": "Litio 1 x 50Ah 12.8V",
                "Programacion": "12 horas al 100% de luz garantizadas",
                "Control": "Control remoto inalámbrico incluido",
                "Grado_Proteccion": "IP66 luminaria, IK08",
                "Montaje": "Brazo para poste 50-60 mm",
                "Garantia": "Luminaria 10 años, Panel 12 años, Batería 5 años"
            }, ensure_ascii=False),
            "Application": "Alumbrado público en caminos rurales, carreteras sin red eléctrica, parques, senderos peatonales y urbanizaciones privadas."
        },
        {
            "Code": "P38140",
            "Name": "Kit Solar Alumbrado Público Syl-Street Litio 36W-60W Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Kit Solar Syl-Street",
            "Description": "Kit de alumbrado público solar de mediana potencia. Luminaria LED Syl-Street de 36W~60W (5.400 a 9.000 lm a 149 lm/W), 2 paneles solares de 165W (330W total), 2 baterías de litio de 35Ah (70Ah total), controlador y estructura de montaje a poste.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Luminaria": "36W ~ 60W",
                "Flujo_Luminoso": "5.400 ~ 9.000 lm",
                "Eficacia": "149 lm/W",
                "Panel_Solar": "2 x 165W (330W)",
                "Bateria": "2 x 35Ah Litio",
                "Autonomia": "12 horas continuas con reserva para días nublados",
                "Proteccion": "IP66, IK08",
                "Garantias": "Luminaria 10 años, Panel 12 años, Batería litio 5 años"
            }, ensure_ascii=False),
            "Application": "Calles principales en comunidades rurales, vías perimetrales de industrias y estacionamientos remotos."
        },
        {
            "Code": "P38141",
            "Name": "Kit Solar Alumbrado Público Syl-Street Litio 66W-100W Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Kit Solar Syl-Street",
            "Description": "Kit de alumbrado público solar de gran potencia. Luminaria LED Syl-Street de 66W~100W que emite hasta 16.100 lúmenes con altísima eficacia de 161 lm/W en 4000K. Cuenta con 2 paneles solares de 165W (330W) y 2 baterías de litio de 50Ah (100Ah total a 12.8V). Resistencia total a la intemperie IP66 e impacto IK08.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Luminaria": "66W ~ 100W",
                "Flujo_Luminoso": "10.226 ~ 16.100 lm",
                "Eficacia": "161 lm/W",
                "Panel_Solar": "2 x 165W",
                "Bateria": "2 x 50Ah Litio (100Ah total)",
                "Proteccion": "IP66, IK08",
                "Vida_Util": "100.000 horas L70"
            }, ensure_ascii=False),
            "Application": "Avenidas perimetrales, carreteras sin tendido eléctrico, plataformas petroleras y plantas solares."
        },
        {
            "Code": "P27322",
            "Name": "Kit Solar Proyector Sylflood Gel 80W 5000K Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Kit Solar Sylflood",
            "Description": "Kit solar de iluminación exterior con reflector Sylflood de 80W y 11.440 lúmenes (143 lm/W) en 5000K. Incluye 2 paneles solares de 165W (330W), 2 baterías de gel de 150Ah de ciclo profundo, gabinete metálico estanco para baterías y controlador programable. Ángulo de proyección 45°, luminaria IP66 e impacto IK08.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Proyector": "80W",
                "Flujo_Luminoso": "11.440 lm",
                "Eficacia": "143 lm/W",
                "Temperatura_Color": "5000K",
                "Panel_Solar": "2 x 165W (330W)",
                "Baterias": "2 x 150Ah Gel",
                "Gabinete": "Gabinete de protección para baterías y controlador incluido",
                "Proteccion": "IP66 proyector, IK08"
            }, ensure_ascii=False),
            "Application": "Canchas deportivas comunitarias aisladas, vías privadas campestres, plazoletas y subestaciones eléctricas."
        },
        {
            "Code": "P27323",
            "Name": "Kit Solar Proyector Sylflood Gel 120W 5000K Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Kit Solar Sylflood",
            "Description": "Kit solar con reflector Sylflood de 120W y 17.760 lúmenes (148 lm/W) en 5000K. Cuenta con 2 paneles de 165W y 2 baterías de gel de 150Ah en gabinete.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Proyector": "120W",
                "Flujo_Luminoso": "17.760 lm",
                "Eficacia": "148 lm/W",
                "Panel_Solar": "2 x 165W",
                "Baterias": "2 x 150Ah Gel",
                "Proteccion": "IP66, IK08"
            }, ensure_ascii=False),
            "Application": "Complejos deportivos rurales, playas de maniobra y patios de almacenamiento sin red eléctrica."
        },
        {
            "Code": "P38346",
            "Name": "Kit Generación Solar Fotovoltaica ON-GRID 3kVA 1.8kWp Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Kit Generación Fotovoltaica",
            "Description": "Kit completo de generación solar conectado a red eléctrica. Incluye inversor solar On-Grid de 3kVA, 4 paneles solares monocristalinos de 450W (potencia total 1.8kWp), estructura de aluminio para montaje en tejado, 10 metros de cable solar con conectores MC4 y tablero eléctrico preensamblado con protecciones AC/DC. Generación estimada de hasta 216 kWh/mes.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Inversor": "3kVA (3.000W)",
                "Arreglo_Solar": "4 paneles x 450W monocristalinos (1.800Wp)",
                "Generacion_Estimada": "Hasta 216 kWh/mes",
                "Tipo_Conexion": "On-Grid (Conectado a la red de distribución eléctrica)",
                "Componentes_Incluidos": "Inversor On-Grid, paneles solares, estructura tejado, cable solar 10m, tablero con protecciones",
                "Garantias": "Inversor 5 años, Paneles 12 años producto / 25 años generación"
            }, ensure_ascii=False),
            "Application": "Autogeneración solar para residencias, oficinas y locales comerciales para reducir la factura de electricidad."
        },
        {
            "Code": "P38347",
            "Name": "Kit Generación Solar Fotovoltaica ON-GRID 3kVA 2.7kWp Sylvania",
            "BusinessLine": "Sistemas Solares y Energías Renovables",
            "Family": "Sistemas Solares Fotovoltaicos y Alumbrado Solar",
            "Series": "Kit Generación Fotovoltaica",
            "Description": "Kit solar On-Grid de 3kVA con 6 paneles monocristalinos de 450W (2.7kWp) que produce hasta 324 kWh/mes. Incluye inversor solar On-Grid con monitoreo WiFi, estructura de aluminio coplanar y tablero preensamblado con descargadores de sobretensión e interruptores termomagnéticos.",
            "TechnicalSpecs": json.dumps({
                "Potencia_Inversor": "3kVA",
                "Arreglo_Solar": "6 paneles x 450W (2.700Wp)",
                "Generacion_Estimada": "Hasta 324 kWh/mes",
                "Monitoreo": "WiFi integrado con App móvil",
                "Garantias": "Inversor 5 años, Paneles 12/25 años"
            }, ensure_ascii=False),
            "Application": "Negocios, talleres, oficinas y viviendas con alto consumo de energía eléctrica diurna."
        }
    ]

def populate_database(db_path):
    if not os.path.exists(db_path):
        print(f"Skipping non-existent DB: {db_path}")
        return

    print(f"\nPopulating Sylvania products in: {db_path}")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    products = get_sylvania_master_catalog()
    inserted = 0
    updated = 0

    for p in products:
        cur.execute("SELECT Id FROM ProductsCatalog WHERE Code = ?", (p["Code"],))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE ProductsCatalog
                SET Brand = 'Sylvania',
                    BusinessLine = ?,
                    Family = ?,
                    Series = ?,
                    Name = ?,
                    Description = ?,
                    TechnicalSpecs = ?,
                    Application = ?,
                    Status = 'Active'
                WHERE Code = ?
            """, (p["BusinessLine"], p["Family"], p["Series"], p["Name"], p["Description"], p["TechnicalSpecs"], p["Application"], p["Code"]))
            updated += 1
        else:
            cur.execute("""
                INSERT INTO ProductsCatalog 
                (Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application, Status, SearchCount, LastQueriedAt)
                VALUES ('Sylvania', ?, ?, ?, ?, ?, ?, ?, ?, 'Active', 0, NULL)
            """, (p["BusinessLine"], p["Family"], p["Series"], p["Code"], p["Name"], p["Description"], p["TechnicalSpecs"], p["Application"]))
            inserted += 1

    conn.commit()
    print(f"Result for {os.path.basename(db_path)}: {inserted} inserted, {updated} updated (Total Sylvania: {len(products)}).")

    # Rebuild FTS5
    try:
        cur.execute("INSERT INTO Products_FTS(Products_FTS) VALUES('rebuild');")
        conn.commit()
        print("  Successfully rebuilt Products_FTS index.")
    except Exception as e:
        print(f"  Notice Products_FTS: {e}")

    try:
        cur.execute("INSERT INTO ProductsCatalog_fts(ProductsCatalog_fts) VALUES('rebuild');")
        conn.commit()
        print("  Successfully rebuilt ProductsCatalog_fts index.")
    except Exception as e:
        print(f"  Notice ProductsCatalog_fts: {e}")

    # Brand counts
    cur.execute("SELECT Brand, COUNT(*) FROM ProductsCatalog GROUP BY Brand ORDER BY COUNT(*) DESC")
    brand_counts = cur.fetchall()
    print("Catalog product counts by brand:")
    for b, c in brand_counts:
        print(f"  - {b}: {c}")

    cur.execute("SELECT COUNT(*) FROM ProductsCatalog")
    total = cur.fetchone()[0]
    print(f"Total catalog products: {total}")

    conn.close()

if __name__ == "__main__":
    for path in DB_PATHS:
        populate_database(path)
    print("\nSylvania catalog population complete across all databases!")
