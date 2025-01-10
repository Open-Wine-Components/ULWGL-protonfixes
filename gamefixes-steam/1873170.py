"""Cease to Breathe
Replace included nwjs(0.71) wich doesn't work with 0.86
Fix cursor hitbox (set frame=false in package.json)
Updated from 0.85 that didn't display custom cursors.
"""

import os
import glob
import shutil
import urllib.request
import zipfile
import subprocess
import hashlib
from .. import util
from ..logger import log


def main() -> None:
    util.replace_command('CTB.exe', 'nw.exe')
    install_dir = glob.escape(util.get_game_install_path())
    if not os.path.isfile(os.path.join(install_dir, 'nw.exe')):
        url = 'https://dl.nwjs.io/v0.86.0/nwjs-v0.86.0-win-x64.zip'
        hashsum = 'ed2681847162e0fa457dd55e293b6f331ccd58acedd934a98e7fe1406c26dd4f'
        nwjs = os.path.basename(url)
        urllib.request.urlretrieve(url, nwjs)
        with open(nwjs, 'rb') as f:
            nwjs_sum = hashlib.sha256(f.read()).hexdigest()
        if hashsum == nwjs_sum:
            with zipfile.ZipFile(nwjs, 'r') as zip_ref:
                zip_ref.extractall(install_dir)
            nwjs = os.path.join(install_dir, nwjs.rsplit('.', 1)[0])
            shutil.copytree(nwjs, install_dir, dirs_exist_ok=True)
            shutil.rmtree(nwjs)
        else:
            log(f"{nwjs} checksum doesn't match, fix not applied.")
    subprocess.call(
        [f'sed -i \'s/"frame": true/"frame": false/\' "{install_dir}/package.json"'],
        shell=True,
    )
