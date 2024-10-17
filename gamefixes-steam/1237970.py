"""Game fix for Titanfall 2"""

from protonfixes import util


def main() -> None:
    """Allow -northstar option to work"""
    # Path of backup file
    backup_file = util.get_game_install_path() / 'Titanfall2.exe.bak'

    # Restore original titanfall2.exe if NorthstarLauncher.exe was previously symlinked
    if backup_file.is_file():
        backup_file.rename(backup_file.with_suffix(''))
