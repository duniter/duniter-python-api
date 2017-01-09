import attr


@attr.s()
class UserIdentity:
    pubkey = attr.ib(repr=True)
    uid = attr.ib(repr=True)
    blockstamp = attr.ib(repr=True)
    signature = attr.ib()
    member = attr.ib(default=False)
    was_member = attr.ib(default=False)
    revoked = attr.ib(default=False)
    revoked_on = attr.ib(default=None)
    revocation_sig = attr.ib(default=None)
    sources = attr.ib(default=attr.Factory(list))
    certs_sent = attr.ib(default=attr.Factory(list))
    certs_received = attr.ib(default=attr.Factory(list))
    memberships = attr.ib(default=attr.Factory(list))
    tx_sent = attr.ib(default=attr.Factory(list))
    tx_received = attr.ib(default=attr.Factory(list))
    ud_generated = attr.ib(default=attr.Factory(list))

