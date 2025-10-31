from core.http_request import post_request
from core.logger import log
import bot.classic_haiku as jp
from bot.jpcalendar2016 import find_calendar_haiku
from bot.vesna86 import find_vesna_haiku
from core.command import is_command, parse_command_id, parse_command_params
from bot.description import BOT_START_INFO


API_ENDPOINT = 'https://api.telegram.org'


def get_calendar2016(params):
    found = find_calendar_haiku(params)
    if not found:
        return 'Пока не нашел 👻 Повторим?'
    text = found[0]
    url = found[1]
    return '\n'.join([text, url])


def get_vesna86(params):
    found = find_vesna_haiku(params)
    if not found:
        return 'Пока не нашел 👻 Повторим?'
    text = found[0]
    url = found[1]
    if url:
        return '\n'.join([text, url])
    return text


def send_message(token, chat_id, text):
    url = "{0}/bot{1}/sendMessage".format(API_ENDPOINT, token)
    values = {
        'chat_id': chat_id,
        'text': text
    }
    return post_request(url, values)


class TBot:
    def __init__(self, name, token):
        self.__name = name
        self.__token = token

    def __reg_consumer(self, update):
        msg = update.get('message')
        from_user = msg.get('from') if msg else None
        id = from_user.get('id') if from_user else None
        if not id:
            return

        f_name = from_user.get('first_name', '')
        l_name = from_user.get('last_name', '')
        u_name = from_user.get('username', '')

        log.info('[x] USER: {0} {1} {2} aka {3}'.format(id, f_name, l_name, u_name))

    @staticmethod
    def extract_chat_id(update):
        msg = update.get('message')
        chat = msg.get('chat') if msg else None
        return chat.get('id') if chat else None

    @staticmethod
    def extract_text(update):
        msg = update.get('message')
        return msg.get('text') if msg else None

    def handle_request(self, json_data):
        data = json_data
        self.__reg_consumer(data)

        text = self.extract_text(data)

        if not is_command(text):
            return {'ok': True}

        cmd_id = parse_command_id(text)
        params = parse_command_params(text)
        log.debug(params)

        text = ''
        if cmd_id == '/start':
            text = '\n'.join(BOT_START_INFO)

        if cmd_id == '/haiku':
            text = jp.find_classic_haiku(params)

        if cmd_id == '/tag':
            text = jp.find_tagged_haiku(params)

        if cmd_id == '/author':
            found = jp.find_authors(params)
            names = [author['author_name'] for author in found]
            text = '\n'.join(names)

        if cmd_id == '/get100':
            text = jp.find_100verses()

        if cmd_id == '/tanka':
            text = jp.find_tanka()

        if cmd_id == '/saigyo':
            text = jp.find_saigyo()

        if cmd_id == '/calendar':
            text = get_calendar2016(params)

        if cmd_id == '/vesna86':
            text = get_vesna86(params)

        if cmd_id == '/android':
            text = 'https://play.google.com/store/apps/details?id=edu.wbar.jpcalendar2016'

        chat_id = self.extract_chat_id(data)

        not_found_text = 'Не слышал о таком 👻'
        status_code = send_message(
            self.__token, chat_id, text if text else not_found_text)
        log.debug(status_code)
        return {'ok': status_code == 200}
