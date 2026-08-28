import threading

import mcdreforged as mcdr
from mcdreforged.mcdr_server import MCDReforgedServer

from . import state
from .config import load_or_init_config
from .hook import hijack


def my_stop(self: MCDReforgedServer, forced: bool) -> bool:
    self.logger.info("hello there, i want to stop it!")
    if not self.is_server_running():
        self.logger.info("but it's not running!")
    return state.origin_stop(forced)


def on_load(server: mcdr.PluginServerInterface, prev_module):
    logger = server.logger

    state.origin_stop = hijack(server._mcdr_server, "stop", my_stop)
    server.logger.info("hooked server.stop")

    # config = load_or_init_config(server)
    # logger.info("配置文件已加载")


def on_unload(server: mcdr.PluginServerInterface):
    logger = server.logger

    server._mcdr_server.stop = state.origin_stop
    server.logger.info("unhooked server.stop")
