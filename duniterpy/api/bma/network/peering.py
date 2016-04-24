#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
# Caner Candan <caner@candan.fr>, http://caner.candan.fr
#

from duniterpy.api.bma.network import Network, logging

logger = logging.getLogger("duniter/network/peering")


class Base(Network):
    def __init__(self, connection_handler):
        super(Base, self).__init__(connection_handler, 'network/peering')


class Peers(Base):
    """GET peering entries of every node inside the currency network."""
    schema = {
        "type": ["object"],
        "properties": {
            "depth": {
                "type": "number"
            },
            "nodesCount": {
                "type": "number"
            },
            "leavesCount": {
                "type": "number"
            },
            "root": {
                "type": "string"
            },
            "hash": {
                "type": "string"
            },
            "value": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "string"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "pubkey": {
                        "type": "string"
                    },
                    "endpoints": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "signature": {
                        "type": "string"
                    }
                },
                "required": ["version", "currency", "pubkey", "endpoints", "signature"]
            }
        },
        "oneOf": [
            {
                "required": ["depth", "nodesCount", "leavesCount", "root"]
            },
            {
                "required": ["hash", "value"]
            }
        ]
    }

    async def __get__(self, session, **kwargs):
        """creates a generator with one peering entry per iteration."""

        r = await self.requests_get(session, '/peers', **kwargs)
        return (await self.parse_response(r))

    async def __post__(self, session, **kwargs):
        assert 'entry' in kwargs
        assert 'signature' in kwargs

        r = await self.requests_post(session, '/peers', **kwargs)
        return r


class Status(Base):
    """POST a network status document to this node in order notify of its status."""

    async def __post__(self, session, **kwargs):
        assert 'status' in kwargs
        assert 'signature' in kwargs

        r = await self.requests_post(session, '/status', **kwargs)
        return r
