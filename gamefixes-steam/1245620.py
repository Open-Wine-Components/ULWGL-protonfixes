"""Game fix for Elden Ring: Create the `DLC.bdt` and `DLC.bhd` files to work around the "Inappropriate activity detected" error for players that don't own the DLC"""

from pathlib import Path
from .. import util


def main() -> None:
    game_dir = Path(util.get_game_install_path()) / 'Game'
    # Create the DLC.bdt file if it doesn't already exist, which is known to fix Easy AntiCheat not working for players that don't own the DLC
    # A blank file is enough to get multiplayer working
    (game_dir / 'DLC.bdt').touch(exist_ok=True)
    # Now also needs DLC.bhd after 1.14 patch
    (game_dir / 'DLC.bhd').touch(exist_ok=True)
