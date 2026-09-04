import mcdreforged as mcdr

from bdtv_node import state as node_state
from bdtv_node.utils import pure_players, try_get_servers
from online_player_api import get_player_list
from soft_exit.types import BossbarState

from . import state


def transfer_everyone_to_tmp_server_or_kick(server: mcdr.ServerInterface):
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
    if not state.enable or not state.is_waiting_for_up:
        return
    if state.bossbar.state != BossbarState.Custom:
        return
    value = min(max(value, 0), 100)
    if name is not None:
        state.bossbar.set_name(name)
    state.bossbar.set_value(value)
