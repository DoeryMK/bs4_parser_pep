from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException

GET_RESPONSE_LOG_ERROR = 'Возникла ошибка при загрузке страницы {url}'
TAG_NOT_FOUND_LOG_ERROR = 'Не найден тег {tag} {attrs}'
NO_CONTENT_LOG_ERROR = 'Не удалось получить содержимое страницы: {url}'


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except Exception:
        # logging.exception(
        #     GET_RESPONSE_LOG_ERROR.format(url=url),
        #     stack_info=True
        # )
        raise RequestException(
            GET_RESPONSE_LOG_ERROR.format(url=url)
        )


def get_soup(session, url):
    response = get_response(session, url)
    if response is None:
        raise ParserFindTagException(
            NO_CONTENT_LOG_ERROR.format(url=url),
        )
        # logging.error(
        #     NO_CONTENT_LOG_ERROR.format(url=url),
        #     stack_info=True
        #
        # return
    soup = BeautifulSoup(response.text, features='lxml')
    return soup


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        # logging.exception(
        #     TAG_NOT_FOUND_LOG_ERROR.format(tag=tag, attrs=attrs),
        #     stack_info=True
        # )
        raise ParserFindTagException(
            TAG_NOT_FOUND_LOG_ERROR.format(tag=tag, attrs=attrs)
        )
    return searched_tag
