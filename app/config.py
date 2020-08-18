import logging
import sys
from typing import List

from databases import DatabaseURL
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

config = Config('.env')

WEB_PREFIX = ''
API_PREFIX = '/api'

VERSION = '1.0.0'

DEBUG: bool = config('DEBUG', cast=bool, default=False)
DATABASE_URL: DatabaseURL = config('DB_CONNECTION', cast=DatabaseURL)
SECRET_KEY: Secret = config('SECRET_KEY', cast=Secret)

PROJECT_NAME: str = config(
    'PROJECT_NAME', default=
    'Simple insurance - FastAPI / Tortoise ORM / PostgreSQL / Docker'
)
ALLOWED_HOSTS: List[str] = config(
    'ALLOWED_HOSTS', cast=CommaSeparatedStrings, default=''
)

# logging configuration

LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logger.configure(handlers=[
    {
        'sink': sys.stderr,
        'level': LOGGING_LEVEL
    }
])
