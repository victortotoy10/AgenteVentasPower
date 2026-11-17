import sqlite3
import re

conn = sqlite3.connect('agente_ventas.db')
cur = conn.cursor()

test_queries = [
    'Weidmuller',
    'Weidmüller',
    'bornera WDU 2.5',
    '1020000000',
    'bornera tierra WPE',
    'bornera PUSH IN A2C 2.5',
    '1521850000',
    'fuente PROtop 24V 10A',
    '2466880000',
    'disyuntor electronico maxGUARD',
    'rele termseries 24VDC',
    '1122770000',
    'rele RIDERSERIES 230VAC',
    'protector sobretensiones VPU II 40kA',
    '2564330000',
    'VPU solar fotovoltaico 1000V',
    'aislador senal ACT20P 4-20mA',
    'pelacables stripax',
    '9005000000',
    'crimpadora PZ 6 Roto',
    'cortacables KT 8',
    'switch industrial IE-SW 5 puertos',
    '1240840000',
    'acoplador profinet u-remote',
    'conector pesado rockstar 16 polos',
    'analizador redes energy meter 700',
    'caja aluminio klippon K3',
    'marcador bornera DEK 5'
]

print("=== PRUEBAS DE BÚSQUEDA FTS5 WEIDMULLER ===\n")
for tq in test_queries:
    clean = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ]', ' ', tq)
    tokens = [t for t in clean.split() if len(t) >= 2]
    if not tokens:
        tokens = [clean.strip()]
    fts_expr = ' OR '.join([f'"{t}"*' if not t.isalnum() else f"{t}*" for t in tokens])
    
    cur.execute("""
        SELECT p.Code, p.Name, p.Brand, p.BusinessLine, p.Series
        FROM Products_FTS f
        JOIN ProductsCatalog p ON p.Id = f.rowid
        WHERE Products_FTS MATCH ?
        ORDER BY rank
        LIMIT 2;
    """, (fts_expr,))
    rows = cur.fetchall()
    print(f"Consulta: '{tq}' -> {len(rows)} resultado(s):")
    for r in rows:
        print(f"   -> [{r[2]}] Código: {r[0]} | {r[1]} ({r[3]} / {r[4]})")
    print()

cur.execute("SELECT Brand, COUNT(*), COUNT(DISTINCT BusinessLine), COUNT(DISTINCT Family), COUNT(DISTINCT Series) FROM ProductsCatalog GROUP BY Brand;")
print("=== RESUMEN POR MARCA EN LA BASE DE DATOS ===")
for r in cur.fetchall():
    print(f"Marca: {r[0]:<20} | Productos: {r[1]:<4} | Líneas: {r[2]:<2} | Familias: {r[3]:<2} | Series: {r[4]:<2}")

conn.close()
