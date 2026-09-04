from logging import Logger
from types import MethodType

from .bossbar import RemoteBossbar

is_waiting_for_up: bool = False
enable: bool
bossbar: RemoteBossbar
tmp_server_slug: str
origin_stop: MethodType
logger: Logger
