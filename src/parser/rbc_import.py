import sys
sys.path.append("..")

from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup
import requests

from data.models import News


def get_rbc_news_text_and_time(article_url: str) -> Tuple[str, datetime]:
    req = requests.get(article_url)
    req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    articles = soup.find_all(class_='article__text article__text_free')

    result = ''
    pub_time = None

    time_tag = soup.find('time', {'class': 'article__header__date'})
    if time_tag and time_tag.has_attr('datetime'):
        pub_time_str = time_tag['datetime']
        pub_time = datetime.fromisoformat(pub_time_str)

    for div in articles:
        paragraphs = div.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 0 and not text.isspace():
                result += '\n' + text 
    return result, pub_time


def parse_rbc() -> List[News]:
    news_list = []

    req = requests.get('https://www.rbc.ru/tags/?tag=%D0%98%D0%BC%D0%BF%D0%BE%D1%80%D1%82%D0%BE%D0%B7%D0%B0%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D0%B5')
    req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    other_news = soup.find_all('div', class_='search__inner')

    print(other_news)

    for new in other_news:
        a = new.find('a')
        title = new.text.strip()
        link = a['href']
        text, pub_time = get_rbc_news_text_and_time(link)
        
        news_item = News(source="РБК", sourceLink=link, title=title, summary=text, timestamp=pub_time)
        news_list.append(news_item)

    return news_list


if __name__ == "__main__":
    print(parse_rbc())
