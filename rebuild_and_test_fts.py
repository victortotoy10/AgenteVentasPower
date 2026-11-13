import sqlite3
import os

db_paths = [
    "agente_ventas.db",
    "AgentePower/agente_ventas.db",
    "AgentePower/bin/Debug/net8.0/agente_ventas.db",
    "AgentePower/bin/Release/net8.0/agente_ventas.db"
]

for db in db_paths:
    if not os.path.exists(db):
        continue
    print(f"\n--- Processing {db} ---")
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    # Rebuild FTS5 index
    try:
        cur.execute("INSERT INTO Products_FTS(Products_FTS) VALUES('rebuild');")
        conn.commit()
        print("Successfully rebuilt Products_FTS!")
    except Exception as e:
        print(f"Error rebuilding: {e}")

    # Test FTS5 queries
    test_queries = [
        "contactor 25A",
        "LC1D25M7",
        "contactor tesys",
        "3RT2026",
        "breaker 150A",
        "guardamotor 10A"
    ]

    for tq in test_queries:
        tokens = tq.replace("-", " ").split()
        fts_expr = " OR ".join([f"{t}*" for t in tokens])
        cur.execute("""
            SELECT p.Code, p.Name, p.Brand 
            FROM Products_FTS f
            JOIN ProductsCatalog p ON p.Id = f.rowid
            WHERE Products_FTS MATCH ?
            ORDER BY rank
            LIMIT 3;
        """, (fts_expr,))
        rows = cur.fetchall()
        print(f"Search '{tq}':")
        for r in rows:
            print(f"   -> {r[0]} | {r[1]} ({r[2]})")
            
    conn.close()

