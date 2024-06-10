from http import HTTPStatus
import pathlib

from flask import Blueprint, Flask

from data.db_session import create_session, global_init
from data.managers import NewsManager

BASE_DIR = pathlib.Path(__file__).parent
global_init(db_file=f'{BASE_DIR}/local_db/local.sqlite3')
app = Flask(__name__)
api_blueprint = Blueprint('api/v1', __name__)
app.register_blueprint(api_blueprint)
news_manager = NewsManager()


@api_blueprint.route('/recent_news')
def api_recent_news():
    db_session = create_session()
    recent_news = news_manager.get_recent_news(db_session, limit=20)
    jsonified = [it.jsonify() for it in recent_news]
    return jsonified, HTTPStatus.OK


@api_blueprint.route('/archive_news')
def api_archive_news():
    db_session = create_session()
    archive_news = news_manager.get_archive_news(db_session)
    jsonified = [it.jsonify() for it in archive_news]
    return jsonified, HTTPStatus.OK


def main():
    app.run(host='127.0.0.1', port=8080, debug=True)


if __name__ == '__main__':
    main()
