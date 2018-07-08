from datetime import date

from bs4 import BeautifulSoup

from utils import paths


def load_downloaded(date, am_or_pm='pm'):
    filepath = paths.get_raw_file_path(date, am_or_pm)
    with open(filepath, 'rt') as raw_file:
        raw_html = raw_file.read()
    return raw_html

def get_id(raw_html, id_):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.find_all("div", id=id_)

def prettify(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    print(soup.prettify())


if __name__ == '__main__':
    DATE = date(2018, 7, 8)
    TOD = 'pm'

    raw_html = load_downloaded(DATE, TOD)
    the_id = get_id(raw_html, "story-body")
    print(the_id[0].prettify())

