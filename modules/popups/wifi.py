"""
wifi_popup.py
Popup Qtile for WiFi and VPN management.
"""
import subprocess
from math import floor

from qtile_extras.popup.toolkit import PopupImage, PopupRelativeLayout, PopupText
from libqtile.lazy import lazy
from pathlib import Path

from modules.status_reader import Status
from user_profile import theme, GAP

from .commons.buttons import _make_icon_button
from modules.utils.system_utils import get_current_resolution
from modules.commands import commands

# ── colors ───────────────────────────────────────────────────────────────────

BG_POPUP      = theme.colors["background_dark"]
TEXT_PRIMARY  = theme.colors["white"]
TEXT_MUTED    = theme.colors["grey"]
HIGHLIGHT     = theme.colors["background"]
ON_COLOR         = theme.colors["green"]

FONT = theme.font

HOME = Path.home()

ICON_WIFI = f"{HOME}/.config/qtile/assets/icons/usefull/wifi.png"
ICON_VPN  = f"{HOME}/.config/qtile/assets/icons/usefull/vpn.png"

res_x, res_y = get_current_resolution()

POPUP_WIDTH  = floor(res_x/6)
POPUP_HEIGHT = floor(res_y/5)

# ── global status ───────────────────────────────────────────────────────────────

_status = Status()
_popup  = None

# ── network utils ────────────────────────────────────────────────────────

def _get_wifi_info() -> tuple[str, str]:
    try:
        ssid = subprocess.check_output(["iwgetid", "-r"], text=True).strip()
        quality = subprocess.check_output(
            commands["get_wifi_info"],
            text=True,
        ).strip()
        return ssid or "Non connecté", quality or "0%"
    except Exception:
        return "Non connecté", "0%"


def _is_wifi_enabled() -> bool:
    try:
        return subprocess.check_output(
            commands["is_wifi_on"], text=True
        ).strip() == "enabled"
    except Exception:
        return False


# ── popup build ─────────────────────────────────────────────────────


def _open_nm_dmenu(qtile) -> None:
    subprocess.Popen(commands["show_wifi_cli"])


def _build_popup(qtile) -> PopupRelativeLayout:
    ssid, quality = _get_wifi_info()
    wifi_on       = _is_wifi_enabled()
    vpn_on        = _status.is_vpn_on()

    controls = [
        # ── SSID cliquable → networkmanager_dmenu ────────────────────────
        PopupText(
            text=ssid,
            pos_x=0.05,
            pos_y=0.04,
            width=0.90,
            height=0.18,
            h_align="center",
            fontsize=15,
            font=FONT,
            foreground=TEXT_PRIMARY,
            highlight=HIGHLIGHT,
            mouse_callbacks={"Button1": lazy.function(_open_nm_dmenu)},
        ),
        # ── Qualité du signal ────────────────────────────────────────────
        PopupText(
            text=quality,
            pos_x=0.05,
            pos_y=0.22,
            font = FONT, 
            width=0.90,
            height=0.12,
            h_align="center",
            fontsize=11,
            foreground=TEXT_MUTED,
        ),
        # ── Boutons ──────────────────────────────────────────────────────
        *_make_icon_button(
            icon_path=ICON_WIFI,
            label="WiFi",
            pos_x=0.05,
            is_on=wifi_on,
            on_color=ON_COLOR,
            textprimary_color=TEXT_PRIMARY,
            textmuted_color=TEXT_MUTED,
            highlight_color=HIGHLIGHT,
            font_familly=FONT,
            callback=lazy.function(_on_toggle_wifi),
        ),
        *_make_icon_button(
            icon_path=ICON_VPN,
            label="VPN",
            pos_x=0.55,
            is_on=vpn_on,
            on_color=ON_COLOR,
            textprimary_color=TEXT_PRIMARY,
            textmuted_color=TEXT_MUTED,
            highlight_color=HIGHLIGHT,
            font_familly=FONT,
            callback=lazy.function(_on_toggle_vpn),
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
    cmd = commands["vpn_on"] if _status.is_vpn_on() else commands["vpn_off"]
    subprocess.Popen(cmd.split())
    _status.save()
    _refresh_popup(qtile)


def _on_toggle_wifi(qtile) -> None:
    if _is_wifi_enabled():
        subprocess.Popen(commands["wifi_off"])
    else:
        subprocess.Popen(commands["wifi_off"])
    _refresh_popup(qtile)


def _refresh_popup(qtile) -> None:
    global _popup
    if _popup is not None:
        _popup.kill()
    _popup = _build_popup(qtile)
    _popup.show(relative_to=3, relative_to_bar=True, x=(GAP*-2))


# ── entry point ────────────────────────────────────────────────────────────

def show_wifi_popup(qtile) -> None:
    """
    Toggle : displays the popup if it is hidden, closes it if it is visible.
    We query popup.win.hidden directly instead of maintaining a flag
    — which remains correct even after an automatic hide (mouse leaves).
    """
    global _popup

    if _popup is not None:
        _popup.kill()

    _popup = _build_popup(qtile)
    _popup.show(relative_to=3, relative_to_bar=True, x=(GAP*-2))