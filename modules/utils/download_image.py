import requests
from io import BytesIO
from PIL import Image, ImageDraw
from os import path

def download_image(url: str, local_filename: str, radius: int = 16):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGBA")

        # masque avec rectangle arrondi (supersample x4 pour un anti-aliasing propre)
        scale = 4
        w, h = img.size
        mask = Image.new("L", (w * scale, h * scale), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            (0, 0, w * scale, h * scale),
            radius=radius * scale,
            fill=255
        )
        mask = mask.resize((w, h), Image.LANCZOS)

        img.putalpha(mask)
        img.save(local_filename, "PNG")

    except Exception:
        if not path.exists(local_filename):
            return None

    return local_filename