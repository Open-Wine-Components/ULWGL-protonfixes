"""Game fix for Serious Sam 4"""

from pathlib import Path


def main() -> None:
    """Graphics API workaround"""
    lua_file = Path('UserCfg.lua')
    bak_file = lua_file.with_suffix('.lua.bak')

    if bak_file.is_file():
        return
    
    text = lua_file.read_text('utf-8')
    text += '\nsfx_strAPI = "OpenAL";'

    lua_file.rename(bak_file)
    lua_file.write_text(text, 'utf-8')
