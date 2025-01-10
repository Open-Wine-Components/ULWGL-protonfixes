"""Game fix for Trackmania Turbo"""

from .. import util


def main() -> None:
    """Game ships with outdated and not working uPlay launcher."""
    util.protontricks('ubisoftconnect')
