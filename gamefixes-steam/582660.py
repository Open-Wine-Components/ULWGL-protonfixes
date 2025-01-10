"""Game fix for Black Desert Online"""

import os
from .. import util


def main() -> None:
    """Black Desert Online add NOSTEAM option."""
    # Fixes the startup process.
    if 'NOSTEAM' in os.environ:
        util.replace_command('--steam', '')
    # Needed for settings archive
    util.set_environment('SteamGameId', '582660')
    # Needed for Launcher
    util.set_environment('WINE_DISABLE_KERNEL_WRITEWATCH', '1')
