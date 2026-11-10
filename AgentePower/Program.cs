using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Mvc;
using Mscc.GenerativeAI;
using Mscc.GenerativeAI.Types;
using AgentePower;

var builder = WebApplication.CreateBuilder(args);

// Servicios base para documentación OpenAPI / Swagger, cliente HTTP y Base de Datos SQLite
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient();
builder.Services.AddSingleton<DatabaseService>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// =========================================================================
// Constantes de configuración para WhatsApp Cloud API y Gemini
// =========================================================================
string VerifyToken = Environment.GetEnvironmentVariable("VERIFY_TOKEN") ?? "PowerElectriMK_Token_2026";
string MetaAccessToken = Environment.GetEnvironmentVariable("META_TOKEN") ?? "";
string PhoneNumberId = Environment.GetEnvironmentVariable("PHONE_NUMBER_ID") ?? "1366071403267166";
string WhatsAppApiUrl = $"https://graph.facebook.com/v20.0/{PhoneNumberId}/messages";
string GeminiModelId = Environment.GetEnvironmentVariable("GEMINI_MODEL") ?? "gemini-2.0-flash";

// =========================================================================
// System Prompt: Rol de Asesor Comercial para Power ElectriMK
// =========================================================================
const string SystemPromptPowerElectriMK = """
Eres el Asesor Comercial y Agente Virtual de Ventas oficial de 'Power ElectriMK', empresa distribuidora de materiales eléctricos de alta calidad y soluciones de ingeniería eléctrica en baja y media tensión.

Manejamos más de 10 marcas líderes en el mercado, tales como: Schneider Electric, Legrand, Bticino, Centelsa, Siemens, ABB, 3M, Philips, Sylvania y Prysmian.

Tus pautas de atención comercial:
1. Saluda cordialmente en nombre de Power ElectriMK.
2. Si se te proporcionan datos de inventario o productos de nuestro catálogo, úsalos para responder precios, referencias y características técnicas con total precisión.
3. Toma en cuenta el historial reciente de la conversación para no pedirle al cliente que repita lo que ya dijo.
4. Responde en español, de forma breve, concisa y persuasiva (máximo 2 a 3 párrafos cortos), ideal para formato WhatsApp (usa negritas con *texto* y emojis amigables con moderación).
5. Para compras o cotizaciones formales por volumen, invita al cliente a facilitar su lista de cantidades, nombre y correo para que un ejecutivo comercial formalice la proforma.
6. Si el cliente busca una marca o producto que no figura en la lista sugerida, indícale amablemente que sí trabajamos bajo pedido con las principales marcas del país y ofrece canalizarlo con un asesor.
""";

// =========================================================================
// 1. ENDPOINT GET: Handshake de verificación con Meta
// =========================================================================
app.MapGet("/api/whatsapp/webhook", (
    [FromQuery(Name = "hub.mode")] string? mode,
    [FromQuery(Name = "hub.verify_token")] string? token,
    [FromQuery(Name = "hub.challenge")] string? challenge,
    ILogger<Program> logger) =>
{
    if (mode == "subscribe" && token == VerifyToken)
    {
        logger.LogInformation("Verificación de webhook de WhatsApp completada con éxito.");
        return Results.Text(challenge);
    }

    logger.LogWarning("Intento de verificación fallido. Token o modo incorrecto. Mode: {Mode}, Token: {Token}", mode, token);
    return Results.StatusCode(StatusCodes.Status403Forbidden);
})
.WithName("VerifyWhatsAppWebhook")
.WithSummary("Valida el webhook frente a Meta WhatsApp Cloud API");

