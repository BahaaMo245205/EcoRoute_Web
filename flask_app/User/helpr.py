from PIL import Image
import os
import secrets
from flask import current_app # أفضل من استيراد app مباشرة

def save_picture(form_picture):
    # 1. توليد اسم عشوائي لمنع تكرار الأسماء أو المشاكل الأمنية
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    
    # 2. تحديد المسار الكامل (تأكد إن الفولدر ده موجود فعلاً)
    picture_path = os.path.join(current_app.root_path, 'static/images/profile', picture_name)

    # 3. معالجة الصورة (تغيير الحجم)
    output_size = (125, 125)
    i = Image.open(form_picture)
    
    # تحسين: التأكد من تحويل الصور لـ RGB لو كانت PNG بشفافية عشان ميرميش Error عند الحفظ كـ JPEG
    if i.mode in ("RGBA", "P"):
        i = i.convert("RGB")
        
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name