"""Game fix for Evil Genius 2"""

from .. import util


def main() -> None:
    """Launcher workaround"""
    # Fixes the startup process.
    util.replace_command('eg2.exe', '../bin/evilgenius_vulkan.exe')
