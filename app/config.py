from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    redis_url: str = "redis://redis:6379/0"
    deribit_url: str = "https://www.deribit.com/api/v2"

    class Config:
        env_file = ".env"

settings = Settings()