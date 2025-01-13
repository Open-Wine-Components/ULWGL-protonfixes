"""Game fix for Putt-Putt: Pep's Birthday Surprise"""

from protonfixes import util


def main() -> None:
    """The game doesn't run unless there is a CD-ROM drive attached."""
    util.create_dos_device()

    # sets up ID? exported from regedit
    util.regedit_add(
        'HKLM\\System\\MountedDevices',
        '\\??\\Volume{00000000-0000-0000-0000-000000000052}',
        'REG_BINARY',
        '2f746d7000',
    )

    # sets up dosdevice? exported from regedit
    util.regedit_add(
        'HKLM\\System\\MountedDevices',
        '\\DosDevices\\R:',
        'REG_BINARY',
        '5c005c002e005c0064003a000000',
    )
