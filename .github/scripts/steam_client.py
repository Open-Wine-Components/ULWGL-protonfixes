"""Steam Client"""

import sys
from steam.client import SteamClient
from steam.core.msg import MsgProto
from steam.enums import EResult
from steam.enums.emsg import EMsg
from steam.utils.proto import proto_to_dict
from steam.core.connection import WebsocketConnection

class Steam:
    """Minimal implementation of the SteamClient package that allows app id validation"""

    def __init__(self) -> None:
        """Setup SteamClient and it's events

        Raises:
            ValueError: When the SteamClient fires it's "error" event

        """        
        self.logged_on_once = False

        self.steam = client = SteamClient()
        client.connection = WebsocketConnection()

        # FIXME: pyright outputs 'error: Object of type "None" cannot be called (reportOptionalCall)'
        @client.on(SteamClient.EVENT_ERROR) # pyright: ignore (reportOptionalCall)
        def handle_error(result: EResult) -> None:
            raise ValueError(f'Steam error: {repr(result)}')

        @client.on(SteamClient.EVENT_CONNECTED) # pyright: ignore (reportOptionalCall)
        def handle_connected() -> None:
            print(f'Connected to {client.current_server_addr}', file=sys.stderr)

        @client.on(SteamClient.EVENT_CHANNEL_SECURED) # pyright: ignore (reportOptionalCall)
        def send_login() -> None:
            if self.logged_on_once and self.steam.relogin_available:
                self.steam.relogin()

        @client.on(SteamClient.EVENT_DISCONNECTED) # pyright: ignore (reportOptionalCall)
        def handle_disconnect() -> None:
            print('Steam disconnected', file=sys.stderr)
            if self.logged_on_once:
                print('Reconnecting...', file=sys.stderr)
                client.reconnect(maxdelay=30)

        @client.on(SteamClient.EVENT_LOGGED_ON) # pyright: ignore (reportOptionalCall)
        def handle_after_logon() -> None:
            self.logged_on_once = True

        client.anonymous_login()


    def get_valid_appids(self, appids: set[int]) -> set[int]:
        """Queries Steam for the specified appids.

        Args:
            appids (set[int]): The app ids that should be validated

        Raises:
            ValueError: When the response is empty / unexpected

        Returns:
            set[int]: Only valid app ids will be returned

        """     
        # https://github.com/SteamRE/SteamKit/blob/master/SteamKit2/SteamKit2/Base/Generated/SteamMsgClientServerAppInfo.cs#L331
        resp = self.steam.send_job_and_wait(
            message=MsgProto(EMsg.ClientPICSProductInfoRequest),
            body_params={
                'apps': map(lambda x: {'appid': x}, appids),
                'meta_data_only': True,
            },
            timeout=15,
        )

        if not resp:
            err = 'Error retrieving appinfo from Steam'
            raise ValueError(err)

        data = proto_to_dict(resp)
        appids = {app['appid'] for app in data['apps']}

        return appids
