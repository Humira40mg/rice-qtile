from user_profile import theme, GAP

# ── colors ───────────────────────────────────────────────────────────────
BG_POPUP      = theme.colors["background_darkest"]
TEXT_PRIMARY  = theme.colors["white"]
TEXT_MUTED    = theme.colors["grey"]
HIGHLIGHT     = theme.colors["background"]
SUB_POP_BG    = theme.colors["background_dark"]
SELECTED      = theme.colors["selected"]
BLUE          = theme.colors["blue"]
GREEN         = theme.colors["green"]
REALLY_RED    = theme.colors["really_red"]
RED           = theme.colors["red"]
YELLOW        = theme.colors["yellow"]

FONT = theme.font

# ── subpopup constants ───────────────────────────────────────────────────────────────
SUB_GAP = GAP/1000 *2
SUB_X_POS = SUB_GAP*2
SUB_WIDTH= 1 - SUB_X_POS*2
SUB_HEIGHT=0.06
FONT_SIZE=25