import re
from typing import TypeVar, List, Any, Type, Optional, Dict, Union, Tuple

import pypeg2

from duniterpy.grammars.output import Condition
from .block_uid import BlockUID
from .document import Document, MalformedDocumentError
from ..constants import (
    PUBKEY_REGEX,
    TRANSACTION_HASH_REGEX,
    BLOCK_ID_REGEX,
    BLOCK_UID_REGEX,
)
from ..grammars import output


def reduce_base(amount: int, base: int) -> Tuple[int, int]:
    """
    Compute the reduced base of the given parameters

    :param amount: the amount value
    :param base: current base value

    :return: tuple containing computed (amount, base)
    """
    if amount == 0:
        return 0, 0

    next_amount = amount
    next_base = base
    next_amount_is_integer = True
    while next_amount_is_integer:
        amount = next_amount
        base = next_base
        if next_amount % 10 == 0:
            next_amount = int(next_amount / 10)
            next_base += 1
        else:
            next_amount_is_integer = False

    return int(amount), int(base)


# required to type hint cls in classmethod
InputSourceType = TypeVar("InputSourceType", bound="InputSource")


class InputSource:
    """
    A Transaction INPUT

.. note:: Compact :
    INDEX:SOURCE:FINGERPRINT:AMOUNT

    """

    re_inline = re.compile(
        "([0-9]+):([0-9]):(?:(?:(D):({pubkey_regex}):({block_id_regex}))|(?:(T):({transaction_hash_regex}):\
([0-9]+)))".format(
            pubkey_regex=PUBKEY_REGEX,
            block_id_regex=BLOCK_ID_REGEX,
            transaction_hash_regex=TRANSACTION_HASH_REGEX,
        )
    )

    def __init__(
        self, amount: int, base: int, source: str, origin_id: str, index: int
    ) -> None:
        """
        An input source can come from a dividend or a transaction.

        :param amount: amount of the input
        :param base: base of the input
        :param source: D if dividend, T if transaction
        :param origin_id: a Public key if a dividend, a tx hash if a transaction
        :param index: a block id if a dividend, an tx index if a transaction
        :return:
        """
        self.amount = amount
        self.base = base
        self.source = source
        self.origin_id = origin_id
        self.index = index

    def __eq__(self, other: Any) -> bool:
        """
        Check InputSource instances equality
        """
        if not isinstance(other, InputSource):
            return NotImplemented
        return (
            self.amount == other.amount
            and self.base == other.base
            and self.source == other.source
            and self.origin_id == other.origin_id
            and self.index == other.index
        )

    def __hash__(self) -> int:
        return hash((self.amount, self.base, self.source, self.origin_id, self.index))

    @classmethod
    def from_inline(cls: Type[InputSourceType], inline: str) -> InputSourceType:
        """
        Return Transaction instance from inline string format

        :param inline: Inline string format
        :return:
        """
        data = InputSource.re_inline.match(inline)
        if data is None:
            raise MalformedDocumentError("Inline input")
        source_offset = 2
        amount = int(data.group(1))
        base = int(data.group(2))
        if data.group(1 + source_offset):
            source = data.group(1 + source_offset)
            origin_id = data.group(2 + source_offset)
            index = int(data.group(3 + source_offset))
        else:
            source = data.group(4 + source_offset)
            origin_id = data.group(5 + source_offset)
            index = int(data.group(6 + source_offset))

        return cls(amount, base, source, origin_id, index)

    def inline(self) -> str:
        """
        Return an inline string format of the document

        :return:
        """
        return "{0}:{1}:{2}:{3}:{4}".format(
            self.amount, self.base, self.source, self.origin_id, self.index
        )


# required to type hint cls in classmethod
OutputSourceType = TypeVar("OutputSourceType", bound="OutputSource")


