"""Game fix for Mini Ninjas"""

from .. import util


def main() -> None:
    """Game needs OpenAL library for audio to work, but the game doesn't include it by default, leading to missing audio in-game, even on Windows."""
    util.protontricks('openal')
