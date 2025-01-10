"""Game fix for BioShock 2 Remastered"""

from .. import util


def main() -> None:
    """Disable ESYNC and FSYNC"""
    # ESYNC and FSYNC causes low quality texture problems in all BioShock 1 and 2 versions (Original and Remastered).
    util.disable_esync()
    util.disable_fsync()
