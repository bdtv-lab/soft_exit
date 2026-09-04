import threading
from logging import Logger
from types import MethodType

from mcdreforged import FunctionThread

from .bossbar import RemoteBossbar

# 是否是关闭后等待服务器启动的状态
is_waiting_for_up: bool = False
# 是否启用转移至临时服并展示 Bossbar
enable: bool
# Bossbar 实例
bossbar: RemoteBossbar
# 临时服务器 slug
tmp_server_slug: str
# 存储原始的服务器 stop 函数，用于在 hook 后执行与插件卸载后取消 hook
origin_stop: MethodType
# 日志记录器
logger: Logger
# bossbar 清理线程与事件
stop_hide_bar_thread: tuple[FunctionThread, threading.Event] | None = None
