"""Game fix for Supreme Commander"""

from .. import util


def main() -> None:
    """Bad performance unless Esync and Fsync are disabled."""
    util.disable_esync()
    util.disable_fsync()
