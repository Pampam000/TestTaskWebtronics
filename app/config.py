import os

from dotenv import load_dotenv

load_dotenv()

# Database
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTRGES_HOST = os.getenv('POSTRGES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
               f'{POSTRGES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# Encrypting
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_IN_SECONDS = 60 * 10

