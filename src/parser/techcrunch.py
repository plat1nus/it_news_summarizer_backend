import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Определение класса DateTimeEncoder для сериализации объекта datetime в JSON
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Класс для представления новости
class News:
    def __init__(self, source, sourceLink, title, summary, timestamp):
        self.source = source
        self.sourceLink = sourceLink
        self.title = title
        self.summary = summary
        self.timestamp = timestamp

    def jsonify(self):
        data = {
            'source': self.source,
            'sourceLink': self.sourceLink,
            'title': self.title,
            'summary': self.summary,
            'timestamp': self.timestamp
        }
        return data

def get_article_text_and_time(article_url):
    response = requests.get(article_url)
    if response.status_code == 200:
        article_soup = BeautifulSoup(response.text, 'html.parser')
        # Подбираем правильный селектор для тела статьи
        article_body = article_soup.find('div', {'class': 'entry-content'})
        if article_body:
            paragraphs = article_body.find_all('p')
            article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        else:
            article_text = "No article body found"
        
        # Находим время публикации на странице статьи
        time_tag = article_soup.find('time')
        if time_tag and time_tag.has_attr('datetime'):
            pub_time_str = time_tag['datetime']
            # Преобразуем временную метку в объект datetime
            pub_time = datetime.fromisoformat(pub_time_str)
        else:
            pub_time = None
        
        return article_text, pub_time
    else:
        return "Failed to retrieve article", None
    

def parse_techcrunch():

    # URL главной страницы TechCrunch
    url = 'https://techcrunch.com/'

    # Отправляем запрос к странице
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Находим все элементы, содержащие новости
    articles = soup.find_all('article')
    
    news_list = []

    # Проходим по каждому элементу
    for article in articles:
        # Находим заголовок новости и ссылку на новость
        title_tag = article.find('h2')
        if title_tag and title_tag.a:
            title_text = title_tag.get_text(strip=True)
            link_url = title_tag.a['href']
        else:
            continue  # Пропускаем новости без заголовка
        
        # Получаем полный текст статьи и время публикации
        if link_url != "No link":
            article_text, pub_time = get_article_text_and_time(link_url)
        else:
            article_text, pub_time = "No article text", None
        
        # Создаем объект News и добавляем его в список
        news_item = News(source="TechCrunch", sourceLink=link_url, title=title_text, summary=article_text, timestamp=pub_time)
        news_list.append(news_item.jsonify())
    
    # Выводим массив новостей в формате JSON
    news_json = json.dumps(news_list, cls=DateTimeEncoder, indent=2)
    return news_json
