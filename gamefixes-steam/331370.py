"""Game fix for Dauntless"""

from .. import util


def main() -> None:
    """Game needs SteamDeck=1 for EAC to work."""
    util.set_environment('SteamDeck', '1')
