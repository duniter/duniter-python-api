import attr


@attr.s()
class UserIdentity:
    pubkey = attr.ib(repr=True)
    uid = attr.ib(repr=True)
    blockstamp = attr.ib(repr=True)
    member = attr.ib(default=False)
    sources = attr.ib(default=attr.Factory(list))

