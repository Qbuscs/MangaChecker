import threading
import time

from manage import update_manga


class UpdateThread(threading.Thread):
    _UPDATE_INTERVAL = 10

    def __init__(self, action):
        super().__init__()
        self.action = action

    def run(self):
        while True:
            time.sleep(self._UPDATE_INTERVAL)
            self.run_updates()

    def run_updates(self) -> None:
        try:
            updated, errors = update_manga()
            if updated:
                self.action()
        except Exception as e:
            pass
