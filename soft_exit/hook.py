from collections.abc import Callable
from types import MethodType

from mcdreforged.mcdr_server import MCDReforgedServer

from . import state
from .cycle import transfer_everyone_to_tmp_server_or_kick


def hijack(target: object, attr_name: str, function: Callable) -> MethodType:
    origin_func: MethodType = getattr(target, attr_name)
    setattr(target, attr_name, MethodType(function, target))

    return origin_func


def on_stop_requested(self: MCDReforgedServer, forced: bool) -> bool:
    self.logger.info("hello there, i want to stop it!")
    if not self.is_server_running():
        self.logger.info("but it's not running!")
    transfer_everyone_to_tmp_server_or_kick(self.basic_server_interface)
    return state.origin_stop(forced)
