"""Game fix for Rise of Nations: Extended Edition
Source: https://github.com/simons-public/protonfixes/issues/24#issue-372384148
"""

from .. import util


def main() -> None:
    """Installs crypt32 and and bypasses launcher"""
    # Install crypt32 (not required for Proton 3.16-3 and up)
    util.protontricks('crypt32')

    # Install DirectMusic
    util.protontricks('directmusic')

    # Set sound to alsa
    util.protontricks('sound=alsa')

    # Install DirectPlay for reliable multiplayer connections
    util.protontricks('directplay')

    # Disable launcher
    util.replace_command('patriots.exe', 'riseofnations.exe')
