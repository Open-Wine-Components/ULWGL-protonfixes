"""Gabriel Knight 3: Blood of the Sacred, Blood of the Damned
Fix for Insert CD
Fixes graphical issues
Video errors in Sydney
Fixes email issues in Sydney
Widescreen supported (16:9/21:9, 32:9 not tested)
"""

import os
import subprocess
from .. import util


def main() -> None:
    dosdevice = os.path.join(util.protonprefix(), 'dosdevices/r:')
    if not os.path.exists(dosdevice):
        os.symlink('/tmp', dosdevice)  # create symlink for dosdevices
        util.regedit_add(
            'HKLM\\Software\\Wine\\Drives', 'r:', 'REG_SZ', 'cdrom', True
        )  # designate drive as CD-ROM, requires 64-bit access
    util.protontricks('quartz')
    util.protontricks('amstream')
    # No errors but doesn't show videos on SYDNEY
    # util.protontricks('lavfilters')
    # Show videos but green background is visible
    util.protontricks('klite')
    syswow64 = os.path.join(util.protonprefix(), 'drive_c/windows/syswow64')
    if util.protontricks('dgvoodoo2'):
        screen_width, screen_height = util.get_resolution()
        width = int(screen_width / screen_height * 768 // 1)
        subprocess.call(
            [
                f"sed -i '/[DirectX]/ {{/Resolution/s/max/{width}x768/}}' {syswow64}/dgvoodoo.conf"
            ],
            shell=True,
        )
        subprocess.call(
            [
                f"sed -i '/[DirectXExt]/ {{/ExtraEnumeratedResolutions/s/= /= {width}x768,/}}' {syswow64}/dgvoodoo.conf"
            ],
            shell=True,
        )
        util.regedit_add('HKCU\\Software\\Sierra On-Line')
        util.regedit_add('HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3')
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\App',
            'Run Count',
            'REG_DWORD',
            '0x1',
        )
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\Engine',
            'Full Screen',
            'REG_DWORD',
            '0x1',
        )
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\Engine',
            'Monitor',
            'REG_DWORD',
            '0x0',
        )
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\Engine',
            'Rasterizer',
            'REG_SZ',
            'detect',
        )
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\Engine',
            'Rasterizer GUID',
            'REG_SZ',
            '{00000000-0000-0000-0000-000000000000}',
        )
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\Engine',
            'Screen Height',
            'REG_DWORD',
            '0x300',
        )
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\Engine',
            'Screen Width',
            'REG_DWORD',
            hex(width),
        )
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\Engine\\Hardware',
            'Gamma',
            'REG_SZ',
            '1.5',
        )
        util.regedit_add(
            'HKCU\\Software\\Sierra On-Line\\Gabriel Knight 3\\Engine\\Hardware',
            'Surface Quality',
            'REG_SZ',
            'High',
        )
