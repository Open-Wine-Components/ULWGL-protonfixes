"""神都不良探 Underdog Detective"""

from .. import util


def main() -> None:
    util.protontricks('klite')
    util.winedll_override('winegstreamer', '')
    # it uses quartz instead of mfplat on win7
    util.protontricks('win7')
