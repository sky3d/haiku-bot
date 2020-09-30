import logging
from bot import load_bot

log = logging.getLogger()


def handler(request):
    if request.method == "POST":
        bot = load_bot()
        try:
            update = request.get_json(force=True, silent=True)
            return bot.handle_request(update)
        except Exception as err:
            logging.error('ERR! %s', repr(err))
            return {'ok': False}

    return {'ok': True}
