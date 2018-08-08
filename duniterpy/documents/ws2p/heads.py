import attr
import re

from ..block import BlockUID
from ..constants import ws2p_public_prefix_regex, ws2p_private_prefix_regex,\
    pubkey_regex, signature_regex, ws2pid_regex, block_uid_regex, ws2p_head_regex


@attr.s()
class API:
    re_inline = re.compile("WS2P({ws2p_private})?({ws2p_public})?"
                            .format(
                                    ws2p_private=ws2p_private_prefix_regex,
                                    ws2p_public=ws2p_public_prefix_regex))

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
    re_inline = re.compile(ws2p_head_regex)

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
                                .format(ws2p_private=ws2p_private_prefix_regex,
                                        ws2p_public=ws2p_public_prefix_regex,
                                        head=ws2p_head_regex,
                                        version="[0-9]+",
                                        pubkey=pubkey_regex,
                                        blockstamp=block_uid_regex))

    re_signature = re.compile(signature_regex)

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
    re_inline = re.compile("({ws2pid}):" \
                            "({software}):({software_version}):({pow_prefix})(?::)?(.*)"
                            .format(
                                ws2pid=ws2pid_regex,
                                software="[A-Za-z-_]+",
                                software_version="[0-9]+[.][0-9]+[.][0-9]+-?[A-Za-z0-9\.]+",
                                pow_prefix="[0-9]+"))

    v0 = attr.ib(type=HeadV0)
    ws2pid = attr.ib(type=str)
    software = attr.ib(type=str)
    software_version = attr.ib(type=str)
    pow_prefix= attr.ib(type=int)

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
    re_inline = re.compile("({free_member_room}):({free_mirror_room})(?::)?(.*)"
                            .format(
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