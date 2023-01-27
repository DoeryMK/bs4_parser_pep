import logging

from requests import RequestException

from constants import EXPECTED_STATUS
from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        error_msg = f'Возникла ошибка при загрузке страницы {url}'
        logging.exception(
            error_msg, stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(
            error_msg, stack_info=True
        )
        raise ParserFindTagException(error_msg)
    return searched_tag


def status_comparison(url, page_status, table_status):
    if page_status not in EXPECTED_STATUS[table_status]:
        error_msg = f"""
                Несовпадающие статусы:
                {url}
                Статус в карточке: {page_status}
                Ожидаемые статусы: {EXPECTED_STATUS[table_status]}
                """
        logging.warning(
            error_msg, stack_info=True
        )
