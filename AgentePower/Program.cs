using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Mvc;
using Mscc.GenerativeAI;
using Mscc.GenerativeAI.Types;

var builder = WebApplication.CreateBuilder(args);

// Servicios base para documentación OpenAPI / Swagger y cliente HTTP
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddHttpClient();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// =========================================================================
// Constantes de configuración para WhatsApp Cloud API
// =========================================================================
string VerifyToken = Environment.GetEnvironmentVariable("VERIFY_TOKEN") ?? "PowerElectriMK_Token_2026";
string MetaAccessToken = Environment.GetEnvironmentVariable("META_TOKEN") ?? "";
string PhoneNumberId = Environment.GetEnvironmentVariable("PHONE_NUMBER_ID") ?? "1366071403267166";
string WhatsAppApiUrl = $"https://graph.facebook.com/v20.0/{PhoneNumberId}/messages";

// =========================================================================
// System Prompt: Instrucciones de rol para el Agente de Ventas en Gemini
// =========================================================================
const string SystemPromptPowerElectriMK = """
Eres el Agente Virtual de Ventas y Asesor Comercial oficial de 'Power ElectriMK', empresa líder en ingeniería eléctrica, distribución de materiales eléctricos de baja y media tensión, iluminación industrial, cableado, tableros de control y automatización.

Tus objetivos son:
1. Saludar cordialmente y con entusiasmo profesional al cliente en nombre de Power ElectriMK.
2. Identificar qué producto, material o servicio eléctrico está buscando el cliente.
3. Brindar asesoría técnica clara, concisa y orientada a la venta.
4. Responder siempre en español, de forma breve y amigable (máximo 2 a 3 párrafos cortos), ideal para formato WhatsApp (usa negritas con *texto* y emojis con moderación).
5. Si el cliente solicita una cotización formal o desea realizar una compra, invítalo a compartir su lista de materiales o datos de contacto (nombre y correo) e indícale que un asesor comercial humano se comunicará para formalizar su cotización.
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
// 2. ENDPOINT POST: Recepción de eventos / mensajes de WhatsApp
// =========================================================================
app.MapPost("/api/whatsapp/webhook", async (
    [FromBody] WhatsAppWebhookPayload? payload,
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

                        // 1. Consultar a Google Gemini con el mensaje del cliente
                        var respuestaIa = await ConsultarGemini(textoMensaje);

                        Console.WriteLine($"[RESPUESTA GEMINI IA] Para: {numeroCliente} - Respuesta: {respuestaIa}");

                        // 2. Responder dinámicamente con la respuesta de la IA
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
.WithSummary("Recibe y procesa mensajes entrantes de WhatsApp con IA");

// =========================================================================
// Función: Consultar a Google Gemini API
// =========================================================================
async Task<string> ConsultarGemini(string mensajeCliente)
{
    var apiKey = Environment.GetEnvironmentVariable("GEMINI_API_KEY");

    if (string.IsNullOrWhiteSpace(apiKey))
    {
        Console.WriteLine("[ERROR CRÍTICO] La variable 'GEMINI_API_KEY' no está configurada o está vacía.");
        return "¡Hola! Gracias por comunicarte con Power ElectriMK. En este momento nuestro asesor virtual se encuentra en mantenimiento. En breve un asesor comercial te atenderá.";
    }

    try
    {
        var googleAi = new GoogleAI(apiKey: apiKey);
        var model = googleAi.GenerativeModel(
            model: "gemini-1.5-flash",
            systemInstruction: new Content(SystemPromptPowerElectriMK, "system")
        );

        var response = await model.GenerateContent(mensajeCliente);
        var respuestaTexto = response?.Text?.Trim();

        if (string.IsNullOrWhiteSpace(respuestaTexto))
        {
            return "¡Hola! Gracias por comunicarte con Power ElectriMK. ¿En qué producto o material eléctrico te podemos asesorar hoy?";
        }

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
