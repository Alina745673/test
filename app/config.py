from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_CLIENT_ID: str
    ACCESS_KEY: str
    SECRET_ACCESS_KEY: str
    USER_POOL_NAME: str
    USER_POOL_ID: str
    REGION: str
    CLIENT_SECRET: str
    ADMIN_USER_PASSWORD: str
    ADMIN_USER_USERNAME: str
    ADMIN_USER_EMAIL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
