import datetime
import logging
import os
from typing import Optional, Union

from gossip.config import conf

logger = logging.getLogger(__name__)


def create_file_dir(file_path: str, is_dir=False):
    if os.path.exists(file_path):
        return

    if is_dir:
        directory = file_path
    else:
        directory = os.path.dirname(file_path)

    os.makedirs(directory, exist_ok=True)


def get_raw_data_dir() -> str:
    proj_dir = conf['GENERAL']['project_directory']
    data_dir_name = conf['DATA']['directory']
    raw_dir_name = conf['DATA']['raw_directory']

    data_dir = os.path.join(proj_dir, data_dir_name, raw_dir_name)
    return data_dir


def get_raw_file_dir(date: datetime.date) -> str:
    data_dir = get_raw_data_dir()

    logger.info(f"Got parent directory {data_dir}")

    dir_names = map(str, [date.year, date.month, date.day])

    file_dir = os.path.join(data_dir, *dir_names)
    return file_dir


def build_file_name(date: Optional[datetime.date] = None, am_or_pm: Optional[str] = None) -> str:
    if am_or_pm:
        prefix = am_or_pm
    else:
        try:
            if date.hour < 12:
                prefix = 'am'
            else:
                prefix = 'pm'
        except AttributeError:
            raise ValueError("Must specifiy either `am` or `pm`, or provide a date with a time")
    
    filename = f'{prefix}_gossip.html'
    return filename


def get_raw_file_path(date: Union[datetime.date, datetime.datetime], am_or_pm: str = None) -> str:
    file_dir = get_raw_file_dir(date)
    logger.info(f"Got file dir {file_dir}")

    filename = build_file_name(date, am_or_pm)
 
    file_path = os.path.join(file_dir, filename)

    logger.info(f"Got file path: {file_path}")

    return file_path
