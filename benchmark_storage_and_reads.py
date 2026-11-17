import os
import shutil
import sqlite3
import time

def run_benchmark():
    # 1. Almacenamiento en Disco
    disk = shutil.disk_usage('C:\\')
    total_gb = disk.total / (1024**3)
    used_gb = disk.used / (1024**3)
    free_gb = disk.free / (1024**3)
    free_pct = (disk.free / disk.total) * 100

    print("=================== 1. ESPACIO EN DISCO ===================")
    print(f"Disco C: - Total: {total_gb:.2f} GB | Usado: {used_gb:.2f} GB | Libre: {free_gb:.2f} GB ({free_pct:.1f}% libre)")

    # 2. Tamaño de Base de Datos y Catálogos
    db_path = os.path.abspath('agente_ventas.db')
    db_size_mb = os.path.getsize(db_path) / (1024*1024)
    
    cat_size_mb = 0
    cat_count = 0
    for root, dirs, files in os.walk('Catalogos'):
        for f in files:
            cat_size_mb += os.path.getsize(os.path.join(root, f))
            cat_count += 1
    cat_size_mb /= (1024*1024)

    print(f"\nBase de datos 'agente_ventas.db' (1.279 productos + FTS5): {db_size_mb:.2f} MB")
    print(f"Carpeta 'Catalogos/' ({cat_count} archivos PDF originales): {cat_size_mb:.2f} MB")

    # 3. Métricas y Parámetros de SQLite
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("PRAGMA journal_mode;")
    journal = c.fetchone()[0]
    c.execute("PRAGMA page_size;")
    page_size = c.fetchone()[0]
    c.execute("PRAGMA page_count;")
    page_count = c.fetchone()[0]
    c.execute("PRAGMA synchronous;")
    sync_mode = c.fetchone()[0]

    print("\n=================== 2. CONFIGURACIÓN SQLITE ===================")
    print(f"Modo Journal:       {journal.upper()} (Write-Ahead Logging)")
    print(f"Modo Synchronous:   {sync_mode} (NORMAL)")
    print(f"Tamaño de Página:   {page_size} bytes")
    print(f"Total de Páginas:   {page_count} páginas")
    print(f"Datos en Memoria:   {(page_size * page_count) / 1024:.1f} KB (~{db_size_mb:.2f} MB)")

    # 4. Benchmark de Velocidad de Lectura (100 ejecuciones)
    queries = [
        ("Búsqueda por SKU exacto (B-Tree O(log n))", "SELECT * FROM ProductsCatalog WHERE Code = '1020000000'"),
        ("Conteo por Marca (Índice)", "SELECT COUNT(*) FROM ProductsCatalog WHERE Brand = 'Weidmuller'"),
        ("Búsqueda FTS5 un término ('stripax*')", "SELECT p.Code, p.Name FROM Products_FTS f JOIN ProductsCatalog p ON p.Id=f.rowid WHERE Products_FTS MATCH 'stripax*' LIMIT 5"),
        ("Búsqueda FTS5 combinada ('bornera OR PUSH OR WDU')", "SELECT p.Code, p.Name FROM Products_FTS f JOIN ProductsCatalog p ON p.Id=f.rowid WHERE Products_FTS MATCH 'bornera OR PUSH OR WDU' LIMIT 10"),
        ("Búsqueda FTS5 multimarca con ranking BM25", "SELECT p.Code, p.Name, rank FROM Products_FTS f JOIN ProductsCatalog p ON p.Id=f.rowid WHERE Products_FTS MATCH 'disyuntor OR 20A OR UL' ORDER BY rank LIMIT 10")
    ]

    print("\n=================== 3. LATENCIAS DE LECTURA (100 ejecuciones) ===================")
    for name, sql in queries:
        # Warmup
        c.execute(sql)
        c.fetchall()

        t0 = time.perf_counter()
        for _ in range(100):
            c.execute(sql)
            res = c.fetchall()
        t1 = time.perf_counter()
        avg_ms = ((t1 - t0) / 100) * 1000
        print(f"  {name:<46} : {avg_ms:6.3f} ms (Filas devueltas: {len(res)})")

    # 5. Planes de Ejecución
    print("\n=================== 4. PLAN DE EJECUCIÓN (QUERY PLAN) ===================")
    for name, sql in queries[:2]:
        c.execute("EXPLAIN QUERY PLAN " + sql)
        plan = c.fetchall()
        print(f"  {name}:")
        for step in plan:
            print(f"    -> {step[3]}")

    conn.close()

if __name__ == "__main__":
    run_benchmark()
