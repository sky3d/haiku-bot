import os
import json
import logging
from datetime import datetime, timedelta
from random import randint
from core.http_request import get_request

#JPCALENDAR_API_URL = 'http://jpcalendar.herokuapp.com/api/2.0'

log = logging.getLogger()

cal_data = json.loads(open('data/calendar2016.json').read())


def _parse_month_day(params=None):
    if not params:
        now = datetime.today()
        return tuple([now.month, now.day])
    try:
        parts = params.split(' ')
        mm = int(parts[0])
        dd = int(parts[1])
        return tuple([mm, dd])
    except Exception as ex:
        return None


def find_calendar_haiku(params=None):
    try:
        mm_dd = _parse_month_day(params)
        if mm_dd:
            dt = datetime(2016, mm_dd[0], mm_dd[1])
        else:
            dt = datetime(2016, 1, 1) + timedelta(randint(1, 365) - 1)

        # WEB VERION
        #url = '/year/2016/month/{0}/day/{1}'.format(dt.month, dt.day)
        #res = get_request(JPCALENDAR_API_URL + url)

        #data = json.loads(res)

        # LOCAL VERSION
        data = cal_data['2016{:02d}{:02d}'.format(dt.month, dt.day)]

        verse = data['verses'][0]
        url = os.environ.get('CALENDAR_IMAGE_HOST') + data['imageurl'] # url = data['imageurl']

        info = '({0}, {1} )'.format(verse['author'], verse['published'])
        lines = '\n'.join(verse['text'] + [info])
        return lines, url
    except Exception as err:
        log.error(err)
        return None
