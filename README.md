# NexoUno – Bot WhatsApp (MVP)

Proyecto listo para deploy en **DigitalOcean App Platform** y/o Docker.

## Entrypoint FastAPI
Detectado: **bot-whatsapp/app/main.py** → `bot-whatsapp.app.main:app`

## Variables de entorno (.env / App Platform)
Ver `.env.example`. No subas tu `.env` al repo.

## Ejecutar local
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Deploy en DigitalOcean App Platform (Buildpack Python)
1. Subí el repo a GitHub.
2. Create App → Source: GitHub repo.
3. Detecta Python. El **Procfile** define el comando de arranque.
4. Cargá en **Environment Variables** todas las claves de `.env.example`.
5. Deploy.

## Deploy con Docker (opcional)
```bash
docker build -t nexouno-bot .
docker run -p 8000:8000 --env-file .env nexouno-bot
```

## Webhook
- Callback URL: `https://bots.tu-dominio.com.ar/webhook`
- Verify Token: `WA_VERIFY_TOKEN`
- Suscripciones: `messages`, `message_template_status_update`.
