from duniterpy.api.bma import API, logging, parse_response

logger = logging.getLogger("duniter/ws2p")

URL_PATH = 'ws2p'

WS2P_HEADS_SCHEMA = {
                    "type": "object",
                    "properties": {
                        "heads": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string"
                                    },
                                    "sig": {
                                        "type": "string",
                                    },
                                    "messageV2": {
                                        "type": "string"
                                    },
                                    "sigV2": {
                                        "type": "string",
                                    },
                                    "step": {
                                        "type": "number",
                                    },
                                },
                                "required": ["messageV2", "sigV2", "step"]
                            }
                        }
                    },
                    "required": ["heads"]
                }


async def heads(connection):
    """
    GET Certification data over a member

    :param duniterpy.api.bma.ConnectionHandler connection: Connection handler instance
    :rtype: dict
    """

    client = API(connection, URL_PATH)

    r = await client.requests_get('/heads')
    return await parse_response(r, WS2P_HEADS_SCHEMA)
