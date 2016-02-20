import asyncio
import socket
from aiohttp import web
from aiohttp import log


# Thanks to aiohttp tests courtesy
# Here is a nice mocking server
class WebFunctionalSetupMixin:

    def setUp(self):
        self.handler = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        if self.handler:
            self.loop.run_until_complete(self.handler.finish_connections())
        try:
            self.loop.stop()
            self.loop.close()
        finally:
            asyncio.set_event_loop(None)

    def find_unused_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port

    async    def create_server(self, method, path, handler=None, ssl_ctx=None):
        app = web.Application(loop=self.loop)
        if handler:
            app.router.add_route(method, path, handler)

        port = self.find_unused_port()
        self.handler = app.make_handler(
            keep_alive_on=False,
            access_log=log.access_logger)
        srv = await self.loop.create_server(
            self.handler, '127.0.0.1', port, ssl=ssl_ctx)
        protocol = "https" if ssl_ctx else "http"
        url = "{}://127.0.0.1:{}".format(protocol, port) + path
        self.addCleanup(srv.close)
        return app, srv, url