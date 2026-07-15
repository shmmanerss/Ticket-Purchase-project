import qrcode, io, base64
def generate_qr_png(data: dict) -> str:
    img = qrcode.make(data)
    buf = io.BytesIO(); img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode()
