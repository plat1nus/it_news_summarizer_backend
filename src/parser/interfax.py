import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import dateparser

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

def get_new_text_time(url):
    req = requests.get(url)
    # req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    # article = soup.find('div', {'class': 'textM'})
    result = ''
    pub_time = None

    # Извлечение времени публикации
    time_tag = soup.find('time')
    if time_tag and time_tag.has_attr('datetime'):
        pub_time_str = time_tag['datetime']
        pub_time = datetime.fromisoformat(pub_time_str)

    # if article:
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > 0 and not text.isspace():
            result += '\n' + text 

    return result, pub_time

def parse_interfax():
    news_list = []

    base_url = 'https://www.interfax.ru/digital/'
    req = requests.get(base_url)
    # req.encoding = 'utf-8'
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

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
            text, pub_time = get_new_text_time(href)
            
            # Создаем объект News и добавляем его в список
            news_item = News(source="Interfax", sourceLink=href, title=title, summary=text, timestamp=pub_time)
            news_list.append(news_item.jsonify())

    # Возвращаем массив новостей в формате JSON
    return json.dumps(news_list, cls=DateTimeEncoder, ensure_ascii=False, indent=2)

# Пример вызова функции

if __name__ == "__main__":
    news_json = parse_interfax()

