"""Game fix for PixARK"""

from .. import util


def main() -> None:
    """Overrides the mprapi.dll to native."""
    util.winedll_override('mprapi', 'x')
