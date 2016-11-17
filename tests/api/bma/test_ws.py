import unittest
from tests.api.webserver import WebFunctionalSetupMixin
from duniterpy.api.bma.ws import block, peer, WS_BLOCk_SCHEMA, WS_PEER_SCHEMA
from duniterpy.api.bma import parse_text


class Test_BMA_Websocket(WebFunctionalSetupMixin, unittest.TestCase):

    def test_block(self):
        json_sample = """
{
  "version": 2,
  "currency": "beta_brouzouf",
  "nonce": 28,
  "inner_hash": "FD09B0F7CEC5A575CA6E528DC4C854B612AE77B7283F48E0D28677F5C9C9D0DD",
  "number": 1,
  "time": 1408996317,
  "medianTime": 1408992543,
  "dividend": 254,
  "monetaryMass": 18948,
  "issuer": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
  "previousHash": "0009A7A62703F976F683BBA500FC0CB832B8220D",
  "previousIssuer": "CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp",
  "membersCount": 4,
  "hash": "0000F40BDC0399F2E84000468628F50A122B5F16",
  "identities": [
    "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX:1409007070:udid2;c;CAT;LOL;2000-04-19;e+43.70-079.42;0;"
  ],
  "joiners": [
"9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk:1505004141"
  ],
  "leavers": [
    "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk:1505004141"
  ],
  "revoked": [
    "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX"
  ],
  "excluded": [
    "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB"
  ],
  "certifications": [
    "CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp:9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB:1505900000:2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk"
  ],
  "transactions": [
    {
      "signatures": [
        "H41/8OGV2W4CLKbE35kk5t1HJQsb3jEM0/QGLUf80CwJvGZf3HvVCcNtHPUFoUBKEDQO9mPK3KJkqOoxHpqHCw==",
        "2D96KZwNUvVtcapQPq2mm7J9isFcDCfykwJpVEZwBc7tCgL4qPyu17BT5ePozAE9HS6Yvj51f62Mp4n9d9dkzJoX",
        "2XiBDpuUdu6zCPWGzHXXy8c4ATSscfFQG9DjmqMZUxDZVt1Dp4m2N5oHYVUfoPdrU9SLk4qxi65RNrfCVnvQtQJk"
      ],
        "version": 2,
        "currency": "beta_brouzouf",
        "issuers": [
          "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
          "CYYjHsNyg3HMRMpTHqCJAN9McjH5BwFLmDKGV3PmCuKp",
          "9WYHTavL1pmhunFCzUwiiq4pXwvgGG5ysjZnjz9H8yB"
        ],
        "inputs": [
          "T:6991C993631BED4733972ED7538E41CCC33660F554E3C51963E2A0AC4D6453D3:0",
          "T:3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435:0",
          "D:4745EEBA84D4E3C2BDAE4768D4E0F5A671531EE1B0B9F5206744B4551C664FDF:243",
          "T:3A09A20E9014110FD224889F13357BAB4EC78A72F95CA03394D8CCA2936A7435:1",
          "T:67F2045B5318777CC52CD38B424F3E40DDA823FA0364625F124BABE0030E7B5B:0",
          "D:521A760049DF4FAA602FEF86B7A8E306654502FA3A345F6169B8468B81E71AD3:187"
       ],
       "unlocks": [
          "0:SIG(0)",
          "1:SIG(2)",
          "2:SIG(1)",
          "3:SIG(1)",
          "4:SIG(0)",
          "5:SIG(0)"
       ],
      "outputs": [
        "30:SIG(BYfWYFrsyjpvpFysgu19rGK3VHBkz4MqmQbNyEuVU64g)",
        "156:SIG(DSz4rgncXCytsUMW2JU2yhLquZECD2XpEkpP9gG5HyAx)",
        "49:SIG(6DyGr5LFtFmbaJYRvcs9WmBsr4cbJbJ1EV9zBbqG7A6i)"
      ]
    }
  ],
  "signature": "H41/8OGV2W4CLKbE35kk5t1HJQsb3jEM0/QGLUf80CwJvGZf3HvVCcNtHPUFoUBKEDQO9mPK3KJkqOoxHpqHCw=="
}
"""
        parse_text(json_sample, WS_BLOCk_SCHEMA)

    def test_peer(self):
        json_sample = """{
  "version": 1,
  "currency": "beta_brouzouf",
  "pubkey": "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY",
  "endpoints": [
    "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9001",
    "BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:0db8:0000:85a3:0000:0000:ac1f 9002",
    "OTHER_PROTOCOL 88.77.66.55 9001"
    ],
  "signature": "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r"
}
"""
        data = parse_text(json_sample, WS_PEER_SCHEMA)
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["currency"], "beta_brouzouf")
        self.assertEqual(data["pubkey"], "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(len(data["endpoints"]), 3)
        self.assertEqual(data["signature"], "42yQm4hGTJYWkPg39hQAUgP6S6EQ4vTfXdJuxKEHL1ih6YHiDL2hcwrFgBHjXLRgxRhj2VNVqqc6b4JayKqTE14r")
