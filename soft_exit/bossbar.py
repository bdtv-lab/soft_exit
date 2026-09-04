import mcdreforged as mcdr
from mcdreforged.api.decorator import new_thread
from mcdreforged.api.rcon import RconConnection

from bdtv_node import state as node_state
from bdtv_node.utils import try_get_servers
from soft_exit.types import BossbarState

from . import state

TEXT_JSON_FORMAT = mcdr.RTextJsonFormat.V_1_21_5


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
        self.logger = state.logger

        self.NAME = f"{node_state.server_data['nickname']}启动状态"
        self.ID = bar_id(node_state.server_data["slug"])

        self.rcon = rcon
        self.exec_bossbar(f'add {self.ID} "{self.NAME}"')
        self.state = BossbarState.Hide

    def set_state(self, state: BossbarState):
        self.state = state

        match self.state:
            case BossbarState.Hide:
                # 隐藏 BossBar
                self.set_visible(False)
            case BossbarState.Closing:
                # 显示关闭 BossBar
                self.set_max(125)
                self.set_value(0)
                self.set_name(f"{node_state.server_data['nickname']}关闭中")
                self.set_visible(True)
            case BossbarState.Custom:
                # 交给自定义 bossbar 显示者看
                self.set_value(0)
                self.set_name(f"等待{node_state.server_data['nickname']}启动")
            case BossbarState.Starting:
                self.set_value(100)
                self.set_name(f"{node_state.server_data['nickname']}启动中")
            case BossbarState.Started:
                self.set_value(125)
                self.set_name(f"{node_state.server_data['nickname']}启动完毕")
                self.sync_finished_message()

    def sync_finished_message(self):
        goto_command = f"!!goto {node_state.server_data['slug']}"
        rtext = mcdr.RTextList(
            mcdr.RText(
                f"{node_state.server_data['nickname']}已启动，输入或者点击",
                color=mcdr.RColor.green,
            ),
            mcdr.RText(goto_command, color=mcdr.RColor.aqua)
            .c(mcdr.RAction.suggest_command, goto_command)
            .h(f"前往{node_state.server_data['nickname']}"),
            mcdr.RText("进入。", color=mcdr.RColor.green),
        )

        component = rtext.to_json_str(json_format=TEXT_JSON_FORMAT)
        self.exec(f"execute at @p run tellraw @a {component}")

    def close(self):
        self.rcon.disconnect()

    def exec(self, cmd: str):
        try:
            self.logger.info(f"sending! {cmd}")
            self.rcon.send_command(cmd)
        except ConnectionError as e:
            self.logger.error(f"failed to send: {e}")

    def exec_bossbar(self, followed_cmd: str):
        self.exec(f"/bossbar {followed_cmd}")

    def set(self, followed_cmd: str):
        self.exec_bossbar(f"set {self.ID} {followed_cmd}")

    def set_name(self, name: str):
        self.set(f'name "{name}"')

    def set_visible(self, visible: bool):
        self.set(f"visible {visible}")

    def set_max(self, max: int):
        self.set(f"max {max}")

    def set_value(self, value: int):
        self.set(f"value {value}")
