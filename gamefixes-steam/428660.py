"""Deliver us the Moon fix"""

from .. import util


def main() -> None:
    # Replace launcher with game exe in proton arguments
    util.replace_command(
        'MoonMan.exe', 'MoonMan/Binaries/Win64/MoonMan-Win64-Shipping.exe'
    )
