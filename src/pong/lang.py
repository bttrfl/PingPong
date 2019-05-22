import gettext

class localizer:
    

    @classmethod
    def init(cls, path):
        t = gettext.translation('ru', path, languages=['ru'])
        _ = t.gettext
        t.install()
        cls._en = {
            'play': "Play",
            'play_again': "Play again",
            'you_won': "You won!",
            'you_lost': 'You lost!',
            'sign_in': 'Sign in',
            'sign_out': 'Sign out',
            'sign_up': 'Sign up',
            'leaderboars': 'Leaderboard',
            'username': 'Username',
            'password': 'Password',
            'pong_online': 'Pong online'
            }
        cls._rus =  {k: _(cls._en[k]) for k in cls._en}


    @classmethod
    def localize(cls, lang):
        return cls._en if lang == "en" else cls._rus