"""Ceville
Works with dotnet35sp1 only, now without needing Proton5
Videos still don't work.
"""

from pathlib import Path
from protonfixes import util


def main() -> None:
    util.protontricks('dotnet35sp1')
    util.winedll_override('libvkd3d-1', 'n')

    # Videos play and audio works but screen is black.
    # util.protontricks('quartz')
    # util.protontricks('klite')
    video_path = Path('data/shared/videos')
    if video_path.is_dir():
        video_path.rename(video_path.with_name('_videos'))
