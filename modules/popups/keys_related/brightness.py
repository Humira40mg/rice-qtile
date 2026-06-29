from qtile_extras.popup.toolkit import PopupRelativeLayout, PopupText
from math import floor
import subprocess

from user_profile import BAR_SIZE_RATIO

import modules.popups.global_popups as root_pops

from modules.utils.system_utils import get_current_resolution

from time import sleep

#from modules.popups.commons.animation import trancparency_out
from libqtile.lazy import lazy

from user_profile import theme

from modules.popups.home_popups.sliders import get_current_brightness


res_x, res_y = get_current_resolution()
bar_size = floor(res_y/BAR_SIZE_RATIO)

POPUP_WIDTH = floor(res_x/10)
POPUP_HEIGHT = floor(res_y/7.5)

BG_POPUP = theme.colors["background_dark"]
SELECTED = theme.colors["selected"]
GREY = theme.colors["grey"]

ICON_BRIGHTNESS_ON = "󰃠 "
ICON_BRIGHTNESS_OFF = "󰃞 "

_popup = None

# ── popup build ─────────────────────────────────────────────────────
def _build_popup(qtile, brightness) -> PopupRelativeLayout:
    icon = ICON_BRIGHTNESS_ON
    if brightness == 0 :
        icon = ICON_BRIGHTNESS_OFF
    controls = [
        PopupText(
            text=icon,
            pos_x=0.01,
            pos_y=0.02,
            width=0.9,
            height=0.7,
            fontsize=100,
            h_align="center",
        ),
        PopupText(
            text="",
            pos_x=0.1,
            pos_y=0.8,
            width=0.8,
            height=0.1,
            background = GREY
        ),
        PopupText(
            text="",
            pos_x=0.1,
            pos_y=0.8,
            width=brightness*0.8/100,
            height=0.1,
            background = SELECTED
        )
    ]

    return PopupRelativeLayout(
        qtile,
        width=POPUP_WIDTH,
        height=POPUP_HEIGHT,
        controls=controls,
        background=BG_POPUP,
        close_on_click=False,
        initial_focus=None,
        hide_on_mouse_leave=False,
        hide_on_timeout=0.2,
        relative_to_bar=True
    )

# ── entry point ────────────────────────────────────────────────────────────
def show_brightness_popup(qtile, command) -> None:
    
    global _popup
    
    if _popup and not _popup._killed:
        _popup.kill() 

    subprocess.run(["bash", "-c", command])

    brightness = int(get_current_brightness())

    if root_pops.home and not root_pops.home._killed:
        icon = ICON_BRIGHTNESS_ON
        if brightness == 0 :
            icon = ICON_BRIGHTNESS_OFF
        root_pops.home.update_controls(brightness_text=f"{brightness}%", brightness_slider=brightness, brightness_button=icon)

    _popup = _build_popup(qtile, brightness)
    _popup.show(relative_to=5)