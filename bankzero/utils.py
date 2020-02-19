from bankzero.models import DeclarativeBase

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bankzero import config


def get_db_url():
    return f"postgresql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"


def get_connection():
    db_url = get_db_url()
    connection = create_engine(db_url, pool_size=5, pool_pre_ping=True)
    return connection


Session = sessionmaker(bind=get_connection())


@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_tables():
    # Create all the tables in the database which are
    # defined by DeclarativeBase subclasses
    engine = get_connection()
    DeclarativeBase.metadata.create_all(engine)
