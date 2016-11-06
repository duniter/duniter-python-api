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

from duniterpy.api.bma import logging, API

logger = logging.getLogger("duniter/ud")

URL_PATH = 'ud'

async def history(connection, pubkey):
    """
    Get UD history of a member account

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :param str pubkey:  Public key of the member

    :rtype: dict
    """
    schema = {
        "type": "object",
        "properties": {
            "currency": {
                "type": "string"
            },
            "pubkey": {
                "type": "string"
            },
            "history": {
                "type": "object",
                "properties": {
                    "history": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "block_number": {
                                    "type": "number"
                                },

                                "consumed": {
                                    "type": "boolean"
                                },
                                "time": {
                                    "type": "number"
                                },
                                "amount": {
                                    "type": "number"
                                },
                                "base": {
                                    "type": "number"
                                },
                            }
                        }
                    }
                }
            }
        },
        "required": ["currency", "pubkey", "history"]
    }

    client = API(connection, URL_PATH)

    r = await client.requests_get('/history/%s' % pubkey)
    return await client.parse_response(r, schema)
