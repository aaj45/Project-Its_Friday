import threading
import time


class ThinkingIndicator:
    def __init__(self):
        self._running = False
        self._thread = None

    # -----------------------
    # START
    # -----------------------
    def start(self):
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    # -----------------------
    # STOP
    # -----------------------
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.2)
        self._clear_line()

    # -----------------------
    # ANIMATION LOOP
    # -----------------------
    def _animate(self):
        spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0

        while self._running:
            print(f"\r🤖 Friday is thinking {spinner[i % len(spinner)]}", end="", flush=True)
            time.sleep(0.12)
            i += 1

    # -----------------------
    # CLEANUP
    # -----------------------
    def _clear_line(self):
        print("\r" + " " * 50 + "\r", end="", flush=True)