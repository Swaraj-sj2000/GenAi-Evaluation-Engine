#app/Config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "GenAI Eval Engine"
    database_url: str
    secret_key: str
    debug: bool = False
    google_api_key: str
    huggingfacehub_api_key: str
    langchain_api_key: str
    langchain_tracing_v2: str = "true"
    langchain_project: str = "eval-engine"
    class Config:
        env_file=".env"

setting=Settings()

