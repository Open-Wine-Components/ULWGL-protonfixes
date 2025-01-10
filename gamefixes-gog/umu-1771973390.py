"""METAL GEAR SOLID"""

from .. import util


def main() -> None:
    """Override for wrapper shipped with the game"""
    util.winedll_override('ddraw', 'n,b')
    util.winedll_override('dinput', 'n,b')
