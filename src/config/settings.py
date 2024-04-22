from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    db_host: str
