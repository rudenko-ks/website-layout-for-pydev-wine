import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler
from platform import win32_edition

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

winery_founded = 1920
today = datetime.date.today()
winery_age = today.year - winery_founded

rendered_page = template.render(
    winery_age=winery_age,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()



