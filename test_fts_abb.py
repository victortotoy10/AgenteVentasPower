import sqlite3

conn = sqlite3.connect('agente_ventas.db')
cur = conn.cursor()

test_queries = [
    'contactor abb 25A',
    'AF09',
    'guardamotor MS116',
    'arrancador suave abb',
    'PSTX',
    'variador ACS880',
    'breaker abb 160A',
    'Tmax XT',
    'pulsador metalico abb',
    'parada emergencia abb',
    'analizador redes abb',
    'SU201M',
    'disyuntor DC SU201DC',
    'breaker S800U 100A',
    'diferencial DS201',
    'portafusible E90 PV solar'
]

print("=== PRUEBAS DE BÚSQUEDA FTS5 (FULL-TEXT SEARCH) ===\n")
for tq in test_queries:
    tokens = tq.replace('-', ' ').split()
    fts_expr = ' OR '.join([f"{t}*" for t in tokens])
    cur.execute("""
        SELECT p.Code, p.Name, p.Brand, p.BusinessLine, p.Series
        FROM Products_FTS f
        JOIN ProductsCatalog p ON p.Id = f.rowid
        WHERE Products_FTS MATCH ?
        ORDER BY rank
        LIMIT 2;
    """, (fts_expr,))
    rows = cur.fetchall()
    print(f"Consulta: '{tq}'")
    for r in rows:
        print(f"   -> [{r[2]}] {r[0]} | {r[1]} ({r[3]} / {r[4]})")
    print()

cur.execute("SELECT Brand, COUNT(*), COUNT(DISTINCT BusinessLine), COUNT(DISTINCT Family), COUNT(DISTINCT Series) FROM ProductsCatalog GROUP BY Brand;")
print("=== RESUMEN POR MARCA EN LA BASE DE DATOS ===")
for r in cur.fetchall():
    print(f"Marca: {r[0]:<20} | Productos: {r[1]:<4} | Líneas: {r[2]:<2} | Familias: {r[3]:<2} | Series: {r[4]:<2}")

conn.close()
