from libqtile import hook
from pathlib import Path
import subprocess

from user_profile import theme

import modules.status_reader as sr

from modules.commands import commands

HOME = Path.home()
status = sr.Status()

def init_hooks():
    @hook.subscribe.startup_once
    def autostart():
        subprocess.Popen(["systemctl", "--user", "import-environment", "DISPLAY", "XAUTHORITY", "XDG_CURRENT_DESKTOP", "WAYLAND_DISPLAY"])
        subprocess.run(["systemctl", "--user", "start", "qtile-session.target"])
        subprocess.Popen(["picom", "--config", f"{HOME}/.config/picom/picom.conf"])
        subprocess.Popen(["dunst"]) # notif server

        subprocess.Popen(["betterlockscreen", "-u", f"{theme.wallpaper}"])

        if status.is_vpn_on():
            subprocess.Popen(["bash", "-c", commands["vpn_on"]])