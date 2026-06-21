"""
wifi_popup.py
Popup Qtile for WiFi and VPN management.
"""
import subprocess

from qtile_extras.popup.toolkit import PopupImage, PopupRelativeLayout, PopupText
from libqtile.lazy import lazy
from pathlib import Path
from math import floor

from modules.status_reader import Status
from user_profile import theme, GAP, BAR_SIZE_RATIO, USERNAME, USER_IMAGE

from .commons.buttons import _make_icon_button
from modules.commands import commands
from modules.utils.system_utils import get_current_resolution

# ── colors ───────────────────────────────────────────────────────────────────

BG_POPUP      = theme.colors["background_darkest"]
TEXT_PRIMARY  = theme.colors["white"]
TEXT_MUTED    = theme.colors["grey"]
HIGHLIGHT     = theme.colors["background"]
ON_COLOR      = theme.colors["green"]
SUB_POP_BG    = theme.colors["background_dark"]
RED           = theme.colors["red"]

FONT = theme.font

res_x, res_y = get_current_resolution()
bar_size = floor(res_y/BAR_SIZE_RATIO)

POPUP_WIDTH = floor(res_x/5)
POPUP_HEIGHT = floor(res_y - bar_size - 3 * GAP)

# ── subpopup constants ───────────────────────────────────────────────────────────────
SUB_X_POS = 0.01
SUB_WIDTH=0.99
SUB_HEIGHT=0.06
FONT_SIZE=25

# ── global status ───────────────────────────────────────────────────────────────

_status = Status()
_popup  = None


# ── utils ────────────────────────────────────────────────────────

def _get_wifi_info() -> tuple[str, str]:
    try:
        ssid = subprocess.check_output(["iwgetid", "-r"], text=True).strip()
        quality = subprocess.check_output(
            ["bash", "-c", "awk 'NR==3{print int($3*100/70)\"%\"}' /proc/net/wireless"],
            text=True,
        ).strip()
        return ssid or "Non connecté", quality or "0%"
    except Exception:
        return "Non connecté", "0%"


def _is_wifi_enabled() -> bool:
    try:
        return subprocess.check_output(
            ["nmcli", "radio", "wifi"], text=True
        ).strip() == "enabled"
    except Exception:
        return False


# ── popup build ─────────────────────────────────────────────────────


def _open_nm_dmenu(qtile) -> None:
    subprocess.Popen(["networkmanager_dmenu"])


def _build_popup(qtile) -> PopupRelativeLayout:
    greeting_width = SUB_WIDTH*0.66

    controls = [
        # ── greeting ────────────────────────────────────────────
        PopupImage(
            filename=USER_IMAGE,
            pos_x=SUB_X_POS,
            pos_y=0.005,
            width=SUB_WIDTH*0.33,
            height=SUB_HEIGHT*2,
            highlight=None,
        ),

        PopupText(
            text=f"Bonjour, {USERNAME}",
            pos_x=1 - greeting_width,
            pos_y=0.005,
            font = FONT, 
            width=greeting_width,
            height=SUB_HEIGHT,
            h_align="center",
            fontsize=FONT_SIZE,
            foreground=TEXT_PRIMARY,
            background = SUB_POP_BG,
        ),
        # ── buttons  ──────────────────────────────────────────────────────
        PopupText(
            text="☠ Se Défenestrer ☠",
            pos_x=SUB_X_POS,
            pos_y=0.935,
            width=SUB_WIDTH,
            height=SUB_HEIGHT,
            h_align="center",
            fontsize=FONT_SIZE,
            font=FONT,
            foreground=RED,
            highlight=HIGHLIGHT,
            background = SUB_POP_BG,
            mouse_callbacks={"Button1": lazy.spawn(commands["shutdown"])},
        ),
    ]

    return PopupRelativeLayout(
        qtile,
        border_width=5,
        border=None,
        width=POPUP_WIDTH,
        height=POPUP_HEIGHT,
        controls=controls,
        background=BG_POPUP,
        close_on_click=True,
        initial_focus=None,
        hide_on_mouse_leave=True,
        hide_interval=0.2,
    )


# ── Callbacks ─────────────────────────────────────────────────────────────────

def _on_toggle_vpn(qtile) -> None:
    _status.vpn = not _status.vpn
    cmd = "sudo wg-quick up wg0" if _status.is_vpn_on() else "sudo wg-quick down wg0"
    subprocess.Popen(cmd.split())
    _status.save()
    _refresh_popup(qtile)


def _on_toggle_wifi(qtile) -> None:
    if _is_wifi_enabled():
        subprocess.Popen(["nmcli", "radio", "wifi", "off"])
    else:
        subprocess.Popen(["nmcli", "radio", "wifi", "on"])
    _refresh_popup(qtile)


def _refresh_popup(qtile) -> None:
    global _popup
    if _popup is not None:
        _popup.kill()
    _popup = _build_popup(qtile)
    _popup.show(relative_to=1, relative_to_bar=True)


# ── entry point ────────────────────────────────────────────────────────────

def show_home_popup(qtile) -> None:
    """
    Toggle : displays the popup if it is hidden, closes it if it is visible.
    We query popup.win.hidden directly instead of maintaining a flag
    — which remains correct even after an automatic hide (mouse leaves).
    """
    global _popup

    if _popup is not None:
        _popup.kill()

    _popup = _build_popup(qtile)
    _popup.show(relative_to=1, relative_to_bar=True)