from qtile_extras import widget
import itertools
import os
import glob
from PIL import Image as PILImage


def _on_ac_power():
    for ac_path in glob.glob("/sys/class/power_supply/A*/online"):
        try:
            with open(ac_path) as f:
                return f.read().strip() == "1"
        except OSError:
            continue
    return True


class GifImage(widget.Image):
    def __init__(self, filename, frame_interval=0.04, battery_check_interval=2.0, **config):
        super().__init__(**config)
        gif = PILImage.open(filename)
        self._frames = []
        try:
            while True:
                self._frames.append(gif.copy())
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        self._frame_cycle = itertools.cycle(self._frames)
        self._frame_interval = frame_interval
        self._battery_check_interval = battery_check_interval
        self._tmp_path = "/tmp/qtile_animated.png"
        next(self._frame_cycle).save(self._tmp_path)
        self.filename = self._tmp_path

    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)
        self.timeout_add(self._frame_interval, self._next_frame)

    def _next_frame(self):
        if _on_ac_power():
            next(self._frame_cycle).save(self._tmp_path)
            self.filename = self._tmp_path
            self._update_image()
            self.draw()
            self.timeout_add(self._frame_interval, self._next_frame)
        else:
            self.timeout_add(self._battery_check_interval, self._next_frame)