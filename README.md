# Проект парсинга документации Python

## **Основная цель проекта**

Изучение возможностей библиотеки bs4 ([Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/#beautiful-soup-documentation))
для парсинга HTML-страниц и XML-файлов с использованием кеширующих сессий ([requests-cache](https://requests-cache.readthedocs.io/en/latest/user_guide.html)).  
Настройка работы парсера через командную строку с помощью модуля [argparse](https://docs.python.org/3/library/argparse.html#module-argparse).  
Настройка логирования с помощью модуля [logging](https://docs.python.org/3/library/logging.html#module-logging).


##  **Описание проекта**
В качестве таргета используются страницы: 
- главная страница c документацией Python (https://docs.python.org/3/)
- главная страница c информацией о PEP (https://peps.python.org/)
- страница для скачивания документации Python (https://docs.python.org/3/download.html)

### Основные режимы работы парсера:
- **pep**  
_На главной странице с PEP выполняется поиск текущих статусов PEP, а также 
ссылок на станицы со статьями о существующих PEP.  
Далее парсер выполняет сравнение статуса указанного в таблице на основной странице
со статусом из карточки со страницы конкретного PEP. В случае, если статусы отличаются,
выполняется логирование события.  
Данные формируются в следующем формате:_
```
Статус / Количество
```
Также выводится общее количество зарегистрированных PEP.
- **whats-new**  
_На главной странице документации Python выполняется поиск ссылок на страницы 
со статьями о доступных версиях Python, переход по ним и сбор информации 
в следующем формате:_  
```
Ссылка на статью о версии Python / Название статьи / Информация об авторе
```
- **latest-versions**  
_Выполняется сбор информации о доступных версиях Python на главной страницы 
c документацией Python в следующем формате:_  
```
Ссылка на статью о версии Python / Верия / Статус
```
- **download**  
_Со страницы https://docs.python.org/3/download.html выполняется скачивание
архива с документацией последней версии Python.  
Файл сохраняется в папку
```/src/downloads/```._

### Доступно три способа вывода собранных данных пользователю:  
- Обычный вывод в консоль (stdout);  
- Вывод в консоль в табличном виде (аргументы ```-o {pretty}```);
- Сохранение в формате csv (аргументы ```-o {file}```) в папку ```/src/results/```;

Настроено логирование работы парсера.  
Лог сохраняется в папку ```/src/logs/```.

## **Запуск проекта**
Выполните следующие команды в терминале:

1. Клонировать проект из репозитория
```
git@github.com:DoeryMK/bs4_parser_pep.git
```
или
```
https://github.com/DoeryMK/bs4_parser_pep.git
```
2. Создать, активировать виртуальное окружение и в него установить зависимости:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
```
pip install -r requirements.txt 
```
3. Запустить парсер из командной строки, например:
```
python src/main.py pep -o -file
```

### _Доступные аргументы командной строки_
Для просмотра режимов работы парсера в терминале введите команду:
```
python src/main.py -h
```
Результат работы команды будет следующим:
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```

## Авторы: [DoeryMK](https://github.com/DoeryMK) 