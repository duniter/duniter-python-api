import attr
import logging
from duniterpy.documents import Identity, Membership, BlockUID, Certification
from duniterpy.key import SigningKey


@attr.s()
class User:
    """
    The user generates identities documents and sign them
    """
    currency = attr.ib(validator=attr.validators.instance_of(str))
    uid = attr.ib(validator=attr.validators.instance_of(str))
    key = attr.ib(validator=attr.validators.instance_of(SigningKey))
    blockstamp = attr.ib(validator=attr.validators.instance_of(BlockUID))
    _logger = attr.ib(default=attr.Factory(lambda: logging.getLogger('duniter_mock_server')))

    @classmethod
    def create(cls, currency, uid, salt, password, blockstamp):
        return cls(currency, uid, SigningKey(salt, password), blockstamp)

    def identity(self):
        identity = Identity(3, self.currency, self.key.pubkey, self.uid, self.blockstamp, [])
        identity.sign([self.key])

        return identity

    def join(self, blockstamp):
        ms_doc = Membership(3, self.currency, self.key.pubkey, blockstamp,
                 'IN', self.uid, self.blockstamp, [])
        ms_doc.sign([self.key])
        return ms_doc

    def leave(self, blockstamp):
        ms_doc = Membership(3, self.currency, self.key.pubkey, blockstamp,
                 'OUT', self.uid, self.blockstamp, [])
        ms_doc.sign([self.key])
        return ms_doc

    def certify(self, other, blockstamp):
        cert = Certification(3, self.currency, self.key.pubkey, other.key.pubkey, blockstamp, [])
        cert.sign(self.identity(), [self.key])
        return cert
