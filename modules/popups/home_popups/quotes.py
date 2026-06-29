from pathlib import Path
from datetime import datetime, timedelta, timezone
from configparser import RawConfigParser

from .constants import *
from qtile_extras.popup.toolkit import PopupText, PopupImage
from libqtile.lazy import lazy

from user_profile import QUOTES_PATH
from modules.commands import commands

from random import choice

POS_X = SUB_X_POS
POS_Y = SUB_GAP*7 + SUB_HEIGHT*10.25
WIDTH = SUB_WIDTH*0.75 - SUB_X_POS
HEIGHT = SUB_HEIGHT*2.75

def get_quote():
    with open(QUOTES_PATH) as file:
        return choice(file.readlines()).split(" - ")


# ── Popups ───────────────────────────
def init_quotes_popup():
    quote, author = get_quote()
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
        PopupText(
            text=f"<i>{quote}</i>",
            pos_x=POS_X*2,
            pos_y=POS_Y+SUB_GAP,
            width=WIDTH-POS_X*2,
            height=HEIGHT - SUB_GAP*2,
            highlight=None,
            background= SUB_POP_BG,
            font=FONT,
            fontsize=FONT_SIZE*0.75,
            foreground=TEXT_PRIMARY,
            markup=True,
            wrap=True,
            mouse_callbacks = {"Button1":lazy.spawn(commands["open_quotes"])}
        ),
        PopupText(
            text=f" - {author}",
            pos_x=POS_X,
            pos_y=POS_Y+HEIGHT*0.75+SUB_GAP,
            width=WIDTH-POS_X*2,
            height=HEIGHT*0.25 - SUB_GAP*2,
            highlight=None,
            background= SUB_POP_BG,
            font=FONT,
            fontsize=FONT_SIZE*0.75,
            foreground=TEXT_MUTED,
            h_align = "right",
        )
    ]