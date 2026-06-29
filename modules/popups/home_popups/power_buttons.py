from .constants import *

from libqtile.lazy import lazy

from modules.popups.commons.buttons import _make_basic_text_button
from modules.commands import commands

LOCK_WIDTH = SUB_WIDTH * 0.33 - SUB_X_POS/2
REBOOT_WIDTH = SUB_WIDTH * 0.66

# ── Popups ───────────────────────────
def init_power_buttons():
    return [
        *_make_basic_text_button(
            text="",
            pos_x=SUB_X_POS,
            pos_y= 1 - SUB_HEIGHT*2 - SUB_GAP*2,
            width=LOCK_WIDTH,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground_color=GREEN,
            highlight_color=HIGHLIGHT,
            background_color= SUB_POP_BG,
            mouse_callbacks={"Button1": lazy.spawn(commands["lock"])},
        ),
        *_make_basic_text_button(
            text="✟ Réssusciter ✟", #LANGUAGE
            pos_x=SUB_X_POS*2 + LOCK_WIDTH,
            pos_y= 1 - SUB_HEIGHT*2 - SUB_GAP*2,
            width=REBOOT_WIDTH,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground_color=YELLOW,
            highlight_color=HIGHLIGHT,
            background_color= SUB_POP_BG,
            mouse_callbacks={"Button1": lazy.spawn(commands["reboot"])},
        ),
        *_make_basic_text_button(
            text="󱓇  Se Défenestrer  󱓇", #LANGUAGE
            pos_x=SUB_X_POS,
            pos_y= 1 - SUB_HEIGHT - SUB_GAP,
            width=SUB_WIDTH,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground_color=REALLY_RED,
            highlight_color=HIGHLIGHT,
            background_color= SUB_POP_BG,
            mouse_callbacks={"Button1": lazy.spawn(commands["shutdown"])},
        ),
    ]