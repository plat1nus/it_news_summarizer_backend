import sys 
sys.path.append("..")

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


def parse_main_news(soup: BeautifulSoup, news_list: List[News]) -> List[News]:
    top_news = soup.find(class_='newstoplist')

    main_news = top_news.find(class_='ntl-content')
    title_main_news = main_news.text
    href_main_news = main_news['href']
    text, pub_time = get_cnews_news_text_and_time(href_main_news)
    news_list.append(News(source="CNews corp", sourceLink=href_main_news, title=title_main_news, summary=text, timestamp=pub_time))

    other_news = top_news.find('ul')

    for a in other_news.find_all('a'):
        href = a['href']
        title = a.text

        text, pub_time = get_cnews_news_text_and_time(href)
        news_list.append(News(source="CNews corp", sourceLink=href, title=title, summary=text, timestamp=pub_time))

    return news_list 

def parse_other_news(soup: BeautifulSoup, news_list: List[News]) -> List[News]:
    other_news = soup.find(class_='newslist')

    all_other_news = other_news.find_all({'data-test': 'test1'})

    for new in all_other_news:
        current_new = new.find('a', class_='black')
        title = current_new.text 
        href = current_new['href']
        
        text, pub_time = get_cnews_news_text_and_time(href)

        news_list.append(News(source="CNews corp", sourceLink=href, title=title, summary=text, timestamp=pub_time))
    
    return news_list



def parse_cnewscorp(url) -> List[News]:
    news_list = []

    req = requests.get(url)
    req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    parse_main_news(soup, news_list=news_list)
    parse_other_news(soup, news_list)

    return news_list


def test() -> None: 
    for new in parse_cnewscorp('https://www.cnews.ru/'):
        print(new.timestamp, new.title, new.summary)


if __name__ == "__main__":
    test()