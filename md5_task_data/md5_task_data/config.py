from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str


settings = Settings()

