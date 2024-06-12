import sys
from datetime import datetime
from typing import List
from pyhtml2pdf import converter

sys.path.append("..")
sys.path.append("../parser")

from data.models import News
from parser.parser import Parser
from summarizer.summarizer import Summarizer

class PDF_generator:
    @staticmethod
    def generate(news_list: List[News], filename: str) -> None:
        # Сначала сохраняем HTML-контент в отдельный файл
        html_filename = "output.html"
        with open(html_filename, "w", encoding="utf-8") as html_file:
            html_file.write("""
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
                    }
                    .news-summary {
                        font-size: 12px;
                    }
                    .news-source {
                        color: blue;
                    }
                    .news-timestamp {
                        font-style: italic;
                    }
                </style>
            </head>
            <body>
                <h1>News Report</h1>
            """)
            
            for news in news_list:
                html_file.write(f"""
                <div class="news">
                    <div class="news-title">{news.title}</div>
                    <div class="news-summary">{news.summary}</div>
                    <div class="news-source"><a href="{news.sourceLink}">{news.source}</a></div>
                    <div class="news-timestamp">Published: {news.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</div>
                </div>
                """)
            
            html_file.write("""
            </body>
            </html>
            """)
        
        # Теперь конвертируем HTML в PDF из файла
        converter.convert(html_filename, filename)


def test():
    parse = Parser(Summarizer)
    parse.parse_news()
    parse.process_news()
    PDF_generator.generate(parse.news, 'test.pdf')
