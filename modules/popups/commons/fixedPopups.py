from qtile_extras.popup.toolkit import PopupSlider


class PopupSliderFixed(PopupSlider):
    """
    PopupSlider with correction of the inversion bug in vertical mode.

    Original bug (qtile_extras/popup/toolkit.py, pointer_motion) :
    in vertical orientation, the calculation of `percent` directly uses
    the coordinate `y` (which increases towards the bottom of the screen) without
    inverting it, even though the bar is drawn from bottom to top. Result: moving the
    mouse up lowers the value, and vice versa.

    This class only modifies `pointer_motion`; everything else
    (drag_callback, value, colours, etc.) remains unchanged.
    """
    def pointer_motion(self, x, y):
        if self._drag:
            if self.horizontal:
                percent = (x - self.end_margin) / self.bar_length
            else:
                percent = 1 - (y - self.end_margin) / self.bar_length

            percent = max(min(percent, 1), 0)
            self.value = ((self.max_value - self.min_value) * percent) + self.min_value
