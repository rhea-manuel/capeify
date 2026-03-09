from PIL import Image
from io import BytesIO

def convert_cur2png(cur_file, target_size=35):
    img = Image.open(cur_file)
    img = img.resize((target_size, target_size), Image.NEAREST)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
