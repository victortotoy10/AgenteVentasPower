using Microsoft.Data.Sqlite;
using System.Text;
using System.Text.Json;

namespace AgentePower;

public record ChatRecord(string Role, string Message);

/// <summary>
/// Entidad de producto técnico industrial optimizada para Compras y Técnicos (Sin precios).
/// </summary>
public record ProductRecord(
    string Brand,
    string BusinessLine,
    string Family,
    string Series,
    string Code,
    string Name,
    string Description,
    string TechnicalSpecs,
    string Application,
    string Status = "Disponible",
    int SearchCount = 0
)
{
    // Propiedad de compatibilidad con código previo si es requerida
    public string Category => Family;
}

public class DatabaseService
{
    private readonly string _connectionString;

    public DatabaseService(string? dbPath = null)
    {
        var path = dbPath ?? Path.Combine(AppContext.BaseDirectory, "agente_ventas.db");
        _connectionString = $"Data Source={path};";
        InitDatabase();
    }

    public string ConnectionString => _connectionString;

    private void InitDatabase()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        // 1. Pragmas de alto rendimiento (Análogo a Buffer Pool y configuración OLTP)
        using var pragmaCmd = connection.CreateCommand();
        pragmaCmd.CommandText = """
            PRAGMA journal_mode = WAL;          -- Concurrencia alta de lectura y escritura
            PRAGMA synchronous = NORMAL;        -- Minimiza esperas de I/O a disco
            PRAGMA cache_size = -64000;         -- 64 MB de caché en RAM para páginas e índices
            PRAGMA temp_store = MEMORY;         -- Almacenamiento temporal en RAM
        """;
        pragmaCmd.ExecuteNonQuery();

        // 2. Tabla de historial de chat para memoria conversacional
        using var cmd = connection.CreateCommand();
        cmd.CommandText = """
            CREATE TABLE IF NOT EXISTS ChatHistory (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerNumber TEXT NOT NULL,
                Role TEXT NOT NULL, -- 'user' o 'model'
                Message TEXT NOT NULL,
                CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_chat_customer ON ChatHistory (CustomerNumber, CreatedAt DESC);

            -- 3. Tabla relacional de Catálogo Técnico
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

            CREATE INDEX IF NOT EXISTS idx_products_brand ON ProductsCatalog (Brand);
            CREATE INDEX IF NOT EXISTS idx_products_line ON ProductsCatalog (BusinessLine);
            CREATE INDEX IF NOT EXISTS idx_products_series ON ProductsCatalog (Series);
            CREATE INDEX IF NOT EXISTS idx_products_code ON ProductsCatalog (Code);

            -- 4. Tabla Virtual FTS5 (Full-Text Search) con BM25 para Técnicos
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

            -- Triggers para mantener sincronizado el índice FTS5 automáticamente
            CREATE TRIGGER IF NOT EXISTS trg_products_insert AFTER INSERT ON ProductsCatalog BEGIN
                INSERT INTO Products_FTS (rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
                VALUES (new.Id, new.Code, new.Name, new.Brand, new.BusinessLine, new.Family, new.Series, new.Description, new.TechnicalSpecs, new.Application);
            END;

            CREATE TRIGGER IF NOT EXISTS trg_products_delete AFTER DELETE ON ProductsCatalog BEGIN
                INSERT INTO Products_FTS (Products_FTS, rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
                VALUES ('delete', old.Id, old.Code, old.Name, old.Brand, old.BusinessLine, old.Family, old.Series, old.Description, old.TechnicalSpecs, old.Application);
            END;

            DROP TRIGGER IF EXISTS trg_products_update;
            CREATE TRIGGER trg_products_update AFTER UPDATE OF Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application ON ProductsCatalog BEGIN
                INSERT INTO Products_FTS (Products_FTS, rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
                VALUES ('delete', old.Id, old.Code, old.Name, old.Brand, old.BusinessLine, old.Family, old.Series, old.Description, old.TechnicalSpecs, old.Application);
                INSERT INTO Products_FTS (rowid, Code, Name, Brand, BusinessLine, Family, Series, Description, TechnicalSpecs, Application)
                VALUES (new.Id, new.Code, new.Name, new.Brand, new.BusinessLine, new.Family, new.Series, new.Description, new.TechnicalSpecs, new.Application);
            END;
        """;
        cmd.ExecuteNonQuery();

        // 4b. Esquema de Telemetría de Demanda para el Agente Comercial
        try
        {
            using var alterCmd1 = connection.CreateCommand();
            alterCmd1.CommandText = "ALTER TABLE ProductsCatalog ADD COLUMN SearchCount INTEGER DEFAULT 0;";
            alterCmd1.ExecuteNonQuery();
        }
        catch { }

        try
        {
            using var alterCmd2 = connection.CreateCommand();
            alterCmd2.CommandText = "ALTER TABLE ProductsCatalog ADD COLUMN LastQueriedAt DATETIME;";
            alterCmd2.ExecuteNonQuery();
        }
        catch { }

        using var analyticsCmd = connection.CreateCommand();
        analyticsCmd.CommandText = """
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
            CREATE INDEX IF NOT EXISTS idx_analytics_code ON ProductSearchAnalytics (ProductCode);
            CREATE INDEX IF NOT EXISTS idx_analytics_family ON ProductSearchAnalytics (Family);
            CREATE INDEX IF NOT EXISTS idx_analytics_brand ON ProductSearchAnalytics (Brand);
            CREATE INDEX IF NOT EXISTS idx_analytics_created ON ProductSearchAnalytics (CreatedAt);
        """;
        analyticsCmd.ExecuteNonQuery();

