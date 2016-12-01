import attr
from duniterpy.documents import Peer, BMAEndpoint, BlockUID
from duniterpy.api import errors
from duniterpy.key import SigningKey
from .http import HTTPServer
from .block_forge import BlockForge
import logging


@attr.s()
class Node:
    http = attr.ib()
    forge = attr.ib()
    _logger = attr.ib(default=attr.Factory(lambda: logging.getLogger('duniter_mock_server')))

    @classmethod
    async def start(cls, port, currency, salt, password, loop):
        key = SigningKey(salt, password)
        node = cls(HTTPServer(port, loop), BlockForge(currency, key))

        get_routes = {
            '/network/peering': node.peering,
            '/blockchain/block/{number}': node.block_by_number,
            '/blockchain/current': node.current_block,
            '/blockchain/sources/{pubkey}': node.sources,
            '/wot/lookup/{search}': node.lookup,
            '/wot/certifiers-of/{search}': node.certifiers_of,
            '/wot/certified-by/{search}': node.certified_by
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
                "hash": block.sha_hash,
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

    def sources(self, request):
        pubkey = str(request.match_info['pubkey'])
        try:
            sources = self.forge.user_identities[pubkey].sources
            return {
                       "currency": self.forge.currency,
                       "pubkey": pubkey,
                       "sources": [{
                           'type': s.source,
                           'noffset': s.index,
                           'identifier': s.origin_id,
                           'amount': s.amount,
                           'base': s.base
                       } for s in sources]
                   }, 200
        except IndexError:
            return {
                      "currency": self.forge.currency,
                      "pubkey": pubkey,
                      "sources": []
                   }, 200

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

    def certifiers_of(self, request):
        search = str(request.match_info['search'])
        try:
            user_identity = self.forge.user_identities[search]
        except KeyError:
            try:
                user_identity = next(i for i in self.forge.user_identities.values() if i.uid == search)
            except StopIteration:
                return {
                    'error': errors.NO_MEMBER_MATCHING_PUB_OR_UID,
                    'message': "No member matching this pubkey or uid"
                }, 200

        return {
            "pubkey": user_identity.pubkey,
            "uid": user_identity.uid,
            "sigDate": str(user_identity.blockstamp),
            "isMember": user_identity.member,
            "certifications": [
                {
                    "pubkey": c.from_identity.pubkey,
                    "uid": c.from_identity.uid,
                    "isMember": c.from_identity.member,
                    "wasMember": c.from_identity.was_member,
                    "cert_time": {
                        "block": c.block,
                        "medianTime": c.mediantime
                    },
                    "sigDate": str(c.from_identity.blockstamp),
                    "written": {
                        "number": c.written_on.number,
                        "hash": c.written_on.sha_hash
                    },
                    "signature": c.signature
                }
                for c in user_identity.certs_received
            ]
        }, 200

    def certified_by(self, request):
        search = str(request.match_info['search'])
        try:
            user_identity = self.forge.user_identities[search]
        except KeyError:
            try:
                user_identity = next(i for i in self.forge.user_identities.values() if i.uid == search)
            except StopIteration:
                return {
                    'error': errors.NO_MEMBER_MATCHING_PUB_OR_UID,
                    'message': "No member matching this pubkey or uid"
                }, 200

        return {
            "pubkey": user_identity.pubkey,
            "uid": user_identity.uid,
            "sigDate": str(user_identity.blockstamp),
            "isMember": user_identity.member,
            "certifications": [
                {
                    "pubkey": c.from_identity.pubkey,
                    "uid": c.from_identity.uid,
                    "isMember": c.from_identity.member,
                    "wasMember": c.from_identity.was_member,
                    "cert_time": {
                        "block": c.block,
                        "medianTime": c.mediantime
                    },
                    "sigDate": str(c.from_identity.blockstamp),
                    "written": {
                        "number": c.written_on.number,
                        "hash": c.written_on.sha_hash
                    },
                    "signature": c.signature
                }
                for c in user_identity.certs_sent
            ]
        }, 200

    def lookup(self, request):
        search = str(request.match_info['search'])
        matched = [i for i in self.forge.user_identities.values() if search in i.pubkey or search in i.uid]

        return {
            "partial": False,
            "results":  [
                {
                    "pubkey": m.pubkey,
                    "uid": m.uid,
                    "meta": {
                        "timestamp": str(m.blockstamp),
                    },
                    "revoked": m.revoked,
                    "revoked_on": m.revoked_on,
                    "revocation_sig": m.revocation_sig,
                    "self": m.signature,
                    "others": [
                        {
                            "pubkey": c.to_identity.pubkey,
                            "meta": {
                                "block_number": c.block,
                            },
                            "uids": [c.to_identity.uid],
                            "isMember": c.to_identity.member,
                            "wasMember": c.to_identity.was_member,
                            "signature": c.signature
                        } for c in m.certs_received
                    ],
                    "signed": [
                        {
                            "pubkey": c.to_identity.pubkey,
                            "meta": {
                                "block_number": c.block,
                            },
                            "uids": [c.to_identity.uid],
                            "isMember": c.to_identity.member,
                            "wasMember": c.to_identity.was_member,
                            "signature": c.signature
                        } for c in m.certs_sent
                    ]
                }
                for m in matched
            ]
        }, 200

    def peer_doc(self):
        peer = Peer(2, self.forge.currency, self.forge.key.pubkey, BlockUID.empty(),
                    [BMAEndpoint(None, "127.0.0.1", None, self.http.port)], None)
        peer.sign([self.forge.key])
        return peer
