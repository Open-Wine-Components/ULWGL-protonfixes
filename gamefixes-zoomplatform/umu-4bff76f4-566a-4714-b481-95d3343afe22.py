"""Incoming Trilogy"""

from protonfixes import util


def main() -> None:
    util.winedll_override('d3d8', util.DllOverride.NATIVE_BUILTIN)
    util.winedll_override('ddraw', util.DllOverride.BUILTIN)
    util.winedll_override('winmm', util.DllOverride.NATIVE_BUILTIN)
