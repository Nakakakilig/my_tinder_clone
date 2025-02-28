from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    decks: str = "/decks"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001


class ServicesConfig(BaseModel):
    profiles_url: str = "http://0.0.0.0:8000/"


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    services: ServicesConfig = ServicesConfig()


settings = Settings()
