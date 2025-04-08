from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    users: str = "/users"
    profiles: str = "/profiles"
    preferences: str = "/preferences"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class KafkaConfig(BaseModel):
    # bootstrap_servers: str = "kafka:9092"
    bootstrap_servers: str = "localhost:9092"
    profile_topic: str = "profile-events"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "profile-service/.env.template",
            "profile-service/.env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    kafka: KafkaConfig = KafkaConfig()


settings = Settings()  # type: ignore
