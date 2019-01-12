from typing import Union


def ensure_bytes(data: Union[str, bytes]) -> bytes:
    """
    Convert data in bytes if data is a string

    :param data: Data
    :rtype bytes:
    """
    if isinstance(data, str):
        return bytes(data, 'utf-8')

    return data


def ensure_str(data: Union[str, bytes]) -> str:
    """
    Convert data in str if data are bytes

    :param data: Data
    :rtype str:
    """
    if isinstance(data, bytes):
        return str(data, 'utf-8')

    return data


def xor_bytes(b1: bytes, b2: bytes) -> bytearray:
    """
    Apply XOR operation on two bytes arguments

    :param b1: First bytes argument
    :param b2: Second bytes argument
    :rtype bytearray:
    """
    result = bytearray()
    for i1, i2 in zip(b1, b2):
        result.append(i1 ^ i2)
    return result
