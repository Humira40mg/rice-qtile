from libqtile import hook
from libqtile.log_utils import logger
from libqtile.widget import base
from qtile_extras.widget.decorations import RectDecoration


class WindowControls(base._Widget):

    defaults = [
        ("button_size", 14, "Diameter of each button"),
        ("spacing", 8, "Space between buttons"),
        ("padding", 6, "Left/right padding of the widget"),
        ("max_color", "98c379", "Maximize button colour"),
        ("float_color", "e5c07b", "Toggle Float button colour"),
        ("close_color", "e06c75", "Close button colour"),
        ("bg_radius", 6, "Corner radius of the container decoration"),
    ]

    def __init__(self, max_color="#98c379", float_color="#e5c07b", close_color="#e06c75", **config):
        base._Widget.__init__(self, length=base.bar.CALCULATED, **config)
        self.add_defaults(WindowControls.defaults)
        self.max_color = max_color
        self.float_color = float_color
        self.close_color = close_color

        default_decorations = [
            RectDecoration(
                colour="00000000",
                radius=self.bg_radius,
                filled=True,
                group=True,
            )
        ]
        self.decorations = config.get("decorations", default_decorations)

        self.buttons = [
            ("max", self.max_color, self._maximize),
            ("float", self.float_color, self._toggleFloat),
            ("close", self.close_color, self._close),
        ]

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)
        hook.subscribe.client_focus(self._redraw)
        hook.subscribe.client_killed(self._redraw)
        hook.subscribe.focus_change(self._redraw)

    @property
    def has_window(self):
        w = self.qtile.current_window
        return w is not None

    def calculate_length(self):
        if not self.has_window:
            return 0
        n = len(self.buttons)
        return n * self.button_size + (n - 1) * self.spacing + 2 * self.padding

    def draw(self):
        if self.length == 0:
            return

        self.drawer.clear(self.background or self.bar.background)

        x = self.padding
        r = self.button_size / 2
        for _name, color, _action in self.buttons:
            self.drawer.set_source_rgb(color)
            self.drawer.ctx.arc(x + r, self.bar.height / 2, r, 0, 6.283)
            self.drawer.ctx.fill()
            x += self.button_size + self.spacing

        if hasattr(self, "draw_at_default_position"):
            self.draw_at_default_position()
        else:
            self.drawer.draw(offsetx=self.offset, offsety=self.offsety, width=self.length)

    def _redraw(self, *args, **kwargs):
        self.qtile.call_later(0.02, self.bar.draw)

    def button_press(self, x, y, button):
        if button != 1 or not self.has_window:
            return
        pos = self.padding
        for _name, _color, action in self.buttons:
            if pos <= x <= pos + self.button_size:
                action()
                return
            pos += self.button_size + self.spacing

    def _close(self):
        if self.qtile.current_window:
            self.qtile.current_window.kill()

    def _toggleFloat(self):
        w = self.qtile.current_window
        if w:
            w.toggle_floating()

    def _maximize(self):
        w = self.qtile.current_window
        if w:
            w.toggle_maximize()