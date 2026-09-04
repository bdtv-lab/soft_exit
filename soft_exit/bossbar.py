import mcdreforged as mcdr
from mcdreforged.api.decorator import new_thread
from mcdreforged.api.rcon import RconConnection

from bdtv_node import state as node_state
from bdtv_node.utils import try_get_servers
from soft_exit.types import BossBarState


def bar_id(slug: str) -> str:
    return f"minecraft:{slug}-server-status"


def show_bar(server: mcdr.ServerInterface, id: str, target: str):
    server.execute(f"/bossbar set {id} players {target}")


@new_thread
def show_all_bar(server: mcdr.ServerInterface, target: str):
    if servers := try_get_servers(server):
        for slug in servers:
            show_bar(server, bar_id(slug), target)


class RemoteBossbar:
    def __init__(self, rcon: RconConnection) -> None:
        self.NAME = f"{node_state.server_data['nickname']}启动状态"
        self.ID = bar_id(node_state.server_data["slug"])

        self.rcon = rcon
        self.exec(f'add {self.ID} "{self.NAME}"')
        self.state = BossBarState.Hide

    def set_state(self, state: BossBarState):
        self.state = state

        match self.state:
            case BossBarState.Hide:
                # 隐藏 BossBar
                self.set_visible(False)
            case BossBarState.Closing:
                # 显示关闭 BossBar
                self.set_max(100)
                self.set_value(0)
                self.set_name(f"{node_state.server_data['nickname']}关闭中")
                self.set_visible(True)
            case BossBarState.Custom:
                self.set_value(0)
                self.set_name(f"等待{node_state.server_data['nickname']}启动")
            case BossBarState.Starting:
                self.set_value(75)
                self.set_name(f"{node_state.server_data['nickname']}启动中")
            case BossBarState.Started:
                self.set_value(100)
                self.set_name(f"{node_state.server_data['nickname']}启动完毕")

    def close(self):
        self.rcon.disconnect()

    def exec(self, followed_cmd: str):
        try:
            print(f"sending! {f'/bossbar {followed_cmd}'}")
            self.rcon.send_command(f"/bossbar {followed_cmd}")
        except ConnectionError:
            pass

    def set(self, followed_cmd: str):
        self.exec(f"set {self.ID} {followed_cmd}")

    def set_name(self, name: str):
        self.set(f'name "{name}"')

    def set_visible(self, visible: bool):
        self.set(f"visible {visible}")

    def set_max(self, max: int):
        self.set(f"max {max}")

    def set_value(self, value: int):
        self.set(f"value {value}")
