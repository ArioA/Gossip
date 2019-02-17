import argparse
from datetime import date, datetime, time
from pprint import pprint
from typing import Optional

import bs4

from gossip.entities import Paragraph
from gossip.fetch import get_gossip_raw_response
from gossip.utils import paths

TIMES_OF_DAY = ['am', 'pm']


def load_downloaded(data_date: date, am_or_pm: str, fail_on_no_file=True) -> Optional[str]:
    file_path = paths.get_raw_file_path(data_date, am_or_pm)
    try:
        with open(file_path, 'rt') as raw_file:
            raw_html = raw_file.read()
    except FileNotFoundError:
        if fail_on_no_file:
            raise
        else:
            return None
    return raw_html


def get_id(raw_html: str, tag_id: str) -> bs4.ResultSet:
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    return soup.find_all("div", id=tag_id)


def prettify(raw_html: str):
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    print(soup.prettify())


def is_am_or_pm(dt: datetime) -> str:
    if dt.time() < time(12, 0):
        return "am"
    else:
        return "pm"


def set_time_of_day(args):
    if args.time_of_day:
        return args.time_of_day

    args_date = date(args.year, args.month, args.day)

    today = datetime.utcnow()
    if today.date() != args_date:
        time_of_day = "pm"
    else:
        time_of_day = is_am_or_pm(today)

    return time_of_day


def main():
    parser = argparse.ArgumentParser(description='Print the contents of the BBC Sport Football gossip page')

    today = date.today()

    parser.add_argument('--year', '-y', nargs='?', default=today.year,
                        type=int, help='The year of the gossip data to prettyfy (default: current year)')

    parser.add_argument('--month', '-m', nargs='?', default=today.month,
                        type=int, help='The month of the gossip data to prettyfy (default: current month)')

    parser.add_argument('--day', '-d', nargs='?', default=today.day,
                        type=int, help='The day of the gossip data to prettyfy (default: current day)')

    parser.add_argument('--tod', '-t', nargs='?', choices=TIMES_OF_DAY, dest='time_of_day',
                        help='The time of day of the gossip page (default: latest one which can be found)')

    parser.add_argument('--raw', '-r', action='store_true', dest='raw',
                        help='Print the raw, unparsed HTML.')

    args = parser.parse_args()

    page_html = get_raw_html(args, today)

    if args.raw:
        prettify(page_html)
    else:
        print_story_body(page_html)


def get_raw_html(args: argparse.Namespace, today: date) -> str:
    """
    Gets the raw HTML of the gossip page.

    The behaviour is:
        - If the data is available on disk, then the data on disk will be used.
        - Else, if the queried data is available on the internet, then that shall be used.
        - If the user does not specify a time of day, then a best effort shall be made to find any
          data from that day across disk and the internet.

    Args:
        args: Parsed args from the user's input
        today: Today's date

    Returns:
        Raw html from the BBC sport football gossip page.
    """
    time_of_day = set_time_of_day(args)
    data_date = date(args.year, args.month, args.day)
    if args.time_of_day is not None:  # If a specific time of day was specified
        try:
            page_html = load_downloaded(data_date, time_of_day, fail_on_no_file=True)
        except FileNotFoundError:
            if today == data_date and args.time_of_day == is_am_or_pm(datetime.utcnow()):
                page_html = get_gossip_raw_response().text
            else:
                raise
    else:  # If no time of day was specified
        page_html = load_downloaded(data_date, time_of_day, fail_on_no_file=False)

        if page_html is None:
            other_time_of_day = set(TIMES_OF_DAY).difference({args.time_of_day}).pop()
            page_html = load_downloaded(data_date, other_time_of_day, fail_on_no_file=False)

            if page_html is None:
                if today == data_date:
                    page_html = get_gossip_raw_response().text
                else:
                    raise ValueError(f"Unable to find gossip data for {data_date.isoformat()}")
    return page_html


def print_story_body(raw_html):
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
