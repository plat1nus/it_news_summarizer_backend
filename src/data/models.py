import json
from datetime import datetime, date
from json import JSONEncoder

from sqlalchemy import Column, Integer, String, DateTime

from .db_session import SqlAlchemyBase


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()


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

    def jsonify(self) -> dict[str, str]:
        dt_encoder = DateTimeEncoder()
        data = {
            'source': self.source,
            'sourceLink': self.sourceLink,
            'title': self.title,
            'summary': self.summary,
            'timestamp': self.timestamp
        }

        jsonified = json.dumps(data, cls=dt_encoder)
        return jsonified
