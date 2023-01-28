import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (BASE_DIR, CONF_OUTPUT_FILE, CONF_OUTPUT_PRETTY,
                       DATETIME_FORMAT, RESULTS)

FILE_OUTPUT_LOG_INFO = 'Файл с результатами был сохранён: {file_path}'


def default_output(*args):
    results = args[0]
    for row in results:
        print(*row)


def pretty_output(*args):
    results = args[0]
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(*args):
    results, cli_args = args
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
        writer = csv.writer(f, dialect=csv.unix_dialect)
        writer.writerows(results)
    logging.info(
        FILE_OUTPUT_LOG_INFO.format(file_path=file_path)
    )


OUTPUT_ACTIONS = {
    CONF_OUTPUT_PRETTY: pretty_output,
    CONF_OUTPUT_FILE: file_output,
}


def control_output(results, cli_args):
    output_action = OUTPUT_ACTIONS.get(
        cli_args.output,
        default_output
    )
    output_action(results, cli_args)
