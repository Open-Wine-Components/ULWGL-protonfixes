"""Game fix for The Legend of Heroes: Trails in the Sky"""

from protonfixes import util


def main() -> None:
    util.protontricks('quartz')  # Cutscene fixes
    util.protontricks('amstream')
    util.protontricks('lavfilters')
    util.winedll_override('dinput8', 'n,b')  # Set for the SoraVoice mod
