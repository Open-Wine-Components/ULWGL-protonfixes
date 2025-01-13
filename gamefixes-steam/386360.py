"""Game fix for Smite"""

from protonfixes import util


def main() -> None:
    """Fix incorrect EAC locations in smite"""
    install_dir = util.get_game_install_path()
    eac_file_x64 = install_dir / 'Win64/EasyAntiCheat/easyanticheat_x64.so'
    eac_file_x86 = install_dir / 'Win32/EasyAntiCheat/easyanticheat_x86.so'

    # x64
    if not eac_file_x64.exists():
        eac_file_x64.symlink_to(install_dir / 'EasyAntiCheat/easyanticheat_x64.so')

    # x86
    if not eac_file_x86.exists():
        eac_file_x86.symlink_to(install_dir / 'EasyAntiCheat/easyanticheat_x86.so')
