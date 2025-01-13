"""Game fix for Fable III"""

import shutil

from protonfixes import util
from protonfixes.logger import log


def main() -> None:
    # https://www.reddit.com/r/SteamDeck/comments/vuagy2/finally_got_fable_3_working/
    util.protontricks('xliveless')

    # Remove Windows Live folder
    dirpath = (
        util.protonprefix() /
        'drive_c'
        'Program Files'
        'Common Files'
        'Microsoft Shared'
        'Windows Live'
    )
    if dirpath.is_dir():
        shutil.rmtree(dirpath)
    else:
        log.info(f"Path '{dirpath}' could not be found")
