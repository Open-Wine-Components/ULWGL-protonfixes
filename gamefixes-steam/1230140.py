"""Game fix for ATRI -My Dear Moments-"""

from .. import util


def main() -> None:
    # Fix in-game media playback
    # See https://github.com/Open-Wine-Components/umu-protonfixes/issues/111#issuecomment-2317389123
    util.disable_protonmediaconverter()
    util.append_argument('-vomstyle=overlay')
