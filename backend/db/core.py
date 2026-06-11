from sqlmodel import create_engine
from sqlmodel import Session
from os import environ
from dotenv import load_dotenv
load_dotenv()

class Settings():
    DATABASE_URL: str = environ["URL_BANK"] # ou PostgreSQL: postgresql+psycopg://user:pass@localhost/dbname

    class Config:
        env_file = ".env"

settings = Settings()


engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)


