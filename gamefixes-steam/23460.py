"""Ceville
Works with dotnet35sp1 only, now without needing Proton5
Videos still don't work.
"""

import os
import subprocess
from .. import util


def main() -> None:
    util.protontricks('dotnet35sp1')
    # Videos play and audio works but screen is black.
    # util.protontricks('quartz')
    # util.protontricks('klite')
    if os.path.isdir('./data/shared/videos'):
        subprocess.call(['mv', './data/shared/videos', './data/shared/_videos'])
    util.winedll_override('libvkd3d-1', 'n')
