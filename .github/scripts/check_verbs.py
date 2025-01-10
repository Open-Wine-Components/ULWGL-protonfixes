"""This provides a check, if all used verbs are valid. It also warns if local verbs are unused."""

import os
import re
import subprocess

from pathlib import Path
from tempfile import mkdtemp
from collections.abc import Generator

# 'gui' is a virtual verb for opening the Winetricks GUI
# 'vd=1280x720' is a setting for the virtual desktop and valid
whitelist_verbs = {'gui', 'vd=1280x720'}


def extract_verbs_from_glob(path_glob: Generator[Path, None, None]) -> set[str]:
    """Simply strip the extension from all found files."""
    return {file.stem for file in path_glob}


def find_verbs(root: Path) -> set[str]:
    """Find all used verbs in gamefixes"""
    verbs: set[str] = set()
    game_fixes = root.glob('gamefixes-*/*.py')

    for fix in game_fixes:
        f = fix.read_text()
        r = re.finditer(
            r"util\.protontricks\s*\(\s*('|\")(?P<verb>.*)\1\s*\)", f, re.MULTILINE
        )
        for match in r:
            verbs.add(match.group('verb'))

    return verbs


def find_valid_verbs(root: Path) -> set[str]:
    """Winetricks will create temporary files with metadata, these include all valid verbs."""
    # Check if winetricks is present and executable
    wt_path = root.joinpath('winetricks')
    if not wt_path.is_file() or not os.access(wt_path, os.X_OK):
        raise FileNotFoundError('Winetricks can not be found or is not executable')

    # Provide a valid path to create the metadata to winetricks
    tmp_dir = Path(mkdtemp())
    if not tmp_dir.is_dir() or not os.access(tmp_dir, os.W_OK):
        raise PermissionError(f'Can not write into temporary folder "{tmp_dir}".')

    # Setup environment variables
    env = os.environ.copy()
    env['TMPDIR'] = str(tmp_dir)
    env['WINETRICKS_LATEST_VERSION_CHECK'] = 'disabled'

    # Execute winetricks, suppress output
    print(f'Executing winetricks, using tmp path "{tmp_dir}" - this may take a moment.')
    subprocess.run(
        [wt_path, '--no-clean', 'list-all'], env=env, stdout=subprocess.DEVNULL
    )

    # Get all verbs
    vars_glob = tmp_dir.glob('**/*.vars')
    return extract_verbs_from_glob(vars_glob)


def main() -> None:
    """Validate winetricks and protontricks verbs."""
    # Top-level project directory that is expected to contain gamefix directories
    project = Path(__file__).parent.parent.parent
    print(project)

    # Find all verbs that we use
    verbs = find_verbs(project)

    # Find verbs that are in winetricks
    valid_verbs = find_valid_verbs(project)

    # Additionally, we need to include our own verbs.
    valid_verbs_local = extract_verbs_from_glob(project.glob('verbs/*.verb'))

    print(f'Local verbs: {len(valid_verbs_local)}')
    print(f'Winetricks verbs: {len(valid_verbs)}')
    print(f'Unique verbs used: {len(verbs)}')

    # Check for unused local verbs
    unused_local_verbs = valid_verbs_local - verbs
    if unused_local_verbs:
        print(f'WARNING: The following local verbs are unused: {unused_local_verbs}')

    # Compare the results
    # FIXME: Implement a more robust mechanism for "setting" type verbs (eg. "vd")
    invalid_verbs = verbs - (valid_verbs | valid_verbs_local | whitelist_verbs)
    if invalid_verbs:
        raise ValueError(f'The following verbs are invalid: {invalid_verbs}')

    print('All verbs are valid!')


if __name__ == '__main__':
    main()
