from datetime import date, timedelta
from io import BytesIO
import json
import os
import pathlib

from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from dotenv import load_dotenv
from flask import Flask, Response, send_file
from flask_cors import CORS
# from sentence_transformers import SentenceTransformer

from data.db_session import create_session, global_init
from data.managers import NewsManager
from data.models import News
from duplicate_filter.duplicate_filter import DuplicateFilter
from parser.parser import Parser
from pdf_generator.pdf_generator import PDFGenerator
from summarizer.summarizer import Summarizer

# ===
# Backend Setup
# ===
BASE_DIR = pathlib.Path(__file__).parent
PARSER_SPAN_12_HOURS_IN_SECONDS = 30

# model = SentenceTransformer('all-distilroberta-v1')

load_dotenv()
catalogue = os.getenv('CATALOGUE', 'invalidcatalogue')
api_key = os.getenv('API_KEY', 'invalidapikey')

global_init(f'{BASE_DIR}/data/local_database.sqlite3')
app = Flask(__name__)
CORS(app)

summarizer = Summarizer(catalogue, api_key)
news_manager = NewsManager()
duplicate_filter = DuplicateFilter()
parsing_job_runner = Parser(summarizer=summarizer, duplicate_filter=duplicate_filter)
pdfgenerator = PDFGenerator()


def scheduled_parser():
    db_session = create_session()
    parsing_job_runner.parse_news()
    # parsing_job_runner.process_news(model, db_session=db_session)
    parsing_job_runner.process_news(db_session=db_session)
    db_session = create_session()
    try:
        parsing_job_runner.upload_news_to_database(db_session)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"[ERROR] :: {e}")
    finally:
        db_session.close()


scheduler = BackgroundScheduler()

# For DEBUG
scheduler.add_job(func=scheduled_parser, trigger="interval", seconds=60 * 10)

# FOR PRODUCTION
# scheduler.add_job(func=scheduled_parser, trigger="interval", seconds=PARSER_SPAN_12_HOURS_IN_SECONDS)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


def get_closest_past_monday() -> date:
    date_today = date.today()
    for _ in range(8):
        if date_today.weekday() == 0:
            return date_today
        date_today -= timedelta(days=1)
    raise ValueError('[ERROR] :: No mondays in previous 8 days')


def format_date(dt: date) -> str:
    return f'{dt.day:02}.{dt.month:02}.{dt.year:04}'


@app.route('/api/v1/pdf_recent')
def api_recent_pdf():
    print('[INFO] :: Request for recent PDF')
    end = get_closest_past_monday()
    start = end - timedelta(days=7)
    pdf_title = f'НЛМК. Новостной дайджест {format_date(start)} - {format_date(end)}'
    db_session = create_session()
    digest_news = news_manager.get_digest(db_session)
    pdf = pdfgenerator.generate(news_list=digest_news, title=pdf_title)
    bytesio = BytesIO(pdf)
    return send_file(bytesio, as_attachment=True, download_name='fresh_digest.pdf')


@app.route('/api/v1/pdf_archive')
def api_archive_pdf():
    print('[INFO] :: Request for archive PDF')
    pdf_title = 'НЛМК. Архив новостей'
    db_session = create_session()
    all_news = news_manager.get_archive_news(db_session=db_session)[:10]
    pdf = pdfgenerator.generate(news_list=all_news, title=pdf_title)
    bytesio = BytesIO(pdf)
    return send_file(bytesio, as_attachment=True, download_name='archive_digest.pdf')


@app.route('/api/v1/recent_news')
def api_recent_news():
    print('[INFO] :: Request recent news')
    db_session = create_session()
    recent_news = news_manager.get_digest(db_session)
    
    return Response(
        mimetype='application/json',
        response=json.dumps([it.serialize() for it in recent_news]),
        status=200,
    )


@app.route('/api/v1/archive_news')
def api_archive_news():
    print('[INFO] :: Request archive news')
    db_session = create_session()
    archive_news = news_manager.get_archive_news(db_session)

    return Response(
        mimetype='application/json',
        response=json.dumps([it.serialize() for it in archive_news]),
        status=200
    )


def main():
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
