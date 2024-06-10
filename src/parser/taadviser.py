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

def get_tadviser_news_text_and_time(url):
    req = requests.get(url)
    req.encoding = 'utf-8'  # Устанавливаем правильную кодировку
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    article_body = soup.find('div', {'class': 'b-content-inner'})
    result = ''
    pub_time = None

    # Извлечение времени публикации
    time_tag = soup.find('time')
    if time_tag and time_tag.has_attr('datetime'):
        pub_time_str = time_tag['datetime']
        pub_time = datetime.fromisoformat(pub_time_str)

    if article_body:
        paragraphs = article_body.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)  # Получить текст без начальных и конечных пробелов
            if len(text) > 0 and not text.isspace():  # Игнорировать элементы, состоящие только из пробелов
                result += '\n' + text 
    return result, pub_time

def parse_tadviser():
    news_list = []

    req = requests.get('https://www.tadviser.ru/index.php/News')
    req.encoding = 'utf-8'  # Устанавливаем правильную кодировку
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    other_news = soup.find_all('div', class_='news-item')
    for new in other_news:
        title_tag = new.find('a')
        title = title_tag.text.strip()
        link = title_tag['href']
        if not link.startswith('https'):
            link = 'https://www.tadviser.ru' + link
        text, pub_time = get_tadviser_news_text_and_time(link)
        
        # Создаем объект News и добавляем его в список
        news_item = News(source="TAdviser", sourceLink=link, title=title, summary=text, timestamp=pub_time)
        news_list.append(news_item.jsonify())

    # Возвращаем массив новостей в формате JSON
    return json.dumps(news_list, cls=DateTimeEncoder, ensure_ascii=False, indent=2)

# Пример вызова функции
news_json = parse_tadviser()
print(news_json)
