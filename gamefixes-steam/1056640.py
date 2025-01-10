"""Game fix for Phantasy Star Online 2"""

from .. import util


def main() -> None:
    util.set_environment('WINE_NO_OPEN_FILE_SEARCH', 'pso2_bin/data')
