import qrcode
from PIL import Image

import base64

# Đọc nội dung của tệp SVG
with open("path/to/your/file.svg", "rb") as svg_file:
    svg_content = svg_file.read()

# Mã hóa nội dung SVG thành Base64
encoded_svg = base64.b64encode(svg_content).decode("utf-8")

# In chuỗi Base64
print(encoded_svg)


# Đường dẫn tới file QR code và logo
qr_path = "qrcode.png"
logo_path = "logo.png"
output_path = "qrcode_with_logo.png"

logo = Image.open(logo_path)
basewidth = 100

wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.LANCZOS )
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

# Tạo QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data('https://product-bizarre-survey-2024.onrender.com')
qr.make(fit=True)


# Tạo hình ảnh QR code
qr_code_img = qr.make_image(fill_color="black", back_color="white")

pos = ((qr_code_img.size[0] - logo.size[0]) // 2,
       (qr_code_img.size[1] - logo.size[1]) // 2)
qr_code_img.paste(logo, pos)

# Lưu hình ảnh QR code vào file
qr_code_img.save("qrcode.png")


