from sqlmodel import create_engine
from sqlmodel import Session
class Settings():
    DATABASE_URL: str = "sqlite:///./database.db"  # ou PostgreSQL: postgresql+psycopg://user:pass@localhost/dbname

    class Config:
        env_file = ".env"

settings = Settings()


engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)


