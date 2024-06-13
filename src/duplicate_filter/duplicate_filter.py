from typing import List

from sentence_transformers import SentenceTransformer, util
from sqlalchemy.orm import Session

from data.models import News


class DuplicateFilter:
    ''' Class used to remove duplicate news from currently parsed news, using news already in database '''

    @staticmethod
    def clear_duplicates(model:SentenceTransformer, parsed_news: List[News], db_session: Session) -> List[News]:
        # db_news = db_session.query(News).all()
        # db_titles = [it.title for it in db_news]
        # new_news = [it for it in parsed_news if it.title not in db_titles]
        # print(len(new_news), ':: new news')

        # TODO: Fix errors connected to Intel processor interoperability with SentenceTransformer library
        embeddings = [model.encode([it.summary for it in parsed_news], convert_to_tensor=True)]
        cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)
        threshold = 0.7

        unique_news_indices = set()
        seen = set()

        for i in range(len(parsed_news)):
            if i not in seen:
                unique_news_indices.add(i)
                for j in range(i + 1, len(parsed_news)):
                    if cosine_scores[i][j] > threshold:
                        seen.add(j)

        unique_news = [news for (i, news) in enumerate(parsed_news) if i in unique_news_indices]
        return unique_news
        # return new_news
