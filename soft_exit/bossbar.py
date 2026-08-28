import mcdreforged as mcdr
from mcdreforged.api.decorator import new_thread
from mcdreforged.api.rcon import RconConnection

from bdtv_node import state as node_state
from bdtv_node.utils import try_get_servers


def bar_id(slug: str) -> str:
    return f"minecraft:{slug}-server-status"


def show_bar(server: mcdr.ServerInterface, id: str, target: str):
    server.execute(f"/bossbar set {id} players {target}")


@new_thread
def show_all_bar(server: mcdr.ServerInterface, target: str):
    if servers := try_get_servers(server):
        for slug in servers:
            show_bar(server, slug, target)


class Bossbar:
    NAME = f"{node_state.server_data['nickname']} 启动状态"
    ID = bar_id(node_state.server_data["slug"])

    def __init__(self, rcon: RconConnection) -> None:
        self.rcon = rcon
        self.exec(f"add {self.ID} {self.NAME}")

    def exec(self, followed_cmd: str):
        try:
            self.rcon.send_command(f"/bossbar {self.ID} {followed_cmd}")
        except ConnectionError:
            pass

    def set_name(self, name: str):
        self.exec(f"set name {name}")

    def set_visible(self, visible: bool):
        self.exec(f"set visible {visible}")

    def set_max(self, max: int):
        self.exec(f"set max {max}")

    def set_value(self, value: int):
        self.exec(f"set value {value}")
