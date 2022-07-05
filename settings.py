import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
DB_URL = os.environ.get("DB_URL")


SECRET = os.environ.get("SECRET")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
API_AUDIENCE = os.environ.get("API_AUDIENCE")
ALGORITHMS = os.environ.get("ALGORITHMS")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")


CASTING_ASSISTANT_TOKEN = os.environ.get("CASTING_ASSISTANT_TOKEN")
CASTING_DIRECTOR_TOKEN = os.environ.get("CASTING_DIRECTOR_TOKEN")
EXECUTIVE_PRODUCER_TOKEN = os.environ.get("EXECUTIVE_PRODUCER_TOKEN")
