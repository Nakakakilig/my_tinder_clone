from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    decks: str = "/decks"
    profiles: str = "/profiles"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001


class DeckConfig(BaseModel):
    limit_matched_profiles: int = 15


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


class RedisConfig(BaseModel):
    url: str
    expire: int = 3600


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "deck-service/.env.template",
            "deck-service/.env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    deck: DeckConfig = DeckConfig()
    db: DatabaseConfig
    kafka: KafkaConfig = KafkaConfig()
    redis: RedisConfig


settings = Settings()
