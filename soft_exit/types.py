from enum import Enum
from typing import TypedDict


class BossbarState(Enum):
    """
    定义 Bossbar 的状态
    """

    # 服务器已启动
    Started = "Started"
    # 服务器正在关闭
    Closing = "Closing"
    # 服务器已关闭
    Custom = "Custom"
    # 服务器启动中
    Starting = "Starting"
    # Bossbar 初始化
    Hide = "Hide"


class Config(TypedDict):
    """
    配置文件
    """

    # 临时服务器的 slug
    enable: bool
    tmp_server_slug: str
    tmp_server_rcon_host: str
    tmp_server_rcon_port: int
    tmp_server_rcon_password: str
