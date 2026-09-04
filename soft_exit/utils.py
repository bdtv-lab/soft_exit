import threading

import mcdreforged as mcdr

from bdtv_node import state as node_state
from bdtv_node.utils import pure_players, try_get_servers
from online_player_api import get_player_list
from soft_exit.types import BossbarState

from . import state
from .hide import hide_bar_thread


def transfer_everyone_to_tmp_server_or_kick(server: mcdr.ServerInterface):
    """
    如果临时服务器可用，将所有玩家转移至临时服务器

    否则提出所有玩家并提供理由
    """

    servers = try_get_servers(server)
    if servers is None:
        server.say("无法获取临时服务器列表")
        return

    tmp_server = servers.get(state.tmp_server_slug, None)
    playing_players = pure_players(get_player_list())

    if tmp_server is None or tmp_server == node_state.server_data["slug"]:
        for player in playing_players:
            server.execute(
                f"/kick {player['nickname']} {f'临时服务器{state.tmp_server_slug}不可用'}"
            )
        return

    for player in playing_players:
        server.execute(
            f"/transfer {tmp_server['address']} {tmp_server['port']} {player['nickname']}"
        )


def set_custom_progress(value: int, name: str | None = None):
    """
    将 Bossbar 设定为自定义进度和标题

    如果 Bossbar 不在可以自定义的状态，操作将被忽略
    """

    if not state.enable or not state.is_waiting_for_up:
        return
    if state.bossbar.state != BossbarState.Custom:
        return
    value = min(max(value, 0), 100)
    if name is not None:
        state.bossbar.set_name(name)
    state.bossbar.set_value(value)


def send_hide_bar_thread():
    """
    启动一个 Bossbar 隐藏计时器线程

    会先尝试终止已有的计时器线程
    """

    close_hide_bar_thread()

    event = threading.Event()
    thread = hide_bar_thread(event)  # type: ignore
    state.stop_hide_bar_thread = (thread, event)


def close_hide_bar_thread():
    """
    终止已有的 Bossbar 隐藏计时器线程（如果有）

    终止是阻塞的
    """

    if state.stop_hide_bar_thread is None:
        return

    thread, event = state.stop_hide_bar_thread

    event.set()
    thread.join()
