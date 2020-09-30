import os
from bot.t_bot import TBot

TOKEN = os.environ.get('TOKEN')


def load_bot():
    return TBot('classic_haiku_bot', TOKEN)
