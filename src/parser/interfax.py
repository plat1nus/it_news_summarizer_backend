from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup
import requests

from data.models import News


def get_new_text_time(article_url: str) -> Tuple[str, datetime]:
    req = requests.get(article_url)
    req.encoding = 'windows-1251'
    html = req.text
    
    bs_reader = BeautifulSoup(html, 'html.parser')

    result = ''
    pub_time = None

    time_tag = bs_reader.find('time')
    if time_tag and time_tag.has_attr('datetime'):
        pub_time_str = time_tag['datetime']
        pub_time = datetime.fromisoformat(pub_time_str)

    paragraphs = bs_reader.find_all('p')
    for paragraph in paragraphs:
        text = paragraph.get_text(strip=True)
        if len(text) > 0 and not text.isspace():
            result += '\n' + text 

    return result, pub_time


def parse_interfax() -> List[News]:
    news_list = []

    base_url = 'https://www.interfax.ru/digital/'
    req = requests.get(base_url)
    req.encoding = 'windows-1251'
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    other_news = soup.find_all(class_='mainblock')

    for new in other_news:
        links = new.find_all("a")
        for link in links:
            if 'class' in link.attrs:
                continue
            title = link.text.strip()
            href = link['href']
            if not href.startswith('https://'):
                href = 'https://www.interfax.ru' + href
            text, pub_time = get_new_text_time(article_url=href)
            
            news_item = News(source="Интерфакс", sourceLink=href, title=title, summary=text, timestamp=pub_time)
            news_list.append(news_item)

    return news_list