// =========================================================================
// 2. ENDPOINT POST: Recepción de eventos con Memoria y Catálogo
// =========================================================================
app.MapPost("/api/whatsapp/webhook", async (
    [FromBody] WhatsAppWebhookPayload? payload,
    DatabaseService dbService,
    ILogger<Program> logger) =>
{
    try
    {
        var changes = payload?.Entry?
            .Where(e => e.Changes != null)
            .SelectMany(e => e.Changes!)
            .ToList();

        if (changes != null && changes.Count > 0)
        {
            foreach (var change in changes)
            {
                var messages = change.Value?.Messages;
                if (messages == null || messages.Count == 0)
                {
                    continue;
                }

                foreach (var message in messages)
                {
                    if (message.Type == "text" && message.Text != null && !string.IsNullOrWhiteSpace(message.From))
                    {
                        var numeroCliente = message.From;
                        var textoMensaje = message.Text.Body ?? string.Empty;

                        Console.WriteLine($"[NUEVO MENSAJE] De: {numeroCliente} - Texto: {textoMensaje}");

                        // Consultar a Gemini alimentándolo con memoria conversacional y catálogo de marcas
                        var respuestaIa = await ConsultarGemini(numeroCliente, textoMensaje, dbService);

                        Console.WriteLine($"[RESPUESTA GEMINI IA] Para: {numeroCliente} - Respuesta: {respuestaIa}");

                        // Responder al cliente por WhatsApp
                        await EnviarMensajeWhatsApp(numeroCliente, respuestaIa);
                    }
                }
            }
        }
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Error al procesar el webhook entrante de WhatsApp.");
    }

    // Meta exige responder con HTTP 200 inmediatamente
    return Results.Ok();
})
.WithName("ReceiveWhatsAppEvent")
.WithSummary("Recibe y procesa mensajes con IA, memoria y catálogo");

// =========================================================================
// Función: Consultar a Google Gemini con Contexto RAG y Memoria de Chat
// =========================================================================
async Task<string> ConsultarGemini(string numeroCliente, string mensajeCliente, DatabaseService dbService)
{
    var apiKey = Environment.GetEnvironmentVariable("GEMINI_API_KEY");

    if (string.IsNullOrWhiteSpace(apiKey))
    {
        Console.WriteLine("[ERROR CRÍTICO] La variable 'GEMINI_API_KEY' no está configurada o está vacía.");
        return "¡Hola! Gracias por comunicarte con Power ElectriMK. En este momento nuestro asesor virtual se encuentra en mantenimiento. En breve un asesor comercial te atenderá.";
    }

    try
    {
        // 1. Recuperar los últimos 6 mensajes del cliente (Memoria Conversacional)
        var historial = await dbService.GetRecentHistoryAsync(numeroCliente, limit: 6);

        // 2. Buscar productos coincidentes en el Catálogo de 10 Marcas (RAG Local)
        var productos = await dbService.SearchProductsAsync(mensajeCliente, limit: 4);

        // 3. Ensamblar el Prompt Enriquecido para Gemini
        var promptBuilder = new StringBuilder();

        if (historial.Count > 0)
        {
            promptBuilder.AppendLine("[HISTORIAL RECIENTE CON EL CLIENTE]");
            foreach (var h in historial)
            {
                var actor = h.Role == "user" ? "Cliente" : "Asesor (Tú)";
                promptBuilder.AppendLine($"{actor}: {h.Message}");
            }
            promptBuilder.AppendLine();
        }

        if (productos.Count > 0)
        {
            promptBuilder.AppendLine("[PRODUCTOS DE POWER ELECTRIMK COINCIDENTES EN INVENTARIO]");
            foreach (var p in productos)
            {
                promptBuilder.AppendLine($"- [{p.Brand}] {p.Name} (Cód: {p.Code}) | Categoría: {p.Category} | Ref: ${p.Price:F2} /{p.Unit} | Detalle: {p.Description}");
            }
            promptBuilder.AppendLine();
        }

        promptBuilder.AppendLine($"Cliente (Mensaje actual): {mensajeCliente}");

        var promptCompleto = promptBuilder.ToString();

        // 4. Invocar el modelo Gemini (por defecto gemini-2.0-flash)
        var googleAi = new GoogleAI(apiKey: apiKey);
        var model = googleAi.GenerativeModel(
            model: GeminiModelId,
            systemInstruction: new Content(SystemPromptPowerElectriMK, "system")
        );

        var response = await model.GenerateContent(promptCompleto);
        var respuestaTexto = response?.Text?.Trim();

        if (string.IsNullOrWhiteSpace(respuestaTexto))
        {
            respuestaTexto = "¡Hola! Gracias por comunicarte con Power ElectriMK. ¿En qué producto o material eléctrico te podemos asesorar hoy?";
        }

        // 5. Guardar la conversación en SQLite para persistir la memoria
        await dbService.SaveMessageAsync(numeroCliente, "user", mensajeCliente);
        await dbService.SaveMessageAsync(numeroCliente, "model", respuestaTexto);

        return respuestaTexto;
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[EXCEPCIÓN GEMINI API] Error al generar respuesta con IA: {ex.Message}");
        return "¡Hola! Gracias por comunicarte con Power ElectriMK. Hemos recibido tu mensaje y enseguida un asesor de nuestro equipo se pondrá en contacto contigo.";
    }
}

