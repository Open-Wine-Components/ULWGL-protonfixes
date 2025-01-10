"""Hardwar"""

from .. import util


def main() -> None:
    util.winedll_override('dinput', 'n,b')  # DxWrapper component
    util.winedll_override('winmm', 'n,b')  # Music playback
