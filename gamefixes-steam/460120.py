"""Game fix for Megadimension Neptunia VII"""

from .. import util


# Fixes cinematics not showing or spawning in a different window
# also fixes cinematics not playing sound
def main() -> None:
    util.protontricks('quartz_feb2010')
    util.protontricks('wmp11')
    util.protontricks('qasf')
