"""BlazBlue Centralfiction
Missing voices/sounds in cutscenes
Requires disabling the gstreamer protonaudioconverterbin plugin to get full audio in cutscenes
"""

from protonfixes import util


def main():
    util.disable_protonmediaconverter()
