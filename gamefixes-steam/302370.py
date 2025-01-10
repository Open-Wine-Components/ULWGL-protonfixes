"""Tex Murphy: Overseer
Digital Sound Initialization Error (Intel RSX 3D drivers are not installed)
LAV Filters for video and DgVoodoo for textures
edit registry to avoid ffdshow compatibility manager popup
"""

import os
import subprocess
from .. import util


def main() -> None:
    util.protontricks('rsx3d')
    if util.protontricks('lavfilters'):
        util.regedit_add(
            'HKEY_CURRENT_USER\\Software\\GNU\\ffdshow',
            'blacklist',
            'REG_SZ',
            'OVERSEER.EXE',
        )
        util.regedit_add(
            'HKEY_CURRENT_USER\\Software\\GNU\\ffdshow_audio',
            'blacklist',
            'REG_SZ',
            'OVERSEER.EXE',
        )
    if util.protontricks('dgvoodoo2'):
        syswow64 = os.path.join(
            util.protonprefix(), 'drive_c/windows/syswow64', 'dgvoodoo.conf'
        )
        subprocess.call(
            [f"sed -i '/[DirectX]/ {{/Resolution/s/max/unforced/}}' {syswow64}"],
            shell=True,
        )
