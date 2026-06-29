from pathlib import Path
from datetime import datetime, timedelta, timezone
from configparser import RawConfigParser

from .constants import *
from qtile_extras.popup.toolkit import PopupText, PopupImage
from libqtile.lazy import lazy

from user_profile import CUSTOM_BUTTON
from modules.commands import commands

POS_X = SUB_X_POS + SUB_WIDTH*0.75
POS_Y = SUB_GAP*7 + SUB_HEIGHT*10.25
WIDTH = SUB_WIDTH*0.25
HEIGHT = SUB_HEIGHT*2.75

BUTTON_HEIGHT = HEIGHT/len(CUSTOM_BUTTON)

def get_popups():
    popups = []
    for i, button in enumerate(CUSTOM_BUTTON) :
        exec_cmd, icon = button["command"], button["icon"]
        popups.append(PopupImage(
            filename=icon,
            pos_x=POS_X + SUB_X_POS,
            pos_y=POS_Y + SUB_GAP + BUTTON_HEIGHT*i,
            width=WIDTH - SUB_X_POS*2,
            height=BUTTON_HEIGHT - SUB_GAP*2,
            background=SUB_POP_BG,
            highlight=HIGHLIGHT,
            mouse_callbacks = {"Button1": lazy.spawn(exec_cmd)},
        ))
    return popups




# ── Popups ───────────────────────────
def init_custom_shortcuts_popups():
    return [
        PopupText(
            text="",
            pos_x=POS_X,
            pos_y=POS_Y,
            width=WIDTH,
            height=HEIGHT,
            highlight=None,
            background= SUB_POP_BG,
        ),

        *get_popups()
    ]