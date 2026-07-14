from math import floor

from libqtile import bar, qtile
from libqtile.lazy import lazy

from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

from user_profile import (
    GAP, 
    theme, 
    BAR_SIZE_RATIO,
    )

from modules.widgets.GifImage import GifImage
from modules.widgets.WindowControls import WindowControls

from modules.popups.wifi import show_wifi_popup
from modules.popups.home import show_home_popup
from modules.popups.systray import show_systray_popup
from modules.utils.system_utils import get_current_resolution
from modules.commands import commands

powerline = {
    "decorations": [
        PowerLineDecoration(path="back_slash")  # arrow_right, rounded, slash, back_slash
    ]
}

_, res_y = get_current_resolution()
BAR_SIZE = floor(res_y/BAR_SIZE_RATIO)

topbar = bar.Bar(
            [
                GifImage(
                    filename=theme.home_icon,
                    frame_interval=0.04/theme.icon_speed_ratio,
                    margin=GAP,
                    mouse_callbacks={
                        "Button1": lazy.function(show_home_popup), # lambda: qtile.spawn("rofi -show drun"),
                    },
                    **powerline,
                ),
                
                widget.GroupBox(
                    active=theme.colors["white"],         
                    inactive=theme.colors["grey"],         
                    highlight_method="line",      
                    this_current_screen_border=theme.colors["selected"],   
                    block_highlight_text_color=theme.colors["selected"],
                    rounded=True,
                    disable_drag=True,
                    padding = 10,
                    background = theme.colors["background_dark"],
                    **powerline,
                ),
                widget.Prompt(),
                # widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": (theme.colors["red"], theme.colors["white"]),
                    },
                    name_transform=lambda name: name.upper(),
                ),

                widget.Spacer(),
                widget.Clock(format="%H:%M"),
                widget.Spacer(**powerline),

                WindowControls(
                    max_color=theme.colors["green"],
                    float_color=theme.colors["yellow"],
                    close_color=theme.colors["red"], 
                ),
                widget.Spacer(
                    length=1,
                    **powerline,
                ),
                widget.WiFiIcon(
                    background= theme.colors["background_dark"],
                    mouse_callbacks={"Button1": lazy.function(show_wifi_popup)},
                    show_ssid=False,
                    padding=10,
                    **powerline,
                ),     

                widget.TextBox(
                    text="󰂯",
                    fontsize=25,
                    background= theme.colors["background"],
                    mouse_callbacks={"Button1": lazy.spawn(commands["bluetooth"])},
                    **powerline,
                ),

                # widget.Systray(),
                widget.Battery(
                    charge_char="󰂄",
                    discharge_char="󱟞",
                    empty_char="󱟥",
                    full_char="󰁹",
                    not_charging_char="󱉞",
                    unknown_char="󱟩",
                    update_interval=30,
                    show_short_text=False,
                    background=theme.colors["background_light"],
                    low_foreground=theme.colors["really_red"],
                    low_percentage=0.20,
                    format="{char} {percent:2.0%}",
                    mouse_callbacks={"Button1": lazy.function(show_systray_popup)},
                    padding=10,
                ),
            ],
            40,
            margin=[GAP, GAP, 0, GAP],
            background=theme.colors["background_darkest"],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        )
    