from libqtile.lazy import lazy

def trancparency_out(popup, seconds):
    for i in range(0,100,-1):
        popup.popup.opacity = i/100
        yield from lazy.idle_idletime(seconds/100)
        popup.hide()
        popup.unhide()
    popup.kill()