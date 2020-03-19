import attr
from duniterpy.documents import BlockUID, Identity, Certification, Transaction
from duniterpy.documents.peer import Peer
from duniterpy.api.endpoint import BMAEndpoint
from duniterpy.api import errors
from duniterpy.key import SigningKey
from duniterpy.key.scrypt_params import ScryptParams
from .http import HTTPServer
from .block_forge import BlockForge
import logging


@attr.s()
class Node:
    http = attr.ib()
    forge = attr.ib()
    reject_next_post = attr.ib(default=False)
    _logger = attr.ib(default=attr.Factory(lambda: logging.getLogger("mirage")))

    @classmethod
    async def start(cls, port, currency, salt, password, loop):
        key = SigningKey.from_credentials(salt, password, ScryptParams(2 ** 12, 16, 1))
        node = cls(HTTPServer(port, loop), BlockForge(currency, key))

        get_routes = {
            "/network/peering": node.peering,
            "/blockchain/block/{number}": node.block_by_number,
            "/blockchain/current": node.current_block,
            "/tx/sources/{pubkey}": node.sources,
            "/wot/lookup/{search}": node.lookup,
            "/wot/certifiers-of/{search}": node.certifiers_of,
            "/wot/certified-by/{search}": node.certified_by,
            "/wot/requirements/{pubkey}": node.requirements,
            "/blockchain/parameters": node.parameters,
            "/blockchain/with/ud": node.with_ud,
            "/blockchain/memberships/{search}": node.memberships,
            "/tx/history/{search}": node.tx_history,
            "/tx/history/{search}/blocks/{from}/{to}": node.tx_history_range,
            "/ud/history/{search}": node.ud_history,
        }
        post_routes = {
            "/wot/add": node.add,
            "/wot/certify": node.certify,
            "/tx/process": node.process,
        }
        for r, h in get_routes.items():
            node.http.add_route("GET", r, h)
        for r, h in post_routes.items():
            node.http.add_route("POST", r, h)
        port, url = await node.http.create_server()
        print("Server started on {0}".format(url))
        return node

    async def add(self, request):
        data = await request.post()
        if self.reject_next_post:
            self.reject_next_post = False
            return {"ucode": errors.UNHANDLED, "message": "Rejected"}, 400
        identity = Identity.from_signed_raw(data["identity"])
        self.forge.pool.append(identity)
        return {}, 200

    async def process(self, request):
        data = await request.post()
        if self.reject_next_post:
            self.reject_next_post = False
            return {"ucode": errors.UNHANDLED, "message": "Rejected"}, 400
        transaction = Transaction.from_signed_raw(data["transaction"])
        self.forge.pool.append(transaction)
        return {}, 200

    async def certify(self, request):
        data = await request.post()
        if self.reject_next_post:
            self.reject_next_post = False
            return {"ucode": errors.UNHANDLED, "message": "Rejected"}, 400
        certification = Certification.from_signed_raw(data["cert"])
        self.forge.pool.append(certification)
        return {}, 200

    async def requirements(self, request):
        pubkey = request.match_info["pubkey"]
        try:
            user_identity = self.forge.user_identities[pubkey]
        except KeyError:
            try:
                user_identity = next(
                    i for i in self.forge.user_identities.values() if i.uid == pubkey
                )
            except StopIteration:
                return (
                    {
                        "ucode": errors.NO_MEMBER_MATCHING_PUB_OR_UID,
                        "message": "No member matching this pubkey or uid",
                    },
                    404,
                )
        return (
            {
                "identities": [
                    {
                        "pubkey": user_identity.pubkey,
                        "uid": user_identity.uid,
                        "meta": {"timestamp": str(user_identity.blockstamp)},
                        "wasMember": user_identity.was_member,
                        "isSentry": True,
                        "revoked": user_identity.revoked,
                        "revocation_sig": user_identity.revocation_sig,
                        "revoked_on": user_identity.revoked_on,
                        "expired": user_identity.revoked,
                        "outdistanced": not user_identity.member,
                        "certifications": [
                            {
                                "from": c.from_identity.pubkey,
                                "to": c.to_identity.pubkey,
                                "expiresIn": max(
                                    self.forge.blocks[-1].mediantime
                                    - 31557600
                                    - c.mediantime,
                                    0,
                                ),
                            }
                            for c in user_identity.certs_received
                        ],
                        "membershipPendingExpiresIn": 0
                        if not user_identity.member
                        else 10000000,
                        "membershipExpiresIn": max(
                            self.forge.blocks[-1].mediantime
                            - 15778800
                            - user_identity.memberships[-1].timestamp,
                            0,
                        ),
                    },
                ]
            },
            200,
        )

    async def block_by_number(self, request):
        number = int(request.match_info["number"])
        try:
            block = self.forge.blocks[number]
            return (
                {
                    "version": block.version,
                    "nonce": block.noonce,
                    "number": block.number,
                    "powMin": block.powmin,
                    "time": block.time,
                    "medianTime": block.mediantime,
                    "membersCount": block.members_count,
                    "monetaryMass": self.forge.monetary_mass(number),
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
                    "transactions": [t.compact() for t in block.transactions],
                    "raw": block.raw(),
                },
                200,
            )
        except IndexError:
            return {"ucode": errors.BLOCK_NOT_FOUND, "message": "Block not found"}, 404

    async def current_block(self, _):
        try:
            block = self.forge.blocks[-1]
            return (
                {
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
                    "identities": [i.inline() for i in block.identities],
                    "joiners": [m.inline() for m in block.joiners],
                    "actives": [m.inline() for m in block.actives],
                    "leavers": [m.inline() for m in block.leavers],
                    "revoked": [r.inline() for r in block.revoked],
                    "excluded": [i.inline() for i in block.excluded],
                    "certifications": [c.inline() for c in block.certifications],
                    "transactions": [t.inline() for t in block.transactions],
                    "raw": block.raw(),
                },
                200,
            )
        except IndexError:
            return (
                {"ucode": errors.NO_CURRENT_BLOCK, "message": "No current block"},
                404,
            )

    async def sources(self, request):
        pubkey = str(request.match_info["pubkey"])
        try:
            sources = self.forge.user_identities[pubkey].sources
            return (
                {
                    "currency": self.forge.currency,
                    "pubkey": pubkey,
                    "sources": [
                        {
                            "type": s.source,
                            "noffset": s.index,
                            "identifier": s.origin_id,
                            "amount": s.amount,
                            "base": s.base,
                            "conditions": "SIG({0})".format(pubkey),
                        }
                        for s in sources
                    ],
                },
                200,
            )
        except KeyError:
            return (
                {"currency": self.forge.currency, "pubkey": pubkey, "sources": []},
                200,
            )

    async def peering(self, _):
        return (
            {
                "version": 2,
                "currency": self.peer_doc().currency,
                "endpoints": [str(self.peer_doc().endpoints[0])],
                "status": "UP",
                "block": str(self.peer_doc().blockUID),
                "signature": self.peer_doc().signatures[0],
                "raw": self.peer_doc().raw(),
                "pubkey": self.peer_doc().pubkey,
            },
            200,
        )

    async def parameters(self, _):
        return (
            {
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
                "percentRot": 0.66,
                "udTime0": 1488970800,
                "udReevalTime0": 1490094000,
                "dtReeval": 15778800,
            },
            200,
        )

    async def with_ud(self, _):
        return (
            {"result": {"blocks": [b.number for b in self.forge.blocks if b.ud]}},
            200,
        )

    async def memberships(self, request):
        search = str(request.match_info["search"])
        try:
            user_identity = self.forge.user_identities[search]
        except KeyError:
            try:
                user_identity = next(
                    i for i in self.forge.user_identities.values() if i.uid == search
                )
            except StopIteration:
                return (
                    {
                        "ucode": errors.NO_MEMBER_MATCHING_PUB_OR_UID,
                        "message": "No member matching this pubkey or uid",
                    },
                    404,
                )

        return (
            {
                "pubkey": user_identity.pubkey,
                "uid": user_identity.uid,
                "sigDate": str(user_identity.blockstamp),
                "memberships": [
                    {
                        "version": 2,
                        "currency": self.forge.currency,
                        "membership": m.type,
                        "blockNumber": m.blockstamp.number,
                        "blockHash": m.blockstamp.sha_hash,
                        "written": m.written_on,
                    }
                    for m in user_identity.memberships
                ],
            },
            200,
        )

    async def certifiers_of(self, request):
        search = str(request.match_info["search"])
        try:
            user_identity = self.forge.user_identities[search]
        except KeyError:
            try:
                user_identity = next(
                    i for i in self.forge.user_identities.values() if i.uid == search
                )
            except StopIteration:
                return (
                    {
                        "ucode": errors.NO_MEMBER_MATCHING_PUB_OR_UID,
                        "message": "No member matching this pubkey or uid",
                    },
                    404,
                )

        return (
            {
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
                        "cert_time": {"block": c.block, "medianTime": c.mediantime},
                        "sigDate": str(c.from_identity.blockstamp),
                        "written": {
                            "number": c.written_on.number,
                            "hash": c.written_on.sha_hash,
                        },
                        "signature": c.signature,
                    }
                    for c in user_identity.certs_received
                ],
            },
            200,
        )

    async def certified_by(self, request):
        search = str(request.match_info["search"])
        try:
            user_identity = self.forge.user_identities[search]
        except KeyError:
            try:
                user_identity = next(
                    i for i in self.forge.user_identities.values() if i.uid == search
                )
            except StopIteration:
                return (
                    {
                        "ucode": errors.NO_MEMBER_MATCHING_PUB_OR_UID,
                        "message": "No member matching this pubkey or uid",
                    },
                    404,
                )

        return (
            {
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
                        "cert_time": {"block": c.block, "medianTime": c.mediantime},
                        "sigDate": str(c.from_identity.blockstamp),
                        "written": {
                            "number": c.written_on.number,
                            "hash": c.written_on.sha_hash,
                        },
                        "signature": c.signature,
                    }
                    for c in user_identity.certs_sent
                ],
            },
            200,
        )

    async def lookup(self, request):
        search = str(request.match_info["search"])
        matched = [
            i
            for i in self.forge.user_identities.values()
            if search in i.pubkey or search in i.uid
        ]

        return (
            {
                "partial": False,
                "results": [
                    {
                        "pubkey": m.pubkey,
                        "uids": [
                            {
                                "uid": m.uid,
                                "meta": {"timestamp": str(m.blockstamp)},
                                "revoked": m.revoked,
                                "revoked_on": m.revoked_on,
                                "revocation_sig": m.revocation_sig,
                                "self": m.signature,
                                "others": [
                                    {
                                        "pubkey": c.to_identity.pubkey,
                                        "meta": {"block_number": c.block},
                                        "uids": [c.to_identity.uid],
                                        "isMember": c.to_identity.member,
                                        "wasMember": c.to_identity.was_member,
                                        "signature": c.signature,
                                    }
                                    for c in m.certs_received
                                ],
                            }
                        ],
                        "signed": [
                            {
                                "pubkey": c.to_identity.pubkey,
                                "meta": {"timestamp": str(c.to_identity.blockstamp)},
                                "cert_time": {
                                    "block": c.block,
                                    "block_hash": str(
                                        self.forge.blocks[c.block].blockUID
                                    ),
                                },
                                "uid": c.to_identity.uid,
                                "isMember": c.to_identity.member,
                                "wasMember": c.to_identity.was_member,
                                "revoked": c.to_identity.revoked,
                                "revoked_on": c.to_identity.revoked_on,
                                "revocation_sig": c.to_identity.revocation_sig,
                                "signature": c.signature,
                            }
                            for c in m.certs_sent
                        ],
                    }
                    for m in matched
                ],
            },
            200,
        )

    async def tx_history(self, request):
        search = str(request.match_info["search"])
        try:
            user_identity = self.forge.user_identities[search]
        except KeyError:
            try:
                user_identity = next(
                    i for i in self.forge.user_identities.values() if i.uid == search
                )
            except StopIteration:
                return (
                    {
                        "currency": self.forge.currency,
                        "pubkey": search,
                        "history": {
                            "sent": [],
                            "received": [],
                            "sending": [],
                            "receiving": [],
                            "pending": [],
                        },
                    },
                    200,
                )
        return (
            {
                "currency": self.forge.currency,
                "pubkey": user_identity.pubkey,
                "history": {
                    "sent": [
                        {
                            "version": tx.version,
                            "issuers": tx.issuers,
                            "inputs": [i.inline(tx.version) for i in tx.inputs],
                            "unlocks": [u.inline() for u in tx.unlocks],
                            "outputs": [o.inline() for o in tx.outputs],
                            "comment": tx.comment,
                            "locktime": tx.locktime,
                            "blockstamp": str(tx.blockstamp),
                            "blockstampTime": next(
                                [
                                    b.mediantime
                                    for b in self.forge.blocks
                                    if b.number == tx.blockstamp.number
                                ]
                            ),
                            "signatures": tx.signatures,
                            "hash": tx.sha_hash,
                            "block_number": next(
                                (
                                    b.number
                                    for b in self.forge.blocks
                                    if tx.sha_hash
                                    in [tx.sha_hash for tx in b.transactions]
                                )
                            ),
                            "time": next(
                                (
                                    b.mediantime
                                    for b in self.forge.blocks
                                    if tx.sha_hash
                                    in [tx.sha_hash for tx in b.transactions]
                                )
                            ),
                        }
                        for tx in user_identity.tx_sent
                    ],
                    "received": [
                        {
                            "version": tx.version,
                            "issuers": tx.issuers,
                            "inputs": [i.inline(tx.version) for i in tx.inputs],
                            "unlocks": [u.inline() for u in tx.unlocks],
                            "outputs": [o.inline() for o in tx.outputs],
                            "comment": tx.comment,
                            "locktime": tx.locktime,
                            "blockstamp": str(tx.blockstamp),
                            "blockstampTime": next(
                                [
                                    b.mediantime
                                    for b in self.forge.blocks
                                    if b.number == tx.blockstamp.number
                                ]
                            ),
                            "signatures": tx.signatures,
                            "hash": tx.sha_hash,
                            "block_number": next(
                                (
                                    b.number
                                    for b in self.forge.blocks
                                    if tx.sha_hash
                                    in [tx.sha_hash for tx in b.transactions]
                                )
                            ),
                            "time": next(
                                (
                                    b.mediantime
                                    for b in self.forge.blocks
                                    if tx.sha_hash
                                    in [tx.sha_hash for tx in b.transactions]
                                )
                            ),
                        }
                        for tx in user_identity.tx_received
                    ],
                    "sending": [],
                    "receiving": [],
                    "pending": [],
                },
            },
            200,
        )

    async def tx_history_range(self, request):
        try:
            search = str(request.match_info["search"])
            start = int(request.match_info["from"])
            end = int(request.match_info["to"])
            try:
                user_identity = self.forge.user_identities[search]
            except KeyError:
                try:
                    user_identity = next(
                        i
                        for i in self.forge.user_identities.values()
                        if i.uid == search
                    )
                except StopIteration:
                    return (
                        {
                            "currency": self.forge.currency,
                            "pubkey": search,
                            "history": {
                                "sent": [],
                                "received": [],
                                "sending": [],
                                "receiving": [],
                                "pending": [],
                            },
                        },
                        200,
                    )
            return (
                {
                    "currency": self.forge.currency,
                    "pubkey": user_identity.pubkey,
                    "history": {
                        "sent": [
                            {
                                "version": tx.version,
                                "issuers": tx.issuers,
                                "inputs": [i.inline(tx.version) for i in tx.inputs],
                                "unlocks": [u.inline() for u in tx.unlocks],
                                "outputs": [o.inline() for o in tx.outputs],
                                "comment": tx.comment,
                                "locktime": tx.locktime,
                                "blockstamp": str(tx.blockstamp),
                                "blockstampTime": next(
                                    (
                                        b.mediantime
                                        for b in self.forge.blocks
                                        if b.number == tx.blockstamp.number
                                    )
                                ),
                                "signatures": tx.signatures,
                                "hash": tx.sha_hash,
                                "block_number": next(
                                    (
                                        b.number
                                        for b in self.forge.blocks
                                        if tx.sha_hash
                                        in [tx.sha_hash for tx in b.transactions]
                                    )
                                ),
                                "time": next(
                                    (
                                        b.mediantime
                                        for b in self.forge.blocks
                                        if tx.sha_hash
                                        in [tx.sha_hash for tx in b.transactions]
                                    )
                                ),
                            }
                            for tx in user_identity.tx_sent
                            if start <= tx.blockstamp.number <= end
                        ],
                        "received": [
                            {
                                "version": tx.version,
                                "issuers": tx.issuers,
                                "inputs": [i.inline(tx.version) for i in tx.inputs],
                                "unlocks": [u.inline() for u in tx.unlocks],
                                "outputs": [o.inline() for o in tx.outputs],
                                "comment": tx.comment,
                                "locktime": tx.locktime,
                                "blockstamp": str(tx.blockstamp),
                                "blockstampTime": next(
                                    (
                                        b.mediantime
                                        for b in self.forge.blocks
                                        if b.number == tx.blockstamp.number
                                    )
                                ),
                                "signatures": tx.signatures,
                                "hash": tx.sha_hash,
                                "block_number": next(
                                    (
                                        b.number
                                        for b in self.forge.blocks
                                        if tx.sha_hash
                                        in [tx.sha_hash for tx in b.transactions]
                                    )
                                ),
                                "time": next(
                                    (
                                        b.mediantime
                                        for b in self.forge.blocks
                                        if tx.sha_hash
                                        in [tx.sha_hash for tx in b.transactions]
                                    )
                                ),
                            }
                            for tx in user_identity.tx_received
                            if start <= tx.blockstamp.number <= end
                        ],
                        "sending": [],
                        "receiving": [],
                        "pending": [],
                    },
                },
                200,
            )
        except Exception as e:
            print(str(e))

    async def ud_history(self, request):
        search = str(request.match_info["search"])
        try:
            user_identity = self.forge.user_identities[search]
        except KeyError:
            try:
                user_identity = next(
                    i for i in self.forge.user_identities.values() if i.uid == search
                )
            except StopIteration:
                return (
                    {
                        "currency": self.forge.currency,
                        "pubkey": search,
                        "history": {"history": []},
                    },
                    200,
                )
        return (
            {
                "currency": self.forge.currency,
                "pubkey": user_identity.pubkey,
                "history": {
                    "history": [attr.asdict(ud) for ud in user_identity.ud_generated]
                },
            },
            200,
        )

    def peer_doc(self):
        peer = Peer(
            2,
            self.forge.currency,
            self.forge.key.pubkey,
            BlockUID.empty(),
            [BMAEndpoint("", "127.0.0.1", "", self.http.port)],
            None,
        )
        peer.sign([self.forge.key])
        return peer

    async def close(self):
        await self.http.close()
