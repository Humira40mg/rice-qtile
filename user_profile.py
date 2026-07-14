from modules.theme_reader import Theme
from dotenv import load_dotenv
from modules.apis.discord_api import get_discord_info
from os import environ, path, listdir
import random

def get_random_theme(theme_dir="~/.config/qtile/themes"):
    theme_dir_path = path.expanduser(theme_dir)

    files = [f for f in listdir(theme_dir_path) if path.isfile(path.join(theme_dir_path, f))]
    
    if not files or len(files) == 0:
        return "heliocentrisme.yml" 
    
    return random.choice(files)

# ====================================
theme =  Theme(get_random_theme()) #Theme("heliocentrisme.yml")
# ====================================

load_dotenv()
DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
discordname, discordavatarurl = get_discord_info(DISCORD_TOKEN)

mod = "mod4"
TERMINAL = "alacritty"
FOLDER_BROWSER = "nautilus --new-window"
WEB_BROWSER = "firefox"
TEXT_EDITOR = "gedit"

USER_IMAGE = discordavatarurl or "assets/images/linux_logo.png"
USERNAME = discordname or "JoKSo"

# names of desktop files in /usr/share/applications/
FAVORITES_APP = ["spotify", "discord", "vscodium", "org.kde.kdenlive", "others"] # others = show all apps
ICONS_PATH = path.expanduser("~/.icons/Papirus/32x32/apps/")

CUSTOM_BUTTON = [{
        "icon":path.expanduser("~/.config/qtile/assets/icons/odysseus.svg"),
        "command":"chromium --app=http://localhost:7000"
    },
    {
        "icon":path.expanduser("~/.config/qtile/assets/icons/roblox_studio.svg"),
        "command":"flatpak run org.vinegarhq.Vinegar"
    }
]

QUOTES_PATH = path.expanduser("~/.config/qtile/quotes.txt")

# ─────────────| Basic settings |──────────────────────────────────────────────
GAP = 5
BAR_SIZE_RATIO = 27 # 1/27 ratio of the screen height
