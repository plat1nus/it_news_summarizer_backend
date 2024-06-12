import sys
from datetime import datetime
from typing import List
from weasyprint import HTML

sys.path.append("..")
sys.path.append("../parser")

from data.models import News
from parser.parser import Parser
from summarizer.summarizer import Summarizer


class PDF_generator:
    @staticmethod
    def generate(news_list: List[News], filename: str):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>News Report</title>
            <style>
                body {{
                    font-family: 'DejaVuSans', sans-serif;
                }}
                h1 {{
                    text-align: center;
                }}
                .news {{
                    margin-bottom: 20px;
                }}
                .news-title {{
                    font-weight: bold;
                    font-size: 16px;
                }}
                .news-summary {{
                    font-size: 12px;
                }}
                .news-source {{
                    color: blue;
                }}
                .news-timestamp {{
                    font-style: italic;
                }}
            </style>
        </head>
        <body>
            <h1>News Report</h1>
        """

        for news in news_list:
            html_content += f"""
            <div class="news">
                <div class="news-title">{news.title}</div>
                <div class="news-summary">{news.summary}</div>
                <div class="news-source"><a href="{news.sourceLink}">{news.source}</a></div>
                <div class="news-timestamp">Parsed: {news.timestamp_parse.strftime('%Y-%m-%d %H:%M:%S')}</div>
                <div class="news-timestamp">Published: {news.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
            """

        html_content += """
        </body>
        </html>
        """

        # Генерация PDF из HTML
        HTML(string=html_content).write_pdf(filename)


if __name__ == "__main__":
    parse = Parser(Summarizer)
    parse.parse_news()
    PDF_generator.generate(parse.news, 'test.pdf')
