"""Memento Mori
wmp11 (Fixes missing logo videos and problems with working videos)
hangs on logo without override
"""

from .. import util


def main() -> None:
    util.winedll_override('libvkd3d-1', 'n')
    util.protontricks('wmp11')
