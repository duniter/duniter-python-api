"""
Copyright  2014-2020 Vincent Texier <vit@free.fr>

DuniterPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DuniterPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio
import socket
import ssl
from typing import Tuple, Callable, Optional

from aiohttp import web


# Thanks to aiohttp tests courtesy
# Here is a nice mocking server
def find_unused_port() -> int:
    """
    Return first free network port

    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class WebFunctionalSetupMixin:
    def setUp(self) -> None:
        self.handler = None
        self.app = web.Application()
        self.runner = web.AppRunner(self.app)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self) -> None:
        if self.handler:
            self.loop.run_until_complete(self.handler.shutdown())
        if self.runner:
            self.loop.run_until_complete(self.runner.cleanup())
        try:
            self.loop.stop()
            self.loop.close()
        finally:
            asyncio.set_event_loop(None)

    async def create_server(
        self,
        method: str,
        path: str,
        handler: Optional[Callable] = None,
        ssl_ctx: Optional[ssl.SSLContext] = None,
    ) -> Tuple[web.Application, int, str]:
        """
        Create a web server for tests

        :param method: HTTP method type
        :param path: Url path
        :param handler: Callback function
        :param ssl_ctx: SSL context (https is used if not None)
        :return:
        """
        if handler:
            self.app.router.add_route(method, path, handler)

        await self.runner.setup()

        port = find_unused_port()
        site = web.TCPSite(self.runner, "127.0.0.1", port)
        await site.start()

        protocol = "https" if ssl_ctx else "http"
        url = "{}://127.0.0.1:{}".format(protocol, port) + path
        return self.app, port, url
