"""The Big Secret of a Small Town
No cursor or double cursor selecting custom cursor in options
PROTON_USE_WINED3D=1 fixes the problem but removes the antialising
dgvoodoo2 fixes the cursors and keeps the antialising
copy dgvoodoo2 d3d9.dll every time otherwise it gets overwritten
"""

import os
import subprocess
import shutil
from .. import util


def main() -> None:
    syswow64 = os.path.join(util.protonprefix(), 'drive_c/windows/syswow64')
    if util.protontricks('dgvoodoo2'):
        subprocess.call(
            [
                f"sed -i '/[DirectX]/ {{/Resolution/s/max/unforced/}}' {syswow64}/dgvoodoo.conf"
            ],
            shell=True,
        )
    shutil.copy(
        os.path.join(syswow64, 'dgd3d9.dll'), os.path.join(syswow64, 'd3d9.dll')
    )
