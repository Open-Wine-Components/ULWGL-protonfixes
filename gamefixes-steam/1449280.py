"""Game fix for Ghostbusters: The Video Game Remastered (2019)"""

from protonfixes import util
from protonfixes.logger import log


def main() -> None:
    # This directory is required to make the game settings persistent
    # [source: https://www.pcgamingwiki.com/wiki/Ghostbusters:_The_Video_Game_Remastered#Game_settings_do_not_save]
    save_dir = (
        util.protonprefix()
        / 'drive_c/users/steamuser/Local Settings/'
          'Application Data/GHOSTBUSTERS'
    )

    try:
        save_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        log.warn(f"Not able to make the settings directory at '{save_dir}': {e}")
