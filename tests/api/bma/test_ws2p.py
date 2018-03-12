import unittest
import aiohttp
import jsonschema
import json
from duniterpy.documents import BMAEndpoint
from tests.api.webserver import WebFunctionalSetupMixin, web, asyncio
from duniterpy.api.bma.network import heads, WS2P_HEADS_SCHEMA
from duniterpy.api.bma import parse_text


class Test_WS2P_Heads(WebFunctionalSetupMixin, unittest.TestCase):

    def test_block(self):
        json_sample = {
  "heads": [
    {
      "message": "WS2POCAIC:HEAD:1:8iVdpXqFLCxGyPqgVx5YbFSkmWKkceXveRd2yvBKeARL:102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:e66254bf:duniter:1.6.20:1",
      "sig": "ZO5gSUMK6IaUEwU4K40nhuHOfnJ6Zfn8VS+4Ko2FM7t+mDsHf+3gDRT9PgV2p0fz81mF6jVYWpq2UYEsnK/gCg==",
      "messageV2": "WS2POCAIC:HEAD:2:8iVdpXqFLCxGyPqgVx5YbFSkmWKkceXveRd2yvBKeARL:102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:e66254bf:duniter:1.6.20:1:15:14",
      "sigV2": "ReXzbgUya9jo4dL/R4g19Y+RE9BGB0xDkw7mrBWoldlRLkq3KFyRkAf9VthVx1UUb/AINr3nxImZKVQiVH9+DQ==",
      "step": 0
    },
    {
      "message": "WS2POCAIC:HEAD:1:2ny7YAdmzReQxAayyJZsyVYwYhVyax2thKcGknmQy5nQ:102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:a0a45ed2:duniter:1.6.21:1",
      "sig": "pXLMmOpyEMdWihT183g/rnCvMzA2gHki5Cxg7rEl3psQu0RuK0ObCv5YFhmQnRlg+QZ1CWfbYEEbm3G1eGplAQ==",
      "messageV2": "WS2POCAIC:HEAD:2:2ny7YAdmzReQxAayyJZsyVYwYhVyax2thKcGknmQy5nQ:102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:a0a45ed2:duniter:1.6.21:1:34:28",
      "sigV2": "p5f7/KfQqjTaCYSMUXpjUDH7uF2DafetHNgphGzkOXgxM+Upeii0Fz2RFBwnZvN+Gjp81hAqSuH48PJP6HJSAw==",
      "step": 1
    },
    {
      "message": "WS2POCA:HEAD:1:GRBPV3Y7PQnB9LaZhSGuS3BqBJbSHyibzYq65kTh1nQ4:102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:6d0e96f9:duniter:1.6.21:1",
      "sig": "h9o1XBEV18gUzbvj1jdQB1M7U8ifZprIyVwLdlSQEfeG9WZLvZAjYzLGA2nD6h/9RkJLOJPzIQJXysHUHJ2dDQ==",
      "messageV2": "WS2POCA:HEAD:2:GRBPV3Y7PQnB9LaZhSGuS3BqBJbSHyibzYq65kTh1nQ4:102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:6d0e96f9:duniter:1.6.21:1:20:20",
      "sigV2": "VsyQmXOUYrfHWy0FeS4rJrIJCUBI+3BergbSYQ78icJWV6MQzZSw7Z+Yl7urujCYZriDQM76D6GW+6F0EELpBQ==",
      "step": 2
    },
  ]
}

        jsonschema.validate(json_sample, WS2P_HEADS_SCHEMA)

    def test_bma_ws2p_heads_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, port, url = await self.create_server('GET', '/network/ws2p/heads', handler)
            with self.assertRaises(jsonschema.ValidationError):
                async with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await heads(connection)

        self.loop.run_until_complete(go())
