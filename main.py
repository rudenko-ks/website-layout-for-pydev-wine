import os
import argparse
import collections
import datetime

from pathlib import Path
from argparse import RawTextHelpFormatter
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_YEAR_FOUNDED = 1920


def get_age_suffix(age: int) ->  str:
    suffix = "лет"
    if (age//10)%10 != 1:
        if age%10 == 1:
            suffix = "год"
        elif age%10 in (2,3,4):
            suffix = "года"
    return suffix


def load_wine_categories(filepath: Path) -> dict:
    wine_excel_file = pandas.read_excel(filepath, sheet_name='Лист1',
                                        na_values=['nan'], keep_default_na=False,
                                        usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'])
    wine_records = wine_excel_file.to_dict(orient='record')

    wines = collections.defaultdict(list)
    for wine in wine_records:
        category = wine['Категория']
        wines[category].append(wine)
    return wines


def create_argparser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""\
        Скрипт запускает на локальной машине сайт-магазин по продаже вина.\n
        Для запуска требуется указать файл с перечнем продаваемой продукции.
        По умолчанию, скрипт пробует открыть файл "wine.xlsx", находящийся в\n
        директории с запускаемым скриптом, если не указан иной путь до файла.""",
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument('-fp', '--filepath', help='Путь до файла с данными', type=str)
    return parser.parse_args()


def main():
    args = create_argparser()
    filepath = os.getenv("FILEPATH", default='wine.xlsx')
    if args.filepath: filepath = args.filepath
        
    wine_filepath = Path(filepath)
    wine_categories = load_wine_categories(wine_filepath)

    today = datetime.date.today()
    winery_age = today.year - WINERY_YEAR_FOUNDED
    winery_age_suffix = get_age_suffix(winery_age)
    
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        wine_categories = wine_categories,
        winery_age = winery_age, 
        winery_age_suffix = winery_age_suffix
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
