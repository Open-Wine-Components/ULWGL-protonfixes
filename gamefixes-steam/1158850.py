"""The Great Ace Attorney Chronicles
Missing sound in bonus content videos
Requires disabling the gstreamer protonaudioconverterbin to get full audio
"""

from .. import util


def main() -> None:
    util.disable_protonmediaconverter()
