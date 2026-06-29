from pathlib import Path
from datetime import datetime, timedelta, timezone
from configparser import RawConfigParser

from .constants import *
from qtile_extras.popup.toolkit import PopupText, PopupImage
from libqtile.lazy import lazy

from user_profile import ICONS_PATH, FAVORITES_APP
from modules.commands import commands

DESKTOP_PATH = Path("/usr/share/applications/")

POS_Y = SUB_GAP*6 + SUB_HEIGHT*9
WIDTH = SUB_WIDTH/len(FAVORITES_APP)
HEIGHT = SUB_HEIGHT*1.25


def read_desktop_entry(path: Path):
    parser = RawConfigParser()
    parser.optionxform = str
    parser.read(path, encoding="utf-8")
    if not parser.has_section("Desktop Entry"):
        return None, None
    section = parser["Desktop Entry"]
    return section.get("Exec"), section.get("Icon")

def init_other():
    return PopupText(
        text="...",
        pos_x=SUB_X_POS+ (len(FAVORITES_APP)-1) * WIDTH,
        pos_y=POS_Y + SUB_GAP/2,
        width=WIDTH,
        height=HEIGHT - SUB_GAP,
        highlight=HIGHLIGHT,
        background= SUB_POP_BG,
        fontsize=FONT_SIZE*1.5,
        font=FONT,
        h_align="center",
        mouse_callbacks={"Button1":lazy.spawn(commands["launcher"])}
    )

def get_popups():
    popups = []
    others = False

    for i, name in enumerate(FAVORITES_APP) :

        if name == "others":
            others = True
            continue

        path = DESKTOP_PATH / f"{name}.desktop"
        exec_cmd, icon = read_desktop_entry(path)

        popups.append(PopupImage(
            filename=f"{ICONS_PATH}/{icon}.svg",
            pos_x=SUB_X_POS+ i * WIDTH,
            pos_y=POS_Y + SUB_GAP/2,
            width=WIDTH,
            height=HEIGHT - SUB_GAP,
            background=SUB_POP_BG,
            highlight=HIGHLIGHT,
            mouse_callbacks = {"Button1": lazy.spawn(exec_cmd)},
        ))

    if others:
        popups.append(init_other())

    return popups




# ── Popups ───────────────────────────
def init_shortcuts_popups():
    return [
        PopupText(
            text="",
            pos_x=SUB_X_POS,
            pos_y=POS_Y,
            width=SUB_WIDTH,
            height=HEIGHT,
            highlight=None,
            background= SUB_POP_BG,
        ),

        *get_popups()
    ]