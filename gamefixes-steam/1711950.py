"""GWENT: Rogue Mage"""

from .. import util


def main() -> None:
    """Installs mfc140

    mfc140 is necessary to start the game up. GOG login happens inside the Steam overlay.

    vcrun2019 enables full support of the prelauncher interface. GOG login inside the prelauncher.
    This prelauncher is not necessary for the Game. If only mfc is present, it's skipped.
    """
    util.protontricks('mfc140')
