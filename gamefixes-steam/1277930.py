"""Game fix for Riddle Joker"""

from .. import util


def main() -> None:
    """Fixes in-game video playback for the intro and ending."""
    util.disable_protonmediaconverter()
