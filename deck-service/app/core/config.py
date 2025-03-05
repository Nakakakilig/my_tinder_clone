from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    decks: str = "/decks"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001


class ProfileServicesConfig(BaseModel):
    profiles_base_url: str = "http://0.0.0.0:8000/api/profiles"
    limit_matched_profiles: int = 10

    def get_all_profiles_url(self) -> str:
        return f"{self.profiles_base_url}/get-all"

    def get_profile_url(self, profile_id: int) -> str:
        return f"{self.profiles_base_url}/{profile_id}"

    def get_matching_profiles_url(self, profile_id: int) -> str:
        return f"{self.profiles_base_url}/{profile_id}/matches"


class PreferenceServicesConfig(BaseModel):
    preferences_base_url: str = "http://0.0.0.0:8000/api/preferences"

    def get_all_preferences_url(self) -> str:
        return f"{self.preferences_base_url}/get-all"

    def get_preference_url(self, preference_id: int) -> str:
        return f"{self.preferences_base_url}/{preference_id}"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


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
    profile_service: ProfileServicesConfig = ProfileServicesConfig()
    preference_service: PreferenceServicesConfig = PreferenceServicesConfig()
    db: DatabaseConfig


settings = Settings()
