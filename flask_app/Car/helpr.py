import os
import secrets

from flask import current_app
from PIL import Image


def save_picture(form_picture, folder_name="Car_images"):
    file_date = form_picture
    if file_date:
        file_date.seek(0, os.SEEK_END)
        file_size = file_date.tell()
        file_date.seek(0)
        if (
            os.path.splitext(form_picture.filename)[1].lower()
            in [".png", ".jpg", ".jpeg"]
            and file_size <= 16 * 1024 * 1024
        ):
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form_picture.filename)
            picture_fn = random_hex + f_ext

            picture_path = os.path.join(
                current_app.root_path, "static/images/", folder_name, picture_fn
            )

            output_size = (800, 450)
            i = Image.open(form_picture)
            i.thumbnail(output_size)
            i.save(picture_path)

            return picture_fn
