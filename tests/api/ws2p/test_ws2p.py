import unittest

import jsonschema

from duniterpy.api.client import Client, parse_text
from duniterpy.api.endpoint import BMAEndpoint
from duniterpy.api.ws2p.network import heads, WS2P_HEADS_SCHEMA
from duniterpy.api.ws2p.requests import BLOCK_RESPONSE_SCHEMA, ERROR_RESPONSE_SCHEMA, BLOCKS_RESPONSE_SCHEMA, \
    REQUIREMENTS_RESPONSE_SCHEMA
from tests.api.webserver import WebFunctionalSetupMixin, web


class TestWs2pHeads(WebFunctionalSetupMixin, unittest.TestCase):

    def test_block(self):
        json_sample = {
            "heads": [
                {
                    "message": "WS2POCAIC:HEAD:1:8iVdpXqFLCxGyPqgVx5YbFSkmWKkceXveRd2yvBKeARL:\
                    102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:e66254bf:duniter:1.6.20:1",
                    "sig": "ZO5gSUMK6IaUEwU4K40nhuHOfnJ6Zfn8VS+4Ko2FM7t+mDsHf+3gDRT9PgV2p0fz81mF6jVYWpq2UYEsnK/gCg==",
                    "messageV2": "WS2POCAIC:HEAD:2:8iVdpXqFLCxGyPqgVx5YbFSkmWKkceXveRd2yvBKeARL:\
                    102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:e66254bf:\
                    duniter:1.6.20:1:15:14",
                    "sigV2": "ReXzbgUya9jo4dL/R4g19Y+RE9BGB0xDkw7mrBWoldlRLkq3KFyRkAf9VthVx1UUb/AINr3nxImZKVQiVH9+DQ==",
                    "step": 0
                },
                {
                    "message": "WS2POCAIC:HEAD:1:2ny7YAdmzReQxAayyJZsyVYwYhVyax2thKcGknmQy5nQ:\
                    102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:a0a45ed2:duniter:1.6.21:1",
                    "sig": "pXLMmOpyEMdWihT183g/rnCvMzA2gHki5Cxg7rEl3psQu0RuK0ObCv5YFhmQnRlg+QZ1CWfbYEEbm3G1eGplAQ==",
                    "messageV2": "WS2POCAIC:HEAD:2:2ny7YAdmzReQxAayyJZsyVYwYhVyax2thKcGknmQy5nQ:\
                    102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:a0a45ed2:\
                    duniter:1.6.21:1:34:28",
                    "sigV2": "p5f7/KfQqjTaCYSMUXpjUDH7uF2DafetHNgphGzkOXgxM+Upeii0Fz2RFBwnZvN+Gjp81hAqSuH48PJP6HJSAw==",
                    "step": 1
                },
                {
                    "message": "WS2POCA:HEAD:1:GRBPV3Y7PQnB9LaZhSGuS3BqBJbSHyibzYq65kTh1nQ4:\
                    102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:6d0e96f9:duniter:1.6.21:1",
                    "sig": "h9o1XBEV18gUzbvj1jdQB1M7U8ifZprIyVwLdlSQEfeG9WZLvZAjYzLGA2nD6h/9RkJLOJPzIQJXysHUHJ2dDQ==",
                    "messageV2": "WS2POCA:HEAD:2:GRBPV3Y7PQnB9LaZhSGuS3BqBJbSHyibzYq65kTh1nQ4:\
                    102102-000002C0694C7D373A78B095419C86584B81804CFB9641B7EBC3A18040B6FEE6:6d0e96f9:\
                    duniter:1.6.21:1:20:20",
                    "sigV2": "VsyQmXOUYrfHWy0FeS4rJrIJCUBI+3BergbSYQ78icJWV6MQzZSw7Z+Yl7urujCYZriDQM76D6GW+6F0EELpBQ==",
                    "step": 2
                },
            ]
        }

        jsonschema.validate(json_sample, WS2P_HEADS_SCHEMA)

    def test_ws2p_heads_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, port, url = await self.create_server('GET', '/network/ws2p/heads', handler)
            with self.assertRaises(jsonschema.ValidationError):
                client = Client(BMAEndpoint("127.0.0.1", "", "", port))
                await client(heads)
            await client.close()

        self.loop.run_until_complete(go())

    def test_error_response_validation(self):
        error_response_string = """{"resId":"cfe10cc4","err":"Error message"}"""
        error_response = parse_text(error_response_string, ERROR_RESPONSE_SCHEMA)
        self.assertIsInstance(error_response, dict)

    def test_block_response_validation(self):
        response_string = """{"resId":"cfe10cc4","body":{"wrong":false,"version":11,"number":367572,
        "currency":"g1-test","hash":"000024399D612753E59D44415CFA61F3A663919110CD2EB8D30C93F49C61E07F",
        "previousHash":"00007A2931B1B33351151058E8FE5C8368C9A7C6F13F37FEB92AA67B17B7EC46",
        "issuer":"7BGpV28HzE6fyZtteuPmwHf6fHwHkQ9Ssww3Cxq82NnT",
        "previousIssuer":"CrznBiyq8G4RVUprH9jHmAw1n1iuzw8y9FdJbrESnaX7","dividend":null,"time":1557357655,
        "powMin":65,"unitbase":1,"membersCount":18,"issuersCount":4,"issuersFrame":21,"issuersFrameVar":0,
        "identities":[],"joiners":[],"actives":[],"leavers":[],"revoked":[],"excluded":[],"certifications":[],
        "transactions":[],"medianTime":1557355021,"fork":false,"parameters":"",
        "inner_hash":"BA4D939F40D3B6D036659F6B7E0881D69054ADFF399533B44E1D5A9983235721",
        "signature":"Ks0ugrWCZ/jBDyFQ77TnzTIKJrv2lBJKwQqVW64ZEESgD++J4pjPCEP0WDmcbm65VAomKbnkWOJsThdAIgj2DA==",
        "nonce":10400000002073,"monetaryMass":144418724,"writtenOn":367572,
        "written_on":"367572-000024399D612753E59D44415CFA61F3A663919110CD2EB8D30C93F49C61E07F"}} """
        response = parse_text(response_string, BLOCK_RESPONSE_SCHEMA)
        self.assertIsInstance(response, dict)

    def test_blocks_response_validation(self):
        response_string = """{"resId": "f608a5b8", "body": [
            {"identities": [], "joiners": [], "actives": [], "leavers": [], "revoked": [], "excluded": [],
             "certifications": [], "transactions": [], "version": 11, "number": 360000, "currency": "g1-test",
             "hash": "0001826F638E091DEDEC5E6A4D3917BC37772E16B66923818AED44182F9FBA45",
             "inner_hash": "3BB4636E7EB6159CB4BF58E2D47E7AC92D75E42F72EC10D91645B7B2CFD6E84A",
             "previousHash": "0000FBE5B2BA1C88984AEA6FFB16F622A870D1A9DBD2DDF040BFF8E27273B0E1",
             "issuer": "3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
             "previousIssuer": "JyTqcD4Q9aEAR2CWEpwBUAAyMCjfM6gaE5S2e8GWUuq", "dividend": null, "time": 1556123743,
             "powMin": 60, "monetaryMass": 128680804, "unitbase": 1, "membersCount": 18, "issuersCount": 6,
             "issuersFrame": 31, "issuersFrameVar": 0, "medianTime": 1556122058, "fork": false, "parameters": "",
             "signature": "Mu+FgC5qhU1Wp7Ih2v7JYkKMM7rv6Z+I4qxUvmVTEW+BObKy87zHJ7B0PsZORPWFkETNpiNsm10COqPbnt84BA==",
             "nonce": 10200000000241},
            {"identities": [], "joiners": [], "actives": [], "leavers": [], "revoked": [], "excluded": [],
             "certifications": [], "transactions": [], "version": 11, "number": 360001, "currency": "g1-test",
             "hash": "00035B7B452FAB7DBBE6E48DDD1060AC9A1A7096B32DD2C7763CC09A024A1597",
             "inner_hash": "751DCAE2E881B5ABC0A61912033763872ED1D961C63C4A135CCB24E81DE17075",
             "previousHash": "0001826F638E091DEDEC5E6A4D3917BC37772E16B66923818AED44182F9FBA45",
             "issuer": "7BGpV28HzE6fyZtteuPmwHf6fHwHkQ9Ssww3Cxq82NnT",
             "previousIssuer": "3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj", "dividend": null, "time": 1556123777,
             "powMin": 60, "monetaryMass": 128680804, "unitbase": 1, "membersCount": 18, "issuersCount": 6,
             "issuersFrame": 31, "issuersFrameVar": 0, "medianTime": 1556122255, "fork": false, "parameters": "",
             "signature": "T13jarx2EopBhIDAmDLb5X6V9lvuIzrKvoh0ugWmOrUBZs0fcCqFyFew7d1TCPgkgjii/t3Bg/injOOVFrlPAQ==",
             "nonce": 10400000000195}]}"""
        response = parse_text(response_string, BLOCKS_RESPONSE_SCHEMA)
        self.assertIsInstance(response, dict)

    def test_requirements_pending(self):
        response_string = """{"resId":"1986997e","body":{"identities":[
        {"pubkey":"36UhAqrkDx11ifN7WaBM6Q5bMUJxhKb1wJnnPFnkLkCF","uid":"cgeek-2",
        "sig":"Xjuey5pegW8fmS+L8ubOlT3CJVomaNuEA4cn+cwuyiLoKDgnbqpeOQJ213T0fLq4dU16IRFHiffeAVWONtl4Dg==",
        "meta":{"timestamp":"287698-0000297DEC5E92F2D14CBE4E6EFA951E1E79D57E3552D1AD7A98778142EF7E7E"},
        "revocation_sig":"","revoked":false,"revoked_on":0,"expired":false,"outdistanced":false,"isSentry":false,
        "wasMember":true,"certifications":[{"from":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
        "to":"36UhAqrkDx11ifN7WaBM6Q5bMUJxhKb1wJnnPFnkLkCF",
        "sig":"p7sYhYvI2QFu6K4veanTrJGl3ytew0b6FH+NW8ojLKzWgXSX6/GPSf5zYMunYdjtEUG79tNXMqmOIQJPcv/3Cw==",
        "timestamp":1553634062,"expiresIn":8902081},{"from":"5B8iMAzq1dNmFe3ZxFTBQkqhq4fsztg1gZvxHXCk1XYH",
        "to":"36UhAqrkDx11ifN7WaBM6Q5bMUJxhKb1wJnnPFnkLkCF",
        "sig":"Qi9TiAWYcWTxDHJL/DLjBoZ7ReAeYuTYcy1GWrVFE8/wh1TAJgNr9Cc68TUEB+QG6qrqrSEDshPZpCyv8ZeFDw==",
        "timestamp":1554842558,"expiresIn":10110577},{"from":"7BGpV28HzE6fyZtteuPmwHf6fHwHkQ9Ssww3Cxq82NnT",
        "to":"36UhAqrkDx11ifN7WaBM6Q5bMUJxhKb1wJnnPFnkLkCF",
        "sig":"eCqKphYiVWl8t4HYMail1AfTD+xYZg/QMFIAn8RPfj8Rc68gDnDvwulAylq09KLkNofhW9SSfWtpNF8t0X5cBg==",
        "timestamp":1557072594,"expiresIn":12340613},{"from":"81jPYhcyruwKJ9Dy4Vz7MtmxiSdeESuJcvjPotxbCTgS",
        "to":"36UhAqrkDx11ifN7WaBM6Q5bMUJxhKb1wJnnPFnkLkCF",
        "sig":"wxtUU0DtooWxp26F2CyOtVY5WEAXkM0UXildWkXgafgpc03RrtW8FsAql1D8gmz9F3q4h/k86Qqoi25EDrC/Dg==",
        "timestamp":1557070855,"expiresIn":12338874}],"pendingCerts":[{
        "from":"81jPYhcyruwKJ9Dy4Vz7MtmxiSdeESuJcvjPotxbCTgS","to":"36UhAqrkDx11ifN7WaBM6Q5bMUJxhKb1wJnnPFnkLkCF",
        "target":"F617EF4F79317BE9A7767FB17B95C859EB33075CD257635AEBA3C12B5C732E84",
        "sig":"wxtUU0DtooWxp26F2CyOtVY5WEAXkM0UXildWkXgafgpc03RrtW8FsAql1D8gmz9F3q4h/k86Qqoi25EDrC/Dg==",
        "block_number":365809,"block_hash":"00002ABB8E538CE9803B03F62099F18E23CAFF661EE82908D1E65C0B5131D5A5",
        "block":365809,"linked":false,"written":false,"written_block":null,"written_hash":null,
        "expires_on":1558122775,"expired":0,
        "blockstamp":"365809-00002ABB8E538CE9803B03F62099F18E23CAFF661EE82908D1E65C0B5131D5A5"},
        {"from":"7BGpV28HzE6fyZtteuPmwHf6fHwHkQ9Ssww3Cxq82NnT","to":"36UhAqrkDx11ifN7WaBM6Q5bMUJxhKb1wJnnPFnkLkCF",
        "target":"F617EF4F79317BE9A7767FB17B95C859EB33075CD257635AEBA3C12B5C732E84",
        "sig":"eCqKphYiVWl8t4HYMail1AfTD+xYZg/QMFIAn8RPfj8Rc68gDnDvwulAylq09KLkNofhW9SSfWtpNF8t0X5cBg==",
        "block_number":365824,"block_hash":"00009739A9042E94A1267D1D906D132F53EF7633233FB7C8519D57B1ED5ECE09",
        "block":365824,"linked":false,"written":false,"written_block":null,"written_hash":null,
        "expires_on":1558124514,"expired":0,
        "blockstamp":"365824-00009739A9042E94A1267D1D906D132F53EF7633233FB7C8519D57B1ED5ECE09"}],
        "pendingMemberships":[],"membershipPendingExpiresIn":0,"membershipExpiresIn":0},
        {"pubkey":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj","uid":"cgeek",
        "sig":"mmQW40vZNHVLLzJ9lJKTQpTstQSa54X7SpRi5ORSIERyCjZkYF8KN/M5Wg6pYIlX832phKHVg766DNy0HxwuDg==",
        "meta":{"timestamp":"0-E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855"},
        "revocation_sig":"","revoked":false,"revoked_on":0,"expired":false,"outdistanced":false,"isSentry":true,
        "wasMember":true,"certifications":[{"from":"7KL2QXXFULDpsQY4UdSr5oEVx6rFE6oxeagRdkCX35bf",
        "to":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
        "sig":"EaY5FoPqKSP+N2NRJcSfrMUgTkRKcCchPmIrGC9uutXFvuw2cCmYcocHR9xASN9R3X1hkZw1u/B0qcaFYUuZCg==",
        "timestamp":1554890320,"expiresIn":10158339},{"from":"5B8iMAzq1dNmFe3ZxFTBQkqhq4fsztg1gZvxHXCk1XYH",
        "to":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
        "sig":"5Rfo6p76q7cpn+VF2fudvmYL2RBN97h5uIvRSisWbHLZyhcP4o3FYnLbUQVZMW2wnKUnoiHQPlWgSnmA1P5ADQ==",
        "timestamp":1548880791,"expiresIn":4148810},{"from":"39Fnossy1GrndwCnAXGDw3K5UYXhNXAFQe7yhYZp8ELP",
        "to":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
        "sig":"U8SF/OD7E7nSGzEIihSxzDYiPKR/xy7xZqkYz64h6mfORITf80QAt/tDkCPDgnLhMdMkCnbvJqib3dMrhx7FBg==",
        "timestamp":1545522046,"expiresIn":790065},{"from":"JyTqcD4Q9aEAR2CWEpwBUAAyMCjfM6gaE5S2e8GWUuq",
        "to":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
        "sig":"joPfimXiQdCR41TFU3rGGfZasK0g/NA7kExCFIG/wd5H3ArYSYPT1nla8vXTYxDuaavOxeIxfiB4KaKGlnmwBA==",
        "timestamp":1557038934,"expiresIn":12306953},{"from":"81jPYhcyruwKJ9Dy4Vz7MtmxiSdeESuJcvjPotxbCTgS",
        "to":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
        "sig":"4BwyLBjOjM1Js0U/1tV3UmeJ8mR4TskifmAbPxnPKTw2tMvYu8HrBwO4vfhvUIEw7sfwwZcMu+CY1AnEBfegAg==",
        "timestamp":1553633613,"expiresIn":8901632},{"from":"36UhAqrkDx11ifN7WaBM6Q5bMUJxhKb1wJnnPFnkLkCF",
        "to":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
        "sig":"eSnqbh9vyIZl5PA3IidK6LGTd2HuztCmHHChF/UbJbcJDS/f/xN4Iuz4gF6JHNtnAXmqmDcxsNFeQlsOLz8aDA==",
        "timestamp":1553633513,"expiresIn":8901532},{"from":"DVxuMTLKDX8GLBP3mmPBhbn71rXjvQDqSXCszPErYaFM",
        "to":"3dnbnYY9i2bHMQUGyFp5GVvJ2wBkVpus31cDJA5cfRpj",
        "sig":"SDscoRGF4OV7+OtT/CA+d8DDd656vxx9zJVdG9qbKMZ5/nmqziroW0YoVA9kH7AOZj6GJXJWuq7E6KX6X9hNAQ==",
        "timestamp":1555363122,"expiresIn":10631141}],"pendingCerts":[],"pendingMemberships":[],
        "membershipPendingExpiresIn":0,"membershipExpiresIn":6003091}
        ]}} """
        response = parse_text(response_string, REQUIREMENTS_RESPONSE_SCHEMA)
        self.assertIsInstance(response, dict)
