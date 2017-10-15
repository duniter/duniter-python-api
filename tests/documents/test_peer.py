import unittest
from duniterpy.documents.peer import Peer, BMAEndpoint, UnknownEndpoint, WS2PEndpoint


rawpeer = """Version: 2
Type: Peer
Currency: beta_brousouf
PublicKey: HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY
Block: 8-1922C324ABC4AF7EF7656734A31F5197888DDD52
Endpoints:
BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:42d0:52:a00::648 9001
BASIC_MERKLED_API some.dns.name 88.77.66.55 2001:42d0:52:a00::648 9002
WS2P d2edcb92 g1-test.duniter.org 20902
OTHER_PROTOCOL 88.77.66.55 9001
dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==
"""


test_weird_ipv6_peer = """Version: 10
Type: Peer
Currency: g1
PublicKey: 6fFt4zdvtNyVcfJn7Y41mKLmMDizyK3nVeNW3qdDXzpc
Block: 18198-000004AC710E04D8015ED6CA5D87D4B6620A7551233FFEE1B521FF756CE3B9CD
Endpoints:
BASIC_MERKLED_API duniter.aquilenet.fr 141.255.128.35 2a01:474::35 10901
BMAS duniter.aquilenet.fr 443
dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==
"""


class TestPeer(unittest.TestCase):
    def test_fromraw(self):
        peer = Peer.from_signed_raw(rawpeer)
        self.assertEqual(peer.currency, "beta_brousouf")
        self.assertEqual(peer.pubkey, "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(str(peer.blockUID), "8-1922C324ABC4AF7EF7656734A31F5197888DDD52")
        self.assertEqual(len(peer.endpoints), 4)
        self.assertIsInstance(peer.endpoints[0], BMAEndpoint)
        self.assertIsInstance(peer.endpoints[1], BMAEndpoint)
        self.assertIsInstance(peer.endpoints[2], WS2PEndpoint)
        self.assertIsInstance(peer.endpoints[3], UnknownEndpoint)

        self.assertEqual(peer.endpoints[0].server, "some.dns.name")
        self.assertEqual(peer.endpoints[0].ipv4, "88.77.66.55")
        self.assertEqual(peer.endpoints[0].ipv6, "2001:42d0:52:a00::648")
        self.assertEqual(peer.endpoints[0].port, 9001)

        self.assertEqual(peer.endpoints[1].server, "some.dns.name")
        self.assertEqual(peer.endpoints[1].ipv4, "88.77.66.55")
        self.assertEqual(peer.endpoints[1].ipv6, "2001:42d0:52:a00::648")
        self.assertEqual(peer.endpoints[1].port, 9002)

        self.assertEqual(peer.endpoints[2].server, "g1-test.duniter.org")
        self.assertEqual(peer.endpoints[2].ws2pid, "d2edcb92")
        self.assertEqual(peer.endpoints[2].port, 20902)

        self.assertEqual(peer.signatures[0], "dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==")

    def test_fromraw_toraw(self):
        peer = Peer.from_signed_raw(rawpeer)
        rendered_peer = peer.signed_raw()
        from_rendered_peer = Peer.from_signed_raw(rendered_peer)

        self.assertEqual(from_rendered_peer.currency, "beta_brousouf")
        self.assertEqual(from_rendered_peer.pubkey, "HsLShAtzXTVxeUtQd7yi5Z5Zh4zNvbu8sTEZ53nfKcqY")
        self.assertEqual(str(from_rendered_peer.blockUID), "8-1922C324ABC4AF7EF7656734A31F5197888DDD52")
        self.assertEqual(len(peer.endpoints), 4)
        self.assertIsInstance(peer.endpoints[0], BMAEndpoint)
        self.assertIsInstance(peer.endpoints[1], BMAEndpoint)
        self.assertIsInstance(peer.endpoints[2], WS2PEndpoint)
        self.assertIsInstance(peer.endpoints[3], UnknownEndpoint)

        self.assertEqual(from_rendered_peer.endpoints[0].server, "some.dns.name")
        self.assertEqual(from_rendered_peer.endpoints[0].ipv4, "88.77.66.55")
        self.assertEqual(from_rendered_peer.endpoints[0].ipv6, "2001:42d0:52:a00::648")
        self.assertEqual(from_rendered_peer.endpoints[0].port, 9001)

        self.assertEqual(from_rendered_peer.endpoints[1].server, "some.dns.name")
        self.assertEqual(from_rendered_peer.endpoints[1].ipv4, "88.77.66.55")
        self.assertEqual(from_rendered_peer.endpoints[1].ipv6, "2001:42d0:52:a00::648")
        self.assertEqual(from_rendered_peer.endpoints[1].port, 9002)

        self.assertEqual(peer.endpoints[2].server, "g1-test.duniter.org")
        self.assertEqual(peer.endpoints[2].ws2pid, "d2edcb92")
        self.assertEqual(peer.endpoints[2].port, 20902)


        self.assertEqual(from_rendered_peer.signatures[0], "dkaXIiCYUJtCg8Feh/BKvPYf4uFH9CJ/zY6J4MlA9BsjmcMe4YAblvNt/gJy31b1aGq3ue3h14mLMCu84rraDg==")
        self.assertEqual(rawpeer, from_rendered_peer.signed_raw())

    def test_incorrect(self):
        peer = Peer.from_signed_raw(test_weird_ipv6_peer)
        rendered_peer = peer.signed_raw()
        from_rendered_peer = Peer.from_signed_raw(rendered_peer)
