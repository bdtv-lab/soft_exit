import mcdreforged as mcdr
from mcdreforged.api.rcon import RconConnection

from . import hook, state
from .config import load_or_init_config
from .cycle import connect_rcon
from .hook import hijack


def on_server_stop(server: mcdr.PluginServerInterface, server_return_code: int):
    if server_return_code != 0:
        server.logger.info("Is it a server crash?")


def on_server_start(server: mcdr.PluginServerInterface):
    pass


def on_server_startup(server: mcdr.PluginServerInterface):
    pass


def on_load(server: mcdr.PluginServerInterface, prev_module):
    logger = server.logger

    config = load_or_init_config(server)
    state.tmp_server_slug = config["tmp_server_slug"]
    logger.info("配置文件已加载")

    state.tmp_server_rcon = RconConnection(
        config["tmp_server_rcon_host"],
        config["tmp_server_rcon_port"],
        config["tmp_server_rcon_password"],
        logger=logger,
    )
    connect_rcon(state.tmp_server_rcon)

    state.origin_stop = hijack(server._mcdr_server, "stop", hook.on_stop_requested)
    logger.info("hooked server.stop")


def on_unload(server: mcdr.PluginServerInterface):
    logger = server.logger

    server._mcdr_server.stop = state.origin_stop
    state.tmp_server_rcon.disconnect()
    logger.info("unhooked server.stop")
