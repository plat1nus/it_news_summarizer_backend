from time import time
from typing import List

import sys 
sys.path.append("..")

from summarizer.summarizer import Summarizer

from .rbc import parse_rbc 
from .cnews import parse_cnews
from data.models import News
from .interfax import parse_interfax
from .techcrunch import parse_techcrunch
from .severstal import parse_severstal

from sqlalchemy.orm import Session


class Parser:
    def __init__(self, summarizer: Summarizer) -> None:
        self.summarizer = summarizer
        self.news = []

    def parse_news(self):
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

        techcrunch_news = parse_techcrunch()
        print('techcrunch', time() - now)
        result.extend(techcrunch_news)

        # severstal_news = parse_severstal()
        # print('severstal', time() - now)
        # result.extend(severstal_news)

        print(f'[INFO] :: Parsed {len(result)} news')
        self.news = result

    def upload_news_to_database(self, db_session: Session) -> None:
        db_session.bulk_save_objects(self.news)
        db_session.commit()

    def process_news(self) -> None:
        for i in range(len(self.news)):
            self.news[i].summary = self.summarizer.summarize(self.news[i].summary)
            print(self.news[i])

    

if __name__ == '__main__':
    parse = Parser(Summarizer)
    parse.parse_news()
