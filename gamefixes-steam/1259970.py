"""Game fix for Pes 2021"""

from .. import util


def main() -> None:
    # Replace launcher with game exe in proton arguments
    util.protontricks('vcrun2019')
    util.protontricks('allfonts')
    util.protontricks('dotnet462')
