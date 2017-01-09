import attr


@attr.s()
class UD:
    amount = attr.ib(repr=True)
    base = attr.ib(repr=True)
    block_number = attr.ib()
    time = attr.ib()



