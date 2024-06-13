from io import BytesIO
import os
import json
import pathlib

from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from dotenv import load_dotenv
from flask import Flask, Response, send_file
from flask_cors import CORS

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
PARSER_SPAN_12_HOURS_IN_SECONDS = 60 * 60 * 12

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
scheduler.add_job(func=scheduled_parser, trigger="interval", seconds=PARSER_SPAN_12_HOURS_IN_SECONDS)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@app.route('/api/v1/pdf_recent')
def api_recent_pdf():
    print('[INFO] :: New request')
    db_session = create_session()
    digest_news = news_manager.get_digest(db_session)
    pdf = pdfgenerator.generate(digest_news)
    bytesio = BytesIO(pdf)
    return send_file(bytesio, as_attachment=True, download_name='fresh_digest.pdf')


@app.route('/api/v1/pdf_archive')
def api_archive_pdf():
    print('[INFO] :: New request')
    db_session = create_session()
    all_news = news_manager.get_archive_news(db_session=db_session)[:10]
    pdf = pdfgenerator.generate(all_news)
    bytesio = BytesIO(pdf)
    return send_file(bytesio, as_attachment=True, download_name='archive_digest.pdf')


@app.route('/api/v1/recent_news')
def api_recent_news():
    print('[INFO] :: New request')
    db_session = create_session()
    recent_news = news_manager.get_digest(db_session)
    
    return Response(
        mimetype='application/json',
        response=json.dumps([it.serialize() for it in recent_news]),
        status=200,
    )


@app.route('/api/v1/archive_news')
def api_archive_news():
    print('[INFO] :: New request')
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
