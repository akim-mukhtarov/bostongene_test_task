from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str
    celery_broker_url: str
    celery_result_backend_url: str
    logfile: str


settings = Settings()
