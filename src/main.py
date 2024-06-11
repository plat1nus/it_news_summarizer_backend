import json
import pathlib

from flask import Flask, Response
from flask_cors import CORS

from data.db_session import create_session, global_init
from data.managers import NewsManager
from parser.parser import Parser
from summarizer.summarizer import Summarizer

BASE_DIR = pathlib.Path(__file__).parent
global_init('data/local_database.sqlite3')
app = Flask(__name__)
CORS(app)
news_manager = NewsManager()
summarizer = Summarizer()


@app.route('/api/v1/recent_news')
def api_recent_news():
    db_session = create_session()
    parser = Parser(summarizer=summarizer)
    parser.parse_news()
    parser.process_news()
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
    parser = Parser(summarizer=summarizer)
    parser.parse_news()
    parser.process_news()
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
