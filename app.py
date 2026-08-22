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
            # 1. XỬ LÝ ẢNH NỀN
            if os.path.exists('bg.jpg'):
                img = Image.open('bg.jpg').convert("RGB")
            elif os.path.exists('9df0bd08-bcd2-4678-a63f-062cd4f16656.jpg'):
                img = Image.open('9df0bd08-bcd2-4678-a63f-062cd4f16656.jpg').convert("RGB")
            else:
                img = Image.new('RGB', (1500, 1000), (255, 255, 255)) 
                
            img = img.resize((1500, 1000), Image.Resampling.LANCZOS)
            draw = ImageDraw.Draw(img)
            
            draw.rectangle([(50, 50), (1450, 950)], outline=(200, 200, 200), width=3)

            # 2. CHÈN LOGO PULLMAN
            logo_path = 'logo.png'
            if not os.path.exists(logo_path):
                logo_path = 'thumb_1600914642_pullman-vt-removebg-preview.png'
                
            if os.path.exists(logo_path):
                logo = Image.open(logo_path).convert("RGBA")
                logo.thumbnail((280, 130), Image.Resampling.LANCZOS) 
                img.paste(logo, (80, 60), mask=logo)

            # 3. CÀI ĐẶT FONT CHỮ
            try:
                font_title = ImageFont.truetype("arial.ttf", 45)
                font_text = ImageFont.truetype("arial.ttf", 25) 
            except IOError:
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()

            # 4. TIÊU ĐỀ
            pullman_green = (14, 76, 58) 
            try:
                bbox = draw.textbbox((0, 0), "VIP ARRIVAL NOTICE", font=font_title)
                text_w = bbox[2] - bbox[0]
                draw.text(((1500 - text_w) / 2, 90), "VIP ARRIVAL NOTICE", font=font_title, fill=pullman_green)
            except:
                draw.text((580, 90), "VIP ARRIVAL NOTICE", font=font_title, fill=pullman_green)

            # Hàm tính toán chiều cao của một đoạn văn bản sau khi ngắt dòng
            def calculate_height(label, value, max_w):
                if not value or str(value).strip() == '' or str(value).lower() == 'nan' or str(value).lower() == 'n/a': 
                    return 0
                text = f"{label}: {value}"
                lines = textwrap.wrap(text, width=max_w)
                return len(lines) * 32

            # Hàm in chữ
            def print_field(x, y, label, value, max_w):
                if not value or str(value).strip() == '' or str(value).lower() == 'nan' or str(value).lower() == 'n/a': 
                    return y
                text = f"{label}: {value}"
                lines = textwrap.wrap(text, width=max_w)
                for line in lines:
                    draw.text((x, y), line, font=font_text, fill=(0, 0, 0)) 
                    y += 32
                return y

            # 5. BỐ CỤC 2 CỘT CĂN HÀNG THÔNG MINH
            y_current = 190
            
            # Khai báo dữ liệu từng hàng (cột trái, cột phải)
            rows = [
                [("Guest full name", guest_name), ("Title/position", title)],
                [("ETA", eta), ("Organization, agency or company", company)],
                [("Room number and room category", room), ("LOS", los)],
                [("Booking contact/person in charge", contact), ("Booking source/referrer", source)]
            ]

            for left_col, right_col in rows:
                # Tính toán chiều cao cần thiết cho cả hai cột
                h_left = calculate_height(left_col[0], left_col[1], 45)
                h_right = calculate_height(right_col[0], right_col[1], 45)
                
                # In dữ liệu
                print_field(100, y_current, left_col[0], left_col[1], 45)
                print_field(800, y_current, right_col[0], right_col[1], 45)
                
                # Cập nhật vị trí Y dựa trên cột dài nhất, cộng thêm khoảng cách giữa các hàng
                if max(h_left, h_right) > 0:
                    y_current += max(h_left, h_right) + 15
            
            # 6. BỐ CỤC TRUNG TÂM CHO THÔNG TIN DÀI
            y_center = y_current + 10
            
            y_center = print_field(100, y_center, "Special requests, preferences or information requiring attention", requests, 100) + 15
            y_center = print_field(100, y_center, "Transportation and arrival/departure arrangements, if applicable", transport, 100) + 15
            y_center = print_field(100, y_center, "Security, safety, confidentiality or privacy requirements", security, 100) + 15
            y_center = print_field(100, y_center, "Others", others, 100) + 15

            # Xuất ảnh
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=95)
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