class OutputSource:
    """
    A Transaction OUTPUT
    """

    re_inline = re.compile("([0-9]+):([0-9]):(.*)")

    def __init__(self, amount: int, base: int, condition: str) -> None:
        """
        Init OutputSource instance

        :param amount: Amount of the output
        :param base: Base number
        :param condition: Condition expression
        """
        self.amount = amount
        self.base = base
        self.condition = self.condition_from_text(condition)

    def __eq__(self, other: Any) -> bool:
        """
        Check OutputSource instances equality
        """
        if not isinstance(other, OutputSource):
            return NotImplemented
        return (
            self.amount == other.amount
            and self.base == other.base
            and self.condition == other.condition
        )

    def __hash__(self) -> int:
        return hash((self.amount, self.base, self.condition))

    @classmethod
    def from_inline(cls: Type[OutputSourceType], inline: str) -> OutputSourceType:
        """
        Return OutputSource instance from inline string format

        :param inline: Inline string format
        :return:
        """
        data = OutputSource.re_inline.match(inline)
        if data is None:
            raise MalformedDocumentError("Inline output")
        amount = int(data.group(1))
        base = int(data.group(2))
        condition_text = data.group(3)

        return cls(amount, base, condition_text)

    def inline(self) -> str:
        """
        Return an inline string format of the output source

        :return:
        """
        return "{0}:{1}:{2}".format(
            self.amount, self.base, pypeg2.compose(self.condition, output.Condition)
        )

    def inline_condition(self) -> str:
        """
        Return an inline string format of the output source’s condition

        :return:
        """
        return pypeg2.compose(self.condition, output.Condition)

    @staticmethod
    def condition_from_text(text) -> Condition:
        """
        Return a Condition instance with PEG grammar from text

        :param text: PEG parsable string
        :return:
        """
        try:
            condition = pypeg2.parse(text, output.Condition)
        except SyntaxError:
            # Invalid conditions are possible, see https://github.com/duniter/duniter/issues/1156
            # In such a case, they are store as empty PEG grammar object and considered unlockable
            condition = Condition(text)
        return condition


# required to type hint cls in classmethod
SIGParameterType = TypeVar("SIGParameterType", bound="SIGParameter")


class SIGParameter:
    """
    A Transaction UNLOCK SIG parameter
    """

    re_sig = re.compile("SIG\\(([0-9]+)\\)")

    def __init__(self, index: int) -> None:
        """
        Init SIGParameter instance

        :param index: Index in list
        """
        self.index = index

    def __eq__(self, other: Any) -> bool:
        """
        Check SIGParameter instances equality
        """
        if not isinstance(other, SIGParameter):
            return NotImplemented
        return self.index == other.index

    def __hash__(self) -> int:
        return hash(self.index)

    @classmethod
    def from_parameter(
        cls: Type[SIGParameterType], parameter: str
    ) -> Optional[SIGParameterType]:
        """
        Return a SIGParameter instance from an index parameter

        :param parameter: Index parameter

        :return:
        """
        sig = SIGParameter.re_sig.match(parameter)
        if sig:
            return cls(int(sig.group(1)))

        return None

    def __str__(self):
        """
        Return a string representation of the SIGParameter instance

        :return:
        """
        return "SIG({0})".format(self.index)


# required to type hint cls in classmethod
XHXParameterType = TypeVar("XHXParameterType", bound="XHXParameter")


class XHXParameter:
    """
    A Transaction UNLOCK XHX parameter
    """

    re_xhx = re.compile("XHX\\(([0-9]+)\\)")

    def __init__(self, integer: int) -> None:
        """
        Init XHXParameter instance

        :param integer: XHX number
        """
        self.integer = integer

    def __eq__(self, other: Any) -> bool:
        """
        Check XHXParameter instances equality
        """
        if not isinstance(other, XHXParameter):
            return NotImplemented
        return self.integer == other.integer

    def __hash__(self) -> int:
        return hash(self.integer)

    @classmethod
    def from_parameter(
        cls: Type[XHXParameterType], parameter: str
    ) -> Optional[XHXParameterType]:
        """
        Return a XHXParameter instance from an index parameter

        :param parameter: Index parameter

        :return:
        """
        xhx = XHXParameter.re_xhx.match(parameter)
        if xhx:
            return cls(int(xhx.group(1)))

        return None

    def compute(self):
        pass

    def __str__(self):
        """
        Return a string representation of the XHXParameter instance

        :return:
        """
        return "XHX({0})".format(self.integer)


