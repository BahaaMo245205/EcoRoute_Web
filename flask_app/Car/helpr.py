def save_picture(form_picture, folder_name='Car_images'): # ضفنا folder_name هنا
    import os
    import secrets
    from PIL import Image
    from flask import current_app

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # تحديد المسار بناءً على الفولدر المبعوث
    picture_path = os.path.join(current_app.root_path, 'static/images/', folder_name, picture_fn)

    # ضبط الحجم (اللي سألت عليه عشان التناسق)
    output_size = (800, 450) # نسبة 16:9 تقريباً
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn