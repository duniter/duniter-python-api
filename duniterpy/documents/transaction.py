from .document import Document, MalformedDocumentError
from .constants import pubkey_regex, transaction_hash_regex, block_id_regex, block_uid_regex
from ..grammars import output
import pypeg2
import re


def reduce_base(amount, base):
    """
    Compute the reduced base of the given parameters
    :param int amount: the amount value
    :param int base: current base value
    :return: tuple containing computed (amount, base)
    :rtype: tuple
    """
    if amount == 0:
        return 0, 0

    next_amount = amount
    next_base = base
    while int(next_amount) == next_amount:
        amount = next_amount
        base = next_base
        next_amount /= 10
        next_base += 1
    return int(amount), int(base)


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
    re_header = re.compile("TX:([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):(0|1):([0-9]+)\n")
    re_compact_blockstamp = re.compile("({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))
    re_blockstamp = re.compile("Blockstamp: ({block_uid_regex})\n".format(block_uid_regex=block_uid_regex))
    re_locktime = re.compile("Locktime: ([0-9]+)\n")
    re_issuers = re.compile("Issuers:\n")
    re_inputs = re.compile("Inputs:\n")
    re_unlocks = re.compile("Unlocks:\n")
    re_outputs = re.compile("Outputs:\n")
    re_compact_comment = re.compile("([^\n]+)\n")
    re_comment = re.compile("Comment: ([^\n]*)\n")
    re_pubkey = re.compile("({pubkey_regex})\n".format(pubkey_regex=pubkey_regex))

    fields_parsers = {**Document.fields_parsers, **{
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
            "Pubkey": re_pubkey
        }
    }

    def __init__(self, version, currency, blockstamp, locktime, issuers, inputs, unlocks, outputs,
                 comment, signatures):
        """

        :param int version:
        :param str currency:
        :param BlockUID blockstamp:
        :param int locktime:
        :param list[str] issuers:
        :param list[InputSource] inputs:
        :param list[Unlock] unlocks:
        :param list[OutputSource] outputs:
        :param comment:
        :param signatures:
        """
        super().__init__(version, currency, signatures)
        self.blockstamp = blockstamp
        self.locktime = locktime
        self.issuers = issuers
        self.inputs = inputs
        self.unlocks = unlocks
        self.outputs = outputs
        self.comment = comment

    @classmethod
    def from_bma_history(cls, currency, tx_data):
        """
        Get the transaction from json
        :param str currency: the currency of the tx
        :param dict tx_data: json data of the transaction
        :rtype: Transaction
        """
        tx_data = tx_data.copy()
        tx_data["currency"] = currency
        for data_list in ('issuers', 'outputs', 'inputs', 'unlocks', 'signatures'):
            tx_data['multiline_{0}'.format(data_list)] = '\n'.join(tx_data[data_list])
        if tx_data["version"] >= 3:
                signed_raw = """Version: {version}
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
""".format(**tx_data)
        else:
            signed_raw = """Version: {version}
Type: Transaction
Currency: {currency}
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
""".format(**tx_data)
        return Transaction.from_signed_raw(signed_raw)

    @classmethod
    def from_compact(cls, currency, compact):
        from .block import BlockUID
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

        if version >= 3:
            blockstamp = BlockUID.from_str(Transaction.parse_field("CompactBlockstamp", lines[n]))
            n += 1
        else:
            blockstamp = None

        issuers = []
        inputs = []
        unlocks = []
        outputs = []
        signatures = []
        for i in range(0, issuers_num):
            issuer = Transaction.parse_field("Pubkey", lines[n])
            issuers.append(issuer)
            n += 1

        for i in range(0, inputs_num):
            input_source = InputSource.from_inline(version, lines[n])
            inputs.append(input_source)
            n += 1

        for i in range(0, unlocks_num):
            unlock = Unlock.from_inline(lines[n])
            unlocks.append(unlock)
            n += 1

        for i in range(0, outputs_num):
            output_source = OutputSource.from_inline(lines[n])
            outputs.append(output_source)
            n += 1

        comment = ""
        if has_comment == 1:
            if Transaction.re_compact_comment.match(lines[n]):
                comment = Transaction.re_compact_comment.match(lines[n]).group(1)
                n += 1
            else:
                raise MalformedDocumentError("Compact TX Comment")

        while n < len(lines):
            if Transaction.re_signature.match(lines[n]):
                signatures.append(Transaction.re_signature.match(lines[n]).group(1))
                n += 1
            else:
                raise MalformedDocumentError("Compact TX Signatures")

        return cls(version, currency, blockstamp, locktime, issuers, inputs, unlocks, outputs, comment, signatures)

    @classmethod
    def from_signed_raw(cls, raw):
        from .block import BlockUID
        lines = raw.splitlines(True)
        n = 0

        version = int(Transaction.parse_field("Version", lines[n]))
        n += 1

        Transaction.parse_field("Type", lines[n])
        n += 1

        currency = Transaction.parse_field("Currency", lines[n])
        n += 1

        if version >= 3:
            blockstamp = BlockUID.from_str(Transaction.parse_field("Blockstamp", lines[n]))
            n += 1
        else:
            blockstamp = None

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
                input_source = InputSource.from_inline(version, lines[n])
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
                output = OutputSource.from_inline(lines[n])
                outputs.append(output)
                n += 1

        comment = Transaction.parse_field("Comment", lines[n])
        n += 1

        if Transaction.re_signature.match(lines[n]) is not None:
            while n < len(lines):
                sign = Transaction.parse_field("Signature", lines[n])
                signatures.append(sign)
                n += 1

        return cls(version, currency, blockstamp, locktime, issuers, inputs, unlocks, outputs,
                   comment, signatures)

    def raw(self):
        doc = """Version: {0}
Type: Transaction
Currency: {1}
""".format(self.version,
           self.currency)

        if self.version >= 3:
            doc += "Blockstamp: {0}\n".format(self.blockstamp)

        doc += "Locktime: {0}\n".format(self.locktime)

        doc += "Issuers:\n"
        for p in self.issuers:
            doc += "{0}\n".format(p)

        doc += "Inputs:\n"
        for i in self.inputs:
            doc += "{0}\n".format(i.inline(self.version))

        doc += "Unlocks:\n"
        for u in self.unlocks:
            doc += "{0}\n".format(u.inline())

        doc += "Outputs:\n"
        for o in self.outputs:
            doc += "{0}\n".format(o.inline())

        doc += "Comment: "
        doc += "{0}\n".format(self.comment)

        return doc

    def compact(self):
        """
        Return a transaction in its compact format.
        """
        """TX:VERSION:NB_ISSUERS:NB_INPUTS:NB_UNLOCKS:NB_OUTPUTS:HAS_COMMENT:LOCKTIME
PUBLIC_KEY:INDEX
...
INDEX:SOURCE:FINGERPRINT:AMOUNT
...
PUBLIC_KEY:AMOUNT
...
COMMENT
"""
        doc = "TX:{0}:{1}:{2}:{3}:{4}:{5}:{6}\n".format(self.version,
                                              len(self.issuers),
                                              len(self.inputs),
                                              len(self.unlocks),
                                              len(self.outputs),
                                              '1' if self.comment != "" else '0',
                                               self.locktime)
        if self.version >= 3:
            doc += "{0}\n".format(self.blockstamp)

        for pubkey in self.issuers:
            doc += "{0}\n".format(pubkey)
        for i in self.inputs:
            doc += "{0}\n".format(i.inline(self.version))
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
    def __init__(self, version, currency, issuer,
                 single_input, outputs, comment, signature):
        """
        Constructor
        """
        super().__init__(version, currency, [issuer], [single_input],
              outputs, comment, [signature])

    @staticmethod
    def is_simple(tx):
        """
        Filter a transaction and checks if it is a basic one
        A simple transaction is a tx which has only one issuer
        and two outputs maximum. The unlocks must be done with
        simple "SIG" functions, and the outputs must be simple
        SIG conditions.
        :param duniterpy.documents.Transaction tx: the transaction to check
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
            if getattr('right', o.conditions, None):
                simple = False
            elif type(o.conditions.left) is not output.SIG:
                simple = False
        return simple


class InputSource:
    """
    A Transaction INPUT

.. note:: Compact :
    INDEX:SOURCE:FINGERPRINT:AMOUNT

    """
    re_inline = re.compile("(?:(?:(D):({pubkey_regex}):({block_id_regex}))|(?:(T):({transaction_hash_regex}):([0-9]+)))\n"
                           .format(pubkey_regex=pubkey_regex,
                                   block_id_regex=block_id_regex,
                                    transaction_hash_regex=transaction_hash_regex))
    re_inline_v3 = re.compile("([0-9]+):([0-9]+):(?:(?:(D):({pubkey_regex}):({block_id_regex}))|(?:(T):({transaction_hash_regex}):([0-9]+)))\n"
                           .format(pubkey_regex=pubkey_regex,
                                   block_id_regex=block_id_regex,
                                    transaction_hash_regex=transaction_hash_regex))

    def __init__(self, amount, base, source, origin_id, index):
        """
        An input source can come from a dividend or a transaction.

        :param int amount: amount of the input
        :param int base: base of the input
        :param str source: D if dividend, T if transaction
        :param str origin_id: a Public key if a dividend, a tx hash if a transaction
        :param int index: a block id if a dividend, an tx index if a transaction
        :return:
        """
        self.amount = amount
        self.base = base
        self.source = source
        self.origin_id = origin_id
        self.index = index

    @classmethod
    def from_inline(cls, tx_version, inline):
        if tx_version == 2:
            data = InputSource.re_inline.match(inline)
            if data is None:
                raise MalformedDocumentError("Inline input")
            source_offset = 0
            amount = 0
            base = 0
        else:
            data = InputSource.re_inline_v3.match(inline)
            if data is None:
                raise MalformedDocumentError("Inline input")
            source_offset = 2
            amount = data.group(1)
            base = data.group(2)
        if data.group(1 + source_offset):
            source = data.group(1 + source_offset)
            origin_id = data.group(2 + source_offset)
            index = int(data.group(3 + source_offset))
        else:
            source = data.group(4 + source_offset)
            origin_id = data.group(5 + source_offset)
            index = int(data.group(6 + source_offset))

        return cls(amount, base, source, origin_id, index)

    def inline(self, tx_version):
        if tx_version == 2:
            return "{0}:{1}:{2}".format(self.source,
                                        self.origin_id,
                                        self.index)
        else:
            return "{0}:{1}:{2}:{3}:{4}".format(self.amount,
                                        self.base,
                                        self.source,
                                        self.origin_id,
                                        self.index)


class UnlockParameter:

    def __init__(self):
        pass

    @classmethod
    def from_parameter(cls, parameter):
        for params_type in (SIGParameter, XHXParameter):
            param = params_type.from_parameter(parameter)
            if param:
                return param

    def compute(self):
        pass


class SIGParameter:
    """
    A Transaction UNLOCK SIG parameter
    """
    re_sig = re.compile("SIG\(([0-9]+)\)")

    def __init__(self, index):
        self.index = index

    @classmethod
    def from_parameter(cls, parameter):
        sig = SIGParameter.re_sig.match(parameter)
        if sig:
            return SIGParameter(sig.group(1))
        else:
            return None

    def __str__(self):
        return "SIG({0})".format(self.index)


class XHXParameter:
    """
    A Transaction UNLOCK XHX parameter
    """
    re_xhx = re.compile("XHX\(([0-9]+)\)")

    def __init__(self, integer):
        self.integer = integer

    @classmethod
    def from_parameter(cls, parameter):
        xhx = XHXParameter.re_xhx.match(parameter)
        if xhx:
            return XHXParameter(xhx.group(1))
        else:
            return None

    def compute(self):
        return

    def __str__(self):
        return "XHX({0})".format(self.integer)


class Unlock:
    """
    A Transaction UNLOCK
    """
    re_inline = re.compile("([0-9]+):((?:SIG\([0-9]+\)|XHX\([0-9]+\)|\s)+)\n")

    def __init__(self, index, parameters):
        self.index = index
        self.parameters = parameters

    @classmethod
    def from_inline(cls, inline):
        data = Unlock.re_inline.match(inline)
        if data is None:
            raise MalformedDocumentError("Inline input")
        index = int(data.group(1))
        parameters_str = data.group(2).split(' ')
        parameters = []
        for p in parameters_str:
            param = UnlockParameter.from_parameter(p)
            if param:
                parameters.append(param)
        return cls(index, parameters)

    def inline(self):
        return "{0}:{1}".format(self.index, ' '.join([str(p) for p in self.parameters]))


class OutputSource:
    """
    A Transaction OUTPUT
    """
    re_inline = re.compile("([0-9]+):([0-9]+):([A-Za-z0-9\(\)\s]+)\n")

    def __init__(self, amount, base, conditions):
        self.amount = amount
        self.base = base
        self.conditions = conditions

    @classmethod
    def from_inline(cls, inline):
        data = OutputSource.re_inline.match(inline)
        if data is None:
            raise MalformedDocumentError("Inline output")
        amount = int(data.group(1))
        base = int(data.group(2))
        try:
            conditions = pypeg2.parse(data.group(3), output.Condition)
        except SyntaxError:
            raise MalformedDocumentError("Output source syntax error")
        return cls(amount, base, conditions)

    def inline(self):
        return "{0}:{1}:{2}".format(self.amount, self.base,
                                    pypeg2.compose(self.conditions, output.Condition))
