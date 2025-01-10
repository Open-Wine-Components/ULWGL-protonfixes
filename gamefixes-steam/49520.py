"""Game fix for Borderlands 2"""

from .. import util


def main() -> None:
    """Launcherfix and NVIDIA PhysX support."""
    # Fixes the startup process.
    util.replace_command('Launcher.exe', 'Borderlands2.exe')
    util.append_argument('-NoSplash')

    # Disables esync prevents crashes.
    util.disable_esync()

    # Enables NVIDIA PhysX in Borderlands 2.
    util.protontricks('physx')
