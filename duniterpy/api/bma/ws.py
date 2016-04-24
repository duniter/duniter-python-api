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

from duniterpy.api.bma import API, logging
from duniterpy.api.bma.blockchain import Block as _Block
from duniterpy.api.bma.network.peering import Peers as _Peers

logger = logging.getLogger("duniter/ws")


class Websocket(API):
    def __init__(self, connection_handler, module='ws'):
        super(Websocket, self).__init__(connection_handler, module)


class Block(Websocket):
    """Connect to block websocket."""
    schema = _Block.schema

    def connect(self, session):
        r = self.connect_ws(session, '/block')
        return r


class Peer(Websocket):
    """Connect to block websocket."""
    schema = {
        "type": "object",
        "properties": {
            "version": {
                "type": "number"
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

    def connect(self, session):
        r = self.connect_ws(session, '/peer')
        return r
