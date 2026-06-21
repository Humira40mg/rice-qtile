from qtile_extras.popup.toolkit import PopupImage, PopupText
from libqtile.lazy import lazy


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
    """
    Bouton minimaliste :
      - icône
      - texte
      - soulignement coloré si actif
    """

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