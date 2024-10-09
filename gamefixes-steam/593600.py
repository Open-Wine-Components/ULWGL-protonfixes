"""Game fix for PixARK"""

from protonfixes import util


def main() -> None:
    """Overrides the mprapi.dll to native."""
    util.winedll_override('mprapi', 'n')
