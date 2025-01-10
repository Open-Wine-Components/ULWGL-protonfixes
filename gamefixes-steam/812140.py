"""Assassin's Creed: Odyssey"""

from .. import util


def main() -> None:
    # Disable uplay overlay and change close behavior
    # See https://github.com/Open-Wine-Components/umu-protonfixes/pull/94#issuecomment-2227475597
    util.disable_uplay_overlay()
