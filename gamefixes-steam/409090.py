"""The Big Secret of a Small Town
No cursor or double cursor selecting custom cursor in options
PROTON_USE_WINED3D=1 fixes the problem but removes the antialising
dgvoodoo2 fixes the cursors and keeps the antialising
copy dgvoodoo2 d3d9.dll every time otherwise it gets overwritten
"""

import shutil
from protonfixes import util


def main() -> None:
    if util.protontricks('dgvoodoo2'):
        util.patch_voodoo_conf()

    wow64_path = util.get_path_syswow64()
    shutil.copy(wow64_path / 'dgd3d9.dll', wow64_path / 'd3d9.dll')
