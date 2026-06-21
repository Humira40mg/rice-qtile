from libqtile import widget
from qtile_extras import widget as extrawidget
import itertools
from PIL import Image as PILImage

class GifImage(widget.Image):
    def __init__(self, filename, frame_interval=0.04, **config):
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
        self._tmp_path = "/tmp/qtile_animated.png"
        next(self._frame_cycle).save(self._tmp_path)
        self.filename = self._tmp_path

    def _configure(self, qtile, bar):
        super()._configure(qtile, bar)
        self.timeout_add(self._frame_interval, self._next_frame)

    def _next_frame(self):
        next(self._frame_cycle).save(self._tmp_path)
        self.filename = self._tmp_path
        self._update_image()
        self.draw()
        self.timeout_add(self._frame_interval, self._next_frame)