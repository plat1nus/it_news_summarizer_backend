from http import HTTPStatus
import pathlib

from flask import Blueprint, Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from data.db_session import create_session, global_init
from data.managers import NewsManager

from parser.parser import Parser 
from data.models import News
from summarizer.summarizer import Summarizer

BASE_DIR = pathlib.Path(__file__).parent
global_init('data/local_database.sqlite3')
app = Flask(__name__)
news_manager = NewsManager()
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
        print(f"Ошибка при добавлении новостей в базу данных: {e}")
    finally:
        db_session.close()


scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_parser, trigger="interval", seconds=30)
scheduler.start()

# Закрываем планировщик при завершении работы
atexit.register(lambda: scheduler.shutdown())


@app.route('/api/v1/ping')
def ping():
    return '', HTTPStatus.OK


@app.route('/api/v1/recent_news')
def api_recent_news():
    db_session = create_session()
    recent_news = news_manager.get_recent_news(db_session, limit=20)
    jsonified = [it.jsonify() for it in recent_news]
    return jsonified, HTTPStatus.OK


@app.route('/api/v1/archive_news')
def api_archive_news():
    db_session = create_session()
    archive_news = news_manager.get_archive_news(db_session)
    jsonified = [it.jsonify() for it in archive_news]
    return jsonified, HTTPStatus.OK


def main():
    app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
