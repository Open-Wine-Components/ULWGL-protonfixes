"""Game fix for Carnage Cross
Proton issue: https://github.com/ValveSoftware/Proton/issues/6645
"""

from .. import util


def main() -> None:
    util.replace_command(
        'CarnageCross/CarnageCross',
        'CarnageCross/CarnageCross/Binaries/Win64/CarnageCross-Win64-Shipping.exe',
    )
