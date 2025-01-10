"""Duke Nukem: Manhattan Project - Enhanced Edition"""

from .. import util


def main() -> None:
    util.winedll_override('d3d8', 'n,b')
    util.protontricks('vcrun2019')
