import argparse
from datetime import date
from pprint import pprint

import bs4

from gossip.entities import Paragraph
from gossip.utils import paths

TIMES_OF_DAY = ['am', 'pm']


def load_downloaded(data_date: date, am_or_pm: str = 'pm') -> str:
    file_path = paths.get_raw_file_path(data_date, am_or_pm)
    with open(file_path, 'rt') as raw_file:
        raw_html = raw_file.read()
    return raw_html


def get_id(raw_html: str, tag_id: str) -> bs4.ResultSet:
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    return soup.find_all("div", id=tag_id)


def prettify(raw_html: str):
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    print(soup.prettify())


def main():
    parser = argparse.ArgumentParser(description='Print the contents of the BBC Sport Football gossip page')

    today = date.today()

    parser.add_argument('--year', '-y', nargs='?', default=today.year,
                        type=int, help='The year of the gossip data to prettyfy (default: current year)')

    parser.add_argument('--month', '-m', nargs='?', default=today.month,
                        type=int, help='The month of the gossip data to prettyfy (default: current month)')

    parser.add_argument('--day', '-d', nargs='?', default=today.day,
                        type=int, help='The day of the gossip data to prettyfy (default: current day)')

    parser.add_argument('--tod', '-t', nargs='?', default='pm', choices=TIMES_OF_DAY, dest='time_of_day',
                        help='The time of day of the gossip page (default: pm)')

    args = parser.parse_args()

    data_date = date(args.year, args.month, args.day)

    try:
        print_story_body(data_date, args.time_of_day)
    except FileNotFoundError:
        time_of_day = set(TIMES_OF_DAY).difference({args.time_of_day}).pop()
        print_story_body(data_date, time_of_day)


def print_story_body(data_date: date, time_of_day: str):
    raw_html = load_downloaded(data_date, time_of_day)
    the_id = get_id(raw_html, "story-body")[0]

    pars = the_id.find_all('p')

    for par in pars:
        para = Paragraph(par)
        if para:
            print(para.build_paragraph(True))
            print()
    #print(the_id.prettify())


if __name__ == '__main__':
    main()
