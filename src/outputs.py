import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (BASE_DIR, DATETIME_FORMAT, OUTPUT_FORMAT_DEFAULT,
                       OUTPUT_FORMAT_FILE, OUTPUT_FORMAT_PRETTY, RESULTS)

FILE_OUTPUT_LOG_INFO = 'Файл с результатами был сохранён: {file_path}'


def default_output(results, *args):
    for row in results:
        print(*row)


def pretty_output(results, *args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    # BASE_DIR / RESULTS - ДЛЯ ТЕСТОВ ЯП
    # А ДОЛЖНА БЫТЬ ОДНА КОНСТАНТА - RESULTS_DIR
    results_dir = BASE_DIR / RESULTS
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer(
            f, dialect=csv.unix_dialect
        ).writerows(results)
    logging.info(
        FILE_OUTPUT_LOG_INFO.format(file_path=file_path)
    )


OUTPUT_ACTIONS = {
    OUTPUT_FORMAT_PRETTY: pretty_output,
    OUTPUT_FORMAT_FILE: file_output,
    OUTPUT_FORMAT_DEFAULT: default_output,
}


def control_output(results, cli_args):
    OUTPUT_ACTIONS.get(cli_args.output)(results, cli_args)
