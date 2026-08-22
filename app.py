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
            # 1. TẠO NỀN TRẮNG VÀ VIỀN
            img = Image.new('RGB', (1500, 1000), (255, 255, 255)) 
            draw = ImageDraw.Draw(img)
            draw.rectangle([(50, 50), (1450, 950)], outline=(200, 200, 200), width=3)

            # 2. TÌM VÀ CHÈN LOGO (CODE CHỐNG LỖI ẨN ĐUÔI)
            logo_files = ['logo.png', 'logo.png.png', 'thumb_1600914642_pullman-vt-removebg-preview.png', 'thumb_1600914642_pullman-vt-removebg-preview.png.png']
            logo_path = None
            for file in logo_files:
                if os.path.exists(file):
                    logo_path = file
                    break
            
            if logo_path:
                try:
                    logo = Image.open(logo_path).convert("RGBA")
                    logo.thumbnail((280, 130), Image.Resampling.LANCZOS) 
                    img.paste(logo, (80, 60), mask=logo)
                except Exception as e:
                    st.warning(f"⚠️ Lỗi khi đọc file logo: {e}")
            else:
                st.warning("⚠️ Không tìm thấy file Logo. Hệ thống đang rà soát các tên: logo.png, logo.png.png...")

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

            # HÀM ĐO CHIỀU CAO CHỮ
            def calculate_height(label, value, max_w):
                if not value or str(value).strip() == '' or str(value).lower() == 'nan' or str(value).lower() == 'n/a': 
                    return 0
                text = f"{label}: {value}"
                lines = textwrap.wrap(text, width=max_w)
                return len(lines) * 35  # Tăng khoảng cách dòng lên 35px cho dễ đọc

            # HÀM IN CHỮ
            def print_field(x, y, label, value, max_w):
                if not value or str(value).strip() == '' or str(value).lower() == 'nan' or str(value).lower() == 'n/a': 
                    return
                text = f"{label}: {value}"
                lines = textwrap.wrap(text, width=max_w)
                for line in lines:
                    draw.text((x, y), line, font=font_text, fill=(0, 0, 0)) 
                    y += 35

            # 5. BỐ CỤC 2 CỘT (CĂN GIÓNG TUYỆT ĐỐI)
            y_current = 200 # Dời xuống một chút để không dính tiêu đề
            
            rows = [
                [("Guest full name", guest_name), ("Title/position", title)],
                [("ETA", eta), ("Organization, agency or company", company)],
                [("Room number and room category", room), ("LOS", los)],
                [("Booking contact/person in charge", contact), ("Booking source/referrer", source)]
            ]

            for left_col, right_col in rows:
                h_left = calculate_height(left_col[0], left_col[1], 45)
                h_right = calculate_height(right_col[0], right_col[1], 45)
                
                # Chỉ xử lý khi có dữ liệu ở ít nhất 1 trong 2 cột
                if h_left > 0 or h_right > 0:
                    print_field(100, y_current, left_col[0], left_col[1], 45)
                    print_field(800, y_current, right_col[0], right_col[1], 45)
                    
                    # Lấy chiều cao của bên dài nhất cộng thêm 15px khoảng trống
                    y_current += max(h_left, h_right) + 15 
            
            # 6. BỐ CỤC TRUNG TÂM CHO THÔNG TIN DÀI
            y_center = y_current + 15
            
            def print_long_field(y, label, value):
                h = calculate_height(label, value, 100)
                if h > 0:
                    print_field(100, y, label, value, 100)
                    return y + h + 15
                return y

            y_center = print_long_field(y_center, "Special requests, preferences or information requiring attention", requests)
            y_center = print_long_field(y_center, "Transportation and arrival/departure arrangements, if applicable", transport)
            y_center = print_long_field(y_center, "Security, safety, confidentiality or privacy requirements", security)
            y_center = print_long_field(y_center, "Others", others)

            # 7. XUẤT ẢNH
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