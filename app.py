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
    
    st.write("---")
    avatar_upload = st.file_uploader("📸 Tải ảnh đại diện khách VIP (Tùy chọn - Tự động nhận diện khuôn mặt)", type=['png', 'jpg', 'jpeg'])

    submitted = st.form_submit_button("🎨 Tạo Ảnh Thông Báo")

if submitted:
    if not guest_name:
        st.error("❌ Vui lòng nhập Tên Khách (Guest full name)!")
    else:
        try:
            # 1. TẠO NỀN TRẮNG VÀ VIỀN 
            img = Image.new('RGB', (1500, 1350), (255, 255, 255)) 
            draw = ImageDraw.Draw(img)
            draw.rectangle([(50, 50), (1450, 1300)], outline=(200, 200, 200), width=3)

            # 2. TÌM VÀ CHÈN LOGO
            logo_files = ['logo.png', 'logo.png.png', 'thumb_1600914642_pullman-vt-removebg-preview.png', 'thumb_1600914642_pullman-vt-removebg-preview.png.png']
            logo_path = None
            for file in logo_files:
                if os.path.exists(file):
                    logo_path = file
                    break
            
            if logo_path:
                try:
                    logo = Image.open(logo_path).convert("RGBA")
                    logo.thumbnail((320, 160), Image.Resampling.LANCZOS)
                    img.paste(logo, (70, 50), mask=logo)
                except Exception as e:
                    st.warning(f"⚠️ Lỗi khi đọc file logo: {e}")

            # 3. XỬ LÝ ẢNH AVATAR KHÁCH HÀNG (CẮT THÔNG MINH)
            if avatar_upload is not None:
                try:
                    avatar = Image.open(avatar_upload).convert("RGBA")
                    
                    min_dim = min(avatar.width, avatar.height)
                    left = (avatar.width - min_dim) / 2
                    
                    # THUẬT TOÁN MỚI: Nếu là ảnh dọc, ưu tiên cắt phần trên (khuôn mặt)
                    if avatar.height > avatar.width:
                        top = (avatar.height - min_dim) * 0.15 # Chỉ lấy 15% khoảng trống phía trên
                    else:
                        top = (avatar.height - min_dim) / 2    # Ảnh ngang thì cắt chính giữa
                        
                    right = left + min_dim
                    bottom = top + min_dim
                    avatar = avatar.crop((left, top, right, bottom))
                    
                    # Phóng to kích thước lên 220x220
                    avatar_size = (220, 220)
                    avatar = avatar.resize(avatar_size, Image.Resampling.LANCZOS)
                    
                    # Bo góc nhẹ 10px
                    mask = Image.new('L', avatar_size, 0)
                    mask_draw = ImageDraw.Draw(mask)
                    mask_draw.rounded_rectangle((0, 0, avatar_size[0], avatar_size[1]), radius=10, fill=255)
                    
                    # Dán avatar vào góc
                    img.paste(avatar, (1200, 60), mask=mask)
                except Exception as e:
                    st.warning(f"⚠️ Không thể xử lý ảnh Avatar: {e}")

            # 4. CÀI ĐẶT FONT CHỮ
            try:
                font_title = ImageFont.truetype("arial.ttf", 55)
                font_text = ImageFont.truetype("arial.ttf", 26) 
            except IOError:
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()

            # 5. TIÊU ĐỀ
            mint_green = (90, 220, 130)
            try:
                bbox = draw.textbbox((0, 0), "VIP ARRIVAL NOTICE", font=font_title)
                text_w = bbox[2] - bbox[0]
                draw.text(((1500 - text_w) / 2, 65), "VIP ARRIVAL NOTICE", font=font_title, fill=mint_green)
                draw.text((((1500 - text_w) / 2) + 1, 65), "VIP ARRIVAL NOTICE", font=font_title, fill=mint_green)
            except:
                draw.text((580, 65), "VIP ARRIVAL NOTICE", font=font_title, fill=mint_green)

            # HÀM TÍNH CHIỀU CAO
            def calculate_height(value, max_w):
                if not value or str(value).strip() == '' or str(value).lower() == 'nan' or str(value).lower() == 'n/a': 
                    return 0
                lines = textwrap.wrap(str(value), width=max_w)
                return (1 + len(lines)) * 34

            # HÀM IN CHỮ ĐỘC LẬP
            def print_field(x, y, label, value, max_w):
                if not value or str(value).strip() == '' or str(value).lower() == 'nan' or str(value).lower() == 'n/a': 
                    return
                
                draw.text((x, y), label + ":", font=font_text, fill=(110, 110, 110))
                draw.text((x+1, y), label + ":", font=font_text, fill=(110, 110, 110))
                y += 34
                
                lines = textwrap.wrap(str(value), width=max_w)
                for line in lines:
                    draw.text((x, y), line, font=font_text, fill=(0, 0, 0)) 
                    y += 34

            # 6. BỐ CỤC 2 CỘT 
            y_current = 200 
            
            rows = [
                [("Guest full name", guest_name), ("Title/position", title)],
                [("ETA", eta), ("Organization, agency or company", company)],
                [("Room number and room category", room), ("LOS", los)],
                [("Booking contact/person in charge", contact), ("Booking source/referrer", source)]
            ]

            for left_col, right_col in rows:
                h_left = calculate_height(left_col[1], 42)
                h_right = calculate_height(right_col[1], 42)
                
                if h_left > 0 or h_right > 0:
                    print_field(90, y_current, left_col[0], left_col[1], 42)
                    print_field(780, y_current, right_col[0], right_col[1], 42)
                    y_current += max(h_left, h_right) + 15 
            
            # 7. BỐ CỤC TRUNG TÂM
            y_center = y_current + 10
            
            def print_long_field(y, label, value):
                h = calculate_height(value, 95)
                if h > 0:
                    print_field(90, y, label, value, 95)
                    return y + h + 15
                return y

            y_center = print_long_field(y_center, "Special requests, preferences or information requiring attention", requests)
            y_center = print_long_field(y_center, "Transportation and arrival/departure arrangements, if applicable", transport)
            y_center = print_long_field(y_center, "Security, safety, confidentiality or privacy requirements", security)
            y_center = print_long_field(y_center, "Others", others)

            # 8. XUẤT ẢNH
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