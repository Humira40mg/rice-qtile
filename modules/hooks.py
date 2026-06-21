from libqtile import hook
from pathlib import Path
import subprocess

HOME = Path.home()

def init_hooks():
    @hook.subscribe.startup_once
    def autostart():
        subprocess.Popen(["systemctl", "--user", "import-environment", "DISPLAY", "XAUTHORITY", "XDG_CURRENT_DESKTOP", "WAYLAND_DISPLAY"])
        subprocess.run(["systemctl", "--user", "start", "qtile-session.target"])
        subprocess.Popen(["picom", "--config", f"{HOME}/.config/picom/picom.conf"])
        subprocess.Popen(["dunst"]) # notif server