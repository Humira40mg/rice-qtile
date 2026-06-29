from math import floor

from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupWidget
from qtile_extras.widget import Systray
from pathlib import Path

from modules.utils.system_utils import get_current_resolution
from user_profile import GAP, theme

BG_POPUP = theme.colors["background_light"]

res_x, res_y = get_current_resolution()

POPUP_WIDTH = floor(res_x / 8)
POPUP_HEIGHT = 42

_popup = None


def _build_popup(qtile) -> PopupRelativeLayout:
    systray = Systray(
        icon_size=22,
        padding=6,
    )

    return PopupRelativeLayout(
        qtile,
        width=POPUP_WIDTH,
        height=POPUP_HEIGHT,
        background=BG_POPUP,
        border_width=5,
        border=None,
        close_on_click=True,
        hide_on_mouse_leave=False,
        hide_interval=0.2,
        controls=[
            PopupWidget(
                widget=systray,
                pos_x=0.0,
                pos_y=0.0,
                width=1.0,
                height=1.0,
            )
        ],
    )


def show_systray_popup(qtile):
    global _popup

    if _popup and not _popup._killed:
        _popup.kill()
        return

    _popup = _build_popup(qtile)
    _popup.show(
        relative_to=3,
        relative_to_bar=True,
        x=GAP * -2,
    )