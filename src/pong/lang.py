import gettext
import sys
import os

__all__ = [
    "game_handler",
    "landing_handler",
    "show_leaderboard",
    "login_handler",
    "signup_handler",
    "logout_handler",
]

root = '../../lang'

t = gettext.translation('ru', root, languages=['ru'])
_ = t.gettext
t.install()

rus_cookies = {}

_en = {'title': "Ping Pong Game", 'Multiplayer': "Multiplayer", 'GOAL': "GOAL"}
_rus = {k: _(_en[k]) for k in _en}

def localize(cookie):
    if cookie in rus_cookies:
        return _rus
    return _en
