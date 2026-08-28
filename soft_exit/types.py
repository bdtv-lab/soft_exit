from typing import TypedDict


class Config(TypedDict):
    """
    配置文件
    """

    # 临时服务器的 slug
    tmp_server_slug: str
    tmp_server_rcon_host: str
    tmp_server_rcon_port: int
    tmp_server_rcon_password: str
