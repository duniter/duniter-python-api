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

import unittest

import duniterpy.api.endpoint as endpoint


class TestEndpoint(unittest.TestCase):
    def test_gva(self):
        endpoint_str = "GVA test.domain.com 127.0.0.1 2001:0db8:0000:85a3:0000:0000:ac1f:8001 10902 gva"

        gva_endpoint = endpoint.GVAEndpoint.from_inline(endpoint_str)

        self.assertEqual(gva_endpoint.flags, "")
        self.assertEqual(gva_endpoint.server, "test.domain.com")
        self.assertEqual(gva_endpoint.ipv4, "127.0.0.1")
        self.assertEqual(gva_endpoint.ipv6, "2001:0db8:0000:85a3:0000:0000:ac1f:8001")
        self.assertEqual(gva_endpoint.port, 10902)
        self.assertEqual(gva_endpoint.path, "gva")

        self.assertEqual(gva_endpoint.inline(), endpoint_str)

        endpoint_str = "GVA S test.domain.com 10902 gva"

        gva_endpoint = endpoint.GVAEndpoint.from_inline(endpoint_str)

        self.assertEqual(gva_endpoint.flags, "S")
        self.assertEqual(gva_endpoint.server, "test.domain.com")
        self.assertEqual(gva_endpoint.ipv4, None)
        self.assertEqual(gva_endpoint.ipv6, None)
        self.assertEqual(gva_endpoint.port, 10902)
        self.assertEqual(gva_endpoint.path, "gva")

        self.assertEqual(gva_endpoint.inline(), endpoint_str)

    def test_gva_subscription(self):
        endpoint_str = "GVASUB test.domain.com 127.0.0.1 2001:0db8:0000:85a3:0000:0000:ac1f:8001 10902 gva"

        gvasub_endpoint = endpoint.GVASUBEndpoint.from_inline(endpoint_str)

        self.assertEqual(gvasub_endpoint.flags, "")
        self.assertEqual(gvasub_endpoint.server, "test.domain.com")
        self.assertEqual(gvasub_endpoint.ipv4, "127.0.0.1")
        self.assertEqual(
            gvasub_endpoint.ipv6, "2001:0db8:0000:85a3:0000:0000:ac1f:8001"
        )
        self.assertEqual(gvasub_endpoint.port, 10902)
        self.assertEqual(gvasub_endpoint.path, "gva")

        self.assertEqual(gvasub_endpoint.inline(), endpoint_str)

        endpoint_str = "GVASUB S test.domain.com 10902 gva"

        gvasub_endpoint = endpoint.GVASUBEndpoint.from_inline(endpoint_str)

        self.assertEqual(gvasub_endpoint.flags, "S")
        self.assertEqual(gvasub_endpoint.server, "test.domain.com")
        self.assertEqual(gvasub_endpoint.ipv4, None)
        self.assertEqual(gvasub_endpoint.ipv6, None)
        self.assertEqual(gvasub_endpoint.port, 10902)
        self.assertEqual(gvasub_endpoint.path, "gva")

        assert gvasub_endpoint.inline(), endpoint_str
