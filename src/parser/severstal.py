import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    req = requests.get(url, headers=headers, timeout=10, verify=False)
    req.encoding = 'utf-8'  # Устанавливаем правильную кодировку
    html = req.text

    soup = BeautifulSoup(html, "html.parser")

    articles = soup.find_all(class_='typography-content news-detail__content')

    result = ''
    pub_time = None

    # Извлечение времени публикации
    time_tag = soup.find('time', {'class': 'article__header__date'})
    if time_tag and time_tag.has_attr('datetime'):
        pub_time_str = time_tag['datetime']
        pub_time = datetime.fromisoformat(pub_time_str)

    for div in articles:
        text = div.get_text(strip=True)  # Получить текст без начальных и конечных пробелов
        if len(text) > 0 and not text.isspace():  # Игнорировать элементы, состоящие только из пробелов
            result += '\n' + text 
    return result, pub_time

def parse_serverstal():
    news_list = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = 'https://www.severstal.com/rus/media/news/'
    
    try:
        req = requests.get(url, headers=headers, timeout=10, verify=False)
        req.encoding = 'utf-8'  # Устанавливаем правильную кодировку
        html = req.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return json.dumps(news_list, cls=DateTimeEncoder, ensure_ascii=False, indent=2)

    soup = BeautifulSoup(html, "html.parser")

    news = soup.find_all(class_='news-list__wrapper-items')

    for new in news:
        links = new.find_all('a', class_='news-list-card')
        for link in links:
            # print(type(link))
            title = link.find(class_='h-3 news-list-card__title').text
            href = link['href']
            if not href.startswith('https://'):
                href = 'https://www.severstal.com/' + href

            # Попытка извлечь дату из ссылки
            date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', href)
            if date_match:
                pub_date = datetime.strptime(f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}", "%Y-%m-%d")
                pub_time = datetime.combine(pub_date, datetime.min.time())
            else:
                pub_time = None

            # Удаление даты из заголовка
            title = re.sub(r'\d{2}\.\d{2}\.\d{4}', '', title).strip()

            try:
                text, content_pub_time = get_new_text_time(href)
                if not pub_time:
                    pub_time = content_pub_time if content_pub_time else datetime.combine(datetime.today(), datetime.min.time())
            except requests.exceptions.RequestException as e:
                print(f"Error fetching the URL {href}: {e}")
                continue

            # Создаем объект News и добавляем его в список
            news_item = News(source="Severstal", sourceLink=href, title=title, summary=text, timestamp=pub_time)
            news_list.append(news_item.jsonify())

    # Возвращаем массив новостей в формате JSON
    return json.dumps(news_list, cls=DateTimeEncoder, ensure_ascii=False, indent=2)

# Пример вызова функции
if __name__ == "__main__":
    news_json = parse_serverstal()
    print(news_json)
