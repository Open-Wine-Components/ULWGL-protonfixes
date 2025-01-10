"""Street Racing Syndicate"""

from .. import util


def main() -> None:
    util.protontricks('lavfilters')  # fix videos
    util.winedll_override(
        'd3d9', 'n,b'
    )  # in case user uses the ThirteenAG widescreen fix
