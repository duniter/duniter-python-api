import attr
import logging
from duniterpy.documents import Identity, Membership, BlockUID, Certification, \
    InputSource, OutputSource, Transaction, Unlock, SIGParameter
from duniterpy.documents.transaction import reduce_base
from duniterpy.grammars import output
from duniterpy.key import SigningKey, ScryptParams


@attr.s()
class User:
    """
    The user generates identities documents and sign them
    """
    SCRYPT_PARAMS = ScryptParams(2 ** 12, 16, 1)

    currency = attr.ib(validator=attr.validators.instance_of(str))
    uid = attr.ib(validator=attr.validators.instance_of(str))
    key = attr.ib(validator=attr.validators.instance_of(SigningKey))
    salt = attr.ib(validator=attr.validators.instance_of(str))
    password = attr.ib(validator=attr.validators.instance_of(str))
    blockstamp = attr.ib(validator=attr.validators.instance_of(BlockUID))
    _logger = attr.ib(default=attr.Factory(lambda: logging.getLogger('mirage')))

    @classmethod
    def create(cls, currency, uid, salt, password, blockstamp):
        return cls(currency, uid, SigningKey(salt, password, User.SCRYPT_PARAMS), salt, password, blockstamp)

    def identity(self):
        identity = Identity(10, self.currency, self.key.pubkey, self.uid, self.blockstamp, [])
        identity.sign([self.key])

        return identity

    def join(self, blockstamp):
        ms_doc = Membership(10, self.currency, self.key.pubkey, blockstamp,
                 'IN', self.uid, self.blockstamp, [])
        ms_doc.sign([self.key])
        return ms_doc

    def leave(self, blockstamp):
        ms_doc = Membership(10, self.currency, self.key.pubkey, blockstamp,
                 'OUT', self.uid, self.blockstamp, [])
        ms_doc.sign([self.key])
        return ms_doc

    def certify(self, other, blockstamp):
        cert = Certification(10, self.currency, self.key.pubkey, other.key.pubkey, blockstamp, [])
        cert.sign(self.identity(), [self.key])
        return cert

    def outputs_from_sources(self, amount, sources):
        # such a dirty algorithmm
        # shamelessly copy pasted from sakia
        def current_value(inputs, overhs):
            i = 0
            for s in inputs:
                i += s.amount * (10**s.base)
            for o in overhs:
                i -= o[0] * (10**o[1])
            return i

        amount, amount_base = reduce_base(amount, 0)
        current_base = max([src.base for src in sources])
        result_sources = []
        outputs = []
        overheads = []
        buf_sources = list(sources)
        while current_base >= 0:
            for s in [src for src in buf_sources if src.base == current_base]:
                test_sources = result_sources + [s]
                val = current_value(test_sources, overheads)
                # if we have to compute an overhead
                if current_value(test_sources, overheads) > amount * (10**amount_base):
                    overhead = current_value(test_sources, overheads) - int(amount) * (10**amount_base)
                    # we round the overhead in the current base
                    # exemple : 12 in base 1 -> 1*10^1
                    overhead = int(round(float(overhead) / (10**current_base)))
                    source_value = s.amount * (10**s.base)
                    out = int((source_value - (overhead * (10**current_base)))/(10**current_base))
                    if out * (10**current_base) <= amount * (10**amount_base):
                        result_sources.append(s)
                        buf_sources.remove(s)
                        overheads.append((overhead, current_base))
                        outputs.append((out, current_base))
                # else just add the output
                else:
                    result_sources.append(s)
                    buf_sources.remove(s)
                    outputs.append((s.amount, s.base))
                if current_value(result_sources, overheads) == amount * (10 ** amount_base):
                    return result_sources, outputs, overheads

            current_base -= 1
        raise ValueError("Not enough sources")

    def tx_outputs(self, receiver, outputs, overheads):
        total = []
        outputs_bases = set(o[1] for o in outputs)
        for base in outputs_bases:
            output_sum = 0
            for o in outputs:
                if o[1] == base:
                    output_sum += o[0]
            total.append(OutputSource(output_sum, base, output.Condition.token(output.SIG.token(receiver.key.pubkey))))

        overheads_bases = set(o[1] for o in overheads)
        for base in overheads_bases:
            overheads_sum = 0
            for o in overheads:
                if o[1] == base:
                    overheads_sum += o[0]
            total.append(OutputSource(overheads_sum, base, output.Condition.token(output.SIG.token(self.key.pubkey))))

        return total

    def send_money(self, amount, sources, receiver, blockstamp, message):

        result = self.outputs_from_sources(amount, sources)
        inputs = result[0]
        computed_outputs = result[1]
        overheads = result[2]

        unlocks = []
        for i, s in enumerate(sources):
            unlocks.append(Unlock(i, [SIGParameter(0)]))
        outputs = self.tx_outputs(receiver, computed_outputs, overheads)

        tx = Transaction(3, self.currency, blockstamp, 0,
                            [self.key.pubkey], inputs, unlocks,
                            outputs, message, None)
        tx.sign([self.key])
        return tx