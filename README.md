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
git clone git@github.com:DoeryMK/bs4_parser_pep.git
```
или
```
git clone https://github.com/DoeryMK/bs4_parser_pep.git
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
Для просмотра режимов работы парсера в терминале введите команду 
с именованным аргументом ```-h``` или ```--help```:  
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

### _Вывод результатов_
1. Для вывода результатов в терминал в стандартном формате 
запустите парсер с соответствующим позиционным 
аргументом (```whats-new```, ```latest-versions``` или ```pep```), например:
```
python src/main.py latest-versions
```
Вывод будет следующим:  
```
$ python src/main.py latest-versions
"28.01.2023 03:53:47 - [INFO] - Парсер запущен!"
Ссылка на документацию Версия Статус
https://docs.python.org/3.12/ 3.12 in development
https://docs.python.org/3.11/ 3.11 stable
https://docs.python.org/3.10/ 3.10 stable
https://docs.python.org/3.9/ 3.9 security-fixes
https://docs.python.org/3.8/ 3.8 security-fixes
https://docs.python.org/3.7/ 3.7 security-fixes
https://docs.python.org/3.6/ 3.6 EOL
https://docs.python.org/3.5/ 3.5 EOL
https://docs.python.org/2.7/ 2.7 EOL
https://www.python.org/doc/versions/ All versions
```
2. Для вывода результатов в терминал в табличном виде 
запустите парсер с именованным аргументами ```-o pretty```.  
Парсер ```latest-versions```:
```
python src/main.py latest-versions -o pretty
```
Вывод будет следующим: 
```
$ python src/main.py latest-versions -o pretty
"28.01.2023 03:57:56 - [INFO] - Парсер запущен!"
+--------------------------------------+--------------+----------------+
| Ссылка на документацию               | Версия       | Статус         |
+--------------------------------------+--------------+----------------+
| https://docs.python.org/3.12/        | 3.12         | in development |
| https://docs.python.org/3.11/        | 3.11         | stable         |
| https://docs.python.org/3.10/        | 3.10         | stable         |
| https://docs.python.org/3.9/         | 3.9          | security-fixes |
| https://docs.python.org/3.8/         | 3.8          | security-fixes |
| https://docs.python.org/3.7/         | 3.7          | security-fixes |
| https://docs.python.org/3.6/         | 3.6          | EOL            |
| https://docs.python.org/3.5/         | 3.5          | EOL            |
| https://docs.python.org/2.7/         | 2.7          | EOL            |
| https://www.python.org/doc/versions/ | All versions |                |
+--------------------------------------+--------------+----------------+
```

