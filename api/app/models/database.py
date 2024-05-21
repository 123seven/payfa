from datetime import datetime

from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_DSN,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BaseModel(DeclarativeBase):
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, onupdate=datetime.now, default=datetime.now
    )

    def to_dict(self, include=None, exclude=None):
        """
        Convert model instance to dictionary, with options to include or exclude specific fields.

        :param include: List of fields to include. If specified, only these fields will be included.
        :param exclude: List of fields to exclude. These fields will be excluded from the result.
        :return: Dictionary representation of the model instance.
        """
        if include is not None:
            include = set(include)
        if exclude is not None:
            exclude = set(exclude)

        result = {}
        for c in self.__table__.columns:
            if (include is not None and c.name not in include) or (
                exclude is not None and c.name in exclude
            ):
                continue
            result[c.name] = getattr(self, c.name)
        return result


def create_db_and_tables():
    BaseModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_session_maker():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
