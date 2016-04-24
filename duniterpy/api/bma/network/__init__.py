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

from .. import API, logging

logger = logging.getLogger("duniter/network")


class Network(API):
    def __init__(self, connection_handler, module='network'):
        super(Network, self).__init__(connection_handler, module)


class Peering(Network):
    """GET peering information about a peer."""
    schema = {
        "type": "object",
        "properties": {
          "version": {
              "type": ["number", "string"]
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

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/peering', **kwargs)
        return (await self.parse_response(r))

from . import peering
