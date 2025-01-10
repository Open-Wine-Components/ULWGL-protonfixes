import io
import os
import tempfile
import unittest
import urllib.request

from pathlib import Path
from unittest.mock import patch, mock_open

from . import fix


class TestProtonfixes(unittest.TestCase):
    def setUp(self):
        self.env = {
            'STORE': '',
            'SteamAppId': '',
            'SteamGameId': '',
            'STEAM_COMPAT_DATA_PATH': '',
            'UMU_ID': '',
            'DEBUG': '',
        }
        self.game_id = '1293820'
        self.pfx = Path(tempfile.mkdtemp())

    def tearDown(self):
        for key in self.env:
            if key in os.environ:
                os.environ.pop(key)
        if self.pfx.is_dir():
            if self.pfx.joinpath('steamapps').is_dir():
                self.pfx.joinpath('steamapps', 'appmanifest_1628350.acf').unlink(
                    missing_ok=True
                )
                self.pfx.joinpath('steamapps').rmdir()
            self.pfx.joinpath('game_title').unlink(missing_ok=True)
            self.pfx.rmdir()

    def testModuleName(self):
        """Pass a non-numeric game id

        Expects a string that refers to a module in gamefixes-umu
        """
        game_id = 'umu-default'
        result = fix.get_module_name(game_id)
        self.assertEqual(result, 'protonfixes.gamefixes-umu.umu-default')

    def testModuleNameNum(self):
        """Pass a numeric game id

        In this case, it's assumed the game is from Steam when the game id is
        numeric
        Expects a string that refers to a module in gamefixes-steam
        """
        game_id = '1091500'
        result = fix.get_module_name(game_id)
        self.assertEqual(result, f'protonfixes.gamefixes-steam.{game_id}')

    def testModuleNameNoneAndNumeric(self):
        """Pass a numeric gameid and set STORE

        In this case, when the game id is numeric, we always refer to a
        module in the gamefixes-steam.
        """
        game_id = '1091500'
        os.environ['STORE'] = 'none'
        result = fix.get_module_name(game_id)
        self.assertEqual(result, f'protonfixes.gamefixes-steam.{game_id}')

    def testModuleNameStoreAndNumeric(self):
        """Pass a numeric gameid and set STORE

        In this case, when the game id is numeric, we always refer to a
        module in gamefixes-steam
        When passed a valid store, that value should not be used
        """
        game_id = '1091500'
        os.environ['STORE'] = 'gog'
        result = fix.get_module_name(game_id)
        self.assertEqual(result, f'protonfixes.gamefixes-steam.{game_id}')

    def testModuleNameStore(self):
        """Pass a non-numeric game id and setting valid STORE

        For non-numeric game ids, the umu database should always be referenced
        Expects a string that refers to a module in gamefixes-$STORE
        """
        os.environ['STORE'] = 'GOG'
        game_id = 'umu-1091500'
        result = fix.get_module_name(game_id)
        self.assertEqual(result, f'protonfixes.gamefixes-gog.{game_id}')

    def testModuleNameNoStore(self):
        """Pass a non-numeric game id and setting an invalid STORE

        Expects a string that refers to a module in gamefixes-umu
        """
        os.environ['STORE'] = 'foo'
        game_id = 'umu-1091500'
        result = fix.get_module_name(game_id)
        self.assertEqual(result, f'protonfixes.gamefixes-umu.{game_id}')

    def testModuleNameStoreEmpty(self):
        """Pass a non-numeric game id and setting an empty store

        Expects a string that refers to a module in gamefixes-umu
        """
        os.environ['STORE'] = ''
        game_id = 'umu-1091500'
        result = fix.get_module_name(game_id)
        self.assertEqual(result, f'protonfixes.gamefixes-umu.{game_id}')

    def testModuleNameEmpty(self):
        """Pass empty strings for the game id and store"""
        os.environ['STORE'] = ''
        game_id = ''
        result = fix.get_module_name(game_id)
        # TODO Handle the empty string case in fix.py
        # While umu enforces setting a gameid, it would still be a good idea
        # to handle this case
        self.assertEqual(result, 'protonfixes.gamefixes-umu.')

    def testModuleNameDefault(self):
        """Pass a gameid and default=True"""
        game_id = '1091500'
        result = fix.get_module_name(game_id, default=True)
        self.assertEqual(result, 'protonfixes.gamefixes-steam.default')

    def testModuleNameLocal(self):
        """Pass a gameid and local=True"""
        game_id = '1091500'
        result = fix.get_module_name(game_id, local=True)
        self.assertEqual(result, f'localfixes.{game_id}')

    def testModuleNameLocalDefault(self):
        """Pass a gameid and set local=True,default=True

        In this case, the game id will be completely ignored
        """
        game_id = '1091500'
        result = fix.get_module_name(game_id, local=True, default=True)
        self.assertEqual(result, 'localfixes.default')

    def testGetGameSteamAppId(self):
        """Only set the SteamAppId

        Protonfixes depends on being supplied an app id when applying fixes
        to games.

        This appid is typically set by a client application, but the user can
        set it in some cases (e.g., umu-launcher).

        If the app id is numeric, then protonfixes will refer to the
        gamefixes-steam folder. Otherwise, the STORE environment variable will
        be used to determine which fix will be applied.
        """
        os.environ['SteamAppId'] = self.game_id
        result = fix.get_game_id()
        self.assertEqual(result, self.game_id)
        self.assertTrue(os.environ.get('SteamAppId'), 'SteamAppId was unset')

    def testGetGameUmuId(self):
        """Only set the UMU_ID"""
        os.environ['UMU_ID'] = self.game_id
        result = fix.get_game_id()
        self.assertEqual(result, self.game_id)
        self.assertTrue(os.environ.get('UMU_ID'), 'UMU_ID was unset')

    def testGetGameSteamGameId(self):
        """Only set the SteamGameId"""
        os.environ['SteamGameId'] = self.game_id
        result = fix.get_game_id()
        self.assertEqual(result, self.game_id)
        self.assertTrue(os.environ.get('SteamGameId'), 'SteamGameId was unset')

    def testGetGameCompatPath(self):
        """Only set the STEAM_COMPAT_DATA_PATH"""
        os.environ['STEAM_COMPAT_DATA_PATH'] = self.game_id
        result = fix.get_game_id()
        self.assertEqual(result, self.game_id)
        self.assertTrue(
            os.environ.get('STEAM_COMPAT_DATA_PATH'), 'STEAM_COMPAT_DATA_PATH was unset'
        )

    def testGetGameNone(self):
        """Set no environment variables

        Expect None to be returned
        """
        func = fix.get_game_id.__wrapped__  # Do not reference the cache
        self.assertTrue(
            'STEAM_COMPAT_DATA_PATH' not in os.environ, 'STEAM_COMPAT_DATA_PATH is set'
        )
        self.assertTrue('SteamGameId' not in os.environ, 'SteamGameId is set')
        self.assertTrue('UMU_ID' not in os.environ, 'UMU_ID is set')
        self.assertTrue('SteamAppId' not in os.environ, 'SteamAppId is set')
        result = func()
        self.assertFalse(result, 'None was not returned')

    def testGetStoreNameZoom(self):
        """Pass zoomplatform as store name

        The get_store_name function returns a string associated with a
        supported store in the umu database.

        The string will be used to display a message in the console to let the
        user know which fix will be applied.
        """
        store = 'zoomplatform'
        result = fix.get_store_name(store)
        self.assertIsInstance(result, str, 'Expected a str')
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameAmazon(self):
        """Pass amazon as store name"""
        store = 'amazon'
        result = fix.get_store_name(store)
        self.assertIsInstance(result, str, 'Expected a str')
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameEA(self):
        """Pass ea as store name"""
        store = 'ea'
        result = fix.get_store_name(store)
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameEGS(self):
        """Pass egs as store name"""
        store = 'egs'
        result = fix.get_store_name(store)
        self.assertIsInstance(result, str, 'Expected a str')
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameGOG(self):
        """Pass gog as store name"""
        store = 'gog'
        result = fix.get_store_name(store)
        self.assertIsInstance(result, str, 'Expected a str')
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameHumble(self):
        """Pass humble as store name"""
        store = 'humble'
        result = fix.get_store_name(store)
        self.assertIsInstance(result, str, 'Expected a str')
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameItchio(self):
        """Pass itchio as store name"""
        store = 'itchio'
        result = fix.get_store_name(store)
        self.assertIsInstance(result, str, 'Expected a str')
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameSteam(self):
        """Pass steam as store name"""
        store = 'steam'
        result = fix.get_store_name(store)
        self.assertIsInstance(result, str, 'Expected a str')
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameUbisoft(self):
        """Pass ubisoft as store name"""
        store = 'ubisoft'
        result = fix.get_store_name(store)
        self.assertIsInstance(result, str, 'Expected a str')
        self.assertTrue(result, 'Expected a value')

    def testGetStoreNameEmpty(self):
        """Pass an empty string as store name"""
        store = ''
        result = fix.get_store_name(store)
        self.assertFalse(result, 'Expected None')

    def testGetStoreNameFoo(self):
        """Pass a store that is not supported in umu"""
        store = 'jastusa'
        result = fix.get_store_name(store)
        self.assertFalse(result, 'Expected None')

    def testGetGameName(self):
        """Set UMU_ID and access the game_title file for its title

        The get_game_name function returns a string of the running game's
        title.

        It checks a few system paths in the user's system to try to
        determine it, and makes a callout to an owc endpoint to get an
        official title by its UMU_ID.
        """
        os.environ['UMU_ID'] = self.game_id
        os.environ['WINEPREFIX'] = self.pfx.as_posix()
        self.pfx.joinpath('game_title').touch()
        func = fix.get_game_name.__wrapped__  # Do not reference the cache
        result = func()
        self.assertFalse(result, 'Expected an empty string')

    def testGetGameNameDB(self):
        """Set UMU_ID and access umu database"""
        os.environ['UMU_ID'] = 'umu-35140'
        os.environ['STORE'] = 'gog'
        os.environ['WINEPREFIX'] = self.pfx.as_posix()

        # Mock CSV content
        csv_content = """Batman: Arkham Asylum Game of the Year Edition,gog,1482504285,umu-35140,,"""

        with patch('builtins.open', mock_open(read_data=csv_content)):
            func = fix.get_game_name.__wrapped__  # Do not reference the cache
            result = func()
            self.assertEqual(result, 'Batman: Arkham Asylum Game of the Year Edition')

    def testGetGameNameDBFileNotFound(self):
        """Set UMU_ID and simulate FileNotFoundError for the CSV file"""
        os.environ['UMU_ID'] = 'umu-35140'
        os.environ['STORE'] = 'gog'
        os.environ['WINEPREFIX'] = self.pfx.as_posix()

        with patch('builtins.open', mock_open()) as mocked_open:
            mocked_open.side_effect = FileNotFoundError
            with patch('protonfixes.fix.log') as mocked_log:  # Mock the logger separately
                func = fix.get_game_name.__wrapped__  # Do not reference the cache
                result = func()
                self.assertEqual(result, 'UNKNOWN')
                mocked_log.warn.assert_called_with(f"Game title not found in CSV")

    def testGetGameNameDbOS(self):
        """Set UMU_ID and simulate OSError when accessing the CSV file"""
        os.environ['UMU_ID'] = 'umu-35140'
        os.environ['STORE'] = 'gog'
        os.environ['WINEPREFIX'] = self.pfx.as_posix()

        with patch('builtins.open', mock_open()) as mocked_open:
            mocked_open.side_effect = OSError
            with patch('protonfixes.fix.log') as mocked_log:  # Mock the logger separately
                func = fix.get_game_name.__wrapped__  # Do not reference the cache
                result = func()
                self.assertEqual(result, 'UNKNOWN')
                mocked_log.warn.assert_called_with("Game title not found in CSV")

    def testGetGameNameDbIndex(self):
        """Set UMU_ID and simulate IndexError with malformed CSV data"""
        os.environ['UMU_ID'] = 'umu-35140'
        os.environ['STORE'] = 'gog'
        os.environ['WINEPREFIX'] = self.pfx.as_posix()

        # Mock CSV content with missing columns
        csv_content = """Batman: Arkham Asylum Game of the Year Edition,gog"""

        with patch('builtins.open', mock_open(read_data=csv_content)):
            func = fix.get_game_name.__wrapped__  # Do not reference the cache
            result = func()
            self.assertEqual(result, 'UNKNOWN')

    def testGetGameNameDbUnicode(self):
        """Set UMU_ID and simulate UnicodeDecodeError when reading the CSV file"""
        os.environ['UMU_ID'] = 'umu-35140'
        os.environ['STORE'] = 'gog'
        os.environ['WINEPREFIX'] = self.pfx.as_posix()

        with patch('builtins.open', mock_open()) as mocked_open:
            mocked_open.side_effect = UnicodeDecodeError('utf-8', b'', 0, 1, '')
            with patch('protonfixes.fix.log') as mocked_log:  # Mock the logger separately
                func = fix.get_game_name.__wrapped__  # Do not reference the cache
                result = func()
                self.assertEqual(result, 'UNKNOWN')
                mocked_log.warn.assert_called_with("Game title not found in CSV")

    def testGetGameNameNoManifest(self):
        """Do not set UMU_ID and try to get the title from the steam app library"""
        os.environ['SteamAppId'] = '1628350'
        os.environ['WINEPREFIX'] = self.pfx.as_posix()
        os.environ['PWD'] = os.environ['WINEPREFIX']
        steamapps = self.pfx.joinpath('steamapps')
        os.makedirs(steamapps, exist_ok=True)
        func = fix.get_game_name.__wrapped__  # Do not reference the cache
        result = func()
        self.assertEqual(result, 'UNKNOWN')

if __name__ == '__main__':
    unittest.main()
