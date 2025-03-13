import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATA_STORAGE_PATH: str = os.environ.get("DATA_STORAGE_PATH", "data/storage")
    CONFIG_STORAGE_PATH: str = os.environ.get("CONFIG_STORAGE_PATH", "data/configs")
    WIZARD_STAGES_CONFIG_PATH: str = os.environ.get("WIZARD_STAGES_CONFIG_PATH", "data/wizard_stages")
    LOG_FILE: str = os.environ.get("LOG_FILE", "logs/logfile.txt")
    EXCEPTION_FILE: str = os.environ.get("EXCEPTION_FILE", "logs/exceptions.txt")
    LINNWORKS_API_URL: str = os.environ.get("LINNWORKS_API_URL", "https://api.linnworks.net/api")
    APPLICATION_ID: str = os.environ.get("APPLICATION_ID", "a483413e-2aae-4468-9ba2-5682dcac6228")
    APPLICATION_SECRET: str = os.environ.get("APPLICATION_SECRET", "ad6255be-fdba-47c5-b0db-d476bd31c419")

    class Config:
        env_file = ".env"

settings = Settings()

# Create directories if they don't exist
os.makedirs(settings.DATA_STORAGE_PATH, exist_ok=True)
os.makedirs(settings.CONFIG_STORAGE_PATH, exist_ok=True)
os.makedirs(settings.WIZARD_STAGES_CONFIG_PATH, exist_ok=True)
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(settings.EXCEPTION_FILE), exist_ok=True)