from pydantic_settings import BaseSettings


class DevelopConfig(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    REDIS_URL: str
    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    class Config:
        env_file = ".env"
        from_attribute = True


settings = DevelopConfig()
