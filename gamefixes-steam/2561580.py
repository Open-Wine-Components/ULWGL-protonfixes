"""Game fix for Horizon Zero Dawn Remastered"""

from sys import argv
from os import environ
from .. import util


def main() -> None:
    """Won't connect to internet without using `-showlinkingqr` or `SteamDeck=1` options."""
    if environ.get('SteamDeck', '0') == '0' and '-showlinkingqr' not in argv:
        util.append_argument('-showlinkingqr')
