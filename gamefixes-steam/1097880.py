"""Game fix for Super Naughty Maid 2"""

from .. import util


def main() -> None:
    """Installs quartz, wmp9"""
    # The whole game is only videos and require wmp9 & quartz
    util.protontricks('quartz')
    util.protontricks('wmp9')
