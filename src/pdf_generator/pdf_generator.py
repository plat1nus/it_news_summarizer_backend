from datetime import date, timedelta
import sys
from typing import List

sys.path.append("..")

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
            font-family: 'Montserrat', sans-serif;
        }
        h1 {
            text-align: center;
            margin-bottom: 12px;
        }
        .news {
            margin-bottom: 20px;
        }
        .news-title {
            color: #3636b3;
            font-weight: semibold;
            font-size: 16px;
            color: "";
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
        hr {
            background-color: rgba(99, 98, 94, 0.6);
            border: none;
            height: 2px;
            margin-top: 5px;
            margin-bottom: 10px;
        }
        .svg {
            display: flex;
            justify-content: center;
        }
    </style>
    </head>
    <body>
    <div id="reportbox">
    <div class="svg">
        <svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="60pt" height="60pt" viewBox="0 0 400.000000 400.000000" preserveAspectRatio="xMidYMid meet">
        <g transform="translate(0.000000,400.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none">
        <path d="M1845 3994 c-694 -57 -1307 -468 -1625 -1088 -150 -293 -214 -564
        -214 -906 0 -342 64 -613 214 -906 295 -576 830 -963 1480 -1070 145 -24 455
        -24 600 0 268 44 533 140 740 269 508 317 839 814 937 1407 23 145 23 455 0
        600 -51 304 -158 577 -326 823 -313 460 -795 764 -1346 852 -99 16 -365 27
        -460 19z m528 -1200 c703 -78 1137 -382 1137 -794 0 -160 -58 -290 -189 -420
        -258 -259 -708 -392 -1321 -392 -441 0 -756 61 -1045 201 -194 95 -326 211
        -398 349 -148 283 -46 595 260 799 341 226 943 326 1556 257z"/>
        <path d="M1690 2719 c-631 -59 -1049 -305 -1101 -649 -37 -238 111 -463 400
        -610 128 -65 354 -129 564 -161 172 -26 532 -36 717 -20 668 58 1086 297 1141
        651 57 368 -297 664 -911 764 -218 35 -576 46 -810 25z m735 -78 c534 -80 858
        -284 907 -569 38 -221 -95 -422 -367 -559 -133 -68 -346 -127 -570 -160 -170
        -24 -620 -24 -790 0 -383 56 -646 163 -806 328 -210 217 -177 516 78 707 198
        150 492 240 893 276 119 11 529 -4 655 -23z"/>
        <path d="M1788 2640 c-404 -30 -710 -123 -908 -275 -145 -112 -218 -274 -191
        -426 30 -175 144 -301 366 -410 236 -114 551 -172 945 -172 394 0 709 58 945
        172 221 108 336 236 366 410 14 74 1 158 -35 237 -107 234 -454 399 -951 453
        -137 15 -406 21 -537 11z m-708 -463 l0 -94 75 0 75 0 0 94 0 93 80 0 80 0 -2
        -257 -3 -258 -75 0 -75 0 -3 102 -3 101 -74 0 -74 0 -3 -101 -3 -102 -75 0
        -75 0 -3 258 -2 257 80 0 80 0 0 -93z m848 -164 l-3 -258 -75 0 -75 0 -3 193
        -2 192 -43 0 -42 0 3 -75 c10 -223 -52 -321 -198 -313 l-55 3 -3 67 -3 66 37
        -1 c60 -2 64 12 64 210 l0 173 200 0 200 0 -2 -257z m317 117 c21 -77 39 -140
        41 -140 2 0 12 30 23 68 11 37 29 100 41 140 l21 72 79 0 c57 0 80 -4 80 -12
        1 -7 16 -121 35 -253 18 -132 30 -244 26 -248 -5 -4 -37 -7 -72 -5 l-64 3 -8
        35 c-4 19 -13 76 -20 125 l-12 90 -34 -115 c-18 -63 -38 -121 -43 -127 -12
        -15 -94 -18 -103 -4 -3 6 -19 56 -36 113 -16 57 -33 110 -36 118 -3 8 -13 -41
        -22 -110 l-16 -125 -72 -3 c-65 -3 -73 -1 -73 15 0 23 60 474 65 491 3 8 29
        12 83 12 l78 0 39 -140z m563 41 l3 -94 66 96 67 97 83 0 c46 0 83 -3 83 -7 0
        -4 -41 -60 -90 -125 -56 -73 -88 -123 -84 -131 4 -6 47 -65 96 -129 48 -64 88
        -120 88 -123 0 -3 -40 -5 -90 -5 l-90 0 -64 97 -65 97 -3 -95 -3 -94 -77 -3
        -78 -3 0 261 0 261 78 -3 77 -3 3 -94z"/>
        </g>
        </svg>
    </div>
'''


def get_closest_past_monday() -> date:
    date_today = date.today()
    for _ in range(8):
        if date_today.weekday() == 0:
            return date_today
        date_today -= timedelta(days=1)
    raise ValueError('[ERROR] :: No mondays in previous 8 days')


def format_date(dt: date) -> str:
    return f'{dt.day:02}.{dt.month:02}.{dt.year:04}'


class PDFGenerator:
    ''' PDFGenerator is used to generate html template for news digest '''
    
    @staticmethod
    def generate(news_list: List[News]) -> bytes:
        end = get_closest_past_monday()
        start = end - timedelta(days=7)

        template = BASE_TEMPLATE[::]

        template += (
            f'''
            <h1><i>НЛМК. Новостной дайджест {format_date(start)} - {format_date(end)}</i><br></h1>
            <hr>
            '''
        )

        for news in news_list:
            template += f'''
                <div class="news">
                    <div class="news-title"><a href="{news.sourceLink}">{news.title}</a></div>
                    <div class="news-summary"><br>{news.summary}</div>
                    <div class="news-source"><br>Источник: {news.source}</div>
                    <div class="news-timestamp">Опубликовано: {news.timestamp.strftime('%Y-%m-%d %H:%M:%S')}<br></div>
                    <hr>
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
