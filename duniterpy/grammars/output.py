from typing import Optional, TypeVar, Type, Any, Union

from pypeg2 import re, attr, Keyword, Enum, contiguous, maybe_some, whitespace, K

from ..constants import PUBKEY_REGEX, HASH_REGEX


class Pubkey(str):
    """
    Pubkey in transaction output condition
    """

    regex = re.compile(PUBKEY_REGEX)


class Hash(str):
    """
    Hash in transaction output condition
    """

    regex = re.compile(HASH_REGEX)


class Int(str):
    """
    Integer in transaction output condition
    """

    regex = re.compile(r"[0-9]+")


# required to type hint cls in classmethod
SIGType = TypeVar("SIGType", bound="SIG")


class SIG:
    """
    SIGnature function in transaction output condition
    """

    grammar = "SIG(", attr("pubkey", Pubkey), ")"

    def __init__(self, value: str = "") -> None:
        """
        Init SIG instance

        :param value: Content of the string
        """
        self.value = value
        self.pubkey = ""

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        """
        Check SIG instances equality
        """
        if not isinstance(other, SIG):
            return NotImplemented
        return self.value == other.value and self.pubkey == other.pubkey

    def __hash__(self) -> int:
        return hash((self.value, self.pubkey))

    @classmethod
    def token(cls: Type[SIGType], pubkey: str) -> SIGType:
        """
        Return SIG instance from pubkey

        :param pubkey: Public key of the signature issuer
        :return:
        """
        sig = cls()
        sig.pubkey = pubkey
        return sig

    def compose(
        self, parser: Any = None, grammar: Any = None, attr_of: Any = None
    ) -> str:
        """
        Return the SIG(pubkey) expression as string format

        :param parser: Parser instance
        :param grammar: Grammar
        :param attr_of: Attribute of...
        :return:
        """
        return "SIG({0})".format(self.pubkey)


# required to type hint cls in classmethod
CSVType = TypeVar("CSVType", bound="CSV")


class CSV:
    """
    CSV function in transaction output condition
    """

    grammar = "CSV(", attr("time", Int), ")"

    def __init__(self, value: str = "") -> None:
        """
        Init CSV instance

        :param value: Content of the string
        """
        self.value = value
        self.time = ""

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        """
        Check CSV instances equality
        """
        if not isinstance(other, CSV):
            return NotImplemented
        return self.value == other.value and self.time == other.time

    def __hash__(self) -> int:
        return hash((self.value, self.time))

    @classmethod
    def token(cls: Type[CSVType], time: int) -> CSVType:
        """
        Return CSV instance from time

        :param time: Timestamp
        :return:
        """
        csv = cls()
        csv.time = str(time)
        return csv

    def compose(
        self, parser: Any = None, grammar: Any = None, attr_of: str = None
    ) -> str:
        """
        Return the CSV(time) expression as string format

        :param parser: Parser instance
        :param grammar: Grammar
        :param attr_of: Attribute of...
        """
        return "CSV({0})".format(self.time)


# required to type hint cls in classmethod
CLTVType = TypeVar("CLTVType", bound="CLTV")


class CLTV:
    """
    CLTV function in transaction output condition
    """

    grammar = "CLTV(", attr("timestamp", Int), ")"

    def __init__(self, value: str = "") -> None:
        """
        Init CLTV instance

        :param value: Content of the string
        """
        self.value = value
        self.timestamp = ""

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        """
        Check CLTV instances equality
        """
        if not isinstance(other, CLTV):
            return NotImplemented
        return self.value == other.value and self.timestamp == other.timestamp

    def __hash__(self) -> int:
        return hash((self.value, self.timestamp))

    @classmethod
    def token(cls: Type[CLTVType], timestamp: int) -> CLTVType:
        """
        Return CLTV instance from timestamp

        :param timestamp: Timestamp
        :return:
        """
        cltv = cls()
        cltv.timestamp = str(timestamp)
        return cltv

    def compose(
        self, parser: Any = None, grammar: Any = None, attr_of: str = None
    ) -> str:
        """
        Return the CLTV(timestamp) expression as string format

        :param parser: Parser instance
        :param grammar: Grammar
        :param attr_of: Attribute of...
        """
        return "CLTV({0})".format(self.timestamp)


# required to type hint cls in classmethod
XHXType = TypeVar("XHXType", bound="XHX")


