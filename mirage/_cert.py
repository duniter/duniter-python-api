import attr


@attr.s()
class Cert:
    from_identity = attr.ib(repr=True)
    to_identity = attr.ib(repr=True)
    signature = attr.ib()
    written_on = attr.ib()
    block = attr.ib()
    mediantime = attr.ib()
