"""Game fix for Silent Hill 3"""

from .. import util


def main() -> None:
    # Needs directmusic for some cutscenes
    util.protontricks('directmusic')
    util.winedll_override('dsound', 'builtin')
