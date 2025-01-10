"""Game fix for Spider-Man: Shattered Dimensions"""

from .. import util


def main() -> None:
    """Installs d3dx9_43, xact"""
    # https://steamcommunity.com/app/231990/discussions/0/3198117312260185786/#c3470604115208907456
    util.protontricks('d3dx9_43')
    util.protontricks('xact')
