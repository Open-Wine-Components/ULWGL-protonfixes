"""Atelier Rorona ~The Alchemist of Arland~ DX
Missing voices/sounds in cutscenes
Requires disabling the gstreamer protonaudioconverterbin plugin to get full audio in cutscenes.
fixed by Swish in Protondb
further stolen from marianoag by bitwolf
"""

from .. import util


def main() -> None:
    util.disable_protonmediaconverter()
