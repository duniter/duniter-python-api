import attr


@attr.s()
class MS:
    pubkey = attr.ib()
    type = attr.ib()
    written_on = attr.ib()
    blockstamp = attr.ib()
    timestamp = attr.ib()
