"""Simple logging to stdout the same way Proton does"""

import os
import sys

from typing import Literal
from functools import lru_cache

# TypeAliases
LogLevelType = Literal['INFO', 'WARN', 'CRIT', 'DEBUG']

class Log:
    """Log to stderr for steam dumps"""

    pfx = f'ProtonFixes[{os.getpid()}]'

    @staticmethod
    @lru_cache
    def __get_color(level: LogLevelType) -> str:
        return {
            'RESET': '\u001b[0m',
            'INFO': '\u001b[34m',
            'WARN': '\u001b[33m',
            'CRIT': '\u001b[31m',
            'DEBUG': '\u001b[35m',
        }.get(level, '')

    @classmethod
    def __colorize(cls, msg: str, level: LogLevelType) -> str:
        color = cls.__get_color(level)
        reset = cls.__get_color('RESET')
        return f'{color}{msg}{reset}'

    @classmethod
    def __call__(cls, msg: str) -> None:
        """Allows the Log instance to be called directly"""
        cls.log(msg)

    @classmethod
    def log(cls, msg: str = '', level: LogLevelType = 'INFO') -> None:
        """Prints the log message to stdout the same way as Proton"""
        # To terminal
        print(cls.__colorize(f'{cls.pfx} {level}: {msg}', level), file=sys.stderr, flush=True)

        # To log file
        with open('/tmp/test', 'a', 1, encoding='utf-8') as testfile:
            print(f'{cls.pfx} {level}: {msg}', file=testfile)

    @classmethod
    def info(cls, msg: str) -> None:
        """Wrapper for printing info messages"""
        cls.log(msg, 'INFO')

    @classmethod
    def warn(cls, msg: str) -> None:
        """Wrapper for printing warning messages"""
        cls.log(msg, 'WARN')

    @classmethod
    def crit(cls, msg: str) -> None:
        """Wrapper for printing critical messages"""
        cls.log(msg, 'CRIT')

    @classmethod
    def debug(cls, msg: str) -> None:
        """Wrapper for printing debug messages"""
        if 'DEBUG' not in os.environ:
            return
        cls.log(msg, 'DEBUG')


log = Log()
