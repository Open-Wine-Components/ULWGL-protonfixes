"""Shin Megami Tensei III Nocturne HD Remaster
Missing voices/sounds in cutscenes
Requires disabling the gstreamer protonaudioconverterbin plugin to get full audio in cutscenes.
fixed Persona 5 Strikers by Swish in Protondb
"""

from .. import util


def main() -> None:
    util.disable_protonmediaconverter()
