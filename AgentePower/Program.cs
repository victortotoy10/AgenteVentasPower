using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

// =========================================================================
// 0. VALIDACIÓN DE VARIABLES DE ENTORNO AL INICIAR LA APLICACIÓN
// =========================================================================
var verifyToken = Environment.GetEnvironmentVariable("VERIFY_TOKEN");
var metaToken = Environment.GetEnvironmentVariable("META_TOKEN");
var phoneNumberId = Environment.GetEnvironmentVariable("PHONE_NUMBER_ID");

if (string.IsNullOrWhiteSpace(verifyToken))
{
    Console.WriteLine("[ERROR CRÍTICO] La variable de entorno 'VERIFY_TOKEN' no está configurada. El Webhook de Meta no podrá validarse.");
}

if (string.IsNullOrWhiteSpace(metaToken))
{
    Console.WriteLine("[ERROR CRÍTICO] La variable de entorno 'META_TOKEN' no está configurada. El envío de respuestas salientes fallará.");
}

if (string.IsNullOrWhiteSpace(phoneNumberId))
{
    Console.WriteLine("[ERROR CRÍTICO] La variable de entorno 'PHONE_NUMBER_ID' no está configurada. No se podrá construir la URL de Meta Graph API.");
}

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
// 1. ENDPOINT GET: Handshake de verificación con Meta
// =========================================================================
app.MapGet("/api/whatsapp/webhook", (
    [FromQuery(Name = "hub.mode")] string? mode,
    [FromQuery(Name = "hub.verify_token")] string? token,
    [FromQuery(Name = "hub.challenge")] string? challenge,
    ILogger<Program> logger) =>
{
    var currentVerifyToken = Environment.GetEnvironmentVariable("VERIFY_TOKEN");

    if (string.IsNullOrWhiteSpace(currentVerifyToken))
    {
        logger.LogError("[ERROR CRÍTICO] La variable 'VERIFY_TOKEN' no está configurada en el servidor.");
        return Results.StatusCode(StatusCodes.Status500InternalServerError);
    }

    if (mode == "subscribe" && token == currentVerifyToken)
    {
        logger.LogInformation("Verificación de webhook de WhatsApp completada con éxito.");
        return Results.Text(challenge);
    }

    logger.LogWarning("Intento de verificación fallido. Token o modo incorrecto. Mode: {Mode}", mode);
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
                        var textoMensaje = message.Text.Body;

                        Console.WriteLine($"[NUEVO MENSAJE] De: {numeroCliente} - Texto: {textoMensaje}");

                        // Responder siempre de manera dinámica al número del cliente entrante
                        await EnviarMensajeWhatsApp(
                            numeroCliente,
                            $"¡Hola! Soy el Agente virtual de Power ElectriMK. He recibido tu mensaje: '{textoMensaje}'. En qué te puedo ayudar?"
                        );
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
.WithSummary("Recibe y procesa mensajes entrantes de WhatsApp");

// =========================================================================
// Función: Motor de respuesta para WhatsApp Cloud API
// =========================================================================
async Task EnviarMensajeWhatsApp(string numeroDestino, string mensajeBody)
{
    try
    {
        var token = Environment.GetEnvironmentVariable("META_TOKEN");
        var phoneId = Environment.GetEnvironmentVariable("PHONE_NUMBER_ID");

        if (string.IsNullOrWhiteSpace(token))
        {
            Console.WriteLine("[ERROR CRÍTICO] La variable 'META_TOKEN' no está configurada o está vacía. No se realizará la petición HTTP.");
            return;
        }

        if (string.IsNullOrWhiteSpace(phoneId))
        {
            Console.WriteLine("[ERROR CRÍTICO] La variable 'PHONE_NUMBER_ID' no está configurada o está vacía. No se realizará la petición HTTP.");
            return;
        }

        var apiUrl = $"https://graph.facebook.com/v20.0/{phoneId}/messages";

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
        using var request = new HttpRequestMessage(HttpMethod.Post, apiUrl);
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
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