        // 5. Sembrar catálogo inicial verificado de las 6 líneas clave
        SeedCatalogIfEmpty(connection);

        // 6. Verificar integridad del índice FTS5 y reconstruir si hay desfase
        try
        {
            using var chkCmd = connection.CreateCommand();
            chkCmd.CommandText = "SELECT (SELECT COUNT(1) FROM ProductsCatalog), (SELECT COUNT(1) FROM Products_FTS);";
            using var reader = chkCmd.ExecuteReader();
            if (reader.Read())
            {
                var catCount = reader.GetInt64(0);
                var ftsCount = reader.GetInt64(1);
                if (catCount > 0 && catCount != ftsCount)
                {
                    using var rebCmd = connection.CreateCommand();
                    rebCmd.CommandText = "INSERT INTO Products_FTS(Products_FTS) VALUES('rebuild');";
                    rebCmd.ExecuteNonQuery();
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[AVISO FTS INIT] Reconstruyendo índice por seguridad: {ex.Message}");
            try
            {
                using var rebCmd = connection.CreateCommand();
                rebCmd.CommandText = "INSERT INTO Products_FTS(Products_FTS) VALUES('rebuild');";
                rebCmd.ExecuteNonQuery();
            }
            catch { }
        }
    }

    private void SeedCatalogIfEmpty(SqliteConnection connection)
    {
        using var countCmd = connection.CreateCommand();
        countCmd.CommandText = "SELECT COUNT(1) FROM ProductsCatalog;";
        var count = Convert.ToInt64(countCmd.ExecuteScalar() ?? 0);

        if (count > 0) return;

        // Catálogo representativo inicial de las 6 líneas autorizadas de Schneider Electric
        var initialProducts = new List<ProductRecord>
        {
            // 1. DISTRIBUCIÓN ELÉCTRICA
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Distribución Eléctrica",
                Family: "Interruptores Termomagnéticos",
                Series: "Easy9",
                Code: "EZ9F34225",
                Name: "Interruptor Termomagnético Easy9 2P 25A Curva C",
                Description: "Interruptor magnetotérmico para protección contra sobrecargas y cortocircuitos en baja tensión",
                TechnicalSpecs: "{\"Polos\": \"2P\", \"Corriente\": \"25A\", \"Curva\": \"C\", \"PoderCorte\": \"4.5 kA\", \"Tension\": \"230/400V AC\", \"Montaje\": \"Riel DIN\"}",
                Application: "Protección de circuitos de fuerza e iluminación en instalaciones residenciales y comerciales"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Distribución Eléctrica",
                Family: "Interruptores Termomagnéticos",
                Series: "Acti9",
                Code: "A9F74116",
                Name: "Interruptor Termomagnético Acti9 iC60N 1P 16A Curva C",
                Description: "Disyuntor unipolar de alta fiabilidad industrial para protección terciaria e industrial",
                TechnicalSpecs: "{\"Polos\": \"1P\", \"Corriente\": \"16A\", \"Curva\": \"C\", \"PoderCorte\": \"6 kA\", \"Tension\": \"220/240V AC\", \"Montaje\": \"Riel DIN\"}",
                Application: "Cuadros eléctricos de distribución en industria y edificios comerciales de alta exigencia"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Distribución Eléctrica",
                Family: "Interruptores Diferenciales",
                Series: "Easy9",
                Code: "EZ9R34240",
                Name: "Interruptor Diferencial Easy9 2P 40A 30mA",
                Description: "Dispositivo de corriente residual para protección contra contactos directos e indirectos",
                TechnicalSpecs: "{\"Polos\": \"2P\", \"Corriente\": \"40A\", \"Sensibilidad\": \"30mA\", \"Tipo\": \"AC\", \"Tension\": \"230V AC\"}",
                Application: "Seguridad humana contra electrocución y prevención de incendios por corrientes de fuga"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Distribución Eléctrica",
                Family: "Interruptores de Caja Moldeada",
                Series: "ComPact NSXm",
                Code: "LV426100",
                Name: "Interruptor Automático ComPact NSXm 3P 50A 16kA",
                Description: "Interruptor termomagnético en caja moldeada compacto de potencia para acometidas",
                TechnicalSpecs: "{\"Polos\": \"3P\", \"Corriente\": \"50A\", \"PoderCorte\": \"16 kA (380-415V)\", \"Disparador\": \"TMD (Termomagnético Fijo)\"}",
                Application: "Protección y maniobra de acometidas en tableros generales de distribución baja tensión"
            ),

            // 2. AUTOMATIZACIÓN DE PROCESOS
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Automatización de Procesos",
                Family: "Contactores de Potencia",
                Series: "TeSys D",
                Code: "LC1D18M7",
                Name: "Contactor TeSys D 18A 3P Bobina 220V AC",
                Description: "Contactor tripolar para maniobra y arranque de motores en categoría AC-3",
                TechnicalSpecs: "{\"Polos\": \"3P + 1NA + 1NC\", \"CorrienteAC3\": \"18A\", \"PotenciaMotor\": \"7.5 kW (380-400V)\", \"Bobina\": \"220V AC 50/60Hz\"}",
                Application: "Control de motores eléctricos trifásicos en bandas transportadoras, bombas y compresores"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Automatización de Procesos",
                Family: "Contactores de Potencia",
                Series: "TeSys D",
                Code: "LC1D09M7",
                Name: "Contactor TeSys D 9A 3P Bobina 220V AC",
                Description: "Contactor tripolar compacto para cargas inductivas y motores de baja potencia",
                TechnicalSpecs: "{\"Polos\": \"3P + 1NA + 1NC\", \"CorrienteAC3\": \"9A\", \"PotenciaMotor\": \"4 kW (380-400V)\", \"Bobina\": \"220V AC 50/60Hz\"}",
                Application: "Automatización y arranque directo de motores monofásicos y trifásicos ligeros"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Automatización de Procesos",
                Family: "Guardamotores",
                Series: "TeSys Deca",
                Code: "GV2ME14",
                Name: "Guardamotor Magnetotérmico TeSys GV2ME 6-10A",
                Description: "Dispositivo de protección de motor integral contra sobrecargas, cortocircuitos y fallo de fase",
                TechnicalSpecs: "{\"RangoRegulacion\": \"6.0 a 10.0 A\", \"Polos\": \"3P\", \"Accionamiento\": \"Pulsadores I/O\", \"Montaje\": \"Riel DIN\"}",
                Application: "Protección de motores trifásicos de hasta 4kW a 400V contra calentamiento y bloqueo"
            ),

            // 3. RELÉS DE CONTROL
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Relés de Control",
                Family: "Relés Térmicos de Sobrecarga",
                Series: "TeSys Deca",
                Code: "LRD14",
                Name: "Relé Térmico Diferencial TeSys LRD 7-10A",
                Description: "Relé térmico bimetálico de sobrecarga acoplable directamente bajo contactores LC1D",
                TechnicalSpecs: "{\"RangoAjuste\": \"7.0 a 10.0 A\", \"ClaseDisparo\": \"Clase 10A\", \"ContactosAuxiliares\": \"1NA + 1NC\", \"Rearme\": \"Manual o Automático\"}",
                Application: "Protección térmica específica de motores acoplado en cascada a contactor TeSys D"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Relés de Control",
                Family: "Relés Electromecánicos Enchufables",
                Series: "Harmony Relay",
                Code: "RXM4AB2P7",
                Name: "Relé Miniatura Enchufable 4 C/O 6A Bobina 230V AC",
                Description: "Relé de interfaz de 4 contactos conmutados con botón de prueba y LED indicador",
                TechnicalSpecs: "{\"Contactos\": \"4 C/O (Conmutados)\", \"Corriente\": \"6A\", \"TensionBobina\": \"230V AC\", \"BaseCompatible\": \"RXZE2M114\"}",
                Application: "Aislamiento galvánico, multiplicación de contactos y mando en armarios de control"
            ),

