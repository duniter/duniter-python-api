import re

import attr

from ..document import MalformedDocumentError
from ..block import BlockUID
from ...constants import WS2P_PUBLIC_PREFIX_REGEX, WS2P_PRIVATE_PREFIX_REGEX, WS2P_HEAD_REGEX, \
    PUBKEY_REGEX, SIGNATURE_REGEX, WS2PID_REGEX, BLOCK_UID_REGEX


@attr.s()
class API:
    re_inline = re.compile("WS2P({ws2p_private})?({ws2p_public})?".format(
        ws2p_private=WS2P_PRIVATE_PREFIX_REGEX,
        ws2p_public=WS2P_PUBLIC_PREFIX_REGEX))

    private = attr.ib(type=str)
    public = attr.ib(type=str)

    @classmethod
    def from_inline(cls, inline):
        data = API.re_inline.match(inline)
        if data.group(1):
            private = data.group(1)
        else:
            private = ""

        if data.group(2):
            public = data.group(2)
        else:
            public = ""

        return cls(private, public)

    def __str__(self):
        return "WS2P" + self.private + self.public


@attr.s()
class Head:
    re_inline = re.compile(WS2P_HEAD_REGEX)

    version = attr.ib(type=int)

    @classmethod
    def from_inline(cls, inline):
        try:
            data = Head.re_inline.match(inline)
            head = data.group(0).split(':')
            if len(head) == 2:
                version = int(head[1])
            else:
                version = 0
            return cls(version)
        except AttributeError:
            raise MalformedDocumentError("Head")

    def __str__(self):
        return "HEAD" if self.version == 0 else "HEAD:{}".format(str(self.version))


@attr.s()
class HeadV0:
    """
    A document describing a self certification.
    """

    re_inline = re.compile("^(WS2P(?:{ws2p_private})?(?:{ws2p_public})?):({head}):({pubkey}):({blockstamp})(?::)?(.*)"
                           .format(ws2p_private=WS2P_PRIVATE_PREFIX_REGEX,
                                   ws2p_public=WS2P_PUBLIC_PREFIX_REGEX,
                                   head=WS2P_HEAD_REGEX,
                                   version="[0-9]+",
                                   pubkey=PUBKEY_REGEX,
                                   blockstamp=BLOCK_UID_REGEX))

    re_signature = re.compile(SIGNATURE_REGEX)

    signature = attr.ib(type=str)
    api = attr.ib(type=API)
    head = attr.ib(type=Head)
    pubkey = attr.ib(type=str)
    blockstamp = attr.ib(type=BlockUID)

    @classmethod
    def from_inline(cls, inline, signature):
        try:
            data = HeadV0.re_inline.match(inline)
            api = API.from_inline(data.group(1))
            head = Head.from_inline(data.group(2))
            pubkey = data.group(3)
            blockstamp = BlockUID.from_str(data.group(4))
            offload = data.group(5)
            return cls(signature, api, head, pubkey, blockstamp), offload
        except AttributeError:
            raise MalformedDocumentError("HeadV0")

    def inline(self):
        values = (str(v) for v in attr.astuple(self, recurse=False,
                                               filter=attr.filters.exclude(attr.fields(HeadV0).signature)))
        return ":".join(values)


@attr.s()
class HeadV1:
    re_inline = re.compile("({ws2pid}):({software}):({software_version}):({pow_prefix})(?::)?(.*)".format(
        ws2pid=WS2PID_REGEX,
        software="[A-Za-z-_]+",
        software_version="[0-9]+[.][0-9]+[.][0-9]+",
        pow_prefix="[0-9]+"))

    v0 = attr.ib(type=HeadV0)
    ws2pid = attr.ib(type=str)
    software = attr.ib(type=str)
    software_version = attr.ib(type=str)
    pow_prefix = attr.ib(type=int)

    @classmethod
    def from_inline(cls, inline, signature):
        try:
            v0, offload = HeadV0.from_inline(inline, signature)
            data = HeadV1.re_inline.match(offload)
            ws2pid = data.group(1)
            software = data.group(2)
            software_version = data.group(3)
            pow_prefix = int(data.group(4))
            offload = data.group(5)
            return cls(v0, ws2pid, software, software_version, pow_prefix), offload
        except AttributeError:
            raise MalformedDocumentError("HeadV1")

    def inline(self):
        values = [str(v) for v in attr.astuple(self, True, filter=attr.filters.exclude(attr.fields(HeadV1).v0))]
        return self.v0.inline() + ":" + ":".join(values)

    @property
    def pubkey(self):
        return self.v0.pubkey

    @property
    def signature(self):
        return self.v0.signature

    @property
    def blockstamp(self):
        return self.v0.blockstamp


@attr.s
class HeadV2:
    re_inline = re.compile("({free_member_room}):({free_mirror_room})(?::)?(.*)".format(
        free_member_room="[0-9]+",
        free_mirror_room="[0-9]+"))

    v1 = attr.ib(type=HeadV1)
    free_member_room = attr.ib(type=int)
    free_mirror_room = attr.ib(type=int)

    @classmethod
    def from_inline(cls, inline, signature):
        try:
            v1, offload = HeadV1.from_inline(inline, signature)
            data = HeadV2.re_inline.match(offload)
            free_member_room = int(data.group(1))
            free_mirror_room = int(data.group(2))
            return cls(v1, free_member_room, free_mirror_room), ""
        except AttributeError:
            raise MalformedDocumentError("HeadV2")

    def inline(self):
        values = (str(v) for v in attr.astuple(self, True, filter=attr.filters.exclude(attr.fields(HeadV2).v1)))
        return self.v1.inline() + ":" + ":".join(values)

    @property
    def pubkey(self):
        return self.v1.pubkey

    @property
    def signature(self):
        return self.v1.signature

    @property
    def blockstamp(self):
        return self.v1.blockstamp
