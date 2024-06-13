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
                .filter(News.timestamp > datetime.now() - timedelta(days=30))
            )
    
    def get_last_week_news(
        self, 
        db_session: Session
    ) -> List[News]:
        timenow = datetime.now()
        for i in range(7):
            timedayago = timenow - timedelta(days=i)
            if timedayago.weekday() == 0:
                current_monday = datetime.combine(timedayago.date(), datetime.min.time())

        previous_monday= datetime.combine((current_monday - timedelta(days=7)).date(), datetime.min.time())

        return (
            self
                .__get_all_data(db_session)
                .filter(News.timestamp <= current_monday, News.timestamp >= previous_monday).all()
            )
                    

    def get_pdf(
            self, 
            db_session: Session 
    ) -> None:
        pass 
    