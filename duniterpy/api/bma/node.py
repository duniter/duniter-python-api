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

logger = logging.getLogger("duniter/node")

MODULE = 'node'


async def summary(client: Client) -> dict:
    """
    GET Duniter node version and infos

    :param client: Client to connect to the api
    :return:
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

    return await client.get(MODULE + '/summary', schema=schema)
