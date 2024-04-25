from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    db_host: str

    jwt_secret_key: str


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file='./src/.env')
