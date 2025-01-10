"""Hardwar"""

from protonfixes import util


def main() -> None:
    util.winedll_override('dinput', util.DllOverride.NATIVE_BUILTIN)  # DxWrapper component
    util.winedll_override('winmm', util.DllOverride.NATIVE_BUILTIN)  # Music playback
