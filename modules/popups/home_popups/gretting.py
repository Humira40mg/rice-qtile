from random import choice

from qtile_extras.popup.toolkit import PopupText, PopupImage

from user_profile import USERNAME, USER_IMAGE
from .constants import *

def init_greetings_popups():
    greeting_text = choice(["Bonjour", "Salut", "Hey", "今日は", "Salutation"]) #LANGUAGE

    return [
        #hello
        PopupText(
            text=f" {greeting_text}, {USERNAME}",
            pos_x=SUB_X_POS,
            pos_y=SUB_GAP,
            font = FONT, 
            width=SUB_WIDTH,
            height=SUB_HEIGHT,
            h_align="center",
            fontsize=FONT_SIZE,
            foreground=TEXT_PRIMARY,
            background = SUB_POP_BG,
        ),
        
        #pfp
        PopupImage(
            filename=USER_IMAGE,
            pos_x=SUB_X_POS,
            pos_y=SUB_GAP*2 + SUB_HEIGHT,
            width=SUB_WIDTH*0.33,
            height=SUB_HEIGHT*2,
            highlight=None,
        ),
    ]