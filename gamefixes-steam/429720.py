"""Game fix for IMSCARED"""

import os
import getpass
from .. import util


def main() -> None:
    # IMSCARED relies on a folder on the user's Desktop being accessible
    # The problem is that all of the folders in Proton are sandboxed
    # So this protonfix works around that
    desktoppath = os.path.join(util.protonprefix(), 'drive_c/users/steamuser/Desktop')
    if os.path.exists(desktoppath):
        if os.path.islink(desktoppath):
            os.unlink(desktoppath)
        else:
            os.rmdir(desktoppath)
    dst = '/home/' + getpass.getuser() + '/Desktop/'
    os.symlink(dst, desktoppath)
