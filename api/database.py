"""database.py"""

from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, text, DateTime

USERNAME = "root"
PASSWORD = "Abdallah%402004"
HOST = "localhost"
DATABASE = "note_db"

# Base = declarative_base()

class Base(DeclarativeBase):
    """Base class for all models"""


class UserDb(Base):
    """This class represents the user table in the database."""
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    session_id = Column(String(40), default=None)
    time_created = Column(DateTime, default=datetime.now)
    last_opened = Column(DateTime, default=datetime.now)
    date_of_birth = Column(Text, default=None)
    profile_image = Column(Text, default=None)


class NoteDb(Base):
    """This class represents the note table in the database."""
    __tablename__ = 'notes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(100))
    content = Column(Text, nullable=False)
    time_created = Column(DateTime)
    time_edition = Column(DateTime)


engine_without_db = create_engine(f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/')
engine = create_engine(f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}')

SessionLocal = sessionmaker(bind=engine)

def create_database():
    """Creates the database schema."""
    with engine_without_db.connect() as connection:
        connection.execute(
            text(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        )
    print("Database 'note_db' created or already exists.")

def create_tables():
    """Creates the tables in the database schema"""
    Base.metadata.create_all(engine)
    print("Tables created or already exist.")

def drop_db():
    """Drops the database and all tables in it"""
    with engine.connect() as connection:
        connection.execute(
            text(f"DROP DATABASE IF EXISTS {DATABASE}")
        )
    print("Database 'note_db' dropped.")

def get_db():
    """Return a new session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
