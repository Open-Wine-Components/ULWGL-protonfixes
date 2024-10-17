"""Game fix for Doom 2016"""

import urllib.request
import zipfile

from protonfixes import util


def main() -> None:
    # Enable preload options
    util.append_argument('+r_renderAPI 1')
    install_ccel()


def install_ccel() -> None:
    install_path = util.get_game_install_path()
    cchroma_file = install_path / 'CChromaEditorLibrary.dll'
    cchroma_copy = cchroma_file.with_suffix('.dll.bak')

    if cchroma_copy.is_file():
        return

    # Download and backup
    url = 'https://github.com/Riesi/CChromaEditor/files/2277158/CChromaEditorLibrary.zip'
    urllib.request.urlretrieve(url, 'CChromaEditorLibrary.zip')
    cchroma_file.rename(cchroma_copy)

    # Extract
    with zipfile.ZipFile('CChromaEditorLibrary.zip', 'r') as zip_ref:
        zip_ref.extractall(install_path)
