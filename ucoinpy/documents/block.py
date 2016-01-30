from .document import Document, MalformedDocumentError
from .certification import SelfCertification, Certification
from .membership import Membership
from .transaction import Transaction

import re


class BlockId:
    """
    A simple block id
    """
    re_hash = re.compile("([0-9a-fA-F]{5,40})")

    @classmethod
    def empty(cls):
        return cls(0, Block.Empty_Hash)

    def __init__(self, number, sha_hash):
        assert(type(number) is int)
        assert(BlockId.re_hash.match(sha_hash) is not None)
        self.number = number
        self.sha_hash = sha_hash

    @classmethod
    def from_str(cls, blockid):
        """
        :param str blockid: The block id
        """
        data = blockid.split("-")
        if len(data) != 2:
            raise MalformedDocumentError('BlockId')
        number = int(data[0])
        sha_hash = data[1]
        return cls(number, sha_hash)

    def __str__(self):
        return "{0}-{1}".format(self.number, self.sha_hash)

    def __eq__(self, other):
        return self.number == other.number and self.sha_hash == other.sha_hash


class Block(Document):
    """
The class Block handles Block documents.

.. note:: A block document is specified by the following format :

    | Version: VERSION
    | Type: Block
    | Currency: CURRENCY
    | Nonce: NONCE
    | Number: BLOCK_NUMBER
    | PoWMin: NUMBER_OF_ZEROS
    | Time: GENERATED_ON
    | MedianTime: MEDIAN_DATE
    | UniversalDividend: DIVIDEND_AMOUNT
    | Issuer: ISSUER_KEY
    | PreviousHash: PREVIOUS_HASH
    | PreviousIssuer: PREVIOUS_ISSUER_KEY
    | Parameters: PARAMETERS
    | MembersCount: WOT_MEM_COUNT
    | Identities:
    | PUBLIC_KEY:SIGNATURE:TIMESTAMP:USER_ID
    | ...
    | Joiners:
    | PUBLIC_KEY:SIGNATURE:NUMBER:HASH:TIMESTAMP:USER_ID
    | ...
    | Actives:
    | PUBLIC_KEY:SIGNATURE:NUMBER:HASH:TIMESTAMP:USER_ID
    | ...
    | Leavers:
    | PUBLIC_KEY:SIGNATURE:NUMBER:HASH:TIMESTAMP:USER_ID
    | ...
    | Excluded:
    | PUBLIC_KEY
    | ...
    | Certifications:
    | PUBKEY_FROM:PUBKEY_TO:BLOCK_NUMBER:SIGNATURE
    | ...
    | Transactions:
    | COMPACT_TRANSACTION
    | ...
    | BOTTOM_SIGNATURE

    """

    re_type = re.compile("Type: (Block)\n")
    re_noonce = re.compile("Nonce: ([0-9]+)\n")
    re_number = re.compile("Number: ([0-9]+)\n")
    re_powmin = re.compile("PoWMin: ([0-9]+)\n")
    re_time = re.compile("Time: ([0-9]+)\n")
    re_mediantime = re.compile("MedianTime: ([0-9]+)\n")
    re_universaldividend = re.compile("UniversalDividend: ([0-9]+)\n")
    re_issuer = re.compile("Issuer: ([1-9A-Za-z][^OIl]{42,45})\n")
    re_previoushash = re.compile("PreviousHash: ([0-9a-fA-F]{5,40})\n")
    re_previousissuer = re.compile("PreviousIssuer: ([1-9A-Za-z][^OIl]{42,45})\n")
    re_parameters = re.compile("Parameters: ([0-9]+\.[0-9]+):([0-9]+):([0-9]+):([0-9]+):\
([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):\
([0-9]+\.[0-9]+)\n")
    re_memberscount = re.compile("MembersCount: ([0-9]+)\n")
    re_identities = re.compile("Identities:\n")
    re_joiners = re.compile("Joiners:\n")
    re_actives = re.compile("Actives:\n")
    re_leavers = re.compile("Leavers:\n")
    re_excluded = re.compile("Excluded:\n")
    re_exclusion = re.compile("([1-9A-Za-z][^OIl]{42,45})\n")
    re_certifications = re.compile("Certifications:\n")
    re_transactions = re.compile("Transactions:\n")

    fields_parsers = {**Document.fields_parsers, **{
                'Type': re_type,
                'Noonce': re_noonce,
                'Number': re_number,
                'PoWMin': re_powmin,
                'Time': re_time,
                'MedianTime': re_mediantime,
                'UD': re_universaldividend,
                'Issuer': re_issuer,
                'PreviousIssuer': re_previousissuer,
                'PreviousHash': re_previoushash,
                'Parameters': re_parameters,
                'MembersCount': re_memberscount,
                'Identities': re_identities,
                'Joiners': re_joiners,
                'Actives': re_actives,
                'Leavers': re_leavers,
                'Certifications': re_certifications,
                'Transactions': re_transactions
            }
      }

    Empty_Hash = "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"

    def __init__(self, version, currency, noonce, number, powmin, time,
                 mediantime, ud, issuer, prev_hash, prev_issuer,
                 parameters, members_count, identities, joiners,
                 actives, leavers, excluded, certifications,
                 transactions, signature):
        """
        Constructor

        :param int version: ucoin protocol version
        :param str currency: the block currency
        :param int noonce: the noonce value of the block
        :param int number: the number of the block
        :param int powmin: the powmin value of this block
        :param int time: the timestamp of this block
        :param int ud: the dividend amount, or None if no dividend present in this block
        :param str issuer: the pubkey of the issuer of the block
        :param str prev_hash: the previous block hash
        :param str prev_issuer: the previous block issuer
        :param tuple parameters: the parameters of the currency. Should only be present in block 0.
        :param int members_count: the number of members found in this block
        :param list[ucoinpy.documents.SelfCertification] identities: the self certifications declared in this block
        :param list[ucoinpy.documents.Membership] joiners: the joiners memberships via "IN" documents
        :param list[ucoinpy.documents.Membership] actives: renewed memberships via "IN" documents
        :param list[ucoinpy.documents.Membership] leavers: the leavers memberships via "OUT" documents
        :param list[ucoinpy.documents.Membership] excluded: members excluded because of missing certifications
        :param list[ucoinpy.documents.Membership] actives: renewed memberships via "IN" documents
        :param list[ucoinpy.documents.Certification] certifications: certifications documents
        :param list[ucoinpy.documents.Transaction] transactions: transactions documents
        """
        super().__init__(version, currency, [signature])
        self.noonce = noonce
        self.number = number
        self.powmin = powmin
        self.time = time
        self.mediantime = mediantime
        self.ud = ud
        self.issuer = issuer
        self.prev_hash = prev_hash
        self.prev_issuer = prev_issuer
        self.parameters = parameters
        self.members_count = members_count
        self.identities = identities
        self.joiners = joiners
        self.actives = actives
        self.leavers = leavers
        self.excluded = excluded
        self.certifications = certifications
        self.transactions = transactions

    @property
    def blockid(self):
        return BlockId(self.number, self.sha_hash)

    @classmethod
    def from_signed_raw(cls, raw):
        lines = raw.splitlines(True)
        n = 0

        version = int(Block.parse_field("Version", lines[n]))
        n += 1

        Block.parse_field("Type", lines[n])
        n += 1

        currency = Block.parse_field("Currency", lines[n])
        n += 1

        noonce = int(Block.parse_field("Noonce", lines[n]))
        n += 1

        number = int(Block.parse_field("Number", lines[n]))
        n += 1

        powmin = int(Block.parse_field("PoWMin", lines[n]))
        n += 1

        time = int(Block.parse_field("Time", lines[n]))
        n += 1

        mediantime = int(Block.parse_field("MedianTime", lines[n]))
        n += 1

        ud = Block.re_universaldividend.match(lines[n])
        if ud is not None:
            ud = int(ud.group(1))
            n += 1

        issuer = Block.parse_field("Issuer", lines[n])
        n += 1

        prev_hash = None
        prev_issuer = None
        if number > 0:
            prev_hash = Block.parse_field("PreviousHash", lines[n])
            n += 1

            prev_issuer = Block.parse_field("PreviousIssuer", lines[n])
            n += 1

        parameters = None
        if number == 0:
            parameters = Block.re_parameters.match(lines[n]).groups()
            n += 1

        members_count = int(Block.parse_field("MembersCount", lines[n]))
        n += 1

        identities = []
        joiners = []
        actives = []
        leavers = []
        excluded = []
        certifications = []
        transactions = []

        if Block.re_identities.match(lines[n]) is not None:
            n += 1
            while Block.re_joiners.match(lines[n]) is None:
                selfcert = SelfCertification.from_inline(version, currency, lines[n])
                identities.append(selfcert)
                n += 1

        if Block.re_joiners.match(lines[n]):
            n += 1
            while Block.re_actives.match(lines[n]) is None:
                membership = Membership.from_inline(version, currency, "IN", lines[n])
                joiners.append(membership)
                n += 1

        if Block.re_actives.match(lines[n]):
            n += 1
            while Block.re_leavers.match(lines[n]) is None:
                membership = Membership.from_inline(version, currency, "IN", lines[n])
                actives.append(membership)
                n += 1

        if Block.re_leavers.match(lines[n]):
            n += 1
            while Block.re_excluded.match(lines[n]) is None:
                membership = Membership.from_inline(version, currency, "OUT", lines[n])
                leavers.append(membership)
                n += 1

        if Block.re_excluded.match(lines[n]):
            n += 1
            while Block.re_certifications.match(lines[n]) is None:
                membership = Block.re_exclusion.match(lines[n]).group(1)
                excluded.append(membership)
                n += 1

        if Block.re_certifications.match(lines[n]):
            n += 1
            while Block.re_transactions.match(lines[n]) is None:
                certification = Certification.from_inline(version, currency,
                                                          prev_hash, lines[n])
                certifications.append(certification)
                n += 1

        if Block.re_transactions.match(lines[n]):
            n += 1
            while not Block.re_signature.match(lines[n]):
                tx_lines = ""
                header_data = Transaction.re_header.match(lines[n])
                version = int(header_data.group(1))
                issuers_num = int(header_data.group(2))
                inputs_num = int(header_data.group(3))
                outputs_num = int(header_data.group(4))
                has_comment = int(header_data.group(5))
                tx_max = n + issuers_num * 2 + inputs_num + outputs_num + has_comment + 1
                for i in range(n, tx_max):
                    tx_lines += lines[n]
                    n += 1
                transaction = Transaction.from_compact(currency, tx_lines)
                transactions.append(transaction)

        signature = Block.parse_field("Signature", lines[n])

        return cls(version, currency, noonce, number, powmin, time,
                   mediantime, ud, issuer, prev_hash, prev_issuer,
                   parameters, members_count, identities, joiners,
                   actives, leavers, excluded, certifications,
                   transactions, signature)

    def raw(self):
        doc = """Version: {0}
Type: Block
Currency: {1}
Nonce: {2}
Number: {3}
PoWMin: {4}
Time: {5}
MedianTime: {6}
""".format(self.version,
                      self.currency,
                      self.noonce,
                      self.number,
                      self.powmin,
                      self.time,
                      self.mediantime)
        if self.ud:
            doc += "UniversalDividend: {0}\n".format(self.ud)

        doc += "Issuer: {0}\n".format(self.issuer)

        if self.number == 0:
            str_params = ":".join(self.parameters)
            doc += "Parameters: {0}\n".format(str_params)
        else:
            doc += "PreviousHash: {0}\n\
PreviousIssuer: {1}\n".format(self.prev_hash, self.prev_issuer)

        doc += "MembersCount: {0}\n".format(self.members_count)

        doc += "Identities:\n"
        for identity in self.identities:
            doc += "{0}\n".format(identity.inline())

        doc += "Joiners:\n"
        for joiner in self.joiners:
            doc += "{0}\n".format(joiner.inline())

        doc += "Actives:\n"
        for active in self.actives:
            doc += "{0}\n".format(active.inline())

        doc += "Leavers:\n"
        for leaver in self.leavers:
            doc += "{0}\n".format(leaver.inline())

        doc += "Excluded:\n"
        for exclude in self.excluded:
            doc += "{0}\n".format(exclude)

        doc += "Certifications:\n"
        for cert in self.certifications:
            doc += "{0}\n".format(cert.inline())

        doc += "Transactions:\n"
        for transaction in self.transactions:
            doc += "{0}".format(transaction.compact())

        return doc