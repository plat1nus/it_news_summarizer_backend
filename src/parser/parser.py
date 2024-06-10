from rbc import parse_rbc 
from cnews import parse_cnews
from interfax import parse_interfax
from techcrunch import parse_techcrunch

def get_list_news():
    lst = []
    lst.append(parse_rbc())
    lst.append(parse_cnews())
    lst.append(parse_interfax())
    lst.append(parse_techcrunch())
    return lst 