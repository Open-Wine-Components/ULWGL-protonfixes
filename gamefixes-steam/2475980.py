"""Gobliiins 5 (and Demo - 2505910)
Setup doesn't work and language is default to french
"""

from protonfixes import util


def main_with_id(game_id: str) -> None:
    """The game consists of 4 parts, that are located in their own folder
    They each have a separate config, that needs to be patched

    The demo launches from it's install directory and doesn't need a subfolder
    """
    cfg_str = """
    [language]
    translation=English

    [graphics]
    filter=Linear
    """

    # Demo
    if game_id == '2505910':
        util.set_ini_options(cfg_str, 'acsetup.cfg', 'utf-8', 'game')#
        return

    # Full
    for i in range(1, 5):
        util.set_ini_options(cfg_str, f'Gobliiins5-Part{i}/acsetup.cfg', 'utf-8', 'game')
