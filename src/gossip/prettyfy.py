import argparse
from datetime import date

from bs4 import BeautifulSoup

from gossip.utils import paths


def load_downloaded(data_date, am_or_pm='pm'):
    file_path = paths.get_raw_file_path(data_date, am_or_pm)
    with open(file_path, 'rt') as raw_file:
        raw_html = raw_file.read()
    return raw_html


def get_id(raw_html, id_):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.find_all("div", id=id_)


def prettify(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    print(soup.prettify())


def main():
    parser = argparse.ArgumentParser(description='Print the contents of the BBC Sport Football gossip page')

    parser.add_argument('--year', '-y', nargs='?', default=date.today().year,
                        type=int, help='The year of the gossip data to prettyfy')

    parser.add_argument('--month', '-m', nargs='?', default=date.today().year,
                        type=int, help='The month of the gossip data to prettyfy')

    parser.add_argument('--day', '-d', nargs='?', default=date.today().year,
                        type=int, help='The day of the gossip data to prettyfy')

    parser.add_argument('--tod', '-t', nargs='?', default='pm', choices=['am', 'pm'], dest='time_of_day',
                        help='The time of day of the gossip page.')

    args = parser.parse_args()

    data_date = date(args.year, args.month, args.day)
    print_story_body(data_date, args.time_of_day)


def print_story_body(data_date, time_of_day):
    raw_html = load_downloaded(data_date, time_of_day)
    the_id = get_id(raw_html, "story-body")
    print(the_id[0].prettify())


if __name__ == '__main__':
    main()
