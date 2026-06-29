from pathlib import Path
from datetime import datetime, timedelta, timezone

from .constants import *
from qtile_extras.popup.toolkit import PopupText
from modules.status_reader import Status

BOOT_ID_PATH = Path("/proc/sys/kernel/random/boot_id")
UPTIME_PATH = Path("/proc/uptime")


def read_boot_id() -> str:
    return BOOT_ID_PATH.read_text().strip()


def read_boot_time() -> datetime:
    uptime_seconds = float(UPTIME_PATH.read_text().split()[0])
    return datetime.now(timezone.utc) - timedelta(seconds=uptime_seconds)


def format_elapsed(delta: timedelta) -> str:
    total_minutes = int(delta.total_seconds() // 60)
    days, remainder = divmod(total_minutes, 1440)
    hours, minutes = divmod(remainder, 60)
    if days > 0:
        return f"{days}j{hours:02d}h{minutes:02d}" #LANGUAGE
    return f"{hours}h{minutes:02d}"


def check_reboot(status: Status) -> None:
    current_boot_id = read_boot_id()
    if current_boot_id != status.last_boot_id:
        status.last_incident_date = read_boot_time().isoformat()
        status.last_boot_id = current_boot_id
        status.save()


def time_since_last_incident(status: Status) -> str:
    if status.last_incident_date is None:
        return "no incident recorded" #LANGUAGE
    elapsed = datetime.now(timezone.utc) - datetime.fromisoformat(status.last_incident_date)
    return f"{format_elapsed(elapsed)} since last incident" #LANGUAGE


# ── Popups ───────────────────────────
def init_incident_popup():
    status = Status()
    check_reboot(status)
    return [
        PopupText(
            text=time_since_last_incident(status),
            pos_x=SUB_X_POS,
            pos_y=SUB_GAP*3 + SUB_HEIGHT*3,
            width=SUB_WIDTH,
            height=SUB_HEIGHT,
            fontsize=FONT_SIZE,
            foreground=RED,
            highlight=None,
            background= SUB_POP_BG,
            h_align="center"
        ),
    ]