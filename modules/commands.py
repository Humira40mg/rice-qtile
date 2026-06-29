from user_profile import TERMINAL, TEXT_EDITOR, QUOTES_PATH

commands={
    "shutdown":"shutdown now",
    "reboot":"reboot",
    "lock":"betterlockscreen -l blur",

    "screenshot": "flameshot gui",

    "bluetooth":"blueman-manager", 

    "launcher":"rofi -show drun",

    "show_wifi_cli": f"{TERMINAL} --class NetworkManager -e bash -c 'nmtui'",
    "get_wifi_info":["bash", "-c", "awk 'NR==3{print int($3*100/70)\"%\"}' /proc/net/wireless"],
    "is_wifi_on":["nmcli", "radio", "wifi"],
    "wifi_on":["nmcli", "radio", "wifi", "on"],
    "wifi_off":["nmcli", "radio", "wifi", "off"],

    "vpn_on":"sudo wg-quick up wg0",
    "vpn_off":"sudo wg-quick down wg0", 

    "get_stockage_info": ["bash", "-c", "df -h --total | tail -n 1 | awk '{print $3 \"/\" $4}'"],
    "get_number_of_packages": ["bash", "-c", "pacman -Q | wc -l"],
    "get_vram_usage":  ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"],
    "get_ram_usage": ["bash", "-c", "free -m | awk 'NR==2 {printf $3*100/$2}'"],

    "btop":f"{TERMINAL} --class btop -e btop",
    "clean":f"{TERMINAL} -e bash -c 'sudo clean; echo; read -p \"Terminé...\"'", # custom script
    "update":f"{TERMINAL} -e bash -c 'yay -Syu && flatpak update; echo; read -p \"Terminé...\"'",

    "open_quotes":f"{TEXT_EDITOR} {QUOTES_PATH}",


    # ── Player Controller ───────────────────────
    "player_control": {
        "play": "playerctl play-pause",
        "next": "playerctl next",
        "previous": "playerctl previous",
        "status": "playerctl status",
        "metadata": "playerctl metadata --format '{{title}} || {{artist}} || {{mpris:artUrl}}'",
    },

    # ── Brightness ───────────────────────
    "brightness": {
        "max": "brightnessctl max",
        "get": "brightnessctl get",
        "set": "brightnessctl set {}",
        "down": "brightnessctl set 10%-",
        "up": "brightnessctl set +10%",
    },

    "volume": {
        "get":"pactl get-sink-volume @DEFAULT_SINK@ | awk '{print $5}'",
        "mute":"pactl set-sink-volume @DEFAULT_SINK@ 0%",
        "set":"pactl set-sink-volume @DEFAULT_SINK@ {}%",
        "down":"pactl set-sink-volume @DEFAULT_SINK@ -5%",
        "up":"pactl set-sink-volume @DEFAULT_SINK@ +5%",
    }
}