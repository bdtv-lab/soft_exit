import mcdreforged as mcdr
from mcdreforged.api.rcon import RconConnection
from mcdreforged.mcdr_server import MCDReforgedServer

from soft_exit.types import BossbarState

from . import state
from .bossbar import RemoteBossbar, show_all_bar
from .config import load_or_init_config
from .hook import hijack
from .utils import (
    close_hide_bar_thread,
    send_hide_bar_thread,
    transfer_everyone_to_tmp_server_or_kick,
)


def on_stop_requested(self: MCDReforgedServer, forced: bool) -> bool:
    self.logger.info("hello there, i want to stop it!")
    if not self.is_server_running():
        self.logger.info("but it's not running!")
    if state.enable:
        transfer_everyone_to_tmp_server_or_kick(self.basic_server_interface)
        state.is_waiting_for_up = True
        state.bossbar.set_state(BossbarState.Closing)

    return state.origin_stop(forced)


def on_server_stop(server: mcdr.PluginServerInterface, server_return_code: int):
    if server_return_code != 0:
        server.logger.info("Is it a server crash?")
    if not state.is_waiting_for_up:
        return
    if state.enable:
        state.bossbar.set_state(BossbarState.Custom)


def on_server_start(server: mcdr.PluginServerInterface):
    if not state.is_waiting_for_up:
        return
    if state.enable:
        state.bossbar.set_state(BossbarState.Starting)
        send_hide_bar_thread()


def on_server_startup(server: mcdr.PluginServerInterface):
    if not state.is_waiting_for_up:
        return
    if state.enable:
        state.bossbar.set_state(BossbarState.Started)
    state.is_waiting_for_up = False


def on_player_joined(server: mcdr.PluginServerInterface, player: str, info: mcdr.Info):
    show_all_bar(server, player)  # type: ignore


def on_load(server: mcdr.PluginServerInterface, prev_module):
    state.logger = server.logger
    logger = state.logger

    # 加载配置文件
    config = load_or_init_config(server)
    state.tmp_server_slug = config["tmp_server_slug"]
    logger.info("配置文件已加载")

    # 初始化 rcon
    server_rcon = RconConnection(
        config["tmp_server_rcon_host"],
        config["tmp_server_rcon_port"],
        config["tmp_server_rcon_password"],
        logger=logger,
    )
    state.enable = config["enable"]
    if state.enable:
        try:
            # 尝试连接 rcon
            server_rcon.connect()
        except ConnectionError:
            pass
        state.bossbar = RemoteBossbar(server_rcon)
        state.bossbar.set_state(BossbarState.Hide)

    # 注入停止信号
    state.origin_stop = hijack(server._mcdr_server, "stop", on_stop_requested)
    logger.info("hooked server.stop")


def on_unload(server: mcdr.PluginServerInterface):
    logger = state.logger

    server._mcdr_server.stop = state.origin_stop
    if state.enable:
        close_hide_bar_thread()
        state.bossbar.close()
    logger.info("unhooked server.stop")
