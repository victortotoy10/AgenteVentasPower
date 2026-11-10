using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

// Servicios base para documentación OpenAPI / Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Token de verificación configurado para Meta Developer Dashboard
const string VerifyToken = "PowerElectriMK_Token_2026";

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
        // Meta requiere explícitamente el 'challenge' devuelto en texto plano (text/plain) con HTTP 200
        return Results.Text(challenge);
    }

    logger.LogWarning("Intento de verificación fallido. Token o modo incorrecto. Mode: {Mode}, Token: {Token}", mode, token);
    
    // Retornamos 403 Forbidden explícito sin depender de esquemas de autenticación
    return Results.StatusCode(StatusCodes.Status403Forbidden);
})
.WithName("VerifyWhatsAppWebhook")
.WithSummary("Valida el webhook frente a Meta WhatsApp Cloud API");

// =========================================================================
// 2. ENDPOINT POST: Recepción de eventos / mensajes de WhatsApp
// =========================================================================
app.MapPost("/api/whatsapp/webhook", (
    [FromBody] WhatsAppWebhookPayload? payload,
    ILogger<Program> logger) =>
{
    try
    {
        // Validamos la jerarquía completa del payload con null-checks para evitar caídas
        // en eventos de estado (sent, delivered, read) o notificaciones sin mensajes
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
                    // Ignoramos eventos de estado o cambios sin mensajes
                    continue;
                }

                foreach (var message in messages)
                {
                    // Validamos que sea un mensaje de texto real con remitente y contenido
                    if (message.Type == "text" && message.Text != null && !string.IsNullOrWhiteSpace(message.From))
                    {
                        var numeroCliente = message.From;
                        var textoMensaje = message.Text.Body;

                        Console.WriteLine($"[NUEVO MENSAJE] De: {numeroCliente} - Texto: {textoMensaje}");
                    }
                }
            }
        }
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Error al procesar el webhook entrante de WhatsApp.");
    }

    // Meta exige responder con HTTP 200 inmediatamente para evitar reintentos automáticos
    return Results.Ok();
})
.WithName("ReceiveWhatsAppEvent")
.WithSummary("Recibe y procesa mensajes entrantes de WhatsApp");

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
