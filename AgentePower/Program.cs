using System.Text.Json;
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
    [FromBody] JsonElement? payload,
    ILogger<Program> logger) =>
{
    // Meta exige responder con HTTP 200 en menos de 3 segundos para evitar reintentos automáticos
    logger.LogInformation("Evento de WhatsApp recibido exitosamente: {Payload}", payload?.ToString());

    return Results.Ok();
})
.WithName("ReceiveWhatsAppEvent")
.WithSummary("Recibe notificaciones de mensajes y estados de entrega");

app.Run();
