from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Awesome API'
    app_version: str = '0.1.0'
    database_name: str = 'database.db'
    tdx_app_id: str = ''
    tdx_app_key: str = ''
    tdx_auth_url: str = (
        'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
    )
    tdx_api_url: str = ''
    smtp_host: str = 'smtp.gmail.com'
    smtp_port: int = 587
    smtp_username: str = ''
    smtp_password: str = ''

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache
def get_settings() -> Settings:
    return Settings()
