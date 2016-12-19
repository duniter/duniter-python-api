import attr
from duniterpy.documents import Peer, BMAEndpoint, BlockUID
from duniterpy.api import errors
from duniterpy.key import SigningKey, ScryptParams
from .http import HTTPServer
from .block_forge import BlockForge
import logging


@attr.s()
class Node:
    http = attr.ib()
    forge = attr.ib()
    _logger = attr.ib(default=attr.Factory(lambda: logging.getLogger('mirage')))

    @classmethod
    async def start(cls, port, currency, salt, password, loop):
        key = SigningKey(salt, password, ScryptParams(2 ** 12, 16, 1))
        node = cls(HTTPServer(port, loop), BlockForge(currency, key))

        get_routes = {
            '/network/peering': node.peering,
            '/blockchain/block/{number}': node.block_by_number,
            '/blockchain/current': node.current_block,
            '/blockchain/parameters': node.parameters,
            '/blockchain/with/ud': node.with_ud
        }
        for r, h in get_routes.items():
            node.http.add_route("GET", r, h)
        srv, port, url = await node.http.create_server()
        print("Server started on {0}".format(url))
        return node

    def block_by_number(self, request):
        number = int(request.match_info['number'])
        try:
            block = self.forge.blocks[number]
            return {
                "version": block.version,
                "nonce": block.noonce,
                "number": block.number,
                "powMin": block.powmin,
                "time": block.time,
                "medianTime": block.mediantime,
                "membersCount": block.members_count,
                "monetaryMass": self.forge.monetary_mass(),
                "unitbase": block.unit_base,
                "issuersCount": block.different_issuers_count,
                "issuersFrame": block.issuers_frame,
                "issuersFrameVar": block.issuers_frame_var,
                "currency": block.currency,
                "issuer": block.issuer,
                "signature": block.signatures[0],
                "hash": block.sha_hash,
                "parameters": block.parameters if block.parameters else "",
                "previousHash": block.prev_hash,
                "previousIssuer": block.prev_issuer,
                "inner_hash": block.inner_hash,
                "dividend": block.ud,
                "identities": [i.inline() for i in block.identities],
                "joiners": [m.inline() for m in block.joiners],
                "actives": [m.inline() for m in block.actives],
                "leavers": [m.inline() for m in block.leavers],
                "revoked": [r.inline() for r in block.revoked],
                "excluded": [i.inline() for i in block.excluded],
                "certifications": [c.inline() for c in block.certifications],
                "transactions": [t.inline() for t in block.transactions],
                "raw": block.raw()
            }, 200
        except IndexError:
            return {
                "ucode": errors.BLOCK_NOT_FOUND,
                "message": "Block not found"
            }, 404

    def current_block(self, request):
        try:
            block = self.forge.blocks[-1]
            return {
                "version": block.version,
                "nonce": block.noonce,
                "number": block.number,
                "powMin": block.powmin,
                "time": block.time,
                "medianTime": block.mediantime,
                "membersCount": block.members_count,
                "monetaryMass": self.forge.monetary_mass(),
                "unitbase": block.unit_base,
                "issuersCount": block.different_issuers_count,
                "issuersFrame": block.issuers_frame,
                "issuersFrameVar": block.issuers_frame_var,
                "currency": block.currency,
                "issuer": block.issuer,
                "signature": block.signatures[0],
                "hash": block.computed_inner_hash(),
                "parameters": block.parameters if block.parameters else "",
                "previousHash": block.prev_hash,
                "previousIssuer": block.prev_issuer,
                "inner_hash": block.inner_hash,
                "dividend": block.ud,
                "identities": [ i.inline() for i in block.identities],
                "joiners": [m.inline() for m in block.joiners],
                "actives": [m.inline() for m in block.actives],
                "leavers": [m.inline() for m in block.leavers],
                "revoked": [r.inline() for r in block.revoked],
                "excluded": [i.inline() for i in block.excluded],
                "certifications": [c.inline() for c in block.certifications],
                "transactions": [t.inline() for t in block.transactions],
                "raw": block.raw()
            }, 200
        except IndexError:
            return {
                "ucode": errors.NO_CURRENT_BLOCK,
                "message": "No current block"
            }, 404

    def peering(self, request):
        return {
            "version": 2,
            "currency": self.peer_doc().currency,
            "endpoints": [
                str(self.peer_doc().endpoints[0])
            ],
            "status": "UP",
            "block": str(self.peer_doc().blockUID),
            "signature": self.peer_doc().signatures[0],
            "raw": self.peer_doc().raw(),
            "pubkey": self.peer_doc().pubkey
        }, 200

    def parameters(self, request):
        return {
            "currency": self.forge.currency,
            "c": 0.0025,
            "dt": 86400,
            "ud0": 100000,
            "sigPeriod": 10800,
            "sigStock": 40,
            "sigWindow": 2629800,
            "sigValidity": 31557600,
            "sigQty": 1,
            "idtyWindow": 604800,
            "msWindow": 604800,
            "xpercent": 0.9,
            "msValidity": 15778800,
            "stepMax": 5,
            "medianTimeBlocks": 12,
            "avgGenTime": 300,
            "dtDiffEval": 25,
            "blocksRot": 40,
            "percentRot": 0.66
        }, 200

    def with_ud(self, request):
        return {
            "result": {
                "blocks": [b.number for b in self.forge.blocks if b.ud]
            }
        }, 200

    def peer_doc(self):
        peer = Peer(2, self.forge.currency, self.forge.key.pubkey, BlockUID.empty(),
                    [BMAEndpoint(None, "127.0.0.1", None, self.http.port)], None)
        peer.sign([self.forge.key])
        return peer
