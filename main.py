import datetime
from pathlib import Path

import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

WINE_FILENAME = 'wine.xlsx'


def get_age_suffix(age: int) ->  str:
    suffix = "лет"
    if (age//10)%10 != 1:
        if age%10 == 1:
            suffix = "год"
        elif age%10 in (2,3,4):
            suffix = "года"
    return suffix


def load_wine_from_xml(filepath: Path) -> list:
    wine_excel_file = pandas.read_excel(filepath, sheet_name='Лист1', usecols=['Название', 'Сорт', 'Цена', 'Картинка'])
    return wine_excel_file.to_dict(orient='record')



env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

winery_founded = 1920
today = datetime.date.today()
winery_age = today.year - winery_founded
winery_age_suffix = get_age_suffix(winery_age)

wine_filepath = Path(WINE_FILENAME)
wines = load_wine_from_xml(wine_filepath)

rendered_page = template.render(
    wines = wines
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

