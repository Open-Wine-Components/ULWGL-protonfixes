"""Cease to Breathe
Replace included nwjs (0.71) - which doesn't work - with 0.86
Fix cursor hitbox (set frame=false in package.json)
Updated from 0.85 that didn't display custom cursors.
"""

import shutil
import urllib.request
import zipfile
import hashlib

from pathlib import Path

from protonfixes import util
from protonfixes.logger import log


def main() -> None:
    util.replace_command('CTB.exe', 'nw.exe')
    install_dir = util.get_game_install_path()

    install_nwjs(install_dir)
    patch_package_json(install_dir)


def install_nwjs(install_dir: Path) -> None:
    if (install_dir / 'nw.exe').is_file():
        return

    url = 'https://dl.nwjs.io/v0.86.0/nwjs-v0.86.0-win-x64.zip'
    hashsum = 'ed2681847162e0fa457dd55e293b6f331ccd58acedd934a98e7fe1406c26dd4f'
    nwjs = Path(Path(url).name)
    urllib.request.urlretrieve(url, nwjs)

    # Check digest
    nwjs_sum = hashlib.sha256(nwjs.read_bytes()).hexdigest()
    if hashsum != nwjs_sum:
        log.warn(f"{nwjs} checksum doesn't match, fix not applied.")
        return

    # Install
    with zipfile.ZipFile(nwjs, 'r') as zip_ref:
        zip_ref.extractall(install_dir)
    nwjs_dir = install_dir / nwjs.with_suffix('')
    shutil.copytree(nwjs_dir, install_dir, dirs_exist_ok=True)
    shutil.rmtree(nwjs_dir)


def patch_package_json(install_dir: Path) -> None:
    json_file = install_dir / 'package.json'
    json = json_file.read_text()
    json = json.replace('"frame": true', '"frame": false', 1)
    json_file.write_text(json)
