"""Game fix for Conan Exiles"""

from .. import util


def main() -> None:
    """Launcher workaround"""
    # Fixes the startup process.
    util.install_battleye_runtime()
    util.replace_command(
        'FuncomLauncher.exe', '../ConanSandbox/Binaries/Win64/ConanSandbox.exe'
    )
    util.append_argument('-BattlEye')
