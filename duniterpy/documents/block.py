import base64
import hashlib
import re
from typing import TypeVar, Type, Optional, List, Sequence
from .block_uid import BlockUID
from .certification import Certification
from .revocation import Revocation
from .identity import Identity
from .document import Document, MalformedDocumentError
from .membership import Membership
from .transaction import Transaction
from ..constants import PUBKEY_REGEX, BLOCK_HASH_REGEX


# required to type hint cls in classmethod
BlockType = TypeVar("BlockType", bound="Block")


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
    re_number = re.compile("Number: ([0-9]+)\n")
    re_powmin = re.compile("PoWMin: ([0-9]+)\n")
    re_time = re.compile("Time: ([0-9]+)\n")
    re_mediantime = re.compile("MedianTime: ([0-9]+)\n")
    re_universaldividend = re.compile("UniversalDividend: ([0-9]+)\n")
    re_unitbase = re.compile("UnitBase: ([0-9]+)\n")
    re_issuer = re.compile(
        "Issuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX)
    )
    re_issuers_frame = re.compile("IssuersFrame: ([0-9]+)\n")
    re_issuers_frame_var = re.compile("IssuersFrameVar: (0|-?[1-9]\\d{0,18})\n")
    re_different_issuers_count = re.compile("DifferentIssuersCount: ([0-9]+)\n")
    re_previoushash = re.compile(
        "PreviousHash: ({block_hash_regex})\n".format(block_hash_regex=BLOCK_HASH_REGEX)
    )
    re_previousissuer = re.compile(
        "PreviousIssuer: ({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX)
    )
    re_parameters = re.compile(
        "Parameters: ([0-9]+\\.[0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):\
([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+\\.[0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+):([0-9]+\\.[0-9]+):\
([0-9]+):([0-9]+):([0-9]+)\n"
    )
    re_memberscount = re.compile("MembersCount: ([0-9]+)\n")
    re_identities = re.compile("Identities:\n")
    re_joiners = re.compile("Joiners:\n")
    re_actives = re.compile("Actives:\n")
    re_leavers = re.compile("Leavers:\n")
    re_revoked = re.compile("Revoked:\n")
    re_excluded = re.compile("Excluded:\n")
    re_exclusion = re.compile("({pubkey_regex})\n".format(pubkey_regex=PUBKEY_REGEX))
    re_certifications = re.compile("Certifications:\n")
    re_transactions = re.compile("Transactions:\n")
    re_hash = re.compile(
        "InnerHash: ({block_hash_regex})\n".format(block_hash_regex=BLOCK_HASH_REGEX)
    )
    re_nonce = re.compile("Nonce: ([0-9]+)\n")

    fields_parsers = {
        **Document.fields_parsers,
        **{
            "Type": re_type,
            "Number": re_number,
            "PoWMin": re_powmin,
            "Time": re_time,
            "MedianTime": re_mediantime,
            "UD": re_universaldividend,
            "UnitBase": re_unitbase,
            "Issuer": re_issuer,
            "IssuersFrame": re_issuers_frame,
            "IssuersFrameVar": re_issuers_frame_var,
            "DifferentIssuersCount": re_different_issuers_count,
            "PreviousIssuer": re_previousissuer,
            "PreviousHash": re_previoushash,
            "Parameters": re_parameters,
            "MembersCount": re_memberscount,
            "Identities": re_identities,
            "Joiners": re_joiners,
            "Actives": re_actives,
            "Leavers": re_leavers,
            "Revoked": re_revoked,
            "Excluded": re_excluded,
            "Certifications": re_certifications,
            "Transactions": re_transactions,
            "InnerHash": re_hash,
            "Nonce": re_nonce,
        },
    }

    def __init__(
        self,
        version: int,
        currency: str,
        number: int,
        powmin: int,
        time: int,
        mediantime: int,
        ud: Optional[int],
        unit_base: int,
        issuer: str,
        issuers_frame: int,
        issuers_frame_var: int,
        different_issuers_count: int,
        prev_hash: Optional[str],
        prev_issuer: Optional[str],
        parameters: Optional[Sequence[str]],
        members_count: int,
        identities: List[Identity],
        joiners: List[Membership],
        actives: List[Membership],
        leavers: List[Membership],
        revokations: List[Revocation],
        excluded: List[str],
        certifications: List[Certification],
        transactions: List[Transaction],
        inner_hash: str,
        nonce: int,
        signature: str,
    ) -> None:
        """
        Constructor

        :param version: duniter protocol version
        :param currency: the block currency
        :param number: the number of the block
        :param powmin: the powmin value of this block
        :param time: the timestamp of this block
        :param mediantime: the timestamp of the median time of this block
        :param ud: the dividend amount, or None if no dividend present in this block
        :param unit_base: the unit_base of the dividend, or None if no dividend present in this block
        :param issuer: the pubkey of the issuer of the block
        :param issuers_frame:
        :param issuers_frame_var:
        :param different_issuers_count: the count of issuers
        :param prev_hash: the previous block hash
        :param prev_issuer: the previous block issuer
        :param parameters: the parameters of the currency. Should only be present in block 0.
        :param members_count: the number of members found in this block
        :param identities: the self certifications declared in this block
        :param joiners: the joiners memberships via "IN" documents
        :param actives: renewed memberships via "IN" documents
        :param leavers: the leavers memberships via "OUT" documents
        :param revokations: revokations
        :param excluded: members excluded because of missing certifications
        :param certifications: certifications documents
        :param transactions: transactions documents
        :param inner_hash: the block hash
        :param nonce: the nonce value of the block
        :param signature: the block signature
        """
        super().__init__(version, currency, [signature])
        documents_versions = max(
            max([1] + [i.version for i in identities]),
            max([1] + [m.version for m in actives + leavers + joiners]),
            max([1] + [r.version for r in revokations]),
            max([1] + [c.version for c in certifications]),
            max([1] + [t.version for t in transactions]),
        )
        if self.version < documents_versions:
            raise MalformedDocumentError(
                "Block version is too low : {0} < {1}".format(
                    self.version, documents_versions
                )
            )
        self.number = number
        self.powmin = powmin
        self.time = time
        self.mediantime = mediantime
        self.ud = ud
        self.unit_base = unit_base
        self.issuer = issuer
        self.issuers_frame = issuers_frame
        self.issuers_frame_var = issuers_frame_var
        self.different_issuers_count = different_issuers_count
        self.prev_hash = prev_hash
        self.prev_issuer = prev_issuer
        self.parameters = parameters
        self.members_count = members_count
        self.identities = identities
        self.joiners = joiners
        self.actives = actives
        self.leavers = leavers
        self.revoked = revokations
        self.excluded = excluded
        self.certifications = certifications
        self.transactions = transactions
        self.inner_hash = inner_hash
        self.nonce = nonce

    @property
    def blockUID(self) -> BlockUID:
        return BlockUID(self.number, self.proof_of_work())

    @classmethod
    def from_signed_raw(cls: Type[BlockType], signed_raw: str) -> BlockType:
        lines = signed_raw.splitlines(True)
        n = 0

        version = int(Block.parse_field("Version", lines[n]))
        n += 1

        Block.parse_field("Type", lines[n])
        n += 1

        currency = Block.parse_field("Currency", lines[n])
        n += 1

        number = int(Block.parse_field("Number", lines[n]))
        n += 1

        powmin = int(Block.parse_field("PoWMin", lines[n]))
        n += 1

        time = int(Block.parse_field("Time", lines[n]))
        n += 1

        mediantime = int(Block.parse_field("MedianTime", lines[n]))
        n += 1

        ud_match = Block.re_universaldividend.match(lines[n])
        ud = None
        unit_base = 0
        if ud_match is not None:
            ud = int(Block.parse_field("UD", lines[n]))
            n += 1

        unit_base = int(Block.parse_field("UnitBase", lines[n]))
        n += 1

        issuer = Block.parse_field("Issuer", lines[n])
        n += 1

        issuers_frame = Block.parse_field("IssuersFrame", lines[n])
        n += 1
        issuers_frame_var = Block.parse_field("IssuersFrameVar", lines[n])
        n += 1
        different_issuers_count = Block.parse_field("DifferentIssuersCount", lines[n])
        n += 1

        prev_hash = None
        prev_issuer = None
        if number > 0:
            prev_hash = str(Block.parse_field("PreviousHash", lines[n]))
            n += 1

            prev_issuer = str(Block.parse_field("PreviousIssuer", lines[n]))
            n += 1

        parameters = None
        if number == 0:
            try:
                params_match = Block.re_parameters.match(lines[n])
                if params_match is None:
                    raise MalformedDocumentError("Parameters")
                parameters = params_match.groups()
                n += 1
            except AttributeError:
                raise MalformedDocumentError("Parameters")

        members_count = int(Block.parse_field("MembersCount", lines[n]))
        n += 1

        identities = []
        joiners = []
        actives = []
        leavers = []
        revoked = []
        excluded = []
        certifications = []
        transactions = []

        if Block.re_identities.match(lines[n]) is not None:
            n += 1
            while Block.re_joiners.match(lines[n]) is None:
                selfcert = Identity.from_inline(version, currency, lines[n])
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
            while Block.re_revoked.match(lines[n]) is None:
                membership = Membership.from_inline(version, currency, "OUT", lines[n])
                leavers.append(membership)
                n += 1

        if Block.re_revoked.match(lines[n]):
            n += 1
            while Block.re_excluded.match(lines[n]) is None:
                revokation = Revocation.from_inline(version, currency, lines[n])
                revoked.append(revokation)
                n += 1

        if Block.re_excluded.match(lines[n]):
            n += 1
            while Block.re_certifications.match(lines[n]) is None:
                exclusion_match = Block.re_exclusion.match(lines[n])
                if exclusion_match is not None:
                    exclusion = exclusion_match.group(1)
                    excluded.append(exclusion)
                n += 1

        if Block.re_certifications.match(lines[n]):
            n += 1
            while Block.re_transactions.match(lines[n]) is None:
                certification = Certification.from_inline(
                    version, currency, prev_hash, lines[n]
                )
                certifications.append(certification)
                n += 1

        if Block.re_transactions.match(lines[n]):
            n += 1
            while not Block.re_hash.match(lines[n]):
                tx_lines = ""
                header_data = Transaction.re_header.match(lines[n])
                if header_data is None:
                    raise MalformedDocumentError(
                        "Compact transaction ({0})".format(lines[n])
                    )
                issuers_num = int(header_data.group(2))
                inputs_num = int(header_data.group(3))
                unlocks_num = int(header_data.group(4))
                outputs_num = int(header_data.group(5))
                has_comment = int(header_data.group(6))
                sup_lines = 2
                tx_max = (
                    n
                    + sup_lines
                    + issuers_num * 2
                    + inputs_num
                    + unlocks_num
                    + outputs_num
                    + has_comment
                )
                for index in range(n, tx_max):
                    tx_lines += lines[index]
                n += tx_max - n
                transaction = Transaction.from_compact(currency, tx_lines)
                transactions.append(transaction)

        inner_hash = Block.parse_field("InnerHash", lines[n])
        n += 1

        nonce = int(Block.parse_field("Nonce", lines[n]))
        n += 1

        signature = Block.parse_field("Signature", lines[n])

        return cls(
            version,
            currency,
            number,
            powmin,
            time,
            mediantime,
            ud,
            unit_base,
            issuer,
            issuers_frame,
            issuers_frame_var,
            different_issuers_count,
            prev_hash,
            prev_issuer,
            parameters,
            members_count,
            identities,
            joiners,
            actives,
            leavers,
            revoked,
            excluded,
            certifications,
            transactions,
            inner_hash,
            nonce,
            signature,
        )

    def raw(self) -> str:
        doc = """Version: {version}
Type: Block
Currency: {currency}
Number: {number}
PoWMin: {powmin}
Time: {time}
MedianTime: {mediantime}
""".format(
            version=self.version,
            currency=self.currency,
            number=self.number,
            powmin=self.powmin,
            time=self.time,
            mediantime=self.mediantime,
        )
        if self.ud:
            doc += "UniversalDividend: {0}\n".format(self.ud)

        doc += "UnitBase: {0}\n".format(self.unit_base)

        doc += "Issuer: {0}\n".format(self.issuer)

        doc += """IssuersFrame: {0}
IssuersFrameVar: {1}
DifferentIssuersCount: {2}
""".format(
            self.issuers_frame, self.issuers_frame_var, self.different_issuers_count
        )

        if self.number == 0 and self.parameters is not None:
            str_params = ":".join([str(p) for p in self.parameters])
            doc += "Parameters: {0}\n".format(str_params)
        else:
            doc += "PreviousHash: {0}\n\
PreviousIssuer: {1}\n".format(
                self.prev_hash, self.prev_issuer
            )

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

        doc += "Revoked:\n"
        for revokation in self.revoked:
            doc += "{0}\n".format(revokation.inline())

        doc += "Excluded:\n"
        for exclude in self.excluded:
            doc += "{0}\n".format(exclude)

        doc += "Certifications:\n"
        for cert in self.certifications:
            doc += "{0}\n".format(cert.inline())

        doc += "Transactions:\n"
        for transaction in self.transactions:
            doc += "{0}".format(transaction.compact())

        doc += "InnerHash: {0}\n".format(self.inner_hash)

        doc += "Nonce: {0}\n".format(self.nonce)

        return doc

    def proof_of_work(self) -> str:
        doc_str = """InnerHash: {inner_hash}
Nonce: {nonce}
{signature}
""".format(
            inner_hash=self.inner_hash, nonce=self.nonce, signature=self.signatures[0]
        )
        return hashlib.sha256(doc_str.encode("ascii")).hexdigest().upper()

    def computed_inner_hash(self) -> str:
        doc = self.signed_raw()
        inner_doc = "\n".join(doc.split("\n")[:-2]) + "\n"
        return hashlib.sha256(inner_doc.encode("ascii")).hexdigest().upper()

    def sign(self, keys):
        """
        Sign the current document.
        Warning : current signatures will be replaced with the new ones.
        """
        key = keys[0]
        signed = self.raw()[-2:]
        signing = base64.b64encode(key.signature(bytes(signed, "ascii")))
        self.signatures = [signing.decode("ascii")]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Block):
            return NotImplemented
        return self.blockUID == other.blockUID

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Block):
            return False
        return self.blockUID < other.blockUID

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Block):
            return False
        return self.blockUID > other.blockUID

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Block):
            return False
        return self.blockUID <= other.blockUID

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Block):
            return False
        return self.blockUID >= other.blockUID
