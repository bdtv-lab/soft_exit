import mcdreforged as mcdr
from mcdreforged.api.rcon import RconConnection
from mcdreforged.mcdr_server import MCDReforgedServer

from . import state
from .bossbar import Bossbar, show_all_bar
from .config import load_or_init_config
from .cycle import transfer_everyone_to_tmp_server_or_kick
from .hook import hijack


def on_stop_requested(self: MCDReforgedServer, forced: bool) -> bool:
    self.logger.info("hello there, i want to stop it!")
    if not self.is_server_running():
        self.logger.info("but it's not running!")
    if state.enable:
        transfer_everyone_to_tmp_server_or_kick(self.basic_server_interface)
        state.is_waiting_for_up = True
        state.bossbar.set_max(100)
        state.bossbar.set_value(0)
        state.bossbar.set_name("服务器关闭中")
        state.bossbar.set_visible(True)

    return state.origin_stop(forced)


def on_server_stop(server: mcdr.PluginServerInterface, server_return_code: int):
    if server_return_code != 0:
        server.logger.info("Is it a server crash?")
    if not state.is_waiting_for_up:
        return
    state.bossbar.set_value(33)
    state.bossbar.set_name("等待服务器启动")


def on_server_start(server: mcdr.PluginServerInterface):
    if not state.is_waiting_for_up:
        return
    state.bossbar.set_value(66)
    state.bossbar.set_name("服务器启动中")


def on_server_startup(server: mcdr.PluginServerInterface):
    if not state.is_waiting_for_up:
        return
    state.bossbar.set_value(100)
    state.bossbar.set_name("服务器启动完毕")
    state.is_waiting_for_up = False


def on_player_joined(server: mcdr.PluginServerInterface, player: str, info: mcdr.Info):
    show_all_bar(server, player)  # type: ignore


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
    state.enable = config["enable"]
    if state.enable:
        try:
            state.tmp_server_rcon.connect()
        except ConnectionError:
            pass
        state.bossbar = Bossbar(state.tmp_server_rcon)

        state.bossbar.set_visible(False)

    state.origin_stop = hijack(server._mcdr_server, "stop", on_stop_requested)
    logger.info("hooked server.stop")


def on_unload(server: mcdr.PluginServerInterface):
    logger = server.logger

    server._mcdr_server.stop = state.origin_stop
    state.tmp_server_rcon.disconnect()
    logger.info("unhooked server.stop")
