"""Game fix for Assassin's Creed: Brotherhood

Game uses an old customized Ubisoft launcher that's currently not working with Proton.
"""

from .. import util


def main() -> None:
    util.append_argument('-playoffline')
