from libqtile.lazy import lazy
from libqtile.config import Group, Key

from settings.keys import keys

from user_profile import mod

groups = [Group(i) for i in "12345"]
groupKeys = {
    "1": "ampersand",
    "2": "eacute",
    "3": "quotedbl",
    "4": "apostrophe",
    "5": "parenleft",
}

for i in groups :
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                groupKeys[i.name],
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                groupKeys[i.name],
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )