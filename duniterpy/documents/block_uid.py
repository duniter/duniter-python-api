import re
from typing import Union, TypeVar, Type

from .document import MalformedDocumentError
from ..constants import EMPTY_HASH, BLOCK_ID_REGEX, BLOCK_HASH_REGEX

# required to type hint cls in classmethod
BlockUIDType = TypeVar("BlockUIDType", bound="BlockUID")


class BlockUID:
    """
    A simple block id
    """

    re_block_uid = re.compile(
        "({block_id_regex})-({block_hash_regex})".format(
            block_id_regex=BLOCK_ID_REGEX, block_hash_regex=BLOCK_HASH_REGEX
        )
    )
    re_hash = re.compile(
        "({block_hash_regex})".format(block_hash_regex=BLOCK_HASH_REGEX)
    )

    def __init__(self, number: int, sha_hash: str) -> None:
        assert type(number) is int
        assert BlockUID.re_hash.match(sha_hash) is not None
        self.number = number
        self.sha_hash = sha_hash

    @classmethod
    def empty(cls: Type[BlockUIDType]) -> BlockUIDType:
        return cls(0, EMPTY_HASH)

    @classmethod
    def from_str(cls: Type[BlockUIDType], blockid: str) -> BlockUIDType:
        """
        :param blockid: The block id
        """
        data = BlockUID.re_block_uid.match(blockid)
        if data is None:
            raise MalformedDocumentError("BlockUID")
        try:
            number = int(data.group(1))
        except AttributeError:
            raise MalformedDocumentError("BlockUID")

        try:
            sha_hash = data.group(2)
        except AttributeError:
            raise MalformedDocumentError("BlockHash")

        return cls(number, sha_hash)

    def __str__(self) -> str:
        return "{0}-{1}".format(self.number, self.sha_hash)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BlockUID):
            return NotImplemented
        return self.number == other.number and self.sha_hash == other.sha_hash

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BlockUID):
            return NotImplemented
        return self.number < other.number

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, BlockUID):
            return NotImplemented
        return self.number > other.number

    def __le__(self, other: object) -> bool:
        if not isinstance(other, BlockUID):
            return NotImplemented
        return self.number <= other.number

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, BlockUID):
            return NotImplemented
        return self.number >= other.number

    def __hash__(self) -> int:
        return hash((self.number, self.sha_hash))

    def __bool__(self) -> bool:
        return self != BlockUID.empty()


def block_uid(value: Union[str, BlockUID, None]) -> BlockUID:
    """
    Convert value to BlockUID instance

    :param value: Value to convert
    :return:
    """
    if isinstance(value, BlockUID):
        result = value
    elif isinstance(value, str):
        result = BlockUID.from_str(value)
    elif value is None:
        result = BlockUID.empty()
    else:
        raise TypeError("Cannot convert {0} to BlockUID".format(type(value)))

    return result
