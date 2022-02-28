import os
from dotenv import load_dotenv

load_dotenv()

DEBUG_MODE = os.environ.get("DEBUG_MODE").lower() in ['true', 't', '+', '1']
RUN_LOCAL = os.environ.get("RUN_LOCAL").lower() in ['true', 't', '+', '1']
SAVE_TO_DB = os.environ.get("SAVE_TO_DB").lower() in ['true', 't', '+', '1']

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_ADMINS = os.environ.get("TELEGRAM_ADMINS").split(',')
TELEGRAM_NOTIFY_ADMIN = os.environ.get("TELEGRAM_NOTIFY_ADMIN").lower() in ['true', 't', '+', '1']
TELEGRAM_ONLY_ALLOWED = os.environ.get("TELEGRAM_ONLY_ALLOWED").lower() in ['true', 't', '+', '1']
TELEGRAM_ALLOWED_USERS = os.environ.get("TELEGRAM_ALLOWED_USERS").split(',')

WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH")

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
DATABASE_URL = os.environ.get("DATABASE_URL") or f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" \
                                          f"{POSTGRES_PORT}/{POSTGRES_DB}"
