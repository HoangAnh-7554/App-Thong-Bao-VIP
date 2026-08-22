import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os

st.set_page_config(page_title="VIP Arrival - Pullman", layout="centered")
st.title("🌟 VIP Arrival Notice Generator")
st.write("Nhập thông tin khách vào form bên dưới để tạo ảnh thông báo nhanh.")

with st.form("vip_form"):
    guest_name = st.text_input("1. Guest full name *Bắt buộc")
    col1, col2 = st.columns(2)
    title = col1.text_input("2. Title/position")
    company = col2.text_input("3. Organization, agency or company")
    col3, col4 = st.columns(2)
    eta = col3.text_input("4. ETA")
    los = col4.text_input("5. LOS")
    col5, col6 = st.columns(2)
    room = col5.text_input("6. Room number and room category")
    source = col6.text_input("7. Booking source/referrer")
    contact = st.text_input("8. Booking contact/person in charge")
    
    requests = st.text_area("9. Special requests, preferences or information requiring attention")
    transport = st.text_input("10. Transportation and arrival/departure arrangements, if applicable")
    security = st.text_area("11. Security, safety, confidentiality or privacy requirements")
    others = st.text_area("12. Others")

    submitted = st.form_submit_button("🎨 Tạo Ảnh Thông Báo")

if submitted:
    if not guest_name:
        st.error("❌ Vui lòng nhập Tên Khách (Guest full name)!")
    else:
        try:
            # 1. XỬ LÝ ẢNH NỀN TỰ ĐỘNG
            if os.path.exists('template.jpg'):
                img = Image.open('template.jpg').convert("RGBA")
            elif os.path.exists('template.jpg.jpg'):
                img = Image.open('template.jpg.jpg').convert("RGBA")
            else:
                img = Image.new('RGBA', (1500, 1000), (30, 30, 30, 255)) # Nền đen dự phòng
                
            img = img.resize((1500, 1000), Image.Resampling.LANCZOS)
            
            # Phủ lớp đen mờ sang trọng và vẽ viền vàng vuông vức
            overlay = Image.new('RGBA', img.size, (15, 15, 15, 220)) 
            img = Image.alpha_composite(img, overlay)
            
            draw = ImageDraw.Draw(img)
            draw.rectangle([(50, 50), (1450, 950)], outline=(212, 175, 55, 255), width=3)
            
            img = img.convert("RGB")
            draw = ImageDraw.Draw(img)

            # 2. CÀI ĐẶT FONT
            try:
                font_title = ImageFont.truetype("arial.ttf", 45)
                font_text = ImageFont.truetype("arial.ttf", 24) 
            except IOError:
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()

            # Căn giữa tiêu đề
            try:
                bbox = draw.textbbox((0, 0), "VIP ARRIVAL NOTICE", font=font_title)
                text_w = bbox[2] - bbox[0]
                draw.text(((1500 - text_w) / 2, 80), "VIP ARRIVAL NOTICE", font=font_title, fill=(212, 175, 55))
            except:
                draw.text((580, 80), "VIP ARRIVAL NOTICE", font=font_title, fill=(212, 175, 55))

            # HÀM IN CHỮ ĐA NĂNG
            def print_field(x, y, label, value, max_w):
                if not value or str(value).strip() == '' or str(value).lower() == 'nan' or str(value).lower() == 'n/a': 
                    return y
                text = f"{label}: {value}"
                lines = textwrap.wrap(text, width=max_w)
                for line in lines:
                    draw.text((x, y), line, font=font_text, fill=(255, 255, 255))
                    y += 32
                return y + 10 # Khoảng cách giữa các ô

            # 3. BỐ CỤC 2 CỘT (Cho thông tin ngắn)
            y_left = 160
            y_right = 160
            
            # Cột trái (X = 100, ngắt dòng ở 45 ký tự)
            y_left = print_field(100, y_left, "Guest full name", guest_name, 45)
            y_left = print_field(100, y_left, "ETA", eta, 45)
            y_left = print_field(100, y_left, "Room number and room category", room, 45)
            y_left = print_field(100, y_left, "Booking contact/person in charge", contact, 45)
            
            # Cột phải (X = 800, ngắt dòng ở 45 ký tự)
            y_right = print_field(800, y_right, "Title/position", title, 45)
            y_right = print_field(800, y_right, "Organization, agency or company", company, 45)
            y_right = print_field(800, y_right, "LOS", los, 45)
            y_right = print_field(800, y_right, "Booking source/referrer", source, 45)
            
            # 4. BỐ CỤC TRUNG TÂM (Cho thông tin dài)
            # Tìm điểm kết thúc thấp nhất của 2 cột trên để bắt đầu viết tiếp
            y_center = max(y_left, y_right) + 15
            
            # Dàn ngang toàn màn hình (X = 100, ngắt dòng dài hơn ở 100 ký tự)
            y_center = print_field(100, y_center, "Special requests, preferences or information requiring attention", requests, 100)
            y_center = print_field(100, y_center, "Transportation and arrival/departure arrangements, if applicable", transport, 100)
            y_center = print_field(100, y_center, "Security, safety, confidentiality or privacy requirements", security, 100)
            y_center = print_field(100, y_center, "Others", others, 100)

            # Lưu ảnh
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            byte_im = buf.getvalue()

            st.success("✅ Đã tạo ảnh thành công!")
            st.image(img, use_container_width=True) 

            st.download_button(
                label="⬇️ Tải Ảnh Này Về Máy",
                data=byte_im,
                file_name=f"VIP_{guest_name}.jpg",
                mime="image/jpeg"
            )

        except Exception as e:
            st.error(f"❌ Lỗi: {e}")