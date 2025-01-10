"""The Wheel of Time"""

from .. import util


def main() -> None:
    util.winedll_override('ddraw', 'n,b')  # GOG's dxcfg
