"""Game fix for Serious Sam: The Random Encounter"""

from protonfixes import util


def main() -> None:
    """Installs directmusic and directplay"""
    util.protontricks('dmband')
    util.protontricks('dmime')
    util.protontricks('dmloader')
    util.protontricks('dmsynth')
    util.protontricks('dmstyle')
    util.protontricks('dmusic')
    util.protontricks('dsound')
    util.protontricks('dswave')
    util.protontricks('directplay')
    util.winedll_override('streamci', util.DllOverride.NATIVE)
