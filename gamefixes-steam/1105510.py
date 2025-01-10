"""Game fix for Yakuza 5"""

from .. import util


def main() -> None:
    """Needs WINE_DISABLE_SFN set from this patch: https://github.com/ValveSoftware/wine/pull/205"""
    util.set_environment('WINE_DISABLE_SFN', '1')
