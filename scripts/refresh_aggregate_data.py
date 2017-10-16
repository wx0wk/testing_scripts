import argparse
import datetime as dt
import django
import os
import pytz
import sys
from time import sleep
import traceback

import base64
b64_db2s = lambda b: base64.decodebytes(b).decode()
b64_ds2s = lambda s: base64.decodebytes(s.encode()).decode()

DJANGO_PROJECT_PATH = "/path/to/project/"

try:
    sys.path.append(DJANGO_PROJECT_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()
except Exception as e:
    print('Error loading Django project settings: {}'.format(e))
    print(''.join(traceback.format_exception(*sys.exc_info())))
    exit()


from Data.mongoModels import aggregatedFuelData
from Tracking.tasks import aggregate_usage_data

_argparser = argparse.ArgumentParser()
_argparser.add_argument('-f', "--from_date", required=True, help="The beginning date to redo aggregate.")
_argparser.add_argument('-t', "--to_date", help="Defaults to same as -from_date.")
args = _argparser.parse_args()
print(args)

utc = pytz.utc
date_format = '%Y-%m-%d'

def get_daterange(date_range: tuple):
    parse_utc_date = lambda d: utc.localize(dt.datetime.strptime(d, date_format))
    try:
        startdate = parse_utc_date(date_range[0])
    except Exception as e:
        startdate = utc.localize(dt.datetime.combine(
            dt.datetime.now().date(), dt.time(0, 0, 0)
        )) + dt.timedelta(days=-1)
    try:
        enddate = parse_utc_date(date_range[1])
    except Exception as e:
        enddate = startdate
    return startdate, enddate

startdate, enddate = get_daterange((args.from_date, args.to_date)
                                   if args.to_date else (args.from_date, ))

ts0 = dt.datetime.now()
try:
    aggregatedFuelData.objects.filter(
        ts__gte=startdate,
        ts__lt=enddate+dt.timedelta(days=1),
    ).delete(write_concern={'j': True,})
    sleep(5)
except Exception as e:
    print(''.join(traceback.format_exception(*sys.exc_info())))
    exit()

for i in range(9999999999):
    _date = startdate + dt.timedelta(days=i)
    if _date > enddate:
        break
    req_date = utc.localize(dt.datetime.combine(_date, dt.time(0, 0, 0)))
    req_filter = dict(
        ts__gte = req_date,
        ts__lte = req_date + dt.timedelta(days=1, microseconds=-1)
    )
    try:
        print('Day {} result: {}'
              .format(req_date.strftime(date_format),
                      aggregate_usage_data(req_date)))
    except Exception as e:
        print(''.join(traceback.format_exception(*sys.exc_info())))

ts1 = dt.datetime.now()
print('Total Time Elapsed: {}'.format(ts1-ts0))
