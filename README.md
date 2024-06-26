# How to launch backend side of "AI News Aggregator"

1. Clone repository

2. Start terminal

3. Using ```cd``` command, go to ```it_news_summarizer_backend``` folder

4. Create venv: ```python3 -m venv venv```

5. Start venv: ```source venv/bin/activate```

6. Download dependencies: ```pip install -r requirements.txt```

7. Go to ```src``` folder using ```cd``` command ( for example: ```cd src``` )

8. Use ```export PYTHONPATH=$(pwd)``` ( only if running on UNIX OS system: Linux/MacOS )

9. Inside src folder, create ```.env``` file. Add YandexGPT **API_KEY** & **CATALOGUE** constants ( there is a default .env without active api keys, but be sure to copy and paste YOUR api keys inside this file )

10. Run server: ```python3 main.py```

## To launch frontend, see [Frontend Github repository](https://github.com/reproductionprohibited/it_news_summarizer_2.0)
