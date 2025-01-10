"""Rainbow Six Siege"""

from .. import util


def main() -> None:
    """Rainbow Six Siege needs vk_x11_override_min_image_count=2 for AMD, and overlay disabled for Vulkan"""
    util.disable_uplay_overlay()
    util.set_environment('vk_x11_override_min_image_count', '2')
