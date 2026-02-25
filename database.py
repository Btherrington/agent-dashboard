from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///agent_dashboard.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Commit(Base):
    __tablename__ = "commits"
    id = Column(String, primary_key=True)
    repo = Column(String)
    message = Column(String)
    date = Column(DateTime)


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(String, primary_key=True)
    handle = Column(String)
    text = Column(String)
    date = Column(DateTime)


def init_db():
    Base.metadata.create_all(bind=engine)