"""Load configuration settings for protonfixes"""

from config_base import ConfigBase
from dataclasses import dataclass
from pathlib import Path

class Config(ConfigBase):
    """Configuration for umu-protonfix"""

    @dataclass
    class MainSection:
        """General parameters
        
        Attributes:
            enable_checks (bool): Run checks (`checks.py`) before the fix is executed.
            enable_global_fixes (bool): Enables included fixes. If deactivated, only local fixes (`~/.config/protonfixes/localfixes`) are executed.

        """

        enable_checks: bool = True
        enable_global_fixes: bool = True

    @dataclass
    class PathSection:
        """Path parameters

        Attributes:
            cache_dir (Path): The path that should be used to create temporary and cached files.

        """

        cache_dir: Path = Path.home() / '.cache/protonfixes'

    main: MainSection
    path: PathSection

config = Config(Path.home() / '.config/protonfixes/config.ini')
