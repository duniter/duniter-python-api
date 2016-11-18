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

from duniterpy.api.bma import API, logging, parse_response

logger = logging.getLogger("duniter/node")

URL_PATH = 'node'

async def summary(connection):
    """
    GET Certification data over a member

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """
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
    client = API(connection, URL_PATH)

    r = await client.requests_get('/summary')
    return await parse_response(r, schema)
