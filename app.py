import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import os

st.set_page_config(page_title="VIP Arrival - Pullman", layout="centered")
st.title("🌟 VIP Arrival Notice Generator")
st.write("Nhập thông tin khách vào form bên dưới để tạo ảnh thông báo nhanh.")

# Giao diện nhập liệu giữ nguyên 100% tên trường Excel
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

# ... (Phần code giao diện form phía trên giữ nguyên) ...

if submitted:
    if not guest_name:
        st.error("❌ Vui lòng nhập Tên Khách (Guest full name)!")
    else:
        try:
            img = Image.open('template.jpg.jpg')
            img = img.resize((1500, 1000), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(img)

            try:
                # Tiêu đề giữ nguyên size 45
                font_title = ImageFont.truetype("arial.ttf", 45)
                # Thu nhỏ font chữ nội dung xuống 25 để nhét vừa khung mới
                font_text = ImageFont.truetype("arial.ttf", 25) 
            except IOError:
                st.warning("⚠️ Không tìm thấy file 'arial.ttf'. Ảnh sẽ dùng font mặc định.")
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()

            # Dời Tiêu đề lên cao một chút (y = 160 thay vì 200)
            draw.text((380, 160), "VIP ARRIVAL NOTICE", font=font_title, fill=(255, 215, 0)) 
            
            # Dời dòng đầu tiên lên cao hơn (y = 230 thay vì 280)
            start_y = 230 
            line_spacing = 32 # Thu hẹp khoảng cách giữa các dòng (từ 38 xuống 32)
            max_chars = 60    # Tăng số ký tự/dòng vì chữ đã nhỏ hơn
            y_pos = start_y
            
            def draw_info_exact_label(label, value):
                global y_pos
                if not value or str(value).strip() == '' or str(value).lower() == 'nan' or str(value).lower() == 'n/a': 
                    return
                
                text_to_print = f"{label}: {value}"
                wrapped_text = textwrap.wrap(text_to_print, width=max_chars)
                for line in wrapped_text:
                    draw.text((380, y_pos), line, font=font_text, fill=(255, 255, 255))
                    y_pos += line_spacing
                y_pos += 5 # Giảm khoảng cách trống giữa các mục khác nhau

            draw_info_exact_label("Guest full name", guest_name)
            draw_info_exact_label("Title/position", title)
            draw_info_exact_label("Organization, agency or company", company)
            draw_info_exact_label("ETA", eta)
            draw_info_exact_label("LOS", los)
            draw_info_exact_label("Room number and room category", room)
            draw_info_exact_label("Booking source/referrer", source)
            draw_info_exact_label("Booking contact/person in charge", contact)
            draw_info_exact_label("Special requests, preferences or information requiring attention", requests)
            draw_info_exact_label("Transportation and arrival/departure arrangements, if applicable", transport)
            draw_info_exact_label("Security, safety, confidentiality or privacy requirements", security)
            draw_info_exact_label("Others", others)

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