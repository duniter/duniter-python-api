from duniterpy.documents import Block, BlockUID, Certification, Identity, Membership, Revocation, Transaction
from duniterpy.key import SigningKey
import time
import attr
import logging
import random
from ._user_identity import UserIdentity


@attr.s()
class BlockForge:
    """
    The block forge generates a blockchain with a PoW of 1
    """
    currency = attr.ib(validator=attr.validators.instance_of(str))
    key = attr.ib(validator=attr.validators.instance_of(SigningKey))
    _pool = attr.ib(default=attr.Factory(list), validator=attr.validators.instance_of(list))
    blocks = attr.ib(default=attr.Factory(list), validator=attr.validators.instance_of(list))
    _identities = attr.ib(default=attr.Factory(dict), validator=attr.validators.instance_of(dict))
    _ud = attr.ib(default=False, validator=attr.validators.instance_of(bool))
    _logger = attr.ib(default=attr.Factory(lambda: logging.getLogger('mirage')))

    @classmethod
    def start(cls, currency, salt, password, loop):
        key = SigningKey(salt, password)
        return cls(currency, key)

    def push(self, document):
        self._pool.append(document)

    def next_dividend(self):
        if self._ud:
            try:
                latest_dividend = next(reversed([b for b in self.blocks if b.ud]))
            except StopIteration:
                return 100
            return latest_dividend * 1.1

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
        return len([i for i in self._identities.values() if i.member])

    def identities(self):
        return [d for d in self._pool if type(d) is Identity]

    def revocations(self):
        return [r for r in self._pool if type(r) is Revocation]

    def joiners(self):
        return [d for d in self._pool if type(d) is Membership and d.membership_type == 'IN'
                and d.issuer in self._identities and not self._identities[d.issuer].member]

    def actives(self):
        return [d for d in self._pool if type(d) is Membership and d.membership_type == 'IN'
                and d.issuer in self._identities and self._identities[d.issuer].member]

    def leavers(self):
        return [d for d in self._pool if type(d) is Membership and d.membership_type == 'OUT'
                and d.issuer in self._identities and self._identities[d.issuer].member]

    def excluded(self):
        return []

    def certifications(self):
        return [d for d in self._pool if type(d) is Certification]

    def transactions(self):
        return [d for d in self._pool if type(d) is Transaction]

    def parameters(self):
        if not self.blocks:
            return 0.1, 86400, 100000, 10800, 40, 2629800, 31557600, 1, 604800, 604800,\
                                                0.9, 15778800, 5, 12, 300, 25, 40, 0.66

    def monetary_mass(self):
        mass = 0
        for b in self.blocks:
            if b.ud:
                mass += b.ud * b.members_count
        return mass

    def set_member(self, pubkey, member):
        self._logger.info("Set {0} ({1}) as member : {2}".format(self._identities[pubkey].uid,
                                                                 pubkey[:5], member))
        self._identities[pubkey].member = member

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

        block = Block(5, self.currency, len(self.blocks), 1, int(time.time()), 
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
            self._identities[identity.pubkey] = UserIdentity(identity.pubkey, identity.uid, identity.timestamp, False)
        self._pool = []
