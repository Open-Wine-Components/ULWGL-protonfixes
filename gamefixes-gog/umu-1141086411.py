"""Silent Hill 4: The Room"""

from .. import util


def main() -> None:
    util.winedll_override('d3d8', 'n,b')  # GOG's dxcfg / Steam006 fixes
    util.winedll_override(
        'dsound', 'n,b'
    )  # Ultimate ASI Loader / Silent Hill 4 Randomizer
