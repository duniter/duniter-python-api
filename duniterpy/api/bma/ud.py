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
# vit
import logging

from duniterpy.api.client import Client

logger = logging.getLogger("duniter/ud")

MODULE = "ud"

UD_SCHEMA = {
    "type": "object",
    "properties": {
        "currency": {"type": "string"},
        "pubkey": {"type": "string"},
        "history": {
            "type": "object",
            "properties": {
                "history": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "block_number": {"type": "number"},
                            "consumed": {"type": "boolean"},
                            "time": {"type": "number"},
                            "amount": {"type": "number"},
                            "base": {"type": "number"},
                        },
                    },
                }
            },
        },
    },
    "required": ["currency", "pubkey", "history"],
}


async def history(client: Client, pubkey: str) -> dict:
    """
    Get UD history of a member account

    :param client: Client to connect to the api
    :param pubkey:  Public key of the member
    :return:
    """
    return await client.get(MODULE + "/history/%s" % pubkey, schema=UD_SCHEMA)
