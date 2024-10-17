"""Gabriel Knight 3: Blood of the Sacred, Blood of the Damned
Fix for Insert CD
Fixes graphical issues
Video errors in Sydney
Fixes email issues in Sydney
Widescreen supported (16:9/21:9, 32:9 not tested)
"""

from protonfixes import util


def main() -> None:
    # Create a symlink in dosdevices
    util.create_dos_device()

    util.protontricks('quartz')
    util.protontricks('amstream')

    # No errors but doesn't show videos on SYDNEY
    # util.protontricks('lavfilters')
    # Show videos but green background is visible
    util.protontricks('klite')

    # Everything after this call should only be executed once
    if not util.protontricks('dgvoodoo2'):
        return
    
    # Get width of resolution
    screen_width, screen_height = util.get_resolution()
    width = int(screen_width / screen_height * 768 // 1)

    # dgvoodoo2 config patches
    util.patch_voodoo_conf(value=util.ReplaceType('max', f'{width}x768/'))
    util.patch_voodoo_conf(value=util.ReplaceType('', f'{width}x768/,'), key='ExtraEnumeratedResolutions')

    # Registry
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
