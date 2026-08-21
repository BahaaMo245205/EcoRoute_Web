import os
import secrets

from flask import current_app
from PIL import Image


def save_picture(form_picture) -> str | None:
    form_picture.seek(0, os.SEEK_END)
    file_size = form_picture.tell()
    form_picture.seek(0)

    _, f_ext = os.path.splitext(form_picture.filename)
    file_ext = f_ext.lower()

    if file_ext not in [".png", ".jpg", ".jpeg"] or file_size > 16 * 1024 * 1024:
        return None

    random_hex = secrets.token_hex(8)
    picture_name = random_hex + file_ext

    upload_folder = os.path.join(current_app.root_path, "static", "images", "profile")
    os.makedirs(upload_folder, exist_ok=True)
    picture_path = os.path.join(upload_folder, picture_name)

    output_size = (400, 400)

    with Image.open(form_picture) as img:
        if img.mode in ("RGBA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        img.thumbnail(output_size, Image.Resampling.LANCZOS)

        if file_ext in [".jpg", ".jpeg"]:
            img.save(picture_path, "JPEG", quality=90, optimize=True, progressive=True)
        else:
            img.save(picture_path, "PNG", optimize=True)

    return picture_name
