import sqlite3
import glob

def migrate_db(db_path):
    print(f"Migrating {db_path}...")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 1. Add SearchCount if not exists
    cur.execute("PRAGMA table_info(ProductsCatalog)")
    columns = [row[1] for row in cur.fetchall()]
    
    if "SearchCount" not in columns:
        cur.execute("ALTER TABLE ProductsCatalog ADD COLUMN SearchCount INTEGER DEFAULT 0;")
        print("  Added column SearchCount")
    else:
        print("  Column SearchCount already exists")
        
    if "LastQueriedAt" not in columns:
        cur.execute("ALTER TABLE ProductsCatalog ADD COLUMN LastQueriedAt DATETIME;")
        print("  Added column LastQueriedAt")
    else:
        print("  Column LastQueriedAt already exists")
        
    # 2. Create ProductSearchAnalytics table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ProductSearchAnalytics (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductCode TEXT NOT NULL,
            Brand TEXT NOT NULL,
            Family TEXT NOT NULL,
            Series TEXT,
            QueryTerm TEXT NOT NULL,
            CustomerNumber TEXT,
            CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_analytics_code ON ProductSearchAnalytics (ProductCode);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_analytics_family ON ProductSearchAnalytics (Family);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_analytics_brand ON ProductSearchAnalytics (Brand);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_analytics_created ON ProductSearchAnalytics (CreatedAt);")
    print("  Created ProductSearchAnalytics table and indexes")
    
    # 3. Update trigger to only fire on content column updates, not on SearchCount/LastQueriedAt
    cur.execute("DROP TRIGGER IF EXISTS trg_products_update;")
    cur.execute("""
        CREATE TRIGGER trg_products_update AFTER UPDATE OF Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application ON ProductsCatalog BEGIN
            INSERT INTO Products_FTS (Products_FTS, rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
            VALUES ('delete', old.Id, old.Code, old.Name, old.Brand, old.BusinessLine, old.Family, old.Series, old.Description, old.TechnicalSpecs, old.Application);
            INSERT INTO Products_FTS (rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
            VALUES (new.Id, new.Code, new.Name, new.Brand, new.BusinessLine, new.Family, new.Series, new.Description, new.TechnicalSpecs, new.Application);
        END;
    """)
    print("  Optimized trg_products_update trigger")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    dbs = glob.glob("**/agente_ventas.db", recursive=True)
    dbs.append("agente_ventas.db")
    dbs = sorted(list(set(dbs)))
    for d in dbs:
        migrate_db(d)
    print("Migration finished for all databases!")
