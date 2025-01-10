"""Game fix for Re-Volt (287310)"""

from protonfixes import util


def main() -> None:
    """Sets the necessary dll overrides for the wrappers that are shipped with the game"""
    # Set overrides
    util.winedll_override('ddraw', util.DllOverride.NATIVE)
    util.winedll_override('dinput', util.DllOverride.NATIVE)
