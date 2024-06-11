from time import time
from typing import List

from rbc import parse_rbc 
from cnews import parse_cnews
from data.models import News
from interfax import parse_interfax
from techcrunch import parse_techcrunch
from severstal import parse_severstal


class Parser:
    def parse_news(self) -> List[News]:
        now = time()
        rbc_news = parse_rbc()
        print('rbc', time() - now)
        interfax_news = parse_interfax()
        print('interfax', time() - now)
        # cnews_news = parse_cnews()
        # print('cnews', time() - now)
        techcrunch_news = parse_techcrunch()
        print('techcrunch', time() - now)
        severstal_news = parse_severstal()
        print('severstal', time() - now)
        
        result = rbc_news + interfax_news + techcrunch_news + severstal_news
        print(f'[INFO] :: Parsed {len(result)} news')
        return result
