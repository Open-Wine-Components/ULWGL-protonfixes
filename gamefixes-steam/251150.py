"""Game fix for The Legend of Heroes: Trails in the Sky"""

from .. import util


def main() -> None:
    util.protontricks('quartz')  # Cutscene fixes
    util.protontricks('amstream')
    util.protontricks('lavfilters')
