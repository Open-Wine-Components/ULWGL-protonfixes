"""Game fix for Syberia"""

from pathlib import Path


def main() -> None:
    """Needs player.ini to prevent black screen on load"""
    ini_file = Path('player.ini')
    if ini_file.is_file():
        return
    
    ini_file.write_text('800 600 32 0 BaseCMO.cmo', 'utf-8')
