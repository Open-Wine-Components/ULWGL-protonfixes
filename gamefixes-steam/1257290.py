"""Atelier Ryza 2: Lost Legends & the Secret Fairy
Missing voices/sounds in cutscenes
Requires disabling the gstreamer protonaudioconverterbin plugin to get full audio in cutscenes
"""

from .. import util


def main() -> None:
    util.disable_protonmediaconverter()
