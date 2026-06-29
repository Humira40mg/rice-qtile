from qtile_extras.popup.toolkit import PopupImage, PopupText

from user_profile import theme

FONT = theme.font

def _make_icon_button(
    icon_path: str,
    label: str,
    pos_x: float,
    is_on: bool,
    on_color: str,
    textprimary_color:str,
    textmuted_color: str,
    highlight_color:str,
    font_familly:str,
    callback,
) -> list:

    accent = on_color if is_on else textmuted_color


    return [
        # Zone cliquable invisible
        PopupText(
            text="",
            pos_x=pos_x,
            pos_y=0.44,
            width=0.45,
            height=0.45,
            highlight_method="border",
            highlight=highlight_color,
            highlight_border=2,
            highlight_radius=5,
            mouse_callbacks={"Button1": callback},
        ),

        # Icône
        PopupImage(
            filename=icon_path,
            pos_x=pos_x + 0.02,
            pos_y=0.44,
            width=0.18,
            height=0.42,
            highlight=None,
        ),

        # Label
        PopupText(
            text=label,
            pos_x=pos_x + 0.22,
            pos_y=0.50,
            width=0.22,
            height=0.25,
            h_align="left",
            font=font_familly,
            highlight=None,
            fontsize=13,
            foreground=textprimary_color,
        ),

       PopupText(
            text="",
            pos_x=pos_x + 0.22,
            pos_y=0.72,
            width=0.18,
            height=0.06,
            highlight=None,
            background=accent,
        ),
    ]

def _make_basic_text_button(
       text: str, 
       pos_x: float, 
       pos_y: float, 
       width: float, 
       height: float, 
       fontsize: int,
       foreground_color: str, 
       highlight_color: str, 
       background_color: str, 
       mouse_callbacks: dict,
       name: str = None,
):
    return PopupText(
            name=name,
            text=text,
            pos_x=pos_x,
            pos_y=pos_y,
            width=width,
            height=height,
            h_align="center",
            fontsize=fontsize,
            font=FONT,
            foreground=foreground_color,
            highlight=highlight_color,
            background =background_color,
            mouse_callbacks=mouse_callbacks
        ),


def _make_stylish_text_button(
       icon: str,
       icon_color: str,
       text: str, 
       pos_x: float, 
       pos_y: float, 
       width: float, 
       height: float, 
       fontsize: int,
       foreground_color: str, 
       highlight_color: str, 
       background_color: str, 
       mouse_callbacks: dict,
       name: str = None,
):
    
    return [
        
        PopupText( #text / working button
            name=name,
            text=f"{text} ",
            pos_x=pos_x,
            pos_y=pos_y,
            width=width,
            height=height,
            h_align="right",
            fontsize=fontsize*0.75,
            font=FONT,
            foreground=foreground_color,
            highlight=highlight_color,
            background=None,
            highlight_method="text",
            mouse_callbacks=mouse_callbacks
        ),
        PopupText( #Icon
            text=icon,
            pos_x=pos_x,
            pos_y=pos_y,
            width=width/3.5,
            height=height,
            h_align="left",
            fontsize=fontsize*1.2,
            font=FONT,
            foreground=icon_color,
            highlight=None
        ),
        PopupText( #bar
            text="",
            pos_x=pos_x,
            pos_y=pos_y + height/10*9,
            width=width,
            height=height/10,
            background=background_color,
            highlight=None,
        ),
    ]