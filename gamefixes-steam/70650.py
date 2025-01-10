"""Game fix for Worms: Blast"""

from .. import util


def main() -> None:
    """Installs directmusic to fix menu and game music"""
    util.protontricks('directmusic')
