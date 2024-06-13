import os
import json
import pathlib

from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
from apscheduler.schedulers.background import BackgroundScheduler
import atexit


from data.db_session import create_session, global_init
from data.managers import NewsManager

from parser.parser import Parser 
from data.models import News
from summarizer.summarizer import Summarizer

load_dotenv()
catalogue = os.getenv('CATALOGUE', 'invalidcatalogue')
api_key = os.getenv('API_KEY', 'invalidapikey')
print(catalogue, api_key)
BASE_DIR = pathlib.Path(__file__).parent
global_init('data/local_database.sqlite3')
app = Flask(__name__)
news_manager = NewsManager()
summarizer = Summarizer(catalogue, api_key)
duplicate_filter = DuplicateFilter()
model = SentenceTransformer('all-distilroberta-v1')
parse = Parser(Summarizer)


def scheduled_parser():
    parse.parse_news()
    parse.process_news()
    db_session = create_session()
    try:
        parse.upload_news_to_database(db_session)
        
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"[ERROR] :: {e}")
    finally:
        db_session.close()


scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_parser, trigger="interval", seconds=30)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


@app.route('/api/v1/recent_news')
def api_recent_news():
    print('[INFO] :: New request')
    db_session = create_session()
    parser = Parser(summarizer=summarizer, duplicate_filter=duplicate_filter)
    parser.parse_news()
    parser.process_news(model=model, db_session=db_session)
    parser.upload_news_to_database(db_session)
    recent_news = news_manager.get_recent_news(db_session, limit=20)
    
    return Response(
        mimetype='application/json',
        response=json.dumps([it.serialize() for it in recent_news]),
        status=200,
    )


@app.route('/api/v1/archive_news')
def api_archive_news():
    print('[INFO] :: New request')
    db_session = create_session()
    parser = Parser(summarizer=summarizer, duplicate_filter=duplicate_filter)
    parser.parse_news()
    parser.process_news(model=model, db_session=db_session)
    parser.upload_news_to_database(db_session)
    archive_news = news_manager.get_archive_news(db_session)

    return Response(
        mimetype='application/json',
        response=json.dumps([it.serialize() for it in archive_news]),
        status=200
    )


def main():
    app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
