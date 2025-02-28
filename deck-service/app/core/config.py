from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001


class ServicesConfig(BaseModel):
    profiles_url: str = "http://0.0.0.0:8000/"


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    services: ServicesConfig = ServicesConfig()


settings = Settings()
