from duniterpy.documents import Block, BlockUID, Certification, Identity, Membership, \
    Revocation, Transaction, InputSource
from duniterpy.key import SigningKey
import time
import attr
import logging
import random
from ._user_identity import UserIdentity
from ._cert import Cert
from ._ms import MS
from ._ud import UD


@attr.s()
class BlockForge:
    """
    The block forge generates a blockchain with a PoW of 1
    """
    currency = attr.ib(validator=attr.validators.instance_of(str))
    key = attr.ib(validator=attr.validators.instance_of(SigningKey))
    pool = attr.ib(default=attr.Factory(list), validator=attr.validators.instance_of(list))
    blocks = attr.ib(default=attr.Factory(list), validator=attr.validators.instance_of(list))
    user_identities = attr.ib(default=attr.Factory(dict), validator=attr.validators.instance_of(dict))
    _ud = attr.ib(default=False, validator=attr.validators.instance_of(bool))
    _logger = attr.ib(default=attr.Factory(lambda: logging.getLogger('mirage')))

    @classmethod
    def start(cls, currency, salt, password, scrypt_params, loop):
        key = SigningKey(salt, password, scrypt_params)
        return cls(currency, key)

    def push(self, document):
        self.pool.append(document)

    def next_dividend(self):
        if self._ud:
            try:
                latest_dividend = next(reversed([b.ud for b in self.blocks if b.ud]))
                return int(latest_dividend * 1.1)
            except StopIteration:
                return 100
            finally:
                self._ud = False

    def previous_hash(self):
        try:
            latest_block = next(reversed(self.blocks))
        except StopIteration:
            return BlockUID.empty().sha_hash
        return latest_block.sha_hash

    def previous_issuer(self):
        try:
            latest_block = next(reversed(self.blocks))
        except StopIteration:
            return None
        return latest_block.issuer

    def members_count(self):
        return len([i for i in self.user_identities.values() if i.member])

    def identities(self):
        return [d for d in self.pool if type(d) is Identity]

    def revocations(self):
        return [r for r in self.pool if type(r) is Revocation]

    def joiners(self):
        return [d for d in self.pool if type(d) is Membership and d.membership_type == 'IN'
                and ((d.issuer in self.user_identities and not self.user_identities[d.issuer].member)
                     or d.issuer in [d.pubkey for d in self.pool if type(d) is Identity])]

    def actives(self):
        return [d for d in self.pool if type(d) is Membership and d.membership_type == 'IN'
                and d.issuer in self.user_identities and self.user_identities[d.issuer].member]

    def leavers(self):
        return [d for d in self.pool if type(d) is Membership and d.membership_type == 'OUT'
                and d.issuer in self.user_identities and self.user_identities[d.issuer].member]

    def excluded(self):
        return []

    def certifications(self):
        return [d for d in self.pool if type(d) is Certification]

    def transactions(self):
        return [d for d in self.pool if type(d) is Transaction]

    def parameters(self):
        if not self.blocks:
            return 0.1, 86400, 100000, 10800, 40, 2629800, 31557600, 1, 604800, 604800,\
                    0.9, 15778800, 5, 12, 300, 25, 0.66, 1488970800, 1490094000, 15778800


    def monetary_mass(self, number=None):
        mass = 0
        for b in self.blocks:
            if b.ud and (not number or b.number <= number):
                mass += b.ud * b.members_count
        return mass

    def set_member(self, pubkey, member):
        self._logger.info("Set {0} ({1}) as member : {2}".format(self.user_identities[pubkey].uid,
                                                                 pubkey[:5], member))
        self.user_identities[pubkey].member = member
        self.user_identities[pubkey].was_member = self.user_identities[pubkey].was_member or member

    def generate_dividend(self):
        self._logger.info("Generate dividend")
        self._ud = True

    def build_data(self):
        previous_hash = self.previous_hash()
        previous_issuer = self.previous_issuer()
        parameters = self.parameters()
        members_count = self.members_count()
        identities = self.identities()
        joiners = self.joiners()
        actives = self.actives()
        leavers = self.leavers()
        revocations = self.revocations()
        excluded = self.excluded()
        certifications = self.certifications()
        transactions = self.transactions()

        block = Block(10, self.currency, len(self.blocks), 1, int(time.time()),
                      int(time.time()), self.next_dividend(), 0, 
                      self.key.pubkey, 5, 5, 5, previous_hash, previous_issuer, 
                      parameters, members_count, identities, 
                      joiners, actives, leavers, 
                      revocations, excluded, certifications, 
                      transactions, "", 0, None)
        block.inner_hash = block.computed_inner_hash()
        return block

    def forge_block(self):
        block = self.build_data()
        block.sign([self.key])

        block.noonce = int(random.random()*10000000)
        self._logger.info("New block generated : {0}".format(block.blockUID))

        self.blocks.append(block)
        for identity in block.identities:
            self.user_identities[identity.pubkey] = UserIdentity(pubkey=identity.pubkey, uid=identity.uid,
                                                                 blockstamp=identity.timestamp,
                                                                 signature=identity.signatures[0])
            self._logger.info("New identity : {0}".format(self.user_identities[identity.pubkey]))

        if block.ud:
            for identity in self.user_identities.values():
                if identity.member:
                    identity.sources.append(InputSource(block.ud, block.unit_base, 'D', identity.pubkey, block.number))
                    identity.ud_generated.append(UD(amount=block.ud,
                                                    base=block.unit_base,
                                                    block_number=block.number,
                                                    time=block.mediantime))

        for certification in block.certifications:
            cert = Cert(from_identity=self.user_identities[certification.pubkey_from],
                        to_identity=self.user_identities[certification.pubkey_to],
                        signature=certification.signatures[0],
                        written_on=block.blockUID,
                        block=certification.timestamp.number,
                        mediantime=next(b.mediantime
                                        for b in self.blocks if b.number == certification.timestamp.number))
            self.user_identities[certification.pubkey_from].certs_sent.append(cert)
            self.user_identities[certification.pubkey_to].certs_received.append(cert)

        for membership in block.joiners + block.actives + block.leavers:
            self.user_identities[membership.issuer].memberships.append(MS(pubkey=membership.issuer,
                                                                          type=membership.membership_type,
                                                                          written_on=block.number,
                                                                          blockstamp=membership.membership_ts,
                                                                          timestamp=block.mediantime))

        for tx in block.transactions:
            receivers = [o.conditions.left.pubkey for o in tx.outputs
                         if o.conditions.left.pubkey != tx.issuers[0]]
            self.user_identities[tx.issuers[0]].tx_sent.append(tx)
            self.user_identities[receivers[0]].tx_received.append(tx)

        self.pool = []
