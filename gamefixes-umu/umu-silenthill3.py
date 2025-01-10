"""Game fix for Silent Hill 3"""

from protonfixes import util


def main() -> None:
    # Needs directmusic for some cutscenes
    util.protontricks('directmusic')
    util.winedll_override('dsound', util.DllOverride.NATIVE_BUILTIN)
