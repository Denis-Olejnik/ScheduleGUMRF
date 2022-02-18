# This file contains global variables
from environs import Env
env = Env()
env.read_env()

DEBUG_MODE = env.bool("DEBUG_MODE")
RUN_LOCAL = env.bool("RUN_LOCAL")

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
TELEGRAM_ADMINS = env.list("TELEGRAM_ADMINS")

WEBHOOK_PATH = env.str("WEBHOOK_PATH")

POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.str("POSTGRES_PORT")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_URI = env.str("POSTGRES_URI") or f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" \
                                          f"{POSTGRES_PORT}/{POSTGRES_DB}"
