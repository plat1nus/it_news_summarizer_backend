from datetime import date, timedelta
import sys
from typing import List

sys.path.append("..")

from data.models import News

BASE_TEMPLATE = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>News Report</title>
    <style>
        body {
            font-family: 'DejaVuSans', sans-serif;
        }
        h1 {
            text-align: center;
            margin-bottom: 12px;
        }
        .news {
            margin-bottom: 20px;
        }
        .news-title {
            font-weight: bold;
            font-size: 16px;
            text-decoration: underline;
            color: blue;
        }
        .news-summary {
            font-size: 14px;
        }
        .news-source {
            font-size: 12px;
        }
        .news-timestamp {
            font-style: italic;
            font-size: 12px;
        }
    </style>
    </head>
    <body>
    <div id="reportbox">
'''


def get_closest_past_monday() -> date:
    date_today = date.today()
    for _ in range(8):
        if date_today.weekday() == 0:
            return date_today
        date_today -= timedelta(days=1)
    raise ValueError('[ERROR] :: No mondays in previous 8 days')


def format_date(dt: date) -> str:
    return f'{dt.day:02}.{dt.month:02}.{dt.year:04}'


class PDFGenerator:
    ''' PDFGenerator is used to generate html template for news digest '''
    
    @staticmethod
    def generate(news_list: List[News]) -> bytes:
        end = get_closest_past_monday()
        start = end - timedelta(days=7)

        template = BASE_TEMPLATE[::]

        template += (
            f'''
            <h1>Новостной дайджест {format_date(start)} - {format_date(end)}<br></h1>
            '''
        )

        for news in news_list:
            template += f'''
                <div class="news">
                    <div class="news-title"><a href="{news.sourceLink}">{news.title}</a></div>
                    <div class="news-summary"><br>{news.summary}</div>
                    <div class="news-source"><br>Источник: {news.source}</div>
                    <div class="news-timestamp">Опубликовано: {news.timestamp.strftime('%Y-%m-%d %H:%M:%S')}<br></div>
                </div>
            '''
            
        template += (
            '''
                </div>
                </body>
                </html>
            '''
        )
        
        return template.encode()
