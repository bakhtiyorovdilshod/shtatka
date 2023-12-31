import secrets, os, databases

import sqlalchemy
from pydantic import BaseSettings


class MainSettings(BaseSettings):
    DATABASE_NAME: str = os.environ.get('DATABASE_NAME', 'shtatka_db')
    DATABASE_USER: str = os.environ.get('DATABASE_USER', 'shtatka_user')
    DATABASE_PASSWORD: str = os.environ.get('DATABASE_PASSWORD', 'shtatka_user_password')
    DATABASE_HOST: str = os.environ.get('DATABASE_HOST', 'localhost')
    DATABASE_PORT: str = os.environ.get('DATABASE_PORT', '5432')
    PROJECT_NAME: str = 'SHTATKA'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    VERSION: str = '1.0.0'
    DATABASE_URL: str = os.environ.get('DATABASE_URL', f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}')
    ACCESS_TOKEN_EXPIRE_DAY: int = 70
    ALGORITHM: str = "HS256"


settings = MainSettings()
database = databases.Database(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData()



