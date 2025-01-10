"""Mod support for following Bethesda games:

- Fallout 3 - Game of the Year Edition
- Fallout 4
- Fallout: New Vegas
- The Elder Scrolls IV: Oblivion
- The Elder Scrolls V: Skyrim
- The Elder Scrolls V: Skyrim Special Edition
- Starfield
"""

import os

from dataclasses import dataclass
from .. import util


def main_with_id(game_id: str) -> None:
    """Enable modding and fixes"""
    # modorganizer2 features a redirector and breaks if we replace the command. (Issue #103)
    if os.path.exists('modorganizer2'):
        return

    # Run script extender if it exists.
    mapping = get_redirect_name(game_id)
    if os.path.isfile(mapping.to_name):
        util.replace_command(mapping.from_name, mapping.to_name)


@dataclass
class Redirect:
    """Used for replacements"""

    from_name: str
    to_name: str


def get_redirect_name(game_id: str) -> Redirect:
    """Mapping for SteamID -> script extender replacements"""
    mapping = {
        '22380': ('FalloutNV.exe', 'nvse_loader.exe'),  # Fallout New Vegas
        '22370': ('FalloutLauncher.exe', 'fose_loader.exe'),  # Fallout 3
        '377160': ('Fallout4Launcher.exe', 'f4se_loader.exe'),  # Fallout 4
        '22330': ('OblivionLauncher.exe', 'obse_loader.exe'),  # Oblivion
        '72850': ('SkyrimLauncher.exe', 'skse_loader.exe'),  # Skyrim
        '489830': ('SkyrimSELauncher.exe', 'skse64_loader.exe'),  # Skyrim SE
        '1716740': ('Starfield.exe', 'sfse_loader.exe'),  # Starfield
    }.get(game_id, ('', ''))
    return Redirect(*mapping)
