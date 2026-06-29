from qtile_extras.popup.toolkit import PopupRelativeLayout
from math import floor

from user_profile import GAP, BAR_SIZE_RATIO

from .home_popups.constants import *
import modules.popups.global_popups as root_pops

from modules.utils.system_utils import get_current_resolution

from .home_popups.gretting import init_greetings_popups
from .home_popups.system_info import init_system_info_popups 
from .home_popups.power_buttons import init_power_buttons
from .home_popups.player_control import init_player_control_popups
from .home_popups.sliders import init_slider_popups
from .home_popups.last_incident import init_incident_popup
from .home_popups.shortcuts import init_shortcuts_popups
from .home_popups.custom_shortcuts import init_custom_shortcuts_popups
from .home_popups.quotes import init_quotes_popup

res_x, res_y = get_current_resolution()
bar_size = floor(res_y/BAR_SIZE_RATIO)

POPUP_WIDTH = floor(res_x/5)
POPUP_HEIGHT = floor(res_y - bar_size - 3 * GAP)

# ── popup build ─────────────────────────────────────────────────────
def _build_popup(qtile) -> PopupRelativeLayout:
    
    controls = [
        # ── greeting ────────────────────────────────────────────
        *init_greetings_popups(),

        # ── system info ──────────────────────────────────────────────────────
        *init_system_info_popups(qtile),

        # ── last incident ──────────────────────────────────────────────────────
        *init_incident_popup(),

        # ── sliders ───────────────────────────────
        *init_slider_popups(),

        # ── media player ────────────────────────────────────────      
        *init_player_control_popups(qtile),
        
        # ── shortcuts ────────────────────────────────
        *init_shortcuts_popups(),

        # ── quotes ────────────────────────────────
        *init_quotes_popup(),

        # ── custom shortcuts ────────────────────────────────
        *init_custom_shortcuts_popups(),

        # ── power menu ────────────────────────────────────────
        *init_power_buttons(),
    ]

    return PopupRelativeLayout(
        qtile,
        border_width=5,
        border=None,
        width=POPUP_WIDTH,
        height=POPUP_HEIGHT,
        controls=controls,
        background=BG_POPUP,
        close_on_click=False,
        initial_focus=None,
        hide_on_mouse_leave=True,
        hide_interval=0.2,
    )

# ── entry point ────────────────────────────────────────────────────────────
def show_home_popup(qtile) -> None:
    
    if root_pops.home and not root_pops.home._killed:
        root_pops.home.kill() 
        return

    root_pops.home = _build_popup(qtile)
    root_pops.home.show(relative_to=1, relative_to_bar=True)