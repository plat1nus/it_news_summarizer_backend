from datetime import datetime
from typing import List, Tuple
import re

from bs4 import BeautifulSoup
import requests
import urllib3
import warnings

from data.models import News

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.simplefilter('ignore', urllib3.exceptions.InsecureRequestWarning)


def get_new_text_time(article_url: str) -> Tuple[str, datetime]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req = requests.get(article_url, headers=headers, timeout=10, verify=False)
    req.encoding = 'utf-8'
    html = req.text

    bs_reader = BeautifulSoup(html, 'html.parser')

    articles = bs_reader.find_all(class_='typography-content news-detail__content')

    result = ''
    pub_time = None

    time_tag = bs_reader.find('time', {'class': 'article__header__date'})
    if time_tag and time_tag.has_attr('datetime'):
        pub_time_str = time_tag['datetime']
        pub_time = datetime.fromisoformat(pub_time_str)

    for div in articles:
        text = div.get_text(strip=True)
        if len(text) > 0 and not text.isspace():
            result += '\n' + text 
    return result, pub_time


def parse_severstal() -> List[News]:
    news_list = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = 'https://www.severstal.com/rus/media/news/'
    
    try:
        req = requests.get(url, headers=headers, timeout=10, verify=False)
        req.encoding = 'utf-8'
        html = req.text
    except requests.exceptions.RequestException as e:
        print(f'Error fetching the URL {url}: {e}')
        return []

    soup = BeautifulSoup(html, "html.parser")

    news = soup.find_all(class_='news-list__wrapper-items')

    for new in news:
        links = new.find_all('a', class_='news-list-card')
        for link in links:
            title = link.find(class_='h-3 news-list-card__title').text.strip()
            href = link['href']
            if not href.startswith('https://'):
                href = 'https://www.severstal.com/' + href

            date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', href)
            if date_match:
                pub_date = datetime.strptime(f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}", "%Y-%m-%d")
                pub_time = datetime.combine(pub_date, datetime.min.time())
            else:
                pub_time = None

            title = re.sub(r'\d{2}\.\d{2}\.\d{4}', '', title).strip()

            try:
                text, content_pub_time = get_new_text_time(href)
                if not pub_time:
                    pub_time = content_pub_time if content_pub_time else datetime.combine(datetime.today(), datetime.min.time())
            except requests.exceptions.RequestException as e:
                print(f'Error fetching the URL {href}: {e}')
                continue

            news_item = News(source="Северсталь", sourceLink=href, title=title, summary=text, timestamp=pub_time)
            news_list.append(news_item)

    return news_list
