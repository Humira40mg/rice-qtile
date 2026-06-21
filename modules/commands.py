commands={
    "shutdown":"shutdown now",
    "show_wifi_cli": "networkmanager_dmenu",
    "get_wifi_info":["bash", "-c", "awk 'NR==3{print int($3*100/70)\"%\"}' /proc/net/wireless"],
    "is_wifi_on":["nmcli", "radio", "wifi"],
    "wifi_on":["nmcli", "radio", "wifi", "on"],
    "wifi_off":["nmcli", "radio", "wifi", "off"],
    "vpn_on":"sudo wg-quick up wg0",
    "vpn_off":"sudo wg-quick down wg0",
}