// =========================================================================
// Función: Motor de respuesta para WhatsApp Cloud API
// =========================================================================
async Task EnviarMensajeWhatsApp(string numeroDestino, string mensajeBody)
{
    try
    {
        if (string.IsNullOrWhiteSpace(MetaAccessToken))
        {
            Console.WriteLine("[ERROR CRÍTICO] La variable 'META_TOKEN' no está configurada o está vacía. No se enviará el mensaje.");
            return;
        }

        var httpClientFactory = app.Services.GetRequiredService<IHttpClientFactory>();
        var httpClient = httpClientFactory.CreateClient();

        var payload = new
        {
            messaging_product = "whatsapp",
            to = numeroDestino,
            type = "text",
            text = new { body = mensajeBody }
        };

        var jsonPayload = JsonSerializer.Serialize(payload);
        using var request = new HttpRequestMessage(HttpMethod.Post, WhatsAppApiUrl);
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", MetaAccessToken);
        request.Content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");

        var response = await httpClient.SendAsync(request);
        var responseContent = await response.Content.ReadAsStringAsync();

        if (response.IsSuccessStatusCode)
        {
            Console.WriteLine($"[MENSAJE ENVIADO] A: {numeroDestino}");
        }
        else
        {
            Console.WriteLine($"[ERROR AL ENVIAR MENSAJE] Status: {response.StatusCode} - {responseContent}");
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"[EXCEPCIÓN HTTP ENVIANDO MENSAJE] Error: {ex.Message}");
    }
}

app.Run();

// =========================================================================
// Modelos DTO (Data Transfer Objects) para WhatsApp Cloud API Webhook
// =========================================================================
public record WhatsAppWebhookPayload(
    [property: JsonPropertyName("object")] string? Object,
    [property: JsonPropertyName("entry")] List<WhatsAppEntry>? Entry
);

public record WhatsAppEntry(
    [property: JsonPropertyName("id")] string? Id,
    [property: JsonPropertyName("changes")] List<WhatsAppChange>? Changes
);

public record WhatsAppChange(
    [property: JsonPropertyName("value")] WhatsAppValue? Value,
    [property: JsonPropertyName("field")] string? Field
);

public record WhatsAppValue(
    [property: JsonPropertyName("messaging_product")] string? MessagingProduct,
    [property: JsonPropertyName("messages")] List<WhatsAppMessage>? Messages
);

public record WhatsAppMessage(
    [property: JsonPropertyName("from")] string? From,
    [property: JsonPropertyName("id")] string? Id,
    [property: JsonPropertyName("timestamp")] string? Timestamp,
    [property: JsonPropertyName("type")] string? Type,
    [property: JsonPropertyName("text")] WhatsAppText? Text
);

public record WhatsAppText(
    [property: JsonPropertyName("body")] string? Body
);
