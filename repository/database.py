import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL environment variable is not set!")
    exit(1)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)  # echo=False to disable SQL logs

Base = declarative_base()

# Create a session factory
SessionFactory = sessionmaker(bind=engine)

# Create a scoped session (ensures each thread gets its own session)
DBSession = scoped_session(SessionFactory)


def create_tables():
    if not database_exists(engine.url):
        try:
            create_database(engine.url)
        except Exception as e:
            print("Could not connect to ", DATABASE_URL, e)
            exit(1)

        print("Connected to ", DATABASE_URL)
    Base.metadata.create_all(engine)
