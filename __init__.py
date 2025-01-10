"""Starts the protonfix module and runs fixes after pre-flight-checks"""

import os
import sys
import traceback

from . import fix
from .logger import log


def check_conditions() -> bool:
    """Determine, if the actual game was executed and protonfixes isn't deactivated.

    Returns:
        bool: True, if the fix should be executed.

    """    
    return len(sys.argv) >= 1 and \
        'STEAM_COMPAT_DATA_PATH' in os.environ and \
        'PROTONFIXES_DISABLE' not in os.environ and \
        'waitforexitandrun' in sys.argv[1]


def check_iscriptevaluator() -> bool:
    """Determine, if we were invoked while running "iscriptevaluator.exe".

    Returns:
        bool: True, if we were invoked while running "iscriptevaluator.exe".

    """    
    return len(sys.argv) >= 2 and \
        'iscriptevaluator.exe' in sys.argv[2]


if check_iscriptevaluator():
    log.debug('Skipping fix execution. We are running "iscriptevaluator.exe".')
elif not check_conditions():
    log.warn('Skipping fix execution. We are probably running an unit test.')
else:
    try:
        fix.main()

    # Catch any exceptions and print a traceback
    except Exception:
        sys.stderr.write('ProtonFixes ' + traceback.format_exc())
        sys.stderr.flush()
