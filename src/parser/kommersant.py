import sys
sys.path.append("..")

from datetime import datetime
from typing import List, Tuple
import dateparser

from bs4 import BeautifulSoup
import requests

from data.models import News


def get_text(article_url: str) -> str:
    req = requests.get(article_url)
    req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    article = soup.find(class_='article_text_wrapper js-search-mark')

    result = ''

    paragraphs = article.find_all('p')
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > 0 and not text.isspace():
            result += '\n' + text 

    return result


def parse_km() -> List[News]:
    news_list = []

    req = requests.get('https://www.kommersant.ru/theme/2903')
    req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    other_news = soup.find_all('article', class_='uho rubric_lenta__item js-article')

    for new in other_news:
        title = new.find('span', class_='vam').text.strip()
        href = 'https://www.kommersant.ru' + new.find('a')['href']

        time_tag = new.find('p', {'class': 'uho__tag rubric_lenta__item_tag hide_mobile'})
        if time_tag:
            pub_time_str = time_tag.get_text(strip=True)
            pub_time = dateparser.parse(pub_time_str)
        text = get_text(href)
        
        news_item = News(source="Kommersant", sourceLink=href, title=title, summary=text, timestamp=pub_time)
        news_list.append(news_item)

    return news_list


for new in parse_km():
    print(new.title, new.timestamp, new.summary)
    break