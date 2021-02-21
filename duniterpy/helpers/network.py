"""
Copyright  2014-2021 Vincent Texier <vit@free.fr>

DuniterPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DuniterPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import List, Dict, Any

from duniterpy.api import bma
from duniterpy.api.client import Client
from duniterpy.documents.peer import Peer, MalformedDocumentError
from duniterpy.documents.ws2p.heads import HeadV2
from itertools import groupby

from duniterpy.key import VerifyingKey


async def get_available_nodes(client: Client) -> List[List[Dict[str, Any]]]:
    """
    Get available nodes grouped and sorted by descending blockstamp

    Each entry is a list of nodes (HeadV2 instance, inline endpoint list) sharing the same blockstamp:

        [
            [{"head": HeadV2, "endpoints": [str, ...]}, ...],
            [{"head": HeadV2, "endpoints": [str, ...]}, ...],
            ...
        ]

    You can just select the first endpoint of the first node of the first group to quickly get an available node.

        groups = get_available_nodes(client)
        first_node_first_endpoint = groups[0][0]["endpoints"][0]

    If node is down, you can select another node.

    Warning : only nodes with BMAS, BASIC_MERKLED_API, GVA and GVASUB endpoint are selected
              and only those endpoints are available in the endpoint list

    :param client: Client instance
    :return:
    """
    # capture heads and peers
    heads_response = await client(bma.network.ws2p_heads)
    peers_response = await client(bma.network.peers)

    # get heads instances from WS2P messages
    heads = []
    for entry in heads_response["heads"]:
        head, _ = HeadV2.from_inline(entry["messageV2"], entry["sigV2"])
        heads.append(head)

    # sort by blockstamp by descending order
    heads = sorted(heads, key=lambda x: x.blockstamp, reverse=True)

    # group heads by blockstamp
    groups = []
    for _, group in groupby(heads, key=lambda x: x.blockstamp):
        nodes = []
        for head in list(group):

            # if head signature not valid...
            if VerifyingKey(head.pubkey).verify_ws2p_head(head) is False:
                # skip this node
                continue

            bma_peers = [
                bma_peer
                for bma_peer in peers_response["peers"]
                if bma_peer["pubkey"] == head.pubkey
            ]

            # if no peer found...
            if len(bma_peers) == 0:
                # skip this node
                continue

            bma_peer = bma_peers[0]

            try:
                peer = Peer.from_bma(bma_peer)
            # if bad peer... (mostly bad formatted endpoints)
            except MalformedDocumentError:
                # skip this node
                continue

            # set signature in Document
            peer.signatures = [bma_peer["signature"]]
            #  if peer signature not valid
            if VerifyingKey(head.pubkey).verify_document(peer) is False:
                # skip this node
                continue

            # filter endpoints to get only BMAS, BASIC_MERKLED_API, GVA or GVASUB
            endpoints = [
                endpoint
                for endpoint in bma_peers[0]["endpoints"]
                if endpoint.startswith("BMAS")
                or endpoint.startswith("BASIC_MERKLED_API")
                or endpoint.startswith("GVA")
                or endpoint.startswith("GVASUB")
            ]
            if len(endpoints) == 0:
                # skip this node
                continue

            # add node to group nodes
            nodes.append({"head": head, "endpoints": endpoints})

        # if nodes in group...
        if len(nodes) > 0:
            # add group to groups
            groups.append(nodes)

    return groups
