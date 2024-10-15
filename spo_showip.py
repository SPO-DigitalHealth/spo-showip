import socket
import tkinter as tk
from PIL import Image, ImageTk  # ใช้ Pillow สำหรับรูปภาพ


def get_system_info():
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.error:
        ip_address = None
    return hostname, ip_address


def update_info():
    hostname, ip_address = get_system_info()

    hostname_label.config(text=f"Name : {hostname}")
    if ip_address:
        ip_label.config(text=f"IP : {ip_address}", fg="green")
    else:
        ip_label.config(text="IP : Disconnect", fg="red")

    app.after(2000, update_info)


app = tk.Tk()
app.title("SPO ShowIP")
app.overrideredirect(True)
app.attributes('-topmost', False)

# กำหนดขนาดหน้าต่าง
window_width = 300  # ขนาดหน้าต่างกว้างขึ้นเพื่อให้โลโก้และข้อความแสดงได้เต็มที่
window_height = 120  # เพิ่มความสูงเล็กน้อยเพื่อรองรับบรรทัดใหม่
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
taskbar_height = 48
x_position = screen_width - window_width
y_position = screen_height - window_height - taskbar_height
app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# โหลดและตั้งค่าภาพพื้นหลัง
# background_image = Image.open('img/glass_card_mini.png')
# background_photo = ImageTk.PhotoImage(background_image)

# สร้าง Label เพื่อแสดงภาพพื้นหลัง
# background_label = tk.Label(app, image=background_photo)
# background_label.place(relwidth=1, relheight=1)  # ขยายให้เต็มหน้าต่าง

# สร้าง Frame หลักเพื่อจัดวาง Layout
main_frame = tk.Frame(app)
main_frame.place(relwidth=1, relheight=1)

# สร้าง Frame สำหรับจัดวางโลโก้ทางซ้าย
logo_frame = tk.Frame(main_frame)
logo_frame.pack(side=tk.LEFT, padx=(5, 5))

# โหลดโลโก้ (ใช้ Pillow เพื่อให้รองรับหลายรูปแบบ)
logo_path = "img/logo_MOPH.png"
logo_image = Image.open(logo_path)
logo_image = logo_image.resize(
    (90, 90), Image.LANCZOS)  # ปรับขนาดโลโก้ให้ใหญ่ขึ้น
logo_photo = ImageTk.PhotoImage(logo_image)

# สร้าง Label สำหรับแสดงรูปโลโก้
logo_label = tk.Label(logo_frame, image=logo_photo, bd=0)
logo_label.image = logo_photo
logo_label.pack()

# สร้าง Frame สำหรับจัดข้อความทางขวา
text_frame = tk.Frame(main_frame)
text_frame.pack(side=tk.LEFT)

# สร้าง Label เพื่อแสดงข้อมูลในแถวที่ 1 (ชื่อโฮสต์)
hostname_label = tk.Label(text_frame, text="", font=("Arial", 14), bd=0)
hostname_label.pack(anchor="w", pady=(5, 0))

# สร้าง Label สำหรับ IP Address
ip_label = tk.Label(text_frame, font=("Arial", 18, "bold"), bd=0)
ip_label.pack(anchor="w")


# สร้าง Label สำหรับหมายเลขโทรศัพท์ที่ขึ้นบรรทัดใหม่
developer_tel_label = tk.Label(
    text_frame, text="โทรภายใน : 101", font=("Arial", 14, "bold"), bd=0)
# ให้ขึ้นบรรทัดใหม่พร้อมระยะห่างด้านล่าง
developer_tel_label.pack(anchor="w", pady=(2, 0))

# สร้าง Frame สำหรับ Developer Info
dev_info_frame = tk.Frame(text_frame)
dev_info_frame.pack(anchor="w", pady=0)

# สร้าง Label แสดง Developer Info
developer_info_label = tk.Label(dev_info_frame, text="กลุ่มงานสุขภาพดิจิทัล",
                                font=("Arial", 12), bd=0)
developer_info_label.pack(side=tk.LEFT)

# เรียกใช้ update_info เป็นครั้งแรก
update_info()
app.mainloop()
