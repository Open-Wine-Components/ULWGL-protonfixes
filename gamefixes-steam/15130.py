"""Game fix for Beyond Good and Evil"""

from .. import util


def main() -> None:
    """Installs dsound d3dx9 arial d3dcompiler_47"""
    util.protontricks('dsound')
    util.protontricks('d3dx9')
    util.protontricks('arial')
    util.protontricks('d3dcompiler_47')

    """ Add a couple of keys in regedit
    """

    util.regedit_add('HKLM\\Software\\Wow6432Node\\Ubisoft')
    util.regedit_add(
        'HKLM\\Software\\Wow6432Node\\Ubisoft\\Beyond Good & Evil',
        'InstallLanguage',
        'REG_DWORD',
        '1',
    )
