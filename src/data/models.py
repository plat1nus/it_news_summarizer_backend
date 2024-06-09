from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)
    sourceLink = Column(String, nullable=False)
    title = Column(String(128), nullable=False)
    summary = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f'<News> {self.id}'
