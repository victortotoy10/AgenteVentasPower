using Microsoft.Data.Sqlite;

namespace AgentePower;

public record ChatRecord(string Role, string Message);

public record ProductRecord(string Brand, string Code, string Name, string Category, string Description, double Price, string Unit);

public class DatabaseService
{
    private readonly string _connectionString;

    public DatabaseService(string? dbPath = null)
    {
        var path = dbPath ?? Path.Combine(AppContext.BaseDirectory, "agente_ventas.db");
        _connectionString = $"Data Source={path};";
        InitDatabase();
    }

    private void InitDatabase()
    {
        using var connection = new SqliteConnection(_connectionString);
        connection.Open();

        // 1. Activar modo WAL (Write-Ahead Logging) para lecturas y escrituras simultáneas ultrarrápidas
        using var pragmaCmd = connection.CreateCommand();
        pragmaCmd.CommandText = "PRAGMA journal_mode = WAL;";
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

            CREATE TABLE IF NOT EXISTS ProductsCatalog (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Brand TEXT NOT NULL,
                Code TEXT,
                Name TEXT NOT NULL,
                Category TEXT NOT NULL,
                Description TEXT,
                Price REAL NOT NULL,
                Unit TEXT DEFAULT 'unidad'
            );
            CREATE INDEX IF NOT EXISTS idx_products_brand ON ProductsCatalog (Brand);
            CREATE INDEX IF NOT EXISTS idx_products_category ON ProductsCatalog (Category);
        """;
        cmd.ExecuteNonQuery();

        // 3. Sembrar catálogo inicial si está vacío
        SeedCatalogIfEmpty(connection);
    }

    private void SeedCatalogIfEmpty(SqliteConnection connection)
    {
        using var countCmd = connection.CreateCommand();
        countCmd.CommandText = "SELECT COUNT(1) FROM ProductsCatalog;";
        var count = Convert.ToInt64(countCmd.ExecuteScalar() ?? 0);

        if (count > 0) return;

        // Catálogo muestra de 10 marcas líderes del sector eléctrico industrial y residencial
        var sampleProducts = new List<ProductRecord>
        {
            new("Schneider Electric", "A9F74116", "Interruptor Termomagnético Acti9 1P 16A", "Protección", "Disyuntor unipolar curva C para protección de circuitos residenciales e industriales", 12.50, "unidad"),
            new("Schneider Electric", "LC1D18M7", "Contactor TeSys D 18A 220V", "Automatización", "Contactor tripolar para control de motores trifásicos hasta 7.5kW", 45.00, "unidad"),
            new("Legrand", "003802", "Interruptor Diferencial DX3 2P 25A 30mA", "Seguridad", "Protección contra fugas a tierra para viviendas y comercios", 38.00, "unidad"),
            new("Bticino", "E2151N", "Tomacorriente Doble con Puesta a Tierra Modus", "Residencial", "Tomacorriente doble 15A 127/250V color blanco", 4.80, "unidad"),
            new("Centelsa", "THHN-12-AZ", "Cable THHN/THWN-2 Calibre 12 AWG Azul", "Cables", "Conductor de cobre suave con aislamiento PVC y chaqueta nylon, 600V 90°C", 0.65, "metro"),
            new("Centelsa", "THHN-10-NG", "Cable THHN/THWN-2 Calibre 10 AWG Negro", "Cables", "Conductor de cobre suave para acometidas y circuitos ramales de fuerza", 0.98, "metro"),
            new("Siemens", "3VA1116-3ED36-0AA0", "Interruptor Caja Moldeada 3VA1 3P 160A", "Distribución", "Interruptor termomagnético de potencia para tablero de distribución principal", 185.00, "unidad"),
            new("ABB", "OT100F3", "Seccionador Bajo Carga 3P 100A", "Protección", "Interruptor seccionador manual de corte visible para montaje en riel DIN", 68.00, "unidad"),
            new("Philips", "BVP150-100W", "Reflector LED Industrial Essential SmartBright 100W", "Iluminación", "Luminaria LED IP65 luz blanca fría 6500K para bodegas y exteriores", 54.00, "unidad"),
            new("Philips", "BY218P-150W", "Campana Industrial LED HighBay 150W", "Iluminación", "Campana colgante para galpones y naves industriales, 18000 lúmenes", 115.00, "unidad"),
            new("3M", "SCOTCH-33+", "Cinta Aislante Scotch Super 33+ Premium", "Aislamiento", "Cinta vinílica resistente a intemperie, rayos UV y hasta 105°C", 5.20, "rollo"),
            new("Sylvania", "P26815-36", "Panel LED Embutir 60x60 40W 4000K", "Iluminación", "Panel ultrafino para cielo raso comercial u oficinas", 26.50, "unidad"),
            new("Prysmian", "TTU-2-0", "Cable de Cobre TTU 2/0 AWG 2000V", "Cables", "Cable subterráneo resistente a humedad y químicos para acometidas de media tensión", 8.20, "metro")
        };

        using var transaction = connection.BeginTransaction();
        foreach (var p in sampleProducts)
        {
            using var insertCmd = connection.CreateCommand();
            insertCmd.Transaction = transaction;
            insertCmd.CommandText = """
                INSERT INTO ProductsCatalog (Brand, Code, Name, Category, Description, Price, Unit)
                VALUES (@Brand, @Code, @Name, @Category, @Description, @Price, @Unit);
            """;
            insertCmd.Parameters.AddWithValue("@Brand", p.Brand);
            insertCmd.Parameters.AddWithValue("@Code", p.Code);
            insertCmd.Parameters.AddWithValue("@Name", p.Name);
            insertCmd.Parameters.AddWithValue("@Category", p.Category);
            insertCmd.Parameters.AddWithValue("@Description", p.Description);
            insertCmd.Parameters.AddWithValue("@Price", p.Price);
            insertCmd.Parameters.AddWithValue("@Unit", p.Unit);
            insertCmd.ExecuteNonQuery();
        }
        transaction.Commit();
    }

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
            await cmd.ExecuteNonQueryAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR DB] No se pudo guardar mensaje: {ex.Message}");
        }
    }

    public async Task<List<ChatRecord>> GetRecentHistoryAsync(string customerNumber, int limit = 6)
    {
        var list = new List<ChatRecord>();
        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            // Obtenemos los últimos N mensajes ordenados cronológicamente
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

    public async Task<List<ProductRecord>> SearchProductsAsync(string query, int limit = 4)
    {
        var results = new List<ProductRecord>();
        if (string.IsNullOrWhiteSpace(query)) return results;

        try
        {
            await using var connection = new SqliteConnection(_connectionString);
            await connection.OpenAsync();

            // Extraer palabras clave de más de 2 caracteres
            var keywords = query
                .Split(new[] { ' ', ',', '.', ';', '?', '!' }, StringSplitOptions.RemoveEmptyEntries)
                .Where(w => w.Length > 2)
                .Take(4)
                .ToList();

            if (keywords.Count == 0) return results;

            var whereClauses = new List<string>();
            var cmd = connection.CreateCommand();

            for (int i = 0; i < keywords.Count; i++)
            {
                var paramName = $"@kw{i}";
                whereClauses.Add($"(Brand LIKE {paramName} OR Name LIKE {paramName} OR Category LIKE {paramName} OR Description LIKE {paramName})");
                cmd.Parameters.AddWithValue(paramName, $"%{keywords[i]}%");
            }

            cmd.CommandText = $"""
                SELECT Brand, Code, Name, Category, Description, Price, Unit 
                FROM ProductsCatalog 
                WHERE {string.Join(" OR ", whereClauses)}
                LIMIT @Limit;
            """;
            cmd.Parameters.AddWithValue("@Limit", limit);

            await using var reader = await cmd.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                results.Add(new ProductRecord(
                    Brand: reader.GetString(0),
                    Code: reader.IsDBNull(1) ? "" : reader.GetString(1),
                    Name: reader.GetString(2),
                    Category: reader.GetString(3),
                    Description: reader.IsDBNull(4) ? "" : reader.GetString(4),
                    Price: reader.GetDouble(5),
                    Unit: reader.GetString(6)
                ));
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERROR DB] No se pudo buscar productos: {ex.Message}");
        }
        return results;
    }
}
