"""Game fix for From Dust"""

from .. import util


def main() -> None:
    """Game will get stuck on initial loading screen unless these are disabled"""
    util.disable_esync()
    util.disable_fsync()
