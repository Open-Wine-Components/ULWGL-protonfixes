"""Game fix for FFX/X-2 HD Remaster"""

import os
from .. import util


def main() -> None:
    # Game defaults to Japanese language, set this to English instead
    configpath = os.path.join(
        util.protonprefix(),
        'drive_c/users/steamuser/My Documents/SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster',
    )
    if not os.path.exists(configpath):
        os.makedirs(configpath)
    configgame = os.path.join(configpath, 'GameSetting.ini')
    if not os.path.isfile(configgame):
        with open(configgame, 'w+', encoding='utf-8') as f:
            f.write('Language=en')
