from typing import Union, Type, Any
from duniterpy.grammars.output import SIG, CSV, CLTV, XHX, ConditionType


def output_available(
    condition: Type[ConditionType], comparison: Any, value: Union[str, int]
) -> bool:
    """
    Check if output source is available
    Currently only handle unique condition without composition

    operator.lt(a, b) is equivalent to a < b
    operator.le(a, b) is equivalent to a <= b
    operator.gt(a, b) is equivalent to a > b
    operator.ge(a, b) is equivalent to a >= b
    """
    if type(condition.left) == SIG:
        return comparison(condition.left.pubkey, value)
    if type(condition.left) == CSV:
        return comparison(int(condition.left.time), value)
    if type(condition.left) == CLTV:
        return comparison(int(condition.left.timestamp), value)
    if type(condition.left) == XHX:
        return comparison(condition.left.sha_hash, value)
    else:
        return False
