
import subprocess

from modules.commands import commands
from modules.utils.download_image import download_image
from libqtile.lazy import lazy

from qtile_extras.popup.toolkit import PopupText, PopupImage
from .constants import *

from pathlib import Path

from modules.popups.commons.buttons import _make_basic_text_button
import modules.popups.global_popups as root_pops

from threading import Thread


HOME = Path.home()

WIDTH = SUB_WIDTH*0.66
POS_X = 1-SUB_X_POS - WIDTH
POS_Y = SUB_GAP*4 + SUB_HEIGHT*4

LOADING_IMAGE = f"{HOME}/.config/qtile/assets/icons/loading.png"

# ── icons ───────────────────────────────
PLAY_ICON   = "▶"
PAUSE_ICON  = "⏸"
STOP_ICON   = "⏹"
NEXT_ICON   = "⏭"
PREV_ICON   = "⏮"

# ── functions ───────────────────────────

def is_media_found(status):
    return status != ""

def is_media_playing(status):
    return status == "Playing"

def get_player_icon(status):
    if not is_media_found(status):
        return STOP_ICON
    elif is_media_playing(status):
        return PAUSE_ICON
    else:
        return PLAY_ICON 

def get_media_status():
    try:
        out = subprocess.run(["bash", "-c", commands["player_control"]["status"]],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip()
        return out
    except Exception:
        return ""

def get_media_metadata():
    try:
        out = subprocess.run(["bash", "-c", commands["player_control"]["metadata"]],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip()
        # The output is structured like "Title || Artist || ImagePath" or similar separators
        parts = out.split(" || ")
        
        title = parts[0] if len(parts) > 0 else ""
        artist = parts[1] if len(parts) > 1 else ""
        media_image = parts[2] if len(parts) > 2 else None

        if media_image and media_image.startswith("file"):
            media_image = media_image[8:]
        
        return title, artist, media_image
    except Exception:
        return "", "", None

def get_title_artist_popups(title, artist):
    return [
    # ── Title ────────────────────────────────────────────
        PopupText(
            name="playerctl_title",
            text=title,
            pos_x=POS_X,
            pos_y=POS_Y + SUB_HEIGHT*3,
            font = FONT, 
            width=WIDTH,
            height=SUB_HEIGHT*0.5,
            h_align="center",
            fontsize=FONT_SIZE*0.75,
            foreground=TEXT_PRIMARY,
            highlight=None,
            background=SUB_POP_BG,
        ),
        # ── Artist ────────────────────────────────────────────
        PopupText(
            name="playerctl_artist",
            text=artist,
            pos_x=POS_X,
            pos_y=POS_Y + SUB_HEIGHT*3.5,
            font = FONT, 
            width=WIDTH,
            height=SUB_HEIGHT/2,
            h_align="center",
            fontsize=FONT_SIZE/2,
            foreground=TEXT_MUTED,
            highlight=None,
            background=SUB_POP_BG,
        )
    ]

def show_image_popup(status):
    if not is_media_found(status):
        return get_title_artist_popups("Rien en lecture", "Aucun Media"), None #LANGUAGE

    title, artist, media_image = get_media_metadata()

    if not media_image or (not media_image.startswith("/home") and not media_image.startswith("https")): 
        return get_title_artist_popups(title, artist), None

    return [
        PopupImage(
            name="playerctl_image",
            filename=LOADING_IMAGE,
            pos_x=POS_X + SUB_X_POS,
            pos_y=POS_Y + SUB_GAP,
            width=WIDTH - SUB_X_POS*2,
            height=SUB_HEIGHT*3 - SUB_GAP,
            highlight=None,
            background=SUB_POP_BG
        ),
        *get_title_artist_popups(title, artist),
        ], media_image

def refresh_player_info():
    if not root_pops.home or root_pops.home._killed : return

    title, artist, media_image = get_media_metadata()

    root_pops.home.update_controls(
        playerctl_image=LOADING_IMAGE, 
        playerctl_title=title, 
        playerctl_artist=artist,
        )
    update_image(media_image)

def update_image(image):
    if not root_pops.home or root_pops.home._killed : return

    root_pops.home.update_controls(
        playerctl_image=image
        )

def play_pause_handler(qtile):
    subprocess.run(["bash", "-c", commands["player_control"]["play"]])

    def update_button():
        if not root_pops.home or root_pops.home._killed : return

        status = get_media_status()
        root_pops.home.update_controls(
            playerctl_play_pause=get_player_icon(status)
        )

    qtile.call_later(0.2, update_button)

def handler(qtile, command):
    subprocess.run(["bash", "-c", command])
    qtile.call_later(0.2, qtile.run_in_executor, refresh_player_info)


# ── Popups ───────────────────────────
def init_player_control_popups(qtile):
    status = get_media_status()
    image_popups, image = show_image_popup(status)

    if image:
        qtile.call_later(0.2, qtile.run_in_executor, update_image, image)

    return [
        #background
        PopupText(
            text="",
            pos_x=POS_X,
            pos_y=POS_Y,
            width=WIDTH,
            height=SUB_HEIGHT*4,
            background=SUB_POP_BG,
        ),
        
        #image
        *image_popups,

        # play/pause
        *_make_basic_text_button(
            name="playerctl_play_pause",
            text=get_player_icon(status),
            pos_x=POS_X +( WIDTH/5 *2),
            pos_y=POS_Y + SUB_HEIGHT*4 + SUB_GAP,
            width=WIDTH/5,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground_color=TEXT_PRIMARY,
            highlight_color = HIGHLIGHT,
            background_color=SUB_POP_BG,
            mouse_callbacks={
                "Button1": lazy.function(play_pause_handler)
            },
        ),

        # next
        *_make_basic_text_button(
            text=NEXT_ICON,
            pos_x=POS_X +( WIDTH/5 *3) + SUB_X_POS,
            pos_y=POS_Y + SUB_HEIGHT*4 + SUB_GAP,
            width=WIDTH/5 *2 - SUB_X_POS,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground_color=TEXT_PRIMARY,
            highlight_color = HIGHLIGHT,
            background_color=SUB_POP_BG,
            mouse_callbacks={
                "Button1": lazy.function(handler, commands["player_control"]["next"])
            },
        ),

        # previous
        *_make_basic_text_button(
            text=PREV_ICON,
            pos_x=POS_X,
            pos_y=POS_Y + SUB_HEIGHT*4 + SUB_GAP,
            width=WIDTH/5 *2 - SUB_X_POS,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground_color=TEXT_PRIMARY,
            highlight_color = HIGHLIGHT,
            background_color=SUB_POP_BG,
            mouse_callbacks={
                "Button1": lazy.function(handler, commands["player_control"]["previous"])
            },
        ),
    ]