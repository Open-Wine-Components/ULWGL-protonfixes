"""Game fix for Flowers - Le Volume Sur Printemps

This fix installs the font that should be bundled with the game in case it
does not get installed during the setup process. Without this fix, the default
font will be used which doesn't wrap correctly, resulting in the text breaking
outside its text box area.
"""

from hashlib import sha256
from subprocess import run

import __main__ as protonmain
from protonfixes import util
from protonfixes.logger import log


def main() -> None:
    env = protonmain.g_session.env.copy()
    wine = util.protondir() / 'files/bin/wine64'
    install_dir = util.get_game_install_path()

    # Font installer inside the `fonts` subdir
    font_installer = install_dir / 'font/overlock_mod_font_installer.exe'

    # Digest of the font installer
    hashsum = 'd3bd48162d91322c3d2861cdccc538955336eff7f0fe50eeafee1b7551a52152'

    if (util.protonprefix() / 'drive_c/windows/Fonts/Overlock-Mod.ttf').is_file():
        log.info("Font 'Overlock-Mod.ttf' already installed in prefix, skipping...")
        return

    if not font_installer.is_file():
        log.warn(f"Could not find '{font_installer}', skipping...")
        return

    # Verify file
    font_bytes = font_installer.read_bytes()
    font_digest = sha256(font_bytes).hexdigest()
    if font_digest != hashsum:
        log.warn(f'Digest mismatched: {font_installer}')
        log.warn(f"Expected '{hashsum}', got '{font_digest}', skipping...")
        return

    log.info("Installing font 'Overlock-Mod.ttf' in prefix...")
    ret = run(
        [wine, 'start', '/unix', font_installer, '/silent'],
        check=False,
        env=env,
    ).returncode

    if ret:
        log.warn(f"Running '{font_installer}' exited with the status code: {ret}")
