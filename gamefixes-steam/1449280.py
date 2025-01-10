"""Game fix for Ghostbusters: The Video Game Remastered (2019)"""

from pathlib import Path
from .. import util
from ..logger import log


def main() -> None:
    # This directory is required to make the game settings persistent
    # [source: https://www.pcgamingwiki.com/wiki/Ghostbusters:_The_Video_Game_Remastered#Game_settings_do_not_save]
    save_dir = f'{util.protonprefix()}/drive_c/users/steamuser/Local Settings/Application Data/GHOSTBUSTERS'

    try:
        Path(save_dir).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        log(f"Not able to make the settings directory at '{save_dir}': {e}")
