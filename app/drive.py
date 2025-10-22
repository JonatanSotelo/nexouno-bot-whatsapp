from pathlib import Path
from datetime import datetime
from typing import Optional


try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
except Exception: # paquetes opcionales
    build = None
    service_account = None


class DriveClient:
    def __init__(self, enabled: bool, folder_id: str, creds_path: str):
        self.enabled = enabled
        self.folder_id = folder_id
        self.creds_path = creds_path
        self._svc = None


    def _service(self):
        if not self.enabled:
            return None
        if self._svc is None:
            if service_account is None or build is None:
                raise RuntimeError("google-api-python-client no instalado")
            scopes = ["https://www.googleapis.com/auth/drive.file"]
            creds = service_account.Credentials.from_service_account_file(self.creds_path, scopes=scopes)
            self._svc = build("drive", "v3", credentials=creds)
        return self._svc


    def upload_bytes(self, filename: str, content: bytes) -> str:
        if not self.enabled:
            # Guardar localmente en outbox
            Path("outbox").mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            p = Path("outbox") / f"{ts}-{filename}"
            p.write_bytes(content)
            return str(p)

        from googleapiclient.http import MediaInMemoryUpload
        svc = self._service()
        file_metadata = {"name": filename, "parents": [self.folder_id]} if self.folder_id else {"name": filename}
        media = MediaInMemoryUpload(content, mimetype="text/plain", resumable=False)
        file = svc.files().create(body=file_metadata, media_body=media, fields="id, name").execute()
        return f"drive_file_id:{file.get('id')}"