from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    #Security
    SECRET_KEY: str
    ALGORITHM:  str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    #Database
    DATABASE_URL: str = "sqlite:///.app/database.bd"

    #Limits
    MAX_LETERS_ADMIN: int = 1000000
    MAX_LETERS_USER:  int = 1000
    
    model_config = SettingsConfigDict(
        env_file          = os.getenv("ENV_FILE", ".env"),
        env_file_encoding = "utf-8",
        case_sensitive    = True,
        extra             = "ignore"
    )

settings = Settings()