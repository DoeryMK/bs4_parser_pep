from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

GET_RESPONSE_LOG_ERROR = 'Возникла ошибка при загрузке страницы {url}'
TAG_NOT_FOUND_LOG_ERROR = 'Не найден тег {tag} {attrs}'
ELEMENTS_NOT_FOUND_LOG_ERROR = 'Не найдены элементы по запросу: {expression}'


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except Exception:
        raise RequestException(
            GET_RESPONSE_LOG_ERROR.format(url=url),
        )


def get_soup(session, url):
    response = get_response(session, url)
    soup = BeautifulSoup(response.text, features='lxml')
    return soup


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs={} if attrs is None else attrs)
    if searched_tag is None:
        raise ParserFindTagException(
            TAG_NOT_FOUND_LOG_ERROR.format(tag=tag, attrs=attrs)
        )
    return searched_tag


def select_elements(soup, expression, single_tag=False):
    selected = (soup.select_one(expression) if single_tag
                else soup.select(expression))
    if soup.select_one(expression) is None:
        raise ParserFindTagException(
            ELEMENTS_NOT_FOUND_LOG_ERROR.format(expression=expression)
        )
    return selected
