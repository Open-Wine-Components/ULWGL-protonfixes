"""Silent Hill 4: The Room"""

from protonfixes import util


def main() -> None:
    # GOG's dxcfg / Steam006 fixes
    util.winedll_override('d3d8', util.DllOverride.NATIVE_BUILTIN)

    # Ultimate ASI Loader / Silent Hill 4 Randomizer
    util.winedll_override('dsound', util.DllOverride.NATIVE_BUILTIN)
