"""
core operations
"""

import os
import datetime

from squeezerp.database.database_data import DATE_FORMATS


def get_file_size(input_file):
    return os.path.getsize(input_file)


def convert_date_db(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')


def isint(s):
    try:
        a = float(s)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b


def isfloat(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


def isdate(s):
    for date_format in DATE_FORMATS:
        try:
            datetime.datetime.strptime(s, date_format)
            return True
        except (ValueError, TypeError):
            pass
    return False