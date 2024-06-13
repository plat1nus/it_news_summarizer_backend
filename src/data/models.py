from datetime import datetime
from pathlib import Path

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)
    sourceLink = Column(String, nullable=False)
    title = Column(String(128), nullable=False)
    summary = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    timestamp_parse = Column(DateTime, default=datetime.now)
    is_competitor = Column(Boolean, default=False)
    tags = Column(String(128), nullable=True)
    power = Column(Float, default=0.0)

    def __repr__(self) -> str:
        return f'<News> {self.id}'

    def __word_counter(self, article_text: str) -> int:
        words = article_text.split()
        num_words = len(words)

        return num_words

    def __keyword_counter(self, text: str):
        NORMAL_WEIGHT = 1
        HIGH_WEIGHT = 30
        HIGH_WEIGHT_KEYWORDS_FILENAME = f'{Path(__file__).parent}/keywords/high_weight_keywords.txt'
        NORMAL_WEIGHT_KEYWORDS_FILENAME = f'{Path(__file__).parent}/keywords/normal_weight_keywords.txt'

        with open(NORMAL_WEIGHT_KEYWORDS_FILENAME, 'r', encoding='utf-8') as file:
            keywordslist = [line.strip() for line in file]

        with open(HIGH_WEIGHT_KEYWORDS_FILENAME, 'r', encoding='utf-8') as file:
            topkeywordslist = [line.strip() for line in file]
        
        weight = 0

        words = text.split()
        for word in words:
            if word in keywordslist:
                weight += NORMAL_WEIGHT
            if word in topkeywordslist:
                weight += HIGH_WEIGHT
        
        return weight
    
    def calculate_power(self) -> float:
        I = self.__word_counter(article_text=self.summary)
        W = self.__keyword_counter(text=self.summary)
        N = self.__keyword_counter(text=self.title)

        power = (I ** 2 / W) * (2 ** N)
        self.power = power
        print(self.title, power)
        return power


    def serialize(self) -> dict[str, str]:
        data = {
            'source': self.source,
            'sourceLink': self.sourceLink,
            'title': self.title,
            'summary': self.summary,
            'timestamp': self.timestamp.isoformat()
        }
        return data
