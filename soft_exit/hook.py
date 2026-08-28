from collections.abc import Callable
from types import MethodType


def hijack(target: object, attr_name: str, function: Callable) -> MethodType:
    origin_func: MethodType = getattr(target, attr_name)
    setattr(target, attr_name, MethodType(function, target))

    return origin_func
