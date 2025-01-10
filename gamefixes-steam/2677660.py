"""Game fix for Indiana Jones and the Great Circle"""

from .. import util


def main() -> None:
    """Bad performance on Nvidia due to VRAM under-utilization"""
    util.set_environment('__GL_13ebad', '0x1')
