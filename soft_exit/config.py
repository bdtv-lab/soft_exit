import json
import os

import mcdreforged as mcdr

from .types import Config

CONFIG_FILE = "config.json"

DEFAULT_CONFIG: Config = {
    "tmp_server_slug": "my-server",
}


def load_or_init_config(server: mcdr.PluginServerInterface) -> Config:
    """
    尝试加载配置文件，如果不存在，则会以默认配置初始化

    注意不会处理配置文件错误的情况
    """

    config_path = os.path.join(server.get_data_folder(), CONFIG_FILE)

    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write(
                json.dumps(
                    DEFAULT_CONFIG,
                    indent=4,
                    ensure_ascii=False,
                )
            )
    with open(config_path, "r") as f:
        conf = json.load(f)

    return conf
