"""Duke Nukem: Manhattan Project - Enhanced Edition"""

from protonfixes import util


def main():
    util.winedll_override('d3d8', 'n,b')
    util.protontricks('vcrun2019')
