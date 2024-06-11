from datetime import datetime, timedelta
from typing import List

from flask import jsonify
from sqlalchemy.orm import Session, Query

from .models import News


class NewsManager:
    def __get_all_data(
        self,
        db_session: Session,
    ) -> Query[News]:
        return db_session.query(News).order_by(News.timestamp.desc())

    def get_recent_news(
        self,
        db_session: Session,
        limit: int | None = None,
    ) -> List[News]:
        if limit is None:
            return self.__get_all_data(db_session).all()
        else:
            return self.__get_all_data(db_session).limit(limit).all()
    
    def get_archive_news(
        self,
        db_session: Session,
    ) -> List[News]:
        return (
            self
                .__get_all_data(db_session)
                .filter(News.timestamp < datetime.now() - timedelta(days=30))
            ).all()
    