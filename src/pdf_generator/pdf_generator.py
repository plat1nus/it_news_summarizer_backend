from pathlib import Path
import os
import sys
from typing import List

sys.path.append("..")

import pdfkit

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
    <h1>Новостной дайджест</h1>
'''


class PDFGenerator:
    @staticmethod
    def generate(news_list: List[News]) -> bytes:

        template = BASE_TEMPLATE[::]

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
