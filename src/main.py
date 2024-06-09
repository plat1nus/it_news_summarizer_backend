import pathlib

from flask import Blueprint, Flask, request

from data.managers import NewsManager

BASE_DIR = pathlib.Path(__file__).parent
app = Flask(__name__)
api_blueprint = Blueprint('api/v1', __name__)
news_manager = NewsManager()

@app.route('/recent_news')
def all_news():
    pass