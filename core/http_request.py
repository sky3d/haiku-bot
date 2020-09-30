from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
from core.logger import log

DEFAULT_LOAD_TIMEOUT = 2  # secs


def get_request(url):
    req = Request(url)
    try:
        response = urlopen(req, timeout=DEFAULT_LOAD_TIMEOUT)
        return response.read()
    except HTTPError as e:
        log.error('%s - %d %s' % (url, e.code, e.reason))
    except URLError as e:
        log.error('Server connection failed: %s' % e.reason)


def post_request(url, values):
    data = urlencode(values)
    data = data.encode('utf-8')
    req = Request(url, data)
    try:
        response = urlopen(req)
        return response.getcode()
    except HTTPError as e:
        log.error('%s - %d %s' % (url, e.code, e.reason))
    except URLError as e:
        log.error('Server connection failed: %s' % e.reason)