Парсер ```whats-new```:
```
python src/main.py whats-new -o pretty
```
Вывод будет следующим: 
```
+----------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------+
| Ссылка на статью                             | Заголовок                  | Редактор, Автор                                                                                                 |
+----------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------+
| https://docs.python.org/3/whatsnew/3.11.html | What’s New In Python 3.11¶ |  Release 3.11.1  Date January 27, 2023  Editor Pablo Galindo Salgado                                            |
| https://docs.python.org/3/whatsnew/3.10.html | What’s New In Python 3.10¶ |  Editor Pablo Galindo Salgado                                                                                   |
| https://docs.python.org/3/whatsnew/3.9.html  | What’s New In Python 3.9¶  |  Editor Łukasz Langa                                                                                            |
| https://docs.python.org/3/whatsnew/3.8.html  | What’s New In Python 3.8¶  |  Editor Raymond Hettinger                                                                                       |
| https://docs.python.org/3/whatsnew/3.7.html  | What’s New In Python 3.7¶  |  Editor Elvis Pranskevichus <elvis@magic.io>                                                                    |
| https://docs.python.org/3/whatsnew/3.6.html  | What’s New In Python 3.6¶  |  Editors Elvis Pranskevichus <elvis@magic.io>, Yury Selivanov <yury@magic.io>                                   |
| https://docs.python.org/3/whatsnew/3.5.html  | What’s New In Python 3.5¶  |  Editors Elvis Pranskevichus <elvis@magic.io>, Yury Selivanov <yury@magic.io>                                   |
| https://docs.python.org/3/whatsnew/3.4.html  | What’s New In Python 3.4¶  |  Author R. David Murray <rdmurray@bitdance.com> (Editor)                                                        |
| https://docs.python.org/3/whatsnew/3.3.html  | What’s New In Python 3.3¶  |  PEP 405 - Python Virtual EnvironmentsPEP written by Carl Meyer; implementation by Carl Meyer and Vinay Sajip   |
| https://docs.python.org/3/whatsnew/3.2.html  | What’s New In Python 3.2¶  |  Author Raymond Hettinger                                                                                       |
| https://docs.python.org/3/whatsnew/3.1.html  | What’s New In Python 3.1¶  |  Author Raymond Hettinger                                                                                       |
| https://docs.python.org/3/whatsnew/3.0.html  | What’s New In Python 3.0¶  |  Author Guido van Rossum                                                                                        |
| https://docs.python.org/3/whatsnew/2.7.html  | What’s New in Python 2.7¶  |  Author A.M. Kuchling (amk at amk.ca)                                                                           |
| https://docs.python.org/3/whatsnew/2.6.html  | What’s New in Python 2.6¶  |  Author A.M. Kuchling (amk at amk.ca)                                                                           |
| https://docs.python.org/3/whatsnew/2.5.html  | What’s New in Python 2.5¶  |  Author A.M. Kuchling                                                                                           |
| https://docs.python.org/3/whatsnew/2.4.html  | What’s New in Python 2.4¶  |  Author A.M. Kuchling                                                                                           |
| https://docs.python.org/3/whatsnew/2.3.html  | What’s New in Python 2.3¶  |  Author A.M. Kuchling                                                                                           |
| https://docs.python.org/3/whatsnew/2.2.html  | What’s New in Python 2.2¶  |  Author A.M. Kuchling                                                                                           |
| https://docs.python.org/3/whatsnew/2.1.html  | What’s New in Python 2.1¶  |  Author A.M. Kuchling                                                                                           |
| https://docs.python.org/3/whatsnew/2.0.html  | What’s New in Python 2.0¶  |  Author A.M. Kuchling and Moshe Zadka                                                                           |
+----------------------------------------------+----------------------------+-----------------------------------------------------------------------------------------------------------------+
```

Парсер ```pep```:
```
python src/main.py pep -o pretty
```
Вывод будет следующим: 
```
+----------------------+------------+
| Статус               | Количество |
+----------------------+------------+
| Active               | 74         |
| Accepted             | 84         |
| Final                | 526        |
| Draft                | 58         |
| Superseded           | 40         |
| Deferred             | 72         |
| Withdrawn            | 110        |
| Rejected             | 240        |
| April Fool!          | 2          |
| Общее количество PEP | 1206       |
+----------------------+------------+
```

3. Для сохранения результатов в файл формата csv
запустите парсер с именованным аргументами ```-o file```, например:  
```
python src/main.py latest-versions -o file
```
В родительской директории ```src/``` будет создана новая ```results/```, 
в которую сохранится файл с результатами работы парсера.  

4. Для сохранения документации Python запустите парсер следующей 
командой без именованных аргументов:  
```
python src/main.py download
```
В родительской директории ```src/``` будет создана новая ```downloads/```, 
в которую сохранится zip-архив c документами в формате PDF (A4 paper size).  

### _Дополнительные функции_
Для очистки кеша при создании сессии необходимо запустить 
парсер с именованным аргументом ```-с``` или ```--clear-cache```, например:
```
python src/main.py latest-versions -c -o pretty
```

## Авторы: Мухамеджанова Д.С. ([DoeryMK](https://github.com/DoeryMK)) 