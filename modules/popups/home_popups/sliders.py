from random import choice

from libqtile.lazy import lazy

from modules.popups.commons.fixedPopups import PopupSliderFixed
from qtile_extras.popup.toolkit import PopupText
from modules.popups.commons.buttons import _make_basic_text_button

import subprocess

from modules.commands import commands

from .constants import *
import modules.popups.global_popups as root_pops

ICON_VOLUME_ON = "󰕾"
ICON_VOLUME_OFF = "󰖁"
ICON_BRIGHTNESS_ON = "󰃠 "
ICON_BRIGHTNESS_OFF = "󰃞 "

WIDTH = SUB_WIDTH*0.33/2 - SUB_GAP*1.5
POS_X = SUB_X_POS
POS_Y = SUB_GAP*4 + SUB_HEIGHT*4

# common functions
def set_value(what, val):
    try:
        subprocess.run(["bash", "-c", commands[what]["set"].format(val)])
    except Exception:
        pass  

# ===================== BRIGHTNESS =========================================================
def get_max_brightness():
    try:
        out = subprocess.run(["bash", "-c", commands["brightness"]["max"]],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip()
        return int(out)
    except Exception:
        return 96000

MAX_BRIGHTNESS = get_max_brightness()


# FUNCTIONS
def get_current_brightness():
    try:
        out = int(subprocess.run(["bash", "-c", commands["brightness"]["get"]],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip())
        return value_to_percent(out)
    except Exception:
        return 100

def percent_to_value(percent):
    return int(percent * MAX_BRIGHTNESS / 100)

def value_to_percent(value):
    return int(value * 100 / MAX_BRIGHTNESS)

def on_drag_brightness(new_value):

    val = percent_to_value(int(new_value))
    set_value("brightness", val)
    root_pops.home.update_controls(brightness_text=f"{int(new_value)}%")

    if new_value == 0:
        root_pops.home.update_controls(brightness_button=ICON_BRIGHTNESS_OFF)
    else:
        root_pops.home.update_controls(brightness_button=ICON_BRIGHTNESS_ON)


# button
def no_brightness():
    set_value("brightness", 0)
    root_pops.home.update_controls(brightness_slider=0, brightness_button=ICON_BRIGHTNESS_OFF, brightness_text="0%")



# ===================== VOLUME =========================================================

# FUNCTIONS
def get_current_volume():
    try:
        out = int(subprocess.run(["bash", "-c", commands["volume"]["get"]],
            capture_output=True, text=True, timeout=0.5
        ).stdout.strip().replace("%", ""))
        return out
    except Exception:
        return 100    

def on_drag_volume(new_value):

    set_value("volume", new_value)
    root_pops.home.update_controls(volume_text=f"{int(new_value)}%")

    if new_value == 0:
        root_pops.home.update_controls(volume_button=ICON_VOLUME_OFF)
    else:
        root_pops.home.update_controls(volume_button=ICON_VOLUME_ON)

# button
def mute():
    set_value("volume", 0)
    root_pops.home.update_controls(volume_slider=0, volume_button=ICON_VOLUME_OFF, volume_text="0%")



# ===================== POPUPS ==================================================================
def init_slider_popups():
    current_brightness = get_current_brightness()
    bright_icon = ICON_BRIGHTNESS_ON
    if current_brightness == 0 :
        bright_icon = ICON_BRIGHTNESS_OFF
    
    current_volume = get_current_volume()
    vol_icon = ICON_VOLUME_ON
    if current_volume == 0 :
        vol_icon = ICON_VOLUME_OFF
    
    return [
        # brightness %
        PopupText(
            name="brightness_text",
            text=f"{current_brightness}%",
            pos_x=POS_X,
            pos_y=POS_Y + SUB_HEIGHT*3.5+SUB_GAP/2,
            width=WIDTH,
            height=SUB_HEIGHT/2.5,
            fontsize=FONT_SIZE/2,
            font=FONT,
            h_align="center",
            foreground_color=TEXT_MUTED,
        ),

        # brightness slider
        PopupSliderFixed(
            name="brightness_slider",
            value=current_brightness,                  
            min_value=0,
            max_value=100,
            horizontal=False,          
            pos_x=POS_X,
            pos_y=POS_Y,
            width=WIDTH,
            height=SUB_HEIGHT*3.5,
            bar_size=10,
            end_margin=0,
            colour_below=SELECTED,   
            colour_above=SUB_POP_BG,  
            marker_colour=TEXT_PRIMARY,
            marker_size=18,
            drag_callback=on_drag_brightness,
        ),

        # brightness button
        *_make_basic_text_button(
            name="brightness_button",
            text=bright_icon,
            pos_x=POS_X,
            pos_y=POS_Y + SUB_HEIGHT*4 + SUB_GAP,
            width=WIDTH,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground_color=TEXT_PRIMARY,
            highlight_color=HIGHLIGHT,
            background_color= SUB_POP_BG,
            mouse_callbacks={"Button1": no_brightness},
        ),
        
        # volume %
        PopupText(
            name="volume_text",
            text=f"{current_volume}%",
            pos_x=POS_X + WIDTH + SUB_X_POS,
            pos_y=POS_Y + SUB_HEIGHT*3.5+SUB_GAP/2,
            width=WIDTH,
            height=SUB_HEIGHT/2.5,
            fontsize=FONT_SIZE/2,
            font=FONT,
            h_align="center",
            foreground_color=TEXT_MUTED,
        ),

        # volume
        PopupSliderFixed(
            name="volume_slider",
            value=current_volume,                  
            min_value=0,
            max_value=100,
            horizontal=False,          
            pos_x=POS_X + WIDTH + SUB_X_POS,
            pos_y=POS_Y,
            width=WIDTH,
            height=SUB_HEIGHT*3.5,
            bar_size=10,
            end_margin=0,
            colour_below=SELECTED,   
            colour_above=SUB_POP_BG,  
            marker_colour=TEXT_PRIMARY,
            marker_size=18,
            drag_callback=on_drag_volume,
        ),

        # volume button
        *_make_basic_text_button(
            name="volume_button",
            text=vol_icon,
            pos_x=POS_X + WIDTH + SUB_X_POS,
            pos_y=POS_Y + SUB_HEIGHT*4 + SUB_GAP,
            width=WIDTH,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground_color=TEXT_PRIMARY,
            highlight_color=HIGHLIGHT,
            background_color= SUB_POP_BG,
            mouse_callbacks={"Button1": mute},
        ),
    ]