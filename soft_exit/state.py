from types import MethodType

from mcdreforged.api.rcon import RconConnection

from .bossbar import Bossbar

is_waiting_for_up: bool = False
enable: bool
bossbar: Bossbar
tmp_server_slug: str
tmp_server_rcon: RconConnection
origin_stop: MethodType
