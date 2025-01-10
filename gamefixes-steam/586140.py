"""BlazBlue Centralfiction
Missing voices/sounds in cutscenes
Requires disabling the gstreamer protonaudioconverterbin plugin to get full audio in cutscenes
"""

from .. import util


def main() -> None:
    util.disable_protonmediaconverter()
