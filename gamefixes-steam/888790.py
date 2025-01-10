"""Game fix for Sabbat of the Witch"""

from .. import util


def main() -> None:
    """Fixes in-game video playback for the intro and ending."""
    util.disable_protonmediaconverter()
    # Changes the video renderer to 'overlay' to prevent random crashes
    # See https://github.com/Open-Wine-Components/umu-protonfixes/pull/115#issuecomment-2319197337
    util.append_argument('-vomstyle=overlay')
