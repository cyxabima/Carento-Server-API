from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URI: str
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "validate_default": True,
    }


# or we can use modelConfigDict from Pydantic_settings instead of simple dict

Config = Settings()
