from time import time

import sys 
sys.path.append("..")

# from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session

from summarizer.summarizer import Summarizer
from duplicate_filter.duplicate_filter import DuplicateFilter

from .rbc import parse_rbc 
from .cnews import parse_cnews
from data.models import News
from .interfax import parse_interfax
from .techcrunch import parse_techcrunch
from .severstal import parse_severstal
from .tadviser import parse_tadviser
from .kommersant import parse_kommersant

class Parser:
    ''' Aggregator of all parsing functions. Used to gather all news together and process them '''

    def __init__(self, summarizer: Summarizer, duplicate_filter: DuplicateFilter) -> None:
        self.__duplicate_filter = duplicate_filter
        self.__summarizer = summarizer
        self.__news = []

    def parse_news(self) -> None:
        """
        cnews default, corp & import are parcing by one file because of similar html structure
        """
        result = []
        now = time()
        
        rbc_news = parse_rbc()
        print('rbc', time() - now)
        result.extend(rbc_news)

        km_news = parse_kommersant()
        print('kommersant', time() - now)
        result.extend(km_news)

        interfax_news = parse_interfax()
        print('interfax', time() - now)
        result.extend(interfax_news)

        cnews_news = parse_cnews('https://www.cnews.ru/')
        print('cnews', time() - now)
        result.extend(cnews_news)

        cnewscorp_news = parse_cnews('https://corp.cnews.ru/')
        print('cnews corp', time() - now)
        result.extend(cnewscorp_news)

        cnews_import = parse_cnews('https://importfree.cnews.ru/')
        print('cnews import', time() - now)
        result.extend(cnews_import)

        tadviser_news = parse_tadviser()
        print('tadviser', time() - now)
        result.extend(tadviser_news)

        severstal_news = parse_severstal()
        print('severstal', time() - now)
        result.extend(severstal_news)

        # TODO: If techcrunch necessary, uncomment
        # techcrunch_news = parse_techcrunch()
        # print('techcrunch', time() - now)
        # result.extend(techcrunch_news)

        # TODO: Fix parsing errors

        print(f'[INFO] :: Parsed {len(result)} news')
        self.__news = result

    def upload_news_to_database(self, db_session: Session) -> None:
        db_session.bulk_save_objects(self.__news)
        db_session.commit()
        print(f'[INFO] :: Added {len(self.__news)} news to DB')

    def process_news(self, db_session: Session, threshold: float = 0.2, limit: int = 5) -> None:
        self.__news = self.__duplicate_filter.clear_duplicates(parsed_news=self.__news, db_session=db_session)
        # self.__news = self.__duplicate_filter.clear_duplicates(parsed_news=self.__news, db_session=db_session)
        self.__news = [news for news in self.__news if news.calculate_power() >= threshold]
        self.__news.sort(key=lambda news: news.calculate_power(), reverse=True)
        self.__news = self.__news[:limit]

        for i in range(len(self.__news)):
            self.__news[i].summary = self.__summarizer.summarize(self.__news[i].summary)
