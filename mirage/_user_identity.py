import attr


@attr.s()
class UserIdentity:
    pubkey = attr.ib()
    uid = attr.ib()
    blockstamp = attr.ib()
    member = attr.ib()
