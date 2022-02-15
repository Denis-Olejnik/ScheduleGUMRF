# Read data from .env file:

from environs import Env

env = Env()
env.read_env()

# Database
# DB_HOST = env.str("DB_HOST")
# DB_PORT = env.str("DB_PORT")
# DB_NAME = env.str("DB_NAME")
# DB_USER = env.str("DB_USER")
# DB_PASS = env.str("DB_PASS")


# Heroku
# HOOK_URL = env.str("HOOK_URL")
HOOK_URL = "https://schedule-gumrf.herokuapp.com/"

# Telegram
TG_TOKEN = env.str("TG_TOKEN")
