from typing import Optional

from .constants import SCRYPT_PARAMS


class ScryptParams:
    """
    Class to simplify handling of scrypt parameters
    """

    def __init__(
        self,
        n: Optional[int] = SCRYPT_PARAMS["N"],
        r: Optional[int] = SCRYPT_PARAMS["r"],
        p: Optional[int] = SCRYPT_PARAMS["p"],
        seed_length: Optional[int] = SCRYPT_PARAMS["seed_length"],
    ) -> None:
        """
        Init a ScryptParams instance with crypto parameters

        :param n: Optional scrypt param N, default see constant SCRYPT_PARAMS
        :param r: Optional scrypt param r, default see constant SCRYPT_PARAMS
        :param p: Optional scrypt param p, default see constant SCRYPT_PARAMS
        :param seed_length: Optional scrypt param seed_length, default see constant SCRYPT_PARAMS
        """
        self.N = n
        self.r = r
        self.p = p
        self.seed_length = seed_length
