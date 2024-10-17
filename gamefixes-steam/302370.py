"""Tex Murphy: Overseer
Digital Sound Initialization Error (Intel RSX 3D drivers are not installed)
LAV Filters for video and DgVoodoo for textures
edit registry to avoid ffdshow compatibility manager popup
"""

from protonfixes import util


def main() -> None:
    util.protontricks('rsx3d')

    if util.protontricks('lavfilters'):
        patch_lavfilter_registry()

    if util.protontricks('dgvoodoo2'):
        util.patch_voodoo_conf()


def patch_lavfilter_registry() -> None:
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
