import json
import re
from random import choices, choice, randint
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from urllib.request import urlopen
from core.utils import calc_tokens, damerau_levenshtein_distance

jp_data = json.loads(open('data/japanpoetry_ru.json').read())

JAPAN_AUTHORS = jp_data['japan_classics']

VERSE100_COLLECTION = jp_data['collections'][0]
TANKA_COLLECTION = jp_data['collections'][1]
SAIGYO_COLLECTIONS = (jp_data['collections'][2], jp_data['collections'][3])

TAGS = jp_data['tags']
TAGS_KEYS = list(TAGS.keys())

JAPAN_POETRY_ROOT_URL = 'http://japanpoetry.ru'
CATALOG_PAGE_FORMAT = '/page-{0}-catalog'


def __load_haiku(url):
    data = urlopen(JAPAN_POETRY_ROOT_URL + url)
    soup = BeautifulSoup(data, "html5lib")

    result = []
    for item in soup.find_all('div', 'poetry'):
        title = item.find('div', 'title')
        author = title.find('a').text

        details = item.find('div', 'details')
        link_el = details.find('a')
        link = link_el['href'] if link_el else ''

        info = item.find('div', 'info')
        trans = info.find('a').text

        text = item.find('div', 'poetry_text')
        haiku = ''
        for el in text.children:
            if isinstance(el, NavigableString):
                haiku += el.string.strip() + '\n'

        result.append((link, trans, haiku, author))

    return result


def find_authors(name):
    if not name:
        return JAPAN_AUTHORS

    tokens = calc_tokens(name)
    patterns = [re.compile('%s' % t, re.IGNORECASE) for t in tokens]
    result = []
    for el in JAPAN_AUTHORS:
        author_name = el['author_name']
        if all([x.search(author_name) for x in patterns]):
            result.append(el)

    return result


def _random_haiku(list):
    n = min(1, len(list))
    result = choices(list, k=n)
    res = ''
    for verse in result:
        (link, trans, haiku, author) = verse
        res = '\n'.join([
            haiku,
            "{0} (пер. {1})".format(author, trans) if trans else author,
            JAPAN_POETRY_ROOT_URL + link
        ])

    return res


def find_classic_haiku(author):
    found = None
    if author:
        found = find_authors(author)

    author = found[0] if found else choice(JAPAN_AUTHORS)
    target_url = author['link']

    result = __load_haiku(target_url)
    return _random_haiku(result)


def find_tag_link(tag_name):
    if not tag_name:
        return None

    s = tag_name.lower()
    found = TAGS.get(s)

    if found:
        return found

    tags = list(TAGS.keys())
    for item in tags:
        n = damerau_levenshtein_distance(tag_name, item)
        if n < len(tag_name) * 0.4:
            return TAGS.get(item)

    return None


def find_tagged_haiku(tag_name):
    tag = find_tag_link(tag_name)
    if not tag:
        return 'Не найдено! 👻 Используйте:\n%s' % ', '.join(TAGS_KEYS)

    result = __load_haiku(tag)
    return _random_haiku(result)


def _find_collection_link(tag, page_count):
    page_no = randint(1, page_count)
    if page_no > 1:
        tag += CATALOG_PAGE_FORMAT.format(page_no)
    return tag


def find_tanka():
    link = TANKA_COLLECTION['link']
    page_count = TANKA_COLLECTION['page_count']

    tag = _find_collection_link(link, page_count)

    result = __load_haiku(tag)
    return _random_haiku(result)


def find_100verses():
    link = VERSE100_COLLECTION['link']
    page_count = VERSE100_COLLECTION['page_count']

    tag = _find_collection_link(link, page_count)

    result = __load_haiku(tag)
    return _random_haiku(result)


def find_saigyo():
    index = randint(0, 1)
    coll = SAIGYO_COLLECTIONS[index]

    link = coll['link']
    page_count = coll['page_count']

    tag = _find_collection_link(link, page_count)

    result = __load_haiku(tag)
    return _random_haiku(result)
