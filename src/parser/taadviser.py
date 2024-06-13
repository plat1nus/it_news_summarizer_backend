import sys 
sys.path.append("..")

import requests
from bs4 import BeautifulSoup
import dateparser

from data.models import News 


def get_tadviser_news_text_and_time(url):
    req = requests.get(url)
    req.encoding = 'utf-8'  
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    pub_time = None

    time_tag = soup.find(class_='data_timer')
    if time_tag:
        pub_time_str = time_tag.get_text(strip=True)
        pub_time = dateparser.parse(pub_time_str)

    article_body = soup.find('div', {'class': 'pub_body'})
    result = ''

    if article_body:
        paragraphs = article_body.find_all('p')
        for p in paragraphs:
            text = p.text.strip()
            if len(text) > 0 and not text.isspace():  # Игнорировать элементы, состоящие только из пробелов
                result += '\n' + text 

    return result, pub_time

def parse_tadviser():
    news_list = []

    req = requests.get('https://www.tadviser.ru/index.php/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8')
    req.encoding = 'utf-8' 
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    other_news = soup.find('div', class_='news_body')
    all_news = other_news.find_all('a', class_='bold')
    for new in all_news:
        title = new.text.strip()
        href = new['href']
        href = 'https://www.tadviser.ru' + href
        text, pub_time = get_tadviser_news_text_and_time(href)

        news_item = News(source="TAdviser", sourceLink=href, title=title, summary=text, timestamp=pub_time)
        news_list.append(news_item)

    return news_list


def test():
    news = parse_tadviser()
    for new in news:
        print(new.summary)


if __name__ == "__main__":
    test()


