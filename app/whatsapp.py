# app/whatsapp.py
import httpx
from typing import Any

class WhatsAppClient:
    def __init__(self, phone_number_id: str, access_token: str, api_version: str = "v24.0", send_enabled: bool = False):
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.api_version = api_version
        self.send_enabled = send_enabled
        self.base_url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    async def send_text(self, to: str, text: str) -> dict[str, Any]:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,  # debe ser E164 SIN '+', ej: 5491176207054
            "type": "text",
            "text": {"body": text}
        }
        if not self.send_enabled:
            return {"dry_run": True, "payload": payload}

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(self.base_url, headers=self.headers, json=payload)
            if r.status_code >= 400:
                try:
                    err = r.json()
                except Exception:
                    err = {"raw": r.text}
                print("[WA SEND ERROR]", err)  # <-- esto nos dirá exactamente por qué falla
                # devolvémoslo sin tirar excepción, así el endpoint no explota
                return {"error": True, "status_code": r.status_code, "details": err, "payload": payload}
            return r.json()
