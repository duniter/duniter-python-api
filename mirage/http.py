from aiohttp import web, log
import json
import socket


class Request:
    def __init__(self, method, url, content):
        self.url = url
        self.method = method
        self.content = content


def find_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


async def middleware_factory(_, handler):
    async def middleware_handler(request):
        try:
            resp = await handler(request)
            return resp
        except web.HTTPNotFound:
            return web.Response(
                status=404,
                body=bytes(
                    json.dumps({"ucode": 1001, "message": "404 error"}), "utf-8"
                ),
                headers={"Content-Type": "application/json"},
            )

    return middleware_handler


class HTTPServer:
    def __init__(self, port, loop):
        self.lp = loop
        self.requests = []
        self.app = web.Application(middlewares=[middleware_factory])

        self.handler = None
        self.runner = None
        self.port = find_unused_port() if not port else port

    def get_request(self, i):
        return self.requests[i]

    async def _handler(self, request, handle):
        await request.read()
        self.requests.append(Request(request.method, request.path, request.content))
        json_data, http_code = await handle(request)
        return web.Response(
            body=bytes(json.dumps(json_data), "utf-8"),
            headers={"Content-Type": "application/json"},
            status=http_code,
        )

    def add_route(self, req_type, url, handle):
        self.app.router.add_route(
            req_type, url, lambda request: self._handler(request, handle)
        )

    async def create_server(self, ssl_ctx=None):
        self.handler = web.AppRunner(
            self.app, keep_alive_on=False, access_log=log.access_logger,
        )

        self.port = find_unused_port()
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, "127.0.0.1", self.port)
        await site.start()

        protocol = "https" if ssl_ctx else "http"
        url = "{}://127.0.0.1:{}".format(protocol, self.port)
        return self.port, url

    async def close(self):
        await self.handler.shutdown()
        await self.runner.cleanup()
