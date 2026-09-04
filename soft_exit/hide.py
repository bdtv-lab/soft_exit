import threading

from mcdreforged.api.decorator import new_thread

from . import state


@new_thread("Hide-Bar")
def hide_bar_thread(event: threading.Event, delay: float = 60.0 * 15):
    """
    倒计时结束后隐藏 bossbar
    """

    logger = state.logger

    event.wait(delay)
    if not event.is_set():
        # 隐藏 bar
        state.bossbar.set_visible(False)
        logger.info("Hided bossbar!")
    else:
        logger.info("Hide Bar exited by event!")
