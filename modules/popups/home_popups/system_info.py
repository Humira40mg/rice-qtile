from .constants import *

import subprocess

from libqtile.lazy import lazy

import modules.popups.global_popups as root_pops

from modules.utils.system_utils import is_plugged_to_power

from modules.popups.commons.buttons import _make_stylish_text_button
from modules.commands import commands

# ── ICONS ───────────────────────────────────────────────────────
ICON_STORAGE = "󰨣"
ICON_PACKAGES = "󰏖"
ICON_RAM = ""
ICON_VRAM = "󰞐"

last_vram = "0%"

# ── utils ────────────────────────────────────────────────────────
def _get_vram_info():
    try:
        out = subprocess.run(commands["get_vram_usage"],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip()
        used, total = map(int, out.split(", "))
        return f"{used*100//total}%"
    except Exception:
        return "N/A"


def _get_ram_info():
    try:
        out = subprocess.run(commands["get_ram_usage"],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip()[:2]
        
        return f"{out}%"
    except Exception:
        return "N/A"

def _get_packages_info():
    try:
        out = subprocess.run(commands["get_number_of_packages"],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip()
        
        return out
    except Exception:
        return "N/A"

def _get_storage_info():
    try:
        out = subprocess.run(commands["get_stockage_info"],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip()
        
        return out
    except Exception:
        return "N/A"

def update_vram():
    if not root_pops.home or root_pops.home._killed : return

    global last_vram

    last_vram = _get_vram_info()
    root_pops.home.update_controls(
        vram_usage=last_vram
        )

# ── Popups ───────────────────────────
def init_system_info_popups(qtile):

    global last_vram

    if is_plugged_to_power():
        last_vram = _get_vram_info()
    else:
        qtile.call_later(0.2, qtile.run_in_executor, update_vram)

    return [
        *_make_stylish_text_button(
            name="vram_usage",
            icon= ICON_VRAM,
            icon_color=GREEN,
            text=last_vram,
            pos_x=SUB_X_POS*2 + SUB_WIDTH*0.33,
            pos_y=SUB_GAP*2 + SUB_HEIGHT,
            width=SUB_WIDTH*0.3,
            height=SUB_HEIGHT - SUB_GAP,
            fontsize=FONT_SIZE*0.75,
            foreground_color=TEXT_PRIMARY,
            highlight_color=GREEN,
            background_color=GREEN,
            mouse_callbacks={
                "Button1": lazy.spawn(commands["btop"])
                },
            ),
        *_make_stylish_text_button(
            icon= ICON_RAM,
            icon_color=GREEN,
            text=_get_ram_info(),
            pos_x=SUB_X_POS*3 + SUB_WIDTH*0.66,
            pos_y=SUB_GAP*2 + SUB_HEIGHT,
            width=SUB_WIDTH*0.3,
            height=SUB_HEIGHT - SUB_GAP,
            fontsize=FONT_SIZE*0.75,
            foreground_color=TEXT_PRIMARY,
            highlight_color=GREEN,
            background_color=GREEN,
            mouse_callbacks={
                "Button1": lazy.spawn(commands["btop"])
                },
            ),
        *_make_stylish_text_button(
            icon= ICON_PACKAGES,
            icon_color=BLUE,
            text=_get_packages_info(),
            pos_x=SUB_X_POS*2 + SUB_WIDTH*0.33,
            pos_y=SUB_GAP*2 + SUB_HEIGHT*2,
            width=SUB_WIDTH*0.3,
            height=SUB_HEIGHT - SUB_GAP,
            fontsize=FONT_SIZE*0.75,
            foreground_color=TEXT_PRIMARY,
            highlight_color=BLUE,
            background_color=BLUE,
            mouse_callbacks={
                "Button1": lazy.spawn(commands["update"])
                },
            ),
        *_make_stylish_text_button(
            icon= ICON_STORAGE,
            icon_color=BLUE,
            text=_get_storage_info(),
            pos_x=SUB_X_POS*3 + SUB_WIDTH*0.66,
            pos_y=SUB_GAP*2 + SUB_HEIGHT*2,
            width=SUB_WIDTH*0.3,
            height=SUB_HEIGHT - SUB_GAP,
            fontsize=FONT_SIZE*0.75,
            foreground_color=TEXT_PRIMARY,
            highlight_color=BLUE,
            background_color=BLUE,
            mouse_callbacks={
                "Button1": lazy.spawn(commands["clean"])
                },
            ),
        ]