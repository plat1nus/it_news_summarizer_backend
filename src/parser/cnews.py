from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup
import dateparser
import requests

from data.models import News


def get_cnews_news_text_and_time(article_url: str) -> Tuple[str, datetime]:
    req = requests.get(article_url)
    req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    article_body = soup.find('article', {'class': 'news_container'})
    result = ''
    pub_time = None

    time_tag = soup.find('time', {'class': 'article-date-desktop'})
    if time_tag:
        pub_time_str = time_tag.get_text(strip=True)
        pub_time = dateparser.parse(pub_time_str)

    if article_body:
        paragraphs = article_body.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 0 and not text.isspace():
                result += '\n' + text 
    return result, pub_time


def parse_cnews() -> List[News]:
    news_list = []

    req = requests.get('https://www.cnews.ru')
    req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    other_news = soup.find_all('a', class_='black')

    for new in other_news:
        title = new.text.strip()
        href = new['href']
        if not href.startswith('https'):
            href = 'https://www.cnews.ru' + href
        text, pub_time = get_cnews_news_text_and_time(href)

        news_item = News(source="CNews", sourceLink=href, title=title, summary=text, timestamp=pub_time)
        news_list.append(news_item)

    return news_list
