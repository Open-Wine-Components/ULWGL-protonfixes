"""Street Racing Syndicate"""

from protonfixes import util


def main() -> None:
    # fix videos
    util.protontricks('lavfilters')

    # in case user uses the ThirteenAG widescreen fix
    util.winedll_override('d3d9', util.DllOverride.NATIVE_BUILTIN)
