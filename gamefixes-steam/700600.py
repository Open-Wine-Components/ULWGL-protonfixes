"""Game fix for Evil Genius 2"""

from protonfixes import util


def main():
    """Launcher workaround"""

    # Fixes the startup process.
    util.replace_command('eg2.exe', '../bin/evilgenius_vulkan.exe')
