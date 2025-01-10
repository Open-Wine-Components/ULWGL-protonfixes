"""Game fix Dark Souls Prepare To Die Edition"""

from .. import util


def main() -> None:
    """Needs WMP9, devenum, quartz, dinput and win7"""
    # For main menu, intro and outro playback
    util.protontricks('devenum')
    util.protontricks('quartz')
    util.protontricks('wmp9')

    # In case if someone wishes to use DSfix
    util.protontricks('dinput8')

    util.protontricks('win7')
