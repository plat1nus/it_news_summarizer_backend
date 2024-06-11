from datetime import datetime
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from data.models import News


def get_article_text_and_time(article_url: str) -> Tuple[str, datetime]:
    response = requests.get(article_url)
    if response.status_code == 200:
        article_soup = BeautifulSoup(response.text, 'html.parser')
        article_body = article_soup.find('div', {'class': 'entry-content'})
        if article_body:
            paragraphs = article_body.find_all('p')
            article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        else:
            article_text = "No article body found"

        time_tag = article_soup.find('time')
        if time_tag and time_tag.has_attr('datetime'):
            pub_time_str = time_tag['datetime']
            pub_time = datetime.fromisoformat(pub_time_str)
        else:
            pub_time = None
        
        return article_text, pub_time
    else:
        return "Failed to retrieve article", None
    

def parse_techcrunch() -> List[News]:
    url = 'https://techcrunch.com/'
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    
    news_list = []

    for article in articles:
        title_tag = article.find('h2')
        if title_tag and title_tag.a:
            title_text = title_tag.get_text(strip=True)
            link_url = title_tag.a['href']
        else:
            continue
        
        if link_url != "No link":
            article_text, pub_time = get_article_text_and_time(link_url)
        else:
            article_text, pub_time = "No article text", None
        
        news_item = News(source="TechCrunch", sourceLink=link_url, title=title_text, summary=article_text, timestamp=pub_time)
        news_list.append(news_item)
    
    return news_list
