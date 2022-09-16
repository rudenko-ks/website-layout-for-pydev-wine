import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler
from platform import win32_edition

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_age_suffix(age: int) ->  str:
    suffix = "лет"
    if (age//10)%10 != 1:
        if age%10 == 1:
            suffix = "год"
        elif age%10 in (2,3,4):
            suffix = "года"
    return suffix


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

winery_founded = 1920
today = datetime.date.today()
winery_age = today.year - winery_founded
winery_age_suffix = get_age_suffix(winery_age)

rendered_page = template.render(
    winery_age=winery_age,
    winery_age_suffix=winery_age_suffix,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

