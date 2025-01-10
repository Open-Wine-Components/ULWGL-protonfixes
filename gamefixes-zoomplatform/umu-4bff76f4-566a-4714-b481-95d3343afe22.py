"""Incoming Trilogy"""

from .. import util


def main() -> None:
    util.winedll_override('d3d8', 'n,b')
    util.winedll_override('ddraw', 'b')
    util.winedll_override('winmm', 'n,b')
