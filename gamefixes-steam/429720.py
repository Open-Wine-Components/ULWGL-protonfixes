"""Game fix for IMSCARED"""

import shutil

from pathlib import Path
from protonfixes import util


def main() -> None:
    # IMSCARED relies on a folder on the user's Desktop being accessible
    # The problem is that all of the folders in Proton are sandboxed
    # So this protonfix works around that
    desktop_path = util.protonprefix() / 'drive_c/users/steamuser/Desktop'

    if desktop_path.is_symlink():
        desktop_path.unlink()
    elif desktop_path.is_dir():
        shutil.rmtree(desktop_path)

    target = Path.home() / 'Desktop'
    desktop_path.symlink_to(target)
