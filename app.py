import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os

# Cấu hình trang web
st.set_page_config(page_title="VIP Arrival - Pullman", layout="centered")
st.title("🌟 VIP Arrival Notice Generator")
st.write("Nhập thông tin khách vào form bên dưới để tạo ảnh thông báo nhanh.")

# Form nhập liệu trực tiếp trên Web
with st.form("vip_form"):
    guest_name = st.text_input("Guest Name (Tên Khách) *Bắt buộc")
    
    col1, col2 = st.columns(2)
    title_comp = col1.text_input("Title / Company (Chức vụ/Công ty)")
    room = col2.text_input("Room / Category (Phòng)")
    
    col3, col4 = st.columns(2)
    eta = col3.text_input("ETA (Giờ đến)")
    los = col4.text_input("LOS (Thời gian lưu trú)")
    
    transport = st.text_input("Transport (Đưa đón)")
    requests = st.text_area("Special Requests (Yêu cầu đặc biệt)")
    security = st.text_area("Security / Privacy (Lưu ý an ninh/Riêng tư)")

    submitted = st.form_submit_button("🎨 Tạo Ảnh Thông Báo")

# Xử lý khi người dùng bấm nút
if submitted:
    if not guest_name:
        st.error("❌ Vui lòng nhập Tên Khách!")
    else:
        try:
            # Mở ảnh template
            img = Image.open('template.jpg.jpg')
            img = img.resize((1500, 1000), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(img)

            # Cài đặt font chữ (Đọc file arial.ttf bạn đã copy vào thư mục)
            try:
                font_title = ImageFont.truetype("arial.ttf", 45)
                font_text = ImageFont.truetype("arial.ttf", 30)
            except IOError:
                st.warning("⚠️ Không tìm thấy file 'arial.ttf'. Ảnh sẽ dùng font mặc định siêu nhỏ.")
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()

            # In chữ lên ảnh
            draw.text((380, 200), "VIP ARRIVAL NOTICE", font=font_title, fill=(255, 215, 0)) 
            
            start_y = 280
            line_spacing = 40
            max_chars = 50
            y_pos = start_y
            
            def draw_info(label, value):
                global y_pos # Sửa lỗi biến cục bộ
                if not value or value.strip() == '': 
                    return
                text_to_print = f"{label}: {value}"
                wrapped_text = textwrap.wrap(text_to_print, width=max_chars)
                for line in wrapped_text:
                    draw.text((380, y_pos), line, font=font_text, fill=(255, 255, 255))
                    y_pos += line_spacing
                y_pos += 10

            draw_info("Guest", guest_name)
            draw_info("Title/Comp", title_comp)
            draw_info("Room", room)
            
            eta_los = []
            if eta: eta_los.append(f"ETA: {eta}")
            if los: eta_los.append(f"LOS: {los}")
            if eta_los:
                draw_info("Arrival", " | ".join(eta_los))
                
            draw_info("Transport", transport)
            draw_info("Requests", requests)
            draw_info("Security", security)

            # Chuyển ảnh thành dạng byte để web có thể tải về
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            byte_im = buf.getvalue()

            st.success("✅ Đã tạo ảnh thành công!")
            st.image(img, use_column_width=True) # Hiện ảnh xem trước

            # Nút tải ảnh về
            st.download_button(
                label="⬇️ Tải Ảnh Này Về Máy",
                data=byte_im,
                file_name=f"VIP_{guest_name}.jpg",
                mime="image/jpeg"
            )

        except Exception as e:
            st.error(f"❌ Lỗi: {e}. (Hãy chắc chắn bạn đã up đủ file template.jpg)")
