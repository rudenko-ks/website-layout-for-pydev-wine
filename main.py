import collections
import datetime
from pathlib import Path
from pprint import pp, pprint
from turtle import clear
from unicodedata import category

import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

WINERY_YEAR_FOUNDED = 1920
WINE_FILENAME = 'wine3.xlsx'


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


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

today = datetime.date.today()
winery_age = today.year - WINERY_YEAR_FOUNDED
winery_age_suffix = get_age_suffix(winery_age)

wine_filepath = Path(WINE_FILENAME)
wine_categories = load_wine_categories(wine_filepath)
        
rendered_page = template.render(
    wine_categories = wine_categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

