

def ensure_bytes(data):
    """
    Convert data in bytes if data is a string

    :param data: Data
    :rtype bytes:
    """
    if isinstance(data, str):
        return bytes(data, 'utf-8')

    return data


def ensure_str(data):
    """
    Convert data in str if data are bytes

    :param data: Data
    :rtype str:
    """
    if isinstance(data, bytes):
        return str(data, 'utf-8')

    return data