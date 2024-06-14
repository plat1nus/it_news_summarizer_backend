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

    article = soup.find_all(class_='box-paragraph__text')

    result = ''
    for p in article:
        text = p.get_text(strip=True)
        if len(text) > 0 and not text.isspace():
            result += '\n' + text 

    return result

def parse_vedomosti() -> List[News]:
    news_list = []

    req = requests.get('https://www.vedomosti.ru/technologies')
    req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    other_news = soup.find_all('div', class_='card-article')
    for new in other_news:
        title_tag = new.find('a')
        if title_tag:
            title = title_tag.get_text(strip=True)
            href = 'https://www.vedomosti.ru' + title_tag['href']

            time_tag = new.find('time', {'class': 'card-article__date'})
            if time_tag:
                pub_time_str = time_tag.get_text(strip=True)
                pub_date = dateparser.parse(pub_time_str)
                pub_time = datetime.combine(pub_date, datetime.min.time())

            text = get_text(href)
            
            news_item = News(source="Vedomosti", sourceLink=href, title=title, summary=text, timestamp=pub_time)
            news_list.append(news_item)
        break

        

    return news_list
res = parse_vedomosti()
print(len(res))
for new in parse_vedomosti():
    print(new.title, new.timestamp, new.summary)