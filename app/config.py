#app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "GenAI Eval Engine"
    database_url: str
    secret_key: str
    debug: bool = False
    google_api_key: str
    huggingfacehub_api_key: str
    langchain_api_key: str
    langchain_tracing_v2: str = "true"
    langchain_project: str = "eval-engine"
    redis_url: str=Field(alias="REDIS_URL")
  

setting=Settings()

