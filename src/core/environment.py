import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Environment:

    MT5_LOGIN = os.getenv("MT5_LOGIN")
    MT5_PASSWORD = os.getenv("MT5_PASSWORD")
    MT5_SERVER = os.getenv("MT5_SERVER")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")


env = Environment()