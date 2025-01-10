"""Game fix for Naruto To Boruto"""

from .. import util


def main() -> None:
    util.replace_command(
        'NARUTO.exe', 'NARUTO/Binaries/Win64/NARUTO-Win64-Shipping.exe'
    )
    util.append_argument('-eac-nop-loaded')
    util.protontricks('hidewineexports=enable')
