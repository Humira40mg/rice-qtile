from os import path
import yaml

class Theme :
    def __init__(self, theme_name) -> None :
        self.name = theme_name.split(".")[0].capitalize()
        self.path = path.expanduser(f"~/.config/qtile/themes/{theme_name}")
        
        with open(self.path) as f:
            data = yaml.safe_load(f)
        
        self.wallpaper = path.expanduser(data["wallpaper"])
        self.home_icon = path.expanduser(data["home_icon"])
        self.fallback_image = path.expanduser(data["fallback_image"])

        self.colors = data["colors"]

        self.font = data["font"]
