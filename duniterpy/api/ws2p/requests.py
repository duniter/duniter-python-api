import json
import re
from typing import Optional

from duniterpy.helpers import get_ws2p_challenge
from duniterpy.api.bma.blockchain import BLOCK_SCHEMA

ERROR_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "resId": {
            "type": "string",
            "pattern": "^[0-9,a-z,A-Z]{8}$"
        },
        "err": {"type": "string"}
    },
    "required": ["resId", "err"]
}

BLOCK_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "resId": {
            "type": "string",
            "pattern": "^[0-9,a-z,A-Z]{8}$"
        },
        "body": BLOCK_SCHEMA
    },
    "required": ["resId", "body"]
}


def get_current(request_id: Optional[str] = None) -> str:
    """
    Return ws2p getCurrent() request as json string

    :return:
    """

    if request_id is None:
        request_id = get_ws2p_challenge()[:8]
    else:
        if not re.fullmatch("^[0-9a-zA-Z]{8}$", request_id):
            raise Exception("Invalid ws2p request unique id")
    return json.dumps({
        "reqId": request_id,
        "body": {
            "name": "CURRENT",
            "params": {}
        }
    })


def get_block(block_number: int, request_id: Optional[str] = None) -> str:
    """
    Return ws2p getBlock() request as json string

    :return:
    """

    if request_id is None:
        request_id = get_ws2p_challenge()[:8]
    else:
        if not re.fullmatch("^[0-9a-zA-Z]{8}$", request_id):
            raise Exception("Invalid ws2p request unique id")
    return json.dumps({
        "reqId": request_id,
        "body": {
            "name": "BLOCK_BY_NUMBER",
            "params": {
                "number": block_number
            }
        }
    })

