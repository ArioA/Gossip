#!/usr/local/bin/python3
from datetime import datetime
import logging

import requests

from gossip.config import conf
from gossip.config.logging import init_logging
from gossip.utils import paths

logger = logging.getLogger(__name__)


def get_gossip_raw(url: str) -> requests.Response:
    logger.info(f"Sending request to {url}")
    resp = requests.get(url)
    logger.info(f"Got response with status={resp.status_code}, length={len(resp.text)}")
    return resp
    

def save_gossip_raw(raw_gossip: str):
    now = datetime.utcnow()
    filename = paths.get_raw_file_path(now)
    paths.create_file_dir(filename)

    with open(filename, 'w') as goss_file:
        goss_file.write(raw_gossip)


def ok_status(response: requests.Response) -> bool:
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.exception("A HTTP error occured")
        return False
    return True


def main():
    init_logging()
    logger.info('START')
    try:
        run()
    except Exception as e:
        logger.exception("Something went wrong!")
    logger.info('END')


def run():
    url = conf['REMOTE']['url']
    resp = get_gossip_raw(url)
    if ok_status(resp):
        save_gossip_raw(resp.text)


if __name__ == '__main__':
    main()
