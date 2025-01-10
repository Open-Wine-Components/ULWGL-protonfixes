"""Game fix for Command & Conquer Red Alert™ 2 and Yuri's Revenge™"""

import os

from .. import util
from ..logger import log


def main() -> None:
    """Install and launch the CnCNet Launcher

    It fixes several issues, allows multiplayer and provides a working UI,
    while the game has sometimes problems like missing or shifted buttons.

    The game will just show a black screen without cnc-ddraw or the patch in place.
    """
    # Opt out of CnCNet with 'NO_CNCNET=1 %command%'
    no_cncnet = os.getenv('NO_CNCNET', '')
    if str.lower(no_cncnet) in ['y', 'yes', 'true', 'on', '1']:
        log("Skipping CnCNet on user's request.")
        use_cnc_ddraw()
        return

    # Install the CnCNet Launcher
    if not util.checkinstalled('cncnet_ra2') and not util.protontricks('cncnet_ra2'):
        log("Failed to install CnCNet Launcher, let's try cnc-ddraw.")
        use_cnc_ddraw()

    # CnCNet Launcher is in place, run it
    if os.path.isfile('CnCNetYRLauncher.exe'):
        log('CnCNet Launcher found, bypass game execution!')
        util.replace_command('Ra2.exe', 'CnCNetYRLauncher.exe')
        util.replace_command('RA2MD.exe', 'CnCNetYRLauncher.exe')


def use_cnc_ddraw() -> None:
    """Install cnc-ddraw, the current replacement from EA isn't working."""
    log('Using cnc-ddraw.')

    # Return early, if cnc-ddraw is installed
    if util.checkinstalled('cnc_ddraw'):
        log('cnc-ddraw found, nothing to do!')
        return

    # Install cnc-ddraw
    if not util.protontricks('cnc_ddraw'):
        log('Failed to install cnc-ddraw')
        return

    # After installing cnc_ddraw, we need to prevent the game
    # from loading the local ddraw.dll, instead of our override.
    # Note: This is only done once.
    if os.path.isfile('ddraw.dll'):
        log('Renaming local ddraw.dll to ddraw.dll.bak')
        os.rename('ddraw.dll', 'ddraw.dll.bak')
