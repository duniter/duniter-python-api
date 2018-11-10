import asyncio
import socket
import ssl
from typing import Tuple, Callable, Optional

from aiohttp import web


# Thanks to aiohttp tests courtesy
# Here is a nice mocking server
class WebFunctionalSetupMixin:

    def setUp(self) -> None:
        self.handler = None
        self.runner = None
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

    def find_unused_port(self) -> int:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    async def create_server(self, method: str, path: str, handler: Optional[Callable] = None,
                            ssl_ctx: Optional[ssl.SSLContext] = None) -> Tuple[web.Application, int, str]:
        """
        Create a web server for tests

        :param method: HTTP method type
        :param path: Url path
        :param handler: Callback function
        :param ssl_ctx: SSL context (https is used if not None)
        :return:
        """
        app = web.Application()
        if handler:
            app.router.add_route(method, path, handler)

        port = self.find_unused_port()
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, '127.0.0.1', port)
        await site.start()

        protocol = "https" if ssl_ctx else "http"
        url = "{}://127.0.0.1:{}".format(protocol, port) + path
        return app, port, url
