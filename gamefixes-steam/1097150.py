"""Game fix for Fall Guys"""

from .. import util


def main() -> None:
    """Create symlink of eac so at the right location"""
    util.install_eac_runtime()
    util.set_environment('DOTNET_BUNDLE_EXTRACT_BASE_DIR', '')
