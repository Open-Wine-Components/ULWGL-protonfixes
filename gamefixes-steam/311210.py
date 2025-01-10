"""Game fix for Black Ops III"""

from .. import util


def main() -> None:
    """Installs devenum, quartz, wmp9"""
    # If you have too many audio devices the game shows a black screen with audio only, this works around the issue.
    # https://www.reddit.com/r/blackops3/comments/3rpd4f/black_screen_with_only_audio_pc/
    util.protontricks('sound=alsa')
