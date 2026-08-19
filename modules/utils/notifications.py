from dataclasses import dataclass
from os import path
from pathlib import Path
from string import Template
#from subprocess import CalledProcessError, run

DEFAULT_DUNSTRC_PATH = path.expanduser("~/.config/dunst/dunstrc")

_DUNSTRC_TEMPLATE = Template(
    """\
[global]
    width = (300, 400)
    height = 300
    origin = top-right
    offset = 10x50
    padding = 12
    horizontal_padding = 12
    frame_width = 2
    frame_color = "$selected"
    font = $font 10
    corner_radius = 8
    transparency = 10

[urgency_low]
    background = "$background_dark"
    foreground = "$background_lightest"
    frame_color = "$grey"
    timeout = 5

[urgency_normal]
    background = "$background"
    foreground = "$background_lightest"
    frame_color = "$selected"
    timeout = 8

[urgency_critical]
    background = "$background_darkest"
    foreground = "$really_red"
    frame_color = "$really_red"
    timeout = 0
"""
)

_REQUIRED_COLOR_KEYS = (
    "background_darkest",
    "background_dark",
    "background",
    "background_lightest",
    "selected",
    "grey",
    "really_red",
)


class MissingColorKeyError(KeyError):
    pass

@dataclass(frozen=True)
class DunstPalette:

    background_darkest: str
    background_dark: str
    background: str
    background_lightest: str
    selected: str
    grey: str
    really_red: str

    @classmethod
    def from_theme_colors(cls, colors: dict[str, str]) -> "DunstPalette":
        missing_keys = [key for key in _REQUIRED_COLOR_KEYS if key not in colors]
        if missing_keys:
            raise MissingColorKeyError(
                f"Couleurs manquantes dans le thème : {', '.join(missing_keys)}"
            )

        return cls(
            **{key: _to_hex(colors[key]) for key in _REQUIRED_COLOR_KEYS}
        )


def _to_hex(color: str) -> str:
    return color if color.startswith("#") else f"#{color}"


def build_dunstrc_content(theme) -> str:
    palette = DunstPalette.from_theme_colors(theme.colors)
    return _DUNSTRC_TEMPLATE.substitute(font=theme.font, **palette.__dict__)


def write_dunstrc(content: str, output_path: str = DEFAULT_DUNSTRC_PATH) -> Path:
    destination = Path(output_path).expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    return destination


"""def reload_dunst() -> bool:
    try:
        run(["dunstctl", "reload"], check=True, capture_output=True)
        return True
    except (CalledProcessError, FileNotFoundError):
        return False"""


def apply_dunst_theme(theme, output_path: str = DEFAULT_DUNSTRC_PATH) -> Path:
    content = build_dunstrc_content(theme)
    destination = write_dunstrc(content, output_path)
    return destination