# required to type hint cls in classmethod
UnlockParameterType = TypeVar("UnlockParameterType", bound="UnlockParameter")


class UnlockParameter:
    @classmethod
    def from_parameter(
        cls: Type[UnlockParameterType], parameter: str
    ) -> Optional[Union[SIGParameter, XHXParameter]]:
        """
        Return UnlockParameter instance from parameter string

        :param parameter: Parameter string
        :return:
        """
        result = None  # type: Optional[Union[SIGParameter, XHXParameter]]
        sig_param = SIGParameter.from_parameter(parameter)
        if sig_param:
            result = sig_param
        else:
            xhx_param = XHXParameter.from_parameter(parameter)
            if xhx_param:
                result = xhx_param

        return result

    def compute(self):
        pass


# required to type hint cls in classmethod
UnlockType = TypeVar("UnlockType", bound="Unlock")


class Unlock:
    """
    A Transaction UNLOCK
    """

    re_inline = re.compile("([0-9]+):((?:SIG\\([0-9]+\\)|XHX\\([0-9]+\\)|\\s)+)")

    def __init__(
        self, index: int, parameters: List[Union[SIGParameter, XHXParameter]]
    ) -> None:
        """
        Init Unlock instance

        :param index: Index number
        :param parameters: List of UnlockParameter instances
        """
        self.index = index
        self.parameters = parameters

    def __eq__(self, other: Any) -> bool:
        """
        Check Unlock instances equality
        """
        if not isinstance(other, Unlock):
            return NotImplemented

        params_equals = True
        for spar, opar in zip(self.parameters, other.parameters):
            if spar != opar:
                params_equals = False
        return self.index == other.index and params_equals

    def __hash__(self) -> int:
        return hash((self.index, self.parameters))

    @classmethod
    def from_inline(cls: Type[UnlockType], inline: str) -> UnlockType:
        """
        Return an Unlock instance from inline string format

        :param inline: Inline string format

        :return:
        """
        data = Unlock.re_inline.match(inline)
        if data is None:
            raise MalformedDocumentError("Inline input")
        index = int(data.group(1))
        parameters_str = data.group(2).split(" ")
        parameters = []
        for parameter in parameters_str:
            param = UnlockParameter.from_parameter(parameter)
            if param:
                parameters.append(param)
        return cls(index, parameters)

    def inline(self) -> str:
        """
        Return inline string format of the instance

        :return:
        """
        return "{0}:{1}".format(
            self.index, " ".join([str(parameter) for parameter in self.parameters])
        )


# required to type hint cls in classmethod
TransactionType = TypeVar("TransactionType", bound="Transaction")


