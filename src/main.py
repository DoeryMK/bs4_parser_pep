import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS, DOWNLOADS_DIR, EXPECTED_STATUS,
                       MAIN_DOC_URL, MAIN_PEP_URL)
from outputs import control_output
from utils import find_tag, get_response, get_soup

DOWNLOAD_LOG_INFO = 'Архив был загружен и сохранён: {archive_path}'
START_LOG_INFO = 'Парсер запущен!'


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup(session, whats_new_url)

    # response = get_response(session, whats_new_url)
    # if response is None:
    #     return
    # soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(
        soup, 'section', attrs={'id': 'what-s-new-in-python'}
    )
    div_with_ul = find_tag(
        main_div, 'div', attrs={'class': 'toctree-wrapper'}
    )
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )

    results = [
        ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')
    ]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_soup(session, version_link)
        # response = get_response(session, version_link)
        # if response is None:
        #     continue
        # soup_href = BeautifulSoup(response.text, features='lxml')

        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')

        results.append(
            (version_link, h1.text, dl_text)
        )

    return results


def latest_versions(session):
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    soup = get_soup(session, MAIN_DOC_URL)

    # response = get_response(session, MAIN_DOC_URL)
    # if response is None:
    #     return
    # soup = BeautifulSoup(response.text, features='lxml')

    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')

    results = [
        ('Ссылка на документацию', 'Версия', 'Статус')
    ]
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')

    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        version = text_match.group(1) if text_match else a_tag.text
        status = text_match.group(2) if text_match else ''
        results.append(
            (a_tag['href'], version, status)
        )

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup(session, downloads_url)

    # response = get_response(session, downloads_url)
    # if response is None:
    #     return
    # soup = BeautifulSoup(response.text, features='lxml')

    main_tag = find_tag(
        soup, 'div', {'role': 'main'}
    )
    table_tag = find_tag(
        main_tag, 'table', {'class': 'docutils'}
    )
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    # BASE_DIR / DOWNLOADS - ДЛЯ ТЕСТОВ ЯП
    # А ДОЛЖНА БЫТЬ ОДНА КОНСТАНТА - DOWNLOADS_DIR
    downloads_dir = BASE_DIR / DOWNLOADS
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(archive_url)

    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(
        DOWNLOAD_LOG_INFO.format(archive_path=archive_path)
    )


def pep(session):
    soup = get_soup(session, MAIN_PEP_URL)
    # response = get_response(session, MAIN_PEP_URL)
    # if response is None:
    #     return
    # soup = BeautifulSoup(response.text, features='lxml')

    tbody_tags = soup.find(id='pep-content').find_all('tbody')
    pep_statuses_dict = defaultdict(int)
    results = [
        ('Статус', 'Количество')
    ]

    for tbody in tqdm(tbody_tags):
        abbr_tags = tbody.find_all('abbr')
        for abbr in abbr_tags:
            status_in_table = abbr.text[1:]

            next_td = abbr.parent.find_next_sibling()
            pep_link = find_tag(next_td, 'a').get('href')
            pep_url = urljoin(MAIN_PEP_URL, pep_link)
            soup = get_soup(session, pep_url)

            # response = get_response(session, pep_url)
            # if response is None:
            #     return
            # soup = BeautifulSoup(response.text, features='lxml')

            info = find_tag(
                soup, 'section', {'id': 'pep-content'}
            )
            info_table = info.find(
                class_='rfc2822 field-list simple'
            )
            status_text_tag = info_table.find(
                string=re.compile('Status')).parent
            status_on_exact_page = status_text_tag.find_next_sibling().text
            pep_statuses_dict[status_on_exact_page] += 1

            # def status_comparison(url, page_status, table_status):
            if status_on_exact_page not in EXPECTED_STATUS[status_in_table]:
                error_msg = f"""
                        Несовпадающие статусы:
                        {pep_url}
                        Статус в карточке: {status_on_exact_page}
                        Ожидаемые статусы: {EXPECTED_STATUS[status_in_table]}
                        """
                logging.warning(
                    error_msg, stack_info=True
                )

    results.extend(
        pep_statuses_dict.items()
    )
    results.append(
        ('Общее количество PEP', sum(pep_statuses_dict.values()))
    )

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info(
        START_LOG_INFO
    )

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)


if __name__ == '__main__':
    main()
