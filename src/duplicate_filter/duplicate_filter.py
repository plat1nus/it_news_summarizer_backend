from typing import List

from data.models import News


class DuplicateFilter:

    @staticmethod
    def clear_duplicates(db_news: List[News], parsed_news: List[News]) -> List[News]:
        db_titles = [it.title for it in db_news]
        new_news = [it for it in parsed_news if it.title not in db_titles]
        return new_news
    