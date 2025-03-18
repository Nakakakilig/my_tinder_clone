from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8002


class ApiPrefix(BaseModel):
    swipes: str = "/swipes"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class KafkaConfig(BaseModel):
    bootstrap_servers: str = "localhost:9092"
    swipe_topic: str = "swipe-events"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "swipe-service/.env.template",
            "swipe-service/.env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    kafka: KafkaConfig = KafkaConfig()


settings = Settings()
