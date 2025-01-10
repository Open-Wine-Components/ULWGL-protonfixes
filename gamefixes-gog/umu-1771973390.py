"""METAL GEAR SOLID"""

from protonfixes import util


def main() -> None:
    """Override for wrapper shipped with the game"""
    util.winedll_override('ddraw', util.DllOverride.NATIVE_BUILTIN)
    util.winedll_override('dinput', util.DllOverride.NATIVE_BUILTIN)
