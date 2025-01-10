"""Game fix for JUMP FORCE"""

from .. import util


def main() -> None:
    util.replace_command(
        'JUMP_FORCE.exe', 'JUMP_FORCE/Binaries/Win64/JUMP_FORCE-Win64-Shipping.exe'
    )
    util.append_argument('-eac-nop-loaded')

    util.protontricks('hidewineexports=enable')
