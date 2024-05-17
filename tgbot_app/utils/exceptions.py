from aiogram.dispatcher.event.bases import CancelHandler


class SilentCancelHandler(CancelHandler):
    def __str__(self):
        return

    def with_traceback(self, __tb):
        return