class Transaction(Document):
    """
.. note:: A transaction document is specified by the following format :

    | Document format :
    | Version: VERSION
    | Type: Transaction
    | Currency: CURRENCY_NAME
    | Issuers:
    | PUBLIC_KEY
    | ...
    | Inputs:
    | INDEX:SOURCE:NUMBER:FINGERPRINT:AMOUNT
    | ...
    | Outputs:
    | PUBLIC_KEY:AMOUNT
    | ...
    | Comment: COMMENT
    | ...
    |
    |
    | Compact format :
    | TX:VERSION:NB_ISSUERS:NB_INPUTS:NB_OUTPUTS:HAS_COMMENT
    | PUBLIC_KEY:INDEX
    | ...
    | INDEX:SOURCE:FINGERPRINT:AMOUNT
    | ...
    | PUBLIC_KEY:AMOUNT
    | ...
    | COMMENT
    | SIGNATURE
    | ...

    """

    re_type = re.compile("Type: (Transaction)\n")
    re_header = re.compile(
        "TX:([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([01]):([0-9]+)\n"
    )
    re_compact_blockstamp = re.compile(
        "({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )
    re_blockstamp = re.compile(
        "Blockstamp: ({block_uid_regex})\n".format(block_uid_regex=BLOCK_UID_REGEX)
    )
    re_locktime = re.compile("Locktime: ([0-9]+)\n")
    re_issuers = re.compile("Issuers:\n")
    re_inputs = re.compile("Inputs:\n")
    re_unlocks = re.compile("Unlocks:\n")
    re_outputs = re.compile("Outputs:\n")
    re_compact_comment = re.compile("([^\n]+)\n")
    re_comment = re.compile("Comment: ([^\n]*)\n")
    re_pubkey = re.compile("({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX))

    fields_parsers = {
        **Document.fields_parsers,
        **{
            "Type": re_type,
            "Blockstamp": re_blockstamp,
            "CompactBlockstamp": re_compact_blockstamp,
            "Locktime": re_locktime,
            "TX": re_header,
            "Issuers": re_issuers,
            "Inputs": re_inputs,
            "Unlocks": re_unlocks,
            "Outputs": re_outputs,
            "Comment": re_comment,
            "Compact comment": re_compact_comment,
            "Pubkey": re_pubkey,
        },
    }

    def __init__(
        self,
        version: int,
        currency: str,
        blockstamp: Optional[BlockUID],
        locktime: int,
        issuers: List[str],
        inputs: List[InputSource],
        unlocks: List[Unlock],
        outputs: List[OutputSource],
        comment: str,
        signatures: List[str],
        time: Optional[int] = None,
    ) -> None:
        """
        Init Transaction instance

        :param version: Version number of the document
        :param currency: Name of the currency
        :param blockstamp: BlockUID timestamp of the block
        :param locktime: Lock time in seconds
        :param issuers: List of issuers public key
        :param inputs: List of InputSource instances
        :param unlocks: List of Unlock instances
        :param outputs: List of OutputSource instances
        :param comment: Comment field
        :param time: time when the transaction enters the blockchain
        :param signatures: List of signatures
        """
        super().__init__(version, currency, signatures)
        self.blockstamp = blockstamp
        self.locktime = locktime
        self.issuers = issuers
        self.inputs = inputs
        self.unlocks = unlocks
        self.outputs = outputs
        self.comment = comment
        self.time = time

    def __eq__(self, other: Any) -> bool:
        """
        Check Transaction instances equality
        """
        if not isinstance(other, Transaction):
            return NotImplemented
        return (
            self.version == other.version
            and self.currency == other.currency
            and self.signatures == other.signatures
            and self.blockstamp == other.blockstamp
            and self.locktime == other.locktime
            and self.issuers == other.issuers
            and self.inputs == other.inputs
            and self.unlocks == other.unlocks
            and self.outputs == other.outputs
            and self.comment == other.comment
            and self.time == other.time
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.version,
                self.currency,
                self.signatures,
                self.blockstamp,
                self.locktime,
                self.issuers,
                self.inputs,
                self.unlocks,
                self.outputs,
                self.comment,
                self.time,
            )
        )

    @classmethod
    def from_bma_history(
        cls: Type[TransactionType], currency: str, tx_data: Dict
    ) -> TransactionType:
        """
        Get the transaction instance from json

        :param currency: the currency of the tx
        :param tx_data: json data of the transaction

        :return:
        """
        tx_data = tx_data.copy()
        tx_data["currency"] = currency
        for data_list in ("issuers", "outputs", "inputs", "unlocks", "signatures"):
            tx_data["multiline_{0}".format(data_list)] = "\n".join(tx_data[data_list])
        return cls.from_signed_raw(
            """Version: {version}
Type: Transaction
Currency: {currency}
Blockstamp: {blockstamp}
Locktime: {locktime}
Issuers:
{multiline_issuers}
Inputs:
{multiline_inputs}
Unlocks:
{multiline_unlocks}
Outputs:
{multiline_outputs}
Comment: {comment}
{multiline_signatures}
""".format(
                **tx_data
            ),
            tx_data["time"],
        )

    @classmethod
    def from_compact(
        cls: Type[TransactionType], currency: str, compact: str
    ) -> TransactionType:
        """
        Return Transaction instance from compact string format

        :param currency: Name of the currency
        :param compact: Compact format string
        :return:
        """
        lines = compact.splitlines(True)
        n = 0

        header_data = Transaction.re_header.match(lines[n])
        if header_data is None:
            raise MalformedDocumentError("Compact TX header")
        version = int(header_data.group(1))
        issuers_num = int(header_data.group(2))
        inputs_num = int(header_data.group(3))
        unlocks_num = int(header_data.group(4))
        outputs_num = int(header_data.group(5))
        has_comment = int(header_data.group(6))
        locktime = int(header_data.group(7))
        n += 1

        blockstamp = BlockUID.from_str(
            Transaction.parse_field("CompactBlockstamp", lines[n])
        )
        n += 1

        issuers = []
        inputs = []
        unlocks = []
        outputs = []
        signatures = []
        for index in range(0, issuers_num):
            issuer = Transaction.parse_field("Pubkey", lines[n + index])
            issuers.append(issuer)
        n += issuers_num

        for index in range(0, inputs_num):
            input_source = InputSource.from_inline(lines[n + index])
            inputs.append(input_source)
        n += inputs_num

        for index in range(0, unlocks_num):
            unlock = Unlock.from_inline(lines[n + index])
            unlocks.append(unlock)
        n += unlocks_num

        for index in range(0, outputs_num):
            output_source = OutputSource.from_inline(lines[n + index])
            outputs.append(output_source)
        n += outputs_num

        comment = ""
        if has_comment == 1:
            data = Transaction.re_compact_comment.match(lines[n])
            if data:
                comment = data.group(1)
                n += 1
            else:
                raise MalformedDocumentError("Compact TX Comment")

        while n < len(lines):
            data = Transaction.re_signature.match(lines[n])
            if data:
                signatures.append(data.group(1))
                n += 1
            else:
                raise MalformedDocumentError("Compact TX Signatures")

        return cls(
            version,
            currency,
            blockstamp,
            locktime,
            issuers,
            inputs,
            unlocks,
            outputs,
            comment,
            signatures,
        )

    @classmethod
    def from_signed_raw(
        cls: Type[TransactionType], raw: str, time: int = 0
    ) -> TransactionType:
        """
        Return a Transaction instance from a raw string format

        :param raw: Raw string format
        :param time: time when the transaction enters the blockchain

        :return:
        """
        lines = raw.splitlines(True)
        n = 0

        version = int(Transaction.parse_field("Version", lines[n]))
        n += 1

        Transaction.parse_field("Type", lines[n])
        n += 1

        currency = Transaction.parse_field("Currency", lines[n])
        n += 1

        blockstamp = BlockUID.from_str(Transaction.parse_field("Blockstamp", lines[n]))
        n += 1

        locktime = Transaction.parse_field("Locktime", lines[n])
        n += 1

        issuers = []
        inputs = []
        unlocks = []
        outputs = []
        signatures = []

        if Transaction.re_issuers.match(lines[n]):
            n += 1
            while Transaction.re_inputs.match(lines[n]) is None:
                issuer = Transaction.parse_field("Pubkey", lines[n])
                issuers.append(issuer)
                n += 1

        if Transaction.re_inputs.match(lines[n]):
            n += 1
            while Transaction.re_unlocks.match(lines[n]) is None:
                input_source = InputSource.from_inline(lines[n])
                inputs.append(input_source)
                n += 1

        if Transaction.re_unlocks.match(lines[n]):
            n += 1
            while Transaction.re_outputs.match(lines[n]) is None:
                unlock = Unlock.from_inline(lines[n])
                unlocks.append(unlock)
                n += 1

        if Transaction.re_outputs.match(lines[n]) is not None:
            n += 1
            while not Transaction.re_comment.match(lines[n]):
                _output = OutputSource.from_inline(lines[n])
                outputs.append(_output)
                n += 1

        comment = Transaction.parse_field("Comment", lines[n])
        n += 1

        if Transaction.re_signature.match(lines[n]) is not None:
            while n < len(lines):
                sign = Transaction.parse_field("Signature", lines[n])
                signatures.append(sign)
                n += 1

        return cls(
            version,
            currency,
            blockstamp,
            locktime,
            issuers,
            inputs,
            unlocks,
            outputs,
            comment,
            signatures,
            time,
        )

    def raw(self) -> str:
        """
        Return raw string format from the instance

        :return:
        """
        doc = """Version: {0}
Type: Transaction
Currency: {1}
""".format(
            self.version, self.currency
        )

        doc += "Blockstamp: {0}\n".format(self.blockstamp)

        doc += "Locktime: {0}\n".format(self.locktime)

        doc += "Issuers:\n"
        for p in self.issuers:
            doc += "{0}\n".format(p)

        doc += "Inputs:\n"
        for i in self.inputs:
            doc += "{0}\n".format(i.inline())

        doc += "Unlocks:\n"
        for u in self.unlocks:
            doc += "{0}\n".format(u.inline())

        doc += "Outputs:\n"
        for o in self.outputs:
            doc += "{0}\n".format(o.inline())

        doc += "Comment: "
        doc += "{0}\n".format(self.comment)

        return doc

    def compact(self) -> str:
        """
        Return a transaction in its compact format from the instance

        :return:

        TX:VERSION:NB_ISSUERS:NB_INPUTS:NB_UNLOCKS:NB_OUTPUTS:HAS_COMMENT:LOCKTIME
        PUBLIC_KEY:INDEX
        ...
        INDEX:SOURCE:FINGERPRINT:AMOUNT
        ...
        PUBLIC_KEY:AMOUNT
        ...
        COMMENT
"""
        doc = "TX:{0}:{1}:{2}:{3}:{4}:{5}:{6}\n".format(
            self.version,
            len(self.issuers),
            len(self.inputs),
            len(self.unlocks),
            len(self.outputs),
            "1" if self.comment != "" else "0",
            self.locktime,
        )
        doc += "{0}\n".format(self.blockstamp)

        for pubkey in self.issuers:
            doc += "{0}\n".format(pubkey)
        for i in self.inputs:
            doc += "{0}\n".format(i.inline())
        for u in self.unlocks:
            doc += "{0}\n".format(u.inline())
        for o in self.outputs:
            doc += "{0}\n".format(o.inline())
        if self.comment != "":
            doc += "{0}\n".format(self.comment)
        for s in self.signatures:
            doc += "{0}\n".format(s)

        return doc


class SimpleTransaction(Transaction):
    """
    As transaction class, but for only one issuer.
    ...
    """

    def __init__(
        self,
        version: int,
        currency: str,
        blockstamp: BlockUID,
        locktime: int,
        issuer: str,
        single_input: InputSource,
        unlocks: List[Unlock],
        outputs: List[OutputSource],
        comment: str,
        signature: str,
        time: int,
    ) -> None:
        """
        Init instance

        :param version: Version number of the document
        :param currency: Name of the currency
        :param blockstamp: BlockUID timestamp
        :param locktime: Lock time in seconds
        :param issuer: Issuer public key
        :param single_input: InputSource instance
        :param unlocks: List of Unlock instances
        :param outputs: List of OutputSource instances
        :param comment: Comment field
        :param time: time when the transaction enters the blockchain
        :param signature: Signature
        """
        super().__init__(
            version,
            currency,
            blockstamp,
            locktime,
            [issuer],
            [single_input],
            unlocks,
            outputs,
            comment,
            [signature],
            time,
        )

    @staticmethod
    def is_simple(tx: Transaction) -> bool:
        """
        Filter a transaction and checks if it is a basic one
        A simple transaction is a tx which has only one issuer
        and two outputs maximum. The unlocks must be done with
        simple "SIG" functions, and the outputs must be simple
        SIG conditions.

        :param tx: the transaction to check

        :return: True if a simple transaction
        """
        simple = True
        if len(tx.issuers) != 1:
            simple = False
        for unlock in tx.unlocks:
            if len(unlock.parameters) != 1:
                simple = False
            elif type(unlock.parameters[0]) is not SIGParameter:
                simple = False
        for o in tx.outputs:
            # if right condition is not None...
            if getattr(o.condition, "right", None):
                simple = False
                # if left is not SIG...
            elif type(o.condition.left) is not output.SIG:
                simple = False

        return simple
