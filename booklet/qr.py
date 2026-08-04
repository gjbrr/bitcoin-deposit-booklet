import qrcode
import io
from reportlab.lib.utils import ImageReader

def qr_image_reader(data, box_size=10):
    qr = qrcode.QRCode(border=1, box_size=box_size)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)

