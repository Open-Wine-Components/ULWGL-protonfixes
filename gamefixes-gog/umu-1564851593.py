"""Game fix for Flowers - Le Volume Sur Hiver

This fixes the crash on startup and the in-game font by moving the text
injection framework files
"""

import os
from hashlib import sha256
from tempfile import mkdtemp
from urllib.request import urlopen
from zipfile import ZipFile, is_zipfile

from .. import util
from ..logger import log

# Archive containing the text injecting framework
arc = 'https://github.com/user-attachments/files/16136393/d3d9-2206220222.zip'

# Digest of the archive, d3d9.dll proxy and JSON
hashsum_arc = 'caed98ec44d4270290f0652502344a40c1d45216caa8935b41e7d9f461ae2d24'
hashsum_d3d9 = '17e1c6706c684b19d05e89b588ba5101bf3ee40429cecf803c6e98af9b342129'
hashsum_config = 'aecb441fdc9c9e2ba78df63dfbe14f48c31dfd5ad571adba988ba362fc814377'


def main() -> None:
    tmp = f'{mkdtemp()}/d3d9-2206220222.zip'
    install_dir = util.get_game_install_path()
    path_config = f'{install_dir}/config.json'
    path_dll = f'{install_dir}/d3d9.dll'
    hashsum = sha256()

    # Ensure that the text injection files do not already exist before opening
    if not os.path.isfile(path_config) or not os.path.isfile(path_dll):
        log.warn(
            f"File 'config.json' or 'd3d9.dll' not found in '{install_dir}', skipping..."
        )
        return

    config = open(path_config, mode='rb')
    dll = open(path_dll, mode='rb')

    # Check if the text injection framework files have already been replaced
    if (
        sha256(config.read()).hexdigest() == hashsum_config
        and sha256(dll.read()).hexdigest() == hashsum_d3d9
    ):
        log.info(
            "Fix for 'Flowers - Le Volume Sur Hiver' has already been applied, skipping..."
        )
        config.close()
        dll.close()
        return

    config.close()
    dll.close()

    # Download the archive
    with urlopen(arc, timeout=30) as resp:
        if resp.status != 200:
            log.warn(f'github returned the status code: {resp.status}')
            return

        with open(tmp, mode='wb', buffering=0) as file:
            chunk_size = 64 * 1024  # 64 KB
            buffer = bytearray(chunk_size)
            view = memoryview(buffer)

            while size := resp.readinto(buffer):
                file.write(view[:size])
                hashsum.update(view[:size])

    if hashsum_arc != hashsum.hexdigest():
        log.warn(f'Digest mismatch: {arc}')
        log.warn(f"Expected '{hashsum_arc}', skipping...")
        return

    if not is_zipfile(tmp):
        log.warn(f"Archive '{tmp}' is not zip, skipping...")
        return

    # Rename the old files and apply the fix
    randstr = os.urandom(16).hex()
    log.info(f"Renaming 'config.json' -> '.{randstr}.config.json.bak'")
    log.info(f"Renaming 'd3d9.dll' -> '.{randstr}.d3d9.dll.bak'")
    os.rename(path_config, f'{install_dir}/.{randstr}.config.json.bak')
    os.rename(path_dll, f'{install_dir}/.{randstr}.d3d9.dll.bak')

    with ZipFile(tmp, mode='r') as zipfile:
        log.info("Fixing in-game font for 'Flowers - Le Volume Sur Hiver'...")
        zipfile.extractall(install_dir)

    os.unlink(tmp)
