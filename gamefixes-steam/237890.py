"""Game fix for Agarest: Generations of War"""

from .. import util


def main() -> None:
    util.protontricks('wmp9')
    util.winedll_override('winegstreamer', '')
