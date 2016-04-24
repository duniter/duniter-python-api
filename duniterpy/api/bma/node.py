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

logger = logging.getLogger("duniter/node")


class Node(API):
    def __init__(self, connection_handler, module='node'):
        super(Node, self).__init__(connection_handler, module)


class Summary(Node):
    """GET Certification data over a member."""
    schema = {
        "type": "object",
        "properties": {
            "duniter": {
                "type": "object",
                "properties": {
                    "software": {
                    "type": "string"
                    },
                    "version": {
                        "type": "string",
                    },
                    "forkWindowSize": {
                        "type": "number"
                    }
                },
                "required": ["software", "version"]
            },
        },
        "required": ["duniter"]
    }

    def __init__(self, connection_handler, module='node'):
        super(Summary, self).__init__(connection_handler, module)

    async def __get__(self, session, **kwargs):
        r = await self.requests_get(session, '/summary', **kwargs)
        return await self.parse_response(r)