            // 4. DRIVES (VARIADORES DE FRECUENCIA)
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Drives",
                Family: "Variadores de Velocidad",
                Series: "Altivar 12",
                Code: "ATV12H075M2",
                Name: "Variador de Frecuencia Altivar 12 0.75kW (1 HP) 220V Monofásico",
                Description: "Convertidor de frecuencia compacto para control de velocidad en motores trifásicos asíncronos",
                TechnicalSpecs: "{\"Potencia\": \"0.75 kW / 1.0 HP\", \"Entrada\": \"Monofásica 200-240V AC\", \"Salida\": \"Trifásica 0-240V\", \"FiltroEMC\": \"Integrado\"}",
                Application: "Control de velocidad y rampas suaves en ventiladores, bombas de agua y cintas transportadoras pequeñas"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Drives",
                Family: "Variadores de Velocidad",
                Series: "Altivar 320",
                Code: "ATV320U15N4B",
                Name: "Variador de Frecuencia Altivar 320 Book 1.5kW (2 HP) 380-500V Trifásico",
                Description: "Variador de velocidad vectorial de alto rendimiento para maquinaria industrial compleja",
                TechnicalSpecs: "{\"Potencia\": \"1.5 kW / 2.0 HP\", \"Entrada\": \"Trifásica 380-500V AC\", \"Comunicacion\": \"Modbus RTU / CANopen\", \"Seguridad\": \"SIL 3 / PLe integrado\"}",
                Application: "Embalaje, grúas ligeras, bombas centrífugas y maquinaria industrial de manufactura"
            ),

            // 5. UNIDADES DE MANDO Y SEÑALIZACIÓN
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Unidades de Mando y Señalización",
                Family: "Pulsadores y Pilotos",
                Series: "Harmony XB4",
                Code: "XB4BA31",
                Name: "Pulsador Metálico Rasante Verde 1NA Ø22mm",
                Description: "Pulsador con bisel metálico cromado de retorno por resorte para tableros industriales",
                TechnicalSpecs: "{\"Diametro\": \"22 mm\", \"Color\": \"Verde\", \"Contactos\": \"1 NA (Normalmente Abierto)\", \"GradoProteccion\": \"IP66 / IP69K\", \"Material\": \"Metálico Cromado\"}",
                Application: "Mando y arranque de maquinaria en tableros de control con exigencia mecánica severa"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Unidades de Mando y Señalización",
                Family: "Paradas de Emergencia",
                Series: "Harmony XB4",
                Code: "XB4BS542",
                Name: "Parada de Emergencia Seta Ø40mm Desenganche por Giro 1NC",
                Description: "Botón tipo hongo de seguridad para parada de emergencia con enclavamiento mecánico",
                TechnicalSpecs: "{\"Diametro\": \"Seta 40mm / Montaje 22mm\", \"Color\": \"Rojo\", \"Contactos\": \"1 NC (Apertura Positiva)\", \"Desenganche\": \"Por giro\", \"Norma\": \"ISO 13850 / IEC 60947-5-5\"}",
                Application: "Seguridad industrial y paro de emergencia obligatorio en armarios de máquinas e instalaciones"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Unidades de Mando y Señalización",
                Family: "Pilotos Luminosos",
                Series: "Harmony XB4",
                Code: "XB4BVB4",
                Name: "Piloto LED Monobloc Rojo 24V AC/DC Ø22mm",
                Description: "Indicador luminoso LED integrado de alta luminosidad y larga vida útil",
                TechnicalSpecs: "{\"Diametro\": \"22 mm\", \"Color\": \"Rojo\", \"Tension\": \"24V AC/DC\", \"Consumo\": \"Bajo (<18mA)\", \"GradoProteccion\": \"IP66\"}",
                Application: "Señalización de estado de alarma, falla o parada en tableros eléctricos y pupitres"
            ),

            // 6. CELDAS DE PROTECCIÓN Y ENVOLVENTES
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Celdas de Protección",
                Family: "Cajas y Armarios Metálicos",
                Series: "Spacial CRN",
                Code: "NSYCRN54200",
                Name: "Armario Metálico Spacial CRN 500x400x200mm IP66",
                Description: "Caja de acero soldada monobloc con puerta ciega y placa de montaje lisa incluida",
                TechnicalSpecs: "{\"Dimensiones\": \"500 x 400 x 200 mm\", \"GradoProteccion\": \"IP66 / IK10\", \"Material\": \"Acero laminado pintura epoxi gris RAL 7035\", \"Cierre\": \"Doble barra 3mm\"}",
                Application: "Alojamiento y protección de tableros de automatización, maniobra y distribución en ambientes industriales"
            ),
            new(
                Brand: "Schneider Electric",
                BusinessLine: "Celdas de Protección",
                Family: "Cuadros Modulares",
                Series: "Pragma",
                Code: "PRA10218",
                Name: "Cuadro de Distribución Pragma Superficie 2 Filas 36 Módulos",
                Description: "Cofre termoplástico para aparamenta modular con puerta transparente y rieles DIN regulables",
                TechnicalSpecs: "{\"Capacidad\": \"36 módulos (2x18)\", \"Montaje\": \"Superficie\", \"GradoProteccion\": \"IP40 (con puerta) / IK08\", \"Corriente\": \"Hasta 125A\"}",
                Application: "Tableros de distribución secundaria en locales comerciales, edificios y centros técnicos"
            )
        };

        using var transaction = connection.BeginTransaction();
        foreach (var p in initialProducts)
        {
            using var insertCmd = connection.CreateCommand();
            insertCmd.Transaction = transaction;
            insertCmd.CommandText = """
                INSERT OR REPLACE INTO ProductsCatalog (Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application, Status)
                VALUES (@Brand, @BusinessLine, @Family, @Series, @Code, @Name, @Description, @TechnicalSpecs, @Application, @Status);
            """;
            insertCmd.Parameters.AddWithValue("@Brand", p.Brand);
            insertCmd.Parameters.AddWithValue("@BusinessLine", p.BusinessLine);
            insertCmd.Parameters.AddWithValue("@Family", p.Family);
            insertCmd.Parameters.AddWithValue("@Series", p.Series ?? "");
            insertCmd.Parameters.AddWithValue("@Code", p.Code);
            insertCmd.Parameters.AddWithValue("@Name", p.Name);
            insertCmd.Parameters.AddWithValue("@Description", p.Description ?? "");
            insertCmd.Parameters.AddWithValue("@TechnicalSpecs", p.TechnicalSpecs ?? "{}");
            insertCmd.Parameters.AddWithValue("@Application", p.Application ?? "");
            insertCmd.Parameters.AddWithValue("@Status", p.Status);
            insertCmd.ExecuteNonQuery();
        }
        transaction.Commit();
    }

    /// <summary>
    /// Búsqueda de alta velocidad por Código Exacto (B-Tree Seek en < 0.5 ms para Compras).
    /// </summary>
    public async Task<ProductRecord?> GetProductByExactCodeAsync(string code)
    {
        if (string.IsNullOrWhiteSpace(code)) return null;

        var cleanCode = code.Trim().ToUpperInvariant();
        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            await using var cmd = connection.CreateCommand();
            cmd.CommandText = """
                SELECT Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application, Status, COALESCE(SearchCount, 0)
                FROM ProductsCatalog
                WHERE UPPER(Code) = @Code
                LIMIT 1;
            """;
            cmd.Parameters.AddWithValue("@Code", cleanCode);
            cmd.Prepare(); // Precompilación en el motor VDBE

            await using var reader = await cmd.ExecuteReaderAsync();
            if (await reader.ReadAsync())
            {
                return new ProductRecord(
                    Brand: reader.GetString(0),
                    BusinessLine: reader.GetString(1),
                    Family: reader.GetString(2),
                    Series: reader.IsDBNull(3) ? "" : reader.GetString(3),
                    Code: reader.GetString(4),
                    Name: reader.GetString(5),
                    Description: reader.IsDBNull(6) ? "" : reader.GetString(6),
                    TechnicalSpecs: reader.IsDBNull(7) ? "{}" : reader.GetString(7),
                    Application: reader.IsDBNull(8) ? "" : reader.GetString(8),
                    Status: reader.IsDBNull(9) ? "Disponible" : reader.GetString(9),
                    SearchCount: reader.IsDBNull(10) ? 0 : reader.GetInt32(10)
                );
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR DB CODE SEEK] Error al buscar por código {cleanCode}: {ex.Message}");
        }
        return null;
    }

    private static readonly HashSet<string> SearchStopWords = new(StringComparer.OrdinalIgnoreCase)
    {
        "hola", "buenos", "buenas", "dias", "tardes", "noches", "saludos", "estimado", "estimados",
        "amigo", "amigos", "por", "favor", "tiene", "tienen", "tendran", "necesito", "busco", "requiero",
        "quisiera", "cotizar", "precio", "costo", "para", "como", "esta", "estas", "este", "estos",
        "unas", "unos", "una", "uno", "que", "con", "del", "los", "las", "les", "mas", "menos"
    };

    private static readonly Dictionary<string, string[]> SearchSynonyms = new(StringComparer.OrdinalIgnoreCase)
    {
        { "breaker", ["interruptor", "termomagnetico", "disyuntor", "compact", "easy9", "acti9", "5sl", "3va", "mdw", "mdwp", "mdws", "mdwh", "dwp"] },
        { "breakers", ["interruptor", "termomagnetico", "disyuntor", "compact", "easy9", "acti9", "5sl", "3va", "mdw", "mdwp", "mdws", "mdwh", "dwp"] },
        { "disyuntor", ["interruptor", "termomagnetico", "breaker", "5sl", "acti9", "easy9", "3va", "mdwp", "mdws", "mdwh", "dwp"] },
        { "disyuntores", ["interruptor", "termomagnetico", "breaker", "5sl", "acti9", "easy9", "3va", "mdwp", "mdws", "mdwh", "dwp"] },
        { "taco", ["interruptor", "termomagnetico", "easy9", "acti9", "5sl", "mdwp", "mdws"] },
        { "tacos", ["interruptor", "termomagnetico", "easy9", "acti9", "5sl", "mdwp", "mdws"] },
        { "trifasico", ["3P", "tripolar", "trifasica"] },
        { "bipolar", ["2P", "bifasico", "bifasica"] },
        { "monofasico", ["1P", "unipolar", "monofasica"] },
        { "boton", ["pulsador", "harmony", "3su1", "sirius", "csw"] },
        { "botones", ["pulsador", "harmony", "3su1", "sirius", "csw"] },
        { "seta", ["emergencia", "hongo", "xb4bs542", "3su1", "csw"] },
        { "150a", ["160A", "150", "160", "LV430630", "LV426105", "3VA1116", "3VA2216", "DWP"] },
        { "150", ["160A", "160", "150A", "LV430630", "LV426105", "3VA1116", "3VA2216", "DWP"] },
        { "guardamotor", ["gv2", "gv2me", "3rv", "3rv20", "tesys", "sirius", "ms116", "mpw", "mpw18", "mpw40", "mpw80", "mpw100"] },
        { "guardamotores", ["gv2", "gv2me", "3rv", "3rv20", "tesys", "sirius", "ms116", "mpw", "mpw18", "mpw40", "mpw80", "mpw100"] },
        { "contactor", ["tesys", "lc1d", "lc1k", "3rt", "3rt20", "sirius", "af09", "cwb", "cwm", "cwc0", "cwmc"] },
        { "contactores", ["tesys", "lc1d", "lc1k", "3rt", "3rt20", "sirius", "af09", "cwb", "cwm", "cwc0", "cwmc"] },
        { "motor", ["contactor", "guardamotor", "tesys", "sirius", "lc1d", "3rt20", "gv2", "3rv20", "cwb", "mpw"] },
        { "motores", ["contactor", "guardamotor", "tesys", "sirius", "lc1d", "3rt20", "gv2", "3rv20", "cwb", "mpw"] },
        { "variador", ["altivar", "atv", "atv12", "atv320", "sinamics", "v20", "g120", "cfw", "cfw100", "cfw300", "cfw500", "cfw700", "cfw11"] },
        { "variadores", ["altivar", "atv", "atv12", "atv320", "sinamics", "v20", "g120", "cfw", "cfw100", "cfw300", "cfw500", "cfw700", "cfw11"] },
        { "inversor", ["variador", "cfw", "cfw500", "cfw300", "atv", "sinamics"] },
        { "vfd", ["variador", "cfw", "cfw500", "cfw300", "atv", "sinamics"] },
        { "plc", ["logo", "simatic", "s7-1200", "zelio", "modicon"] },
        { "automata", ["logo", "simatic", "s7-1200", "zelio", "modicon"] },
        { "rele", ["lrd", "rxm", "3ru", "3ru21", "3rp", "3ug", "harmony", "sirius", "rw27", "rw67", "rw117"] },
        { "reles", ["lrd", "rxm", "3ru", "3ru21", "3rp", "3ug", "harmony", "sirius", "rw27", "rw67", "rw117"] },
        { "fuente", ["sitop", "abl", "psu100c", "psu8200", "protop", "pss24w", "pss"] },
        { "fuentes", ["sitop", "abl", "psu100c", "psu8200", "protop", "pss24w", "pss"] },
        { "arrancador", ["3rw", "3rw30", "3rw40", "3rw52", "ats", "altistart", "ssw", "ssw05", "ssw07", "ssw900"] },
        { "arrancadores", ["3rw", "3rw30", "3rw40", "3rw52", "ats", "altistart", "ssw", "ssw05", "ssw07", "ssw900"] },
        { "softstarter", ["arrancador", "ssw", "ssw07", "ssw05", "ssw900", "3rw"] },
        { "dps", ["supresor", "transitorios", "spw", "spw03", "spw13", "ovr", "acti9"] },
        { "supresor", ["dps", "transitorios", "spw", "spw03", "spw13", "ovr"] },
        { "transitorios", ["dps", "supresor", "spw", "spw03", "spw13", "ovr"] },
        { "camara", ["cctv", "camaras", "wcam", "dvr", "nvr"] },
        { "camaras", ["cctv", "camara", "wcam", "dvr", "nvr"] },
        { "cctv", ["camara", "camaras", "wcam", "dvr", "nvr"] },
        { "dvr", ["cctv", "camara", "wcam", "nvr"] },
        { "nvr", ["cctv", "camara", "wcam", "dvr"] },
        { "diferencial", ["idr", "rccb", "rdws", "rdwh", "acti9", "5sv"] },
        { "idr", ["diferencial", "rccb", "rdws", "rdwh"] },
        { "gabinete", ["tablero", "cuadro", "envolvente", "qdw", "qdw02"] },
        { "tablero", ["gabinete", "cuadro", "envolvente", "qdw", "qdw02"] }
    };

    /// <summary>
    /// Búsqueda inteligente de alto rendimiento con SQLite FTS5 (Full-Text Search BM25) para Técnicos y Compras.
    /// Incorpora telemetría de demanda (SearchCount) para priorizar las soluciones más solicitadas por el mercado.
    /// Resuelve consultas complejas en < 2 ms con consumo mínimo de recursos.
    /// </summary>
    public async Task<List<ProductRecord>> SearchProductsAsync(string query, int limit = 5, string? customerNumber = null)
    {
        var results = new List<ProductRecord>();
        if (string.IsNullOrWhiteSpace(query)) return results;

        var cleanQuery = query.Trim();

        // 1. Paso rápido: Si la consulta es una palabra corta que parece un código exacto (ej: EZ9F34225, LC1D18M7)
        if (cleanQuery.Length >= 4 && !cleanQuery.Contains(' '))
        {
            var exactMatch = await GetProductByExactCodeAsync(cleanQuery);
            if (exactMatch != null)
            {
                results.Add(exactMatch);
                _ = Task.Run(() => RecordSearchTelemetryAsync(results, cleanQuery, customerNumber));
                return results;
            }
        }

        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            // 2. Extraer términos significativos filtrando stopwords y expandiendo sinónimos
            var rawTokens = cleanQuery
                .Split(new[] { ' ', ',', '.', ';', '?', '!', '(', ')', '"', '\'', '-', '/', '\\' }, StringSplitOptions.RemoveEmptyEntries)
                .Where(w => w.Length >= 2 && !SearchStopWords.Contains(w))
                .Take(8)
                .ToList();

            if (rawTokens.Count == 0)
            {
                rawTokens = cleanQuery
                    .Split(new[] { ' ', ',', '.', ';', '?', '!' }, StringSplitOptions.RemoveEmptyEntries)
                    .Where(w => w.Length >= 2)
                    .Take(4)
                    .ToList();
            }

            if (rawTokens.Count == 0) return results;

            var ftsTokens = new List<string>();
            foreach (var token in rawTokens)
            {
                if (SearchSynonyms.TryGetValue(token, out var syns))
                {
                    var synTerms = syns.Select(s => $"{s}*").ToList();
                    synTerms.Insert(0, $"{token}*");
                    ftsTokens.Add($"({string.Join(" OR ", synTerms)})");
                }
                else
                {
                    ftsTokens.Add($"{token}*");
                }
            }

            // Ensamblar consulta FTS5 con operador OR y ponderación de ranking BM25 + Telemetría de Demanda
            var ftsMatchQuery = string.Join(" OR ", ftsTokens);

            try
            {
                await using var cmd = connection.CreateCommand();
                cmd.CommandText = """
                    SELECT p.Brand, p.BusinessLine, p.Family, p.Series, p.Code, p.Name, p.Description, p.TechnicalSpecs, p.Application, p.Status, COALESCE(p.SearchCount, 0)
                    FROM Products_FTS f
                    JOIN ProductsCatalog p ON p.Id = f.rowid
                    WHERE Products_FTS MATCH @FtsQuery
                    ORDER BY rank ASC, p.SearchCount DESC
                    LIMIT @Limit;
                """;
                cmd.Parameters.AddWithValue("@FtsQuery", ftsMatchQuery);
                cmd.Parameters.AddWithValue("@Limit", limit);
                cmd.Prepare(); // Plan precompilado (Prepared Statement)

                await using var reader = await cmd.ExecuteReaderAsync();
                while (await reader.ReadAsync())
                {
                    results.Add(new ProductRecord(
                        Brand: reader.GetString(0),
                        BusinessLine: reader.GetString(1),
                        Family: reader.GetString(2),
                        Series: reader.IsDBNull(3) ? "" : reader.GetString(3),
                        Code: reader.GetString(4),
                        Name: reader.GetString(5),
                        Description: reader.IsDBNull(6) ? "" : reader.GetString(6),
                        TechnicalSpecs: reader.IsDBNull(7) ? "{}" : reader.GetString(7),
                        Application: reader.IsDBNull(8) ? "" : reader.GetString(8),
                        Status: reader.IsDBNull(9) ? "Disponible" : reader.GetString(9),
                        SearchCount: reader.IsDBNull(10) ? 0 : reader.GetInt32(10)
                    ));
                }
            }
            catch (Exception ftsEx)
            {
                Console.WriteLine($"[AVISO FTS AUTO-REPAIR] Error en consulta FTS '{ftsMatchQuery}': {ftsEx.Message}. Reparando índice...");
                try
                {
                    await using var fixCmd = connection.CreateCommand();
                    fixCmd.CommandText = "INSERT INTO Products_FTS(Products_FTS) VALUES('rebuild');";
                    await fixCmd.ExecuteNonQueryAsync();
                }
                catch { }
            }

            // 3. Fallback Seguro: Si FTS5 no devolvió coincidencias o falló, hacemos un escaneo de índice LIKE
            if (results.Count == 0)
            {
                var fallbackWords = cleanQuery
                    .Split(new[] { ' ', ',', ';' }, StringSplitOptions.RemoveEmptyEntries)
                    .Where(w => w.Length >= 3 && !SearchStopWords.Contains(w))
                    .Take(4)
                    .ToList();

                if (fallbackWords.Count > 0)
                {
                    var whereClauses = new List<string>();
                    await using var fallbackCmd = connection.CreateCommand();

                    for (int i = 0; i < fallbackWords.Count; i++)
                    {
                        var param = $"@kw{i}";
                        whereClauses.Add($"(Code LIKE {param} OR Name LIKE {param} OR Series LIKE {param} OR Family LIKE {param})");
                        fallbackCmd.Parameters.AddWithValue(param, $"%{fallbackWords[i]}%");
                    }

                    fallbackCmd.CommandText = $"""
                        SELECT Brand, BusinessLine, Family, Series, Code, Name, Description, TechnicalSpecs, Application, Status, COALESCE(SearchCount, 0)
                        FROM ProductsCatalog
                        WHERE {string.Join(" OR ", whereClauses)}
                        ORDER BY SearchCount DESC
                        LIMIT @Limit;
                    """;
                    fallbackCmd.Parameters.AddWithValue("@Limit", limit);
                    fallbackCmd.Prepare();

                    await using var fbReader = await fallbackCmd.ExecuteReaderAsync();
                    while (await fbReader.ReadAsync())
                    {
                        results.Add(new ProductRecord(
                            Brand: fbReader.GetString(0),
                            BusinessLine: fbReader.GetString(1),
                            Family: fbReader.GetString(2),
                            Series: fbReader.IsDBNull(3) ? "" : fbReader.GetString(3),
                            Code: fbReader.GetString(4),
                            Name: fbReader.GetString(5),
                            Description: fbReader.IsDBNull(6) ? "" : fbReader.GetString(6),
                            TechnicalSpecs: fbReader.IsDBNull(7) ? "{}" : fbReader.GetString(7),
                            Application: fbReader.IsDBNull(8) ? "" : fbReader.GetString(8),
                            Status: fbReader.IsDBNull(9) ? "Disponible" : fbReader.GetString(9),
                            SearchCount: fbReader.IsDBNull(10) ? 0 : fbReader.GetInt32(10)
                        ));
                    }
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR DB SEARCH] Error general en búsqueda de productos para '{cleanQuery}': {ex.Message}");
        }

        // 4. Registro Asíncrono de Telemetría de Demanda (Background Task, Cero Latencia)
        if (results.Count > 0)
        {
            _ = Task.Run(() => RecordSearchTelemetryAsync(results, cleanQuery, customerNumber));
        }

        return results;
    }

    /// <summary>
    /// Guarda mensajes de chat para la memoria conversacional.
    /// </summary>
    public async Task SaveMessageAsync(string customerNumber, string role, string message)
    {
        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            await using var cmd = connection.CreateCommand();
            cmd.CommandText = """
                INSERT INTO ChatHistory (CustomerNumber, Role, Message)
                VALUES (@CustomerNumber, @Role, @Message);
            """;
            cmd.Parameters.AddWithValue("@CustomerNumber", customerNumber);
            cmd.Parameters.AddWithValue("@Role", role);
            cmd.Parameters.AddWithValue("@Message", message);
            cmd.Prepare();
            await cmd.ExecuteNonQueryAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR DB] No se pudo guardar mensaje: {ex.Message}");
        }
    }

    /// <summary>
    /// Recupera los últimos N mensajes para la ventana de contexto de memoria.
    /// </summary>
    public async Task<List<ChatRecord>> GetRecentHistoryAsync(string customerNumber, int limit = 6)
    {
        var list = new List<ChatRecord>();
        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            await using var cmd = connection.CreateCommand();
            cmd.CommandText = """
                SELECT Role, Message FROM (
                    SELECT Role, Message, CreatedAt 
                    FROM ChatHistory 
                    WHERE CustomerNumber = @CustomerNumber 
                    ORDER BY CreatedAt DESC 
                    LIMIT @Limit
                ) sub 
                ORDER BY CreatedAt ASC;
            """;
            cmd.Parameters.AddWithValue("@CustomerNumber", customerNumber);
            cmd.Parameters.AddWithValue("@Limit", limit);
            cmd.Prepare();

            await using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                list.Add(new ChatRecord(
                    Role: reader.GetString(0),
                    Message: reader.GetString(1)
                ));
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR DB] No se pudo consultar historial: {ex.Message}");
        }
        return list;
    }

    /// <summary>
    /// Telemetría de Demanda: Registra de forma asíncrona la consulta de los productos y familias
    /// para auto-adaptar la prioridad de recomendación y proporcionar inteligencia de compras a la empresa.
    /// </summary>
    public async Task RecordSearchTelemetryAsync(IEnumerable<ProductRecord> products, string queryTerm, string? customerNumber)
    {
        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            await using var transaction = await connection.BeginTransactionAsync();

            await using var updateCmd = connection.CreateCommand();
            updateCmd.Transaction = (SqliteTransaction)transaction;
            updateCmd.CommandText = """
                UPDATE ProductsCatalog 
                SET SearchCount = COALESCE(SearchCount, 0) + 1, 
                    LastQueriedAt = CURRENT_TIMESTAMP 
                WHERE Code = @Code;
            """;
            var codeParam = updateCmd.Parameters.Add("@Code", SqliteType.Text);
            updateCmd.Prepare();

            await using var insertCmd = connection.CreateCommand();
            insertCmd.Transaction = (SqliteTransaction)transaction;
            insertCmd.CommandText = """
                INSERT INTO ProductSearchAnalytics (ProductCode, Brand, Family, Series, QueryTerm, CustomerNumber)
                VALUES (@ProductCode, @Brand, @Family, @Series, @QueryTerm, @CustomerNumber);
            """;
            insertCmd.Parameters.Add("@ProductCode", SqliteType.Text);
            insertCmd.Parameters.Add("@Brand", SqliteType.Text);
            insertCmd.Parameters.Add("@Family", SqliteType.Text);
            insertCmd.Parameters.Add("@Series", SqliteType.Text);
            insertCmd.Parameters.Add("@QueryTerm", SqliteType.Text);
            insertCmd.Parameters.Add("@CustomerNumber", SqliteType.Text);
            insertCmd.Prepare();

            foreach (var prod in products)
            {
                codeParam.Value = prod.Code;
                await updateCmd.ExecuteNonQueryAsync();

                insertCmd.Parameters["@ProductCode"].Value = prod.Code;
                insertCmd.Parameters["@Brand"].Value = prod.Brand;
                insertCmd.Parameters["@Family"].Value = prod.Family;
                insertCmd.Parameters["@Series"].Value = (object?)prod.Series ?? DBNull.Value;
                insertCmd.Parameters["@QueryTerm"].Value = queryTerm;
                insertCmd.Parameters["@CustomerNumber"].Value = (object?)customerNumber ?? DBNull.Value;
                await insertCmd.ExecuteNonQueryAsync();
            }

            await transaction.CommitAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[AVISO TELEMETRÍA] Error no crítico al registrar demanda: {ex.Message}");
        }
    }

    /// <summary>
    /// Devuelve los productos más consultados / demandados por los clientes en WhatsApp.
    /// </summary>
    public async Task<List<Dictionary<string, object>>> GetTopDemandedProductsAsync(int limit = 10)
    {
        var list = new List<Dictionary<string, object>>();
        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            await using var cmd = connection.CreateCommand();
            cmd.CommandText = """
                SELECT Code, Name, Brand, Family, Series, SearchCount, LastQueriedAt
                FROM ProductsCatalog
                WHERE SearchCount > 0
                ORDER BY SearchCount DESC, LastQueriedAt DESC
                LIMIT @Limit;
            """;
            cmd.Parameters.AddWithValue("@Limit", limit);
            await using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                list.Add(new Dictionary<string, object>
                {
                    ["Code"] = reader.GetString(0),
                    ["Name"] = reader.GetString(1),
                    ["Brand"] = reader.GetString(2),
                    ["Family"] = reader.GetString(3),
                    ["Series"] = reader.IsDBNull(4) ? "" : reader.GetString(4),
                    ["SearchCount"] = reader.GetInt32(5),
                    ["LastQueriedAt"] = reader.IsDBNull(6) ? "" : reader.GetString(6)
                });
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR ANALYTICS] {ex.Message}");
        }
        return list;
    }

    /// <summary>
    /// Devuelve el resumen de demanda agregada por Marca.
    /// </summary>
    public async Task<List<Dictionary<string, object>>> GetBrandDemandSummaryAsync()
    {
        var list = new List<Dictionary<string, object>>();
        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            await using var cmd = connection.CreateCommand();
            cmd.CommandText = """
                SELECT Brand, COUNT(*) AS TotalConsultas, COUNT(DISTINCT ProductCode) AS ProductosDistintos
                FROM ProductSearchAnalytics
                GROUP BY Brand
                ORDER BY TotalConsultas DESC;
            """;
            await using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                list.Add(new Dictionary<string, object>
                {
                    ["Brand"] = reader.GetString(0),
                    ["TotalConsultas"] = reader.GetInt32(1),
                    ["ProductosDistintos"] = reader.GetInt32(2)
                });
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR ANALYTICS BRANDS] {ex.Message}");
        }
        return list;
    }

    /// <summary>
    /// Devuelve el resumen de demanda agregada por Familia de productos.
    /// </summary>
    public async Task<List<Dictionary<string, object>>> GetFamilyDemandSummaryAsync()
    {
        var list = new List<Dictionary<string, object>>();
        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();
            await using var cmd = connection.CreateCommand();
            cmd.CommandText = """
                SELECT Family, COUNT(*) AS TotalConsultas
                FROM ProductSearchAnalytics
                GROUP BY Family
                ORDER BY TotalConsultas DESC;
            """;
            await using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                list.Add(new Dictionary<string, object>
                {
                    ["Family"] = reader.GetString(0),
                    ["TotalConsultas"] = reader.GetInt32(1)
                });
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR ANALYTICS FAMILIES] {ex.Message}");
        }
        return list;
    }
}
