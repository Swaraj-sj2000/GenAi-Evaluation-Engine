#app/Config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "GenAI Eval Engine"
    database_url: str
    secret_key: str
    debug: bool = False
    class Config:
        env_file=".env"

setting=Settings()

