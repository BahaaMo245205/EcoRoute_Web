from flask import current_app
from PIL import Image
import secrets
import os


def save_picture(form_picture):
    form_picture.seek(0, os.SEEK_END)
    file_size = form_picture.tell()
    form_picture.seek(0)

    _, f_ext = os.path.splitext(form_picture.filename)
    file_ext = f_ext.lower()

    if file_ext in [".png", ".jpg", ".jpeg"] and file_size <= 16 * 1024 * 1024:

        random_hex = secrets.token_hex(8)
        picture_name = random_hex + file_ext

        picture_path = os.path.join(
            current_app.root_path, "static/images/profile", picture_name
        )

        output_size = (125, 125)
        i = Image.open(form_picture)

        if i.mode in ("RGBA", "P"):
            i = i.convert("RGB")

        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_name

    return None
