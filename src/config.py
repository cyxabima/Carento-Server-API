from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ADMIN_NAME: str
    ADMIN_PANEL_PASSWORD: str
    DB_URI: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "validate_default": True,
    }


# or we can use modelConfigDict from Pydantic_settings instead of simple dict

Config = Settings()
