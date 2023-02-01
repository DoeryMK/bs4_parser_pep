import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL,
                       MAIN_PEP_URL)
from exceptions import ParserFindDocURLsException
from outputs import control_output
from utils import (GET_RESPONSE_LOG_ERROR, DelayedLogger, find_tag, get_soup,
                   select_elements)

DOWNLOAD_LOG_INFO = 'Архив был загружен и сохранён: {archive_path}'
START_LOG_INFO = 'Парсер запущен!'
FINISH_LOG_INFO = 'Работа парсера завершена'
URLS_NOT_FOUND_LOG_ERROR = ('Не найдены ссылки на документацию '
                            'на странице {url}')
GENERALISED_LOG_ERROR = 'Ошибка в работе парсера: {error}'


def whats_new(session):
    sections_by_python = select_elements(
        get_soup(session, urljoin(MAIN_DOC_URL, 'whatsnew/')),
        '#what-s-new-in-python li.toctree-l1 > a'
    )
    pattern = r'What’s New.+ (?P<version>\d\.\d+)'
    hrefs = [
        link['href'] for link in sections_by_python if
        re.match(pattern, link.text)
    ]
    results = [
        ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')
    ]
    delayed_logger = DelayedLogger()
    for href in tqdm(hrefs):
        version_link = urljoin(
            urljoin(MAIN_DOC_URL, 'whatsnew/'),
            href
        )
        try:
            soup = get_soup(session, version_link)
        except ConnectionError:
            delayed_logger.add_message(
                GET_RESPONSE_LOG_ERROR.format(url=version_link)
            )
            continue
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append(
            (version_link, h1.text, dl_text)
        )
    delayed_logger.log(logging.warning)
    return results


def latest_versions(session):
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    results = [
        ('Ссылка на документацию', 'Версия', 'Статус')
    ]
    for ul in find_tag(
        get_soup(session, MAIN_DOC_URL),
        'div', {'class': 'sphinxsidebarwrapper'}
    ).find_all('ul'):
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindDocURLsException(
            URLS_NOT_FOUND_LOG_ERROR.format(url=MAIN_DOC_URL)
        )
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        version = text_match.group(1) if text_match else a_tag.text
        status = text_match.group(2) if text_match else ''
        results.append(
            (a_tag['href'], version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(
        MAIN_DOC_URL,
        'download.html'
    )
    archive_url = urljoin(
        downloads_url,
        select_elements(
            get_soup(session, downloads_url),
            'table.docutils a[href$="pdf-a4.zip"]',
            single_tag=True
        )['href']
    )
    filename = archive_url.split('/')[-1]
    # BASE_DIR / DOWNLOADS - ДЛЯ ТЕСТОВ ЯП
    # А ДОЛЖНА БЫТЬ ОДНА КОНСТАНТА - DOWNLOADS_DIR
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(
        DOWNLOAD_LOG_INFO.format(archive_path=archive_path)
    )


def pep(session):
    pep_statuses_dict = defaultdict(int)
    delayed_logger = DelayedLogger()
    for tbody in tqdm(
        get_soup(session, MAIN_PEP_URL).find(
            id='pep-content'
        ).find_all('tbody')
    ):
        abbr_tags = tbody.find_all('abbr')
        for abbr in abbr_tags:
            status_in_table = abbr.text[1:]
            next_td = abbr.parent.find_next_sibling()
            pep_link = find_tag(next_td, 'a').get('href')
            pep_url = urljoin(MAIN_PEP_URL, pep_link)
            try:
                soup = get_soup(session, pep_url)
            except ConnectionError:
                delayed_logger.add_message(
                    GET_RESPONSE_LOG_ERROR.format(url=pep_url)
                )
                continue
            info = find_tag(
                soup, 'section', {'id': 'pep-content'}
            )
            info_table = info.find(
                class_='rfc2822 field-list simple'
            )
            status_text_tag = info_table.find(
                string=re.compile('Status')
            ).parent
            status_on_exact_page = status_text_tag.find_next_sibling().text
            pep_statuses_dict[status_on_exact_page] += 1
            if status_on_exact_page not in EXPECTED_STATUS[status_in_table]:
                delayed_logger.add_message(
                    f'Несовпадающие статусы: '
                    f'{pep_url} '
                    f'Статус в карточке: {status_on_exact_page}'
                )
    delayed_logger.log(logging.warning)
    return [
        ('Статус', 'Количество'),
        *pep_statuses_dict.items(),
        ('Всего', sum(pep_statuses_dict.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info(START_LOG_INFO)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as error:
        logger.exception(
            GENERALISED_LOG_ERROR.format(error=error)
        )
    logger.info(FINISH_LOG_INFO)


if __name__ == '__main__':
    main()