class XHX:
    """
    XHX function in transaction output condition
    """

    grammar = "XHX(", attr("sha_hash", Hash), ")"

    def __init__(self, value: str = "") -> None:
        """
        Init XHX instance

        :param value: Content of the string
        """
        self.value = value
        self.sha_hash = ""

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: Any) -> bool:
        """
        Check XHX instances equality
        """
        if not isinstance(other, XHX):
            return NotImplemented
        return self.value == other.value and self.sha_hash == other.sha_hash

    def __hash__(self) -> int:
        return hash((self.value, self.sha_hash))

    @classmethod
    def token(cls: Type[XHXType], sha_hash: str) -> XHXType:
        """
        Return XHX instance from sha_hash

        :param sha_hash: SHA256 hash
        :return:
        """
        xhx = cls()
        xhx.sha_hash = sha_hash
        return xhx

    def compose(
        self, parser: Any = None, grammar: Any = None, attr_of: str = None
    ) -> str:
        """
        Return the XHX(sha_hash) expression as string format

        :param parser: Parser instance
        :param grammar: Grammar
        :param attr_of: Attribute of...
        """
        return "XHX({0})".format(self.sha_hash)


# required to type hint cls in classmethod
OperatorType = TypeVar("OperatorType", bound="Operator")


class Operator(Keyword):
    """
    Operator in transaction output condition
    """

    grammar = Enum(K("&&"), K("||"), K("AND"), K("OR"))
    regex = re.compile(r"[&&|\|\||\w]+")

    @classmethod
    def token(cls: Type[OperatorType], keyword: str) -> OperatorType:
        """
        Return Operator instance from keyword

        :param keyword: Operator keyword in expression
        :return:
        """
        op = cls(keyword)
        return op

    def compose(
        self, parser: Any = None, grammar: Any = None, attr_of: str = None
    ) -> str:
        """
        Return the Operator keyword as string format

        :param parser: Parser instance
        :param grammar: Grammar
        :param attr_of: Attribute of...
        """
        return "{0}".format(self.name)


# required to type hint cls in classmethod
ConditionType = TypeVar("ConditionType", bound="Condition")


class Condition:
    """
    Condition expression in transaction output

    """

    grammar = None

    def __init__(self, value: str = "") -> None:
        """
        Init Condition instance

        :param value: Content of the condition as string
        """
        self.value = value
        self.left = ""  # type: Union[str, Condition]
        self.right = ""  # type: Union[str, Condition]
        self.op = ""  # type: Union[str, Condition]

    def __eq__(self, other: Any) -> bool:
        """
        Check Condition instances equality
        """
        if not isinstance(other, Condition):
            return NotImplemented
        return (
            self.value == other.value
            and self.left == other.left
            and self.right == other.right
            and self.op == other.op
        )

    def __hash__(self) -> int:
        return hash((self.value, self.left, self.right, self.op))

    def __str__(self) -> str:
        return self.value

    @classmethod
    def token(
        cls: Type[ConditionType],
        left: Any,
        op: Optional[Any] = None,
        right: Optional[Any] = None,
    ) -> ConditionType:
        """
        Return Condition instance from arguments and Operator

        :param left: Left argument
        :param op: Operator
        :param right: Right argument
        :return:
        """
        condition = cls()
        condition.left = left
        if op:
            condition.op = op
        if right:
            condition.right = right
        return condition

    def compose(self, parser: Any, grammar: Any = None, attr_of: str = None) -> str:
        """
        Return the Condition as string format

        :param parser: Parser instance
        :param grammar: Grammar
        :param attr_of: Attribute of...
        """
        if type(self.left) is Condition:
            left = "({0})".format(
                parser.compose(self.left, grammar=grammar, attr_of=attr_of)
            )
        else:
            left = parser.compose(self.left, grammar=grammar, attr_of=attr_of)

        if getattr(self, "op", None):

            if type(self.right) is Condition:
                right = "({0})".format(
                    parser.compose(self.right, grammar=grammar, attr_of=attr_of)
                )
            else:
                right = parser.compose(self.right, grammar=grammar, attr_of=attr_of)
            op = parser.compose(self.op, grammar=grammar, attr_of=attr_of)
            result = "{0} {1} {2}".format(left, op, right)
        else:
            result = left
        return result


Condition.grammar = contiguous(
    attr("left", [SIG, XHX, CSV, CLTV, ("(", Condition, ")")]),
    maybe_some(
        whitespace,
        attr("op", Operator),
        whitespace,
        attr("right", [SIG, XHX, CSV, CLTV, ("(", Condition, ")")]),
    ),
)
