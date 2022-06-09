import threading
import time

from manage import update_manga


class UpdateThread(threading.Thread):
    _UPDATE_INTERVAL = 10

    def run(self):
        while True:
            self.run_updates()
            time.sleep(self._UPDATE_INTERVAL)

    def run_updates(self) -> None:
        updated, errors = update_manga()
        if updated:
            print("Updated")
        else:
            print("No new updates")
        for error in errors:
            print(error)
