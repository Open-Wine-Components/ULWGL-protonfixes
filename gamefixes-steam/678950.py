"""Game fix for DRAGON BALL FighterZ"""

from .. import util


def main() -> None:
    util.replace_command('DBFighterZ.exe', 'RED/Binaries/Win64/RED-Win64-Shipping.exe')
    util.append_argument('-eac-nop-loaded')

    util.protontricks('hidewineexports=enable')
