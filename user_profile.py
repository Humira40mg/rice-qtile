from modules.theme_reader import Theme
from dotenv import load_dotenv
from modules.web_scrap.discord_scrapper import get_discord_info
from os import environ

load_dotenv()
DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
discordname, discordavatarurl = get_discord_info(DISCORD_TOKEN)


USER_IMAGE = discordavatarurl or "assets/images/linux_logo.png"

mod = "mod4"
TERMINAL = "alacritty"
FOLDER_BROWSER = "nautilus --new-window"
WEB_BROWSER = "firefox"

USERNAME = discordname or "JoKSo"

theme = Theme("heliocentrisme.yml")

# ─────────────|Basic settings|──────────────────────────────────────────────
GAP = 5
BAR_SIZE_RATIO = 27 # 1/27 ratio of the screen height
