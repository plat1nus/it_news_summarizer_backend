from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session, Query

from .models import News


class NewsManager:
    def __get_data(
        self,
        db_session: Session,
    ) -> Query:
        return db_session.query(News)

    def __get_sorted_news(
        self,
        db_session: Session,
    ) -> Query[News]:
        return db_session.query(News).order_by(News.power.desc(), News.timestamp.desc())

    def get_recent_news(
        self,
        db_session: Session,
        limit: int | None = None,
    ) -> List[News]:
        if limit is None:
            return self.__get_sorted_news(db_session).all()
        else:
            return self.__get_sorted_news(db_session).limit(limit).all()

    def __get_closest_past_monday(self) -> datetime:
        dtnow = datetime.now()
        for _ in range(8):
            if dtnow.weekday() == 0:
                return datetime.combine(date=dtnow.date(), time=datetime.min)
            dtnow = dtnow - timedelta(days=1)
        raise ValueError('[ERROR] :: No monday in the past 8 days')

    def get_archive_news(
        self,
        db_session: Session,
    ) -> List[News]:
        return (
            self
                .__get_sorted_news(db_session)
                # .filter(News.timestamp < datetime.now() - timedelta(days=30))
            ).all()
    
    def get_digest(
        self,
        db_session: Session,
    ) -> List[News]:
        current_monday = self.__get_closest_past_monday()
        prev_monday = current_monday - timedelta(days=7)

        return (
            self.__get_data(db_session)
                .filter(News.timestamp_parse >= prev_monday, News.timestamp_parse <= current_monday)
                .order_by(News.power.desc(), News.timestamp.desc())
                .all()
        )