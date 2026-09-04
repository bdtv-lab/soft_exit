from collections.abc import Callable
from types import MethodType


def hijack(target: object, attr_name: str, function: Callable) -> MethodType:
    """
    劫持一个类方法，返回原本的方法
    """

    origin_func: MethodType = getattr(target, attr_name)
    setattr(target, attr_name, MethodType(function, target))

    return origin_func
