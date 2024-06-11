class Summarizer:
    @staticmethod
    def summarize(article: str) -> str:
        return article.strip()[:10]
