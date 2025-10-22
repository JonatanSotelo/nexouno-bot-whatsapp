from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from pathlib import Path
from app.config import load_settings
from app.prompts import load_prompts
from app.whatsapp import WhatsAppClient
from app.drive import DriveClient
import json


import os


ENV_FILE = os.getenv("ENV_FILE", "tenants/cliente_a.env")
PROMPTS_FILE = os.getenv("PROMPTS_FILE", "config/prompts_cliente_a.yml")


settings = load_settings(ENV_FILE)
prompts = load_prompts(PROMPTS_FILE)


app = FastAPI(title=f"Bot WhatsApp – {settings.ENV_NAME}")


wa = WhatsAppClient(
phone_number_id=settings.WA_PHONE_NUMBER_ID,
access_token=settings.WA_ACCESS_TOKEN,
api_version=settings.WA_API_VERSION,
send_enabled=settings.SEND_ENABLED,
)


drive = DriveClient(
enabled=settings.DRIVE_ENABLED,
folder_id=settings.DRIVE_FOLDER_ID,
creds_path=settings.GOOGLE_APPLICATION_CREDENTIALS,
)


@app.get("/health")
def health():
    return {"status": "ok", "tenant": settings.ENV_NAME}


# --- Webhook verification (GET) ---
@app.get("/webhook", response_class=PlainTextResponse)
def verify(
    mode: str | None = Query(None, alias="hub.mode"),
    challenge: str | None = Query(None, alias="hub.challenge"),
    verify_token: str | None = Query(None, alias="hub.verify_token")
):
    # Meta envía los parámetros con el prefijo "hub."
    # Usamos Query con alias para manejar los puntos en los nombres
    if mode == "subscribe" and verify_token == settings.WA_VERIFY_TOKEN:
        return challenge or ""
    raise HTTPException(status_code=403, detail="Forbidden")


# --- Webhook receiver (POST) ---
@app.post("/webhook")
async def webhook(req: Request):
    body = await req.json()
    # Extraer mensaje (forma simplificada)
    try:
        entry = body["entry"][0]["changes"][0]["value"]
        msg = entry.get("messages", [])[0]
        from_number = msg["from"]
        text = msg.get("text", {}).get("body", "")
    except Exception:
        return JSONResponse({"status": "ignored"})

    # Ejemplo: saludo + oferta de tomar pedido
    name = entry.get("contacts", [{}])[0].get("profile", {}).get("name", from_number)
    greet = prompts.greet_template.format(name=name)
    await wa.send_text(from_number, greet)
    return {"status": "ok"}


# --- Endpoint para confirmar y generar archivo TXT ---
@app.post("/confirmar")
async def confirmar(payload: dict):
    """Recibe {"to": "+54911...", "resumen": "..."} y genera archivo + avisa al dueño."""
    to = payload.get("to")
    resumen = payload.get("resumen", "")
    if not to:
        raise HTTPException(400, "Falta 'to'")

    # Enviar confirmación al cliente
    await wa.send_text(to, prompts.confirm_template.format(summary=resumen))

    # Generar archivo TXT y subir/guardar
    content = (resumen + "\n").encode("utf-8")
    filename = f"{prompts.file_prefix}-{settings.ENV_NAME}.txt"
    file_ref = drive.upload_bytes(filename, content)

    # Aviso al dueño (si configurado)
    if settings.OWNER_PHONE:
        await wa.send_text(settings.OWNER_PHONE, f"Nuevo pedido de {to}: {filename} ({file_ref})")

    return {"file": file_ref}


# --- Simulación local sin Meta ---
@app.post("/simulate/message")
async def simulate(payload: dict):
    to = payload.get("to", settings.OWNER_PHONE or "54911XXXXXXX")
    text = payload.get("text", "Hola, probando bot")
    return await wa.send_text(to, text)