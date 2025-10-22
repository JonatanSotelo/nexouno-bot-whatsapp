from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    # General
    ENV_NAME: str = Field("dev", description="Nombre del entorno/tenant")
    PROMPTS_FILE: str = Field("config/prompts_cliente_a.yml", description="Ruta a YAML de prompts")
    SEND_ENABLED: bool = Field(False, description="Si False, no envía a WhatsApp/Drive (modo simulación)")

    # WhatsApp Cloud API
    WA_PHONE_NUMBER_ID: str = ""
    WA_ACCESS_TOKEN: str = ""
    WA_VERIFY_TOKEN: str = "changeme-verify" # para el webhook GET verify
    WA_API_VERSION: str = "v21.0"

    # Dueño/avisos
    OWNER_NAME: str = "Duenio"
    OWNER_PHONE: str = "" # en formato internacional, ej: 54911XXXXXXX

    # Google Drive (Service Account)
    DRIVE_ENABLED: bool = False
    DRIVE_FOLDER_ID: str = "" # carpeta destino
    GOOGLE_APPLICATION_CREDENTIALS: str = "" # ruta al JSON de SA

    model_config = SettingsConfigDict(env_file=None, extra='ignore')




def load_settings(env_file: str | None = None) -> Settings:
    from dotenv import load_dotenv
    if env_file:
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)
    return Settings()