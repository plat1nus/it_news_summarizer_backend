from time import time

import sys 
sys.path.append("..")

from summarizer.summarizer import Summarizer
from duplicate_filter.duplicate_filter import DuplicateFilter

from .rbc import parse_rbc 
from .cnews import parse_cnews
from data.models import News
from .interfax import parse_interfax
from .techcrunch import parse_techcrunch
from .severstal import parse_severstal

from sqlalchemy.orm import Session


class Parser:
    def __init__(self, summarizer: Summarizer, duplicate_filter: DuplicateFilter) -> None:
        self.__duplicate_filter = duplicate_filter
        self.__summarizer = summarizer
        self.__news = []

    def parse_news(self) -> None:
        result = []
        now = time()
        rbc_news = parse_rbc()
        print('rbc', time() - now)
        result.extend(rbc_news)

        # interfax_news = parse_interfax()
        # print('interfax', time() - now)
        # result.extend(interfax_news)

        # cnews_news = parse_cnews()
        # print('cnews', time() - now)
        # result.extend(cnews_news)

        # techcrunch_news = parse_techcrunch()
        # print('techcrunch', time() - now)
        # result.extend(techcrunch_news)

        # TODO: Fix parsing errors
        # severstal_news = parse_severstal()
        # print('severstal', time() - now)
        # result.extend(severstal_news)

        print(f'[INFO] :: Parsed {len(result)} news')
        self.__news = result

    def upload_news_to_database(self, db_session: Session) -> None:
        db_session.bulk_save_objects(self.__news)
        db_session.commit()
        print(f'[INFO] :: Added {len(self.__news)} news to DB')

    def process_news(self, db_session: Session) -> None:
        db_news = db_session.query(News).all()
        self.__news = self.__duplicate_filter.clear_duplicates(db_news=db_news, parsed_news=self.__news)

        for i in range(len(self.__news)):
            self.__news[i].summary = self.__summarizer.summarize(self.__news[i].summary)
