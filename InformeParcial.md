Informe Técnico: Despliegue de API Webhook de WhatsApp en AWS EC2
Proyecto: Agente de Ventas WhatsApp - Power ElectriMK
Entorno de Despliegue: Producción (AWS EC2)
Sistema Operativo: Ubuntu 24.04.5 LTS
Stack Tecnológico: .NET 8 (C#), Nginx, Systemd, Certbot (Let's Encrypt), Git.

1. Arquitectura del Servidor y Entorno
El servidor fue aprovisionado en una instancia de Amazon EC2. Se configuró el entorno base instalando el SDK de .NET 8 para permitir la compilación y ejecución de la API desarrollada en C#.

Ruta del Proyecto: /var/www/AgenteVentasPower/AgentePower

Repositorio Git: origin main (Blindado y gestionado mediante variables de entorno).

Dirección IP Pública (AWS): [IP_PROTEGIDA_AWS]

2. Compilación y Configuración del Servicio (Systemd)
Para garantizar que la API se ejecute continuamente en segundo plano y se reinicie automáticamente ante fallas o reinicios del servidor, se configuró como un demonio del sistema operativo.

Compilación en Producción: Se ejecutó dotnet publish -c Release -o /var/www/AgenteVentasPower/publish para generar los binarios optimizados.

Creación del Servicio: Se creó el archivo /etc/systemd/system/agenteventas.service.

Parámetros del Servicio:

Puerto interno: 5252 (ASPNETCORE_URLS=http://localhost:5252)

Entorno: Producción (ASPNETCORE_ENVIRONMENT=Production)

Variables de Entorno Ciberseguras:
- VERIFY_TOKEN
- PHONE_NUMBER_ID
- META_TOKEN

Usuario: ubuntu

Ejecutable: /usr/bin/dotnet /var/www/AgenteVentasPower/publish/AgentePower.dll

Estado: Habilitado y en ejecución (active (running)).

3. Configuración de Red (DNS y Nginx)
Dado que Meta exige una conexión HTTPS estricta y segura para los Webhooks, se configuró un subdominio y un proxy inverso.

Registro DNS (Cloudflare):

Se creó un registro tipo A.

Nombre: agente (Subdominio: agente.powerelectrimk.com).

Destino: [IP_PROTEGIDA_AWS].

Estado del Proxy: Desactivado ("Solo DNS") para permitir la validación del certificado SSL.

Proxy Inverso (Nginx):

Instalado vía apt install nginx.

Configurado en /etc/nginx/sites-available/default.

Se configuró el bloque server para escuchar el tráfico del dominio agente.powerelectrimk.com y redirigirlo internamente al puerto 5252 (donde reside la API de .NET).

4. Seguridad y Cifrado (Certbot / Let's Encrypt)
Se aseguró el tráfico de datos mediante la instalación de un certificado SSL gratuito.

Herramienta: Instalación de certbot y python3-certbot-nginx.

Emisión: Se ejecutó certbot --nginx -d agente.powerelectrimk.com.

Resultado: Certificado generado exitosamente e instalado automáticamente en la configuración de Nginx. El tráfico HTTP ahora es redirigido forzosamente a HTTPS.

5. Integración con Meta for Developers
El último paso de infraestructura fue el enlace ("Handshake") entre la API oficial de WhatsApp y el servidor EC2.

Configuración del Webhook (Panel de Meta):

URL de devolución de llamada: https://agente.powerelectrimk.com/api/whatsapp/webhook

Token de verificación: Gestionado de forma segura mediante variable de entorno (VERIFY_TOKEN).

Suscripciones: Se activó la suscripción al campo messages.

Lógica C# de Procesamiento:

Se desarrolló la estructura DTO para mapear el JSON complejo que envía Meta.

La API deserializa los eventos entrantes y valida nulos para ignorar eventos de estado.

Prueba en Vivo: Se envió un mensaje de prueba ("prueba de envio de mensaje") desde un dispositivo móvil de pruebas (+[NUMERO_CLIENTE_PROTEGIDO]) al número de pruebas de Meta.

Resultado de Validación (Journalctl): El monitor del servidor (Logs) confirmó la recepción exitosa y la extracción del número del cliente y del cuerpo del mensaje en texto plano.

Estado Final de la Infraestructura: Fases 1 y 2 completadas y blindadas bajo buenas prácticas de ciberseguridad.
