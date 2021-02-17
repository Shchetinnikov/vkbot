from time import time
import datetime

timer_start = time()
timer_threshold = datetime.timedelta(1)


def separate(date):
    separate_date = {"year": date.year,
                     "month": date.month,
                     "day": date.day,
                     "hour": date.hour,
                     "minute": date.minute,
                     "second": date.second,
                     "microsecond": date.microsecond,
                     "tzinfo": date.tzinfo}
    return separate_date


def compound(date):
    compound_date = datetime.datetime(
        date['year'],
        date['month'],
        date['day'],
        date['hour'],
        date['minute'],
        date['second'],
        date['microsecond'],
        date['tzinfo']
    )
    return compound_date
