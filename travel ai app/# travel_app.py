# travel_app.py

import streamlit as st
import google.generativeai as genai
from urllib.parse import quote

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(
    page_title="AI Tư vấn Du lịch",
    page_icon="✈️",
    layout="wide"
)

# --- HÀM CẤU HÌNH GEMINI API ---
def configure_gemini():
    try:
        # Cách 1: Dùng secrets khi triển khai
        # api_key = st.secrets["GOOGLE_API_KEY"]

        # Cách 2: Nhập trực tiếp để chạy cục bộ (chỉ dùng thử nghiệm)
        api_key = st.secrets["GOOGLE_API_KEY"]  # <-- Thay bằng API Key thật

        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Lỗi cấu hình API Gemini: {e}")
        st.stop()

# --- HÀM TẠO PROMPT ---
def build_prompt(destination):
    return f"""
    Hãy đóng vai một chuyên gia tư vấn du lịch.
    Tạo một lịch trình du lịch chi tiết trong 3 ngày cho địa điểm hoặc loại hình du lịch sau: "{destination}".

    Yêu cầu đầu ra phải có cấu trúc rõ ràng như sau:
    - **Tổng quan chuyến đi:** Một đoạn giới thiệu ngắn về điểm đến.
    - **Lịch trình chi tiết từng ngày:**
        - **## Ngày 1: [Tên chủ đề cho ngày 1]**
        - **Sáng:** Gợi ý 1-2 hoạt động.
        - **Trưa:** Gợi ý địa điểm ăn trưa.
        - **Chiều:** Gợi ý 1-2 hoạt động.
        - **Tối:** Gợi ý địa điểm ăn tối và hoạt động buổi tối.
    - Lặp lại cấu trúc tương tự cho **Ngày 2** và **Ngày 3**.
    - **Ẩm thực đặc sản:** Liệt kê 5-7 món ăn đặc sản không thể bỏ lỡ kèm mô tả ngắn gọn.
    - **Điểm tham quan nổi bật khác:** Liệt kê thêm 3-5 địa điểm nổi bật khác nếu có thời gian.

    Sử dụng ngôn ngữ hấp dẫn, lôi cuốn và định dạng Markdown để dễ đọc (in đậm, gạch đầu dòng).
    """

# --- GIAO DIỆN ỨNG DỤNG ---
model = configure_gemini()

st.title("✈️ AI Tư vấn Du lịch")
st.markdown("Chào mừng bạn! Hãy để tôi giúp bạn lên kế hoạch cho chuyến đi đáng nhớ.")

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_input(
        "📍 Bạn muốn đi đâu hoặc trải nghiệm loại hình du lịch nào?",
        placeholder="Ví dụ: Đà Lạt, Du lịch biển ở miền Trung, Khám phá Hà Giang..."
    )

    if st.button("Gợi ý cho tôi!", type="primary"):
        if not user_input:
            st.warning("Vui lòng nhập địa điểm hoặc loại hình du lịch bạn muốn.")
        else:
            with st.spinner("AI đang sáng tạo lịch trình cho bạn, vui lòng chờ..."):
                try:
                    prompt = build_prompt(user_input)
                    response = model.generate_content(prompt)
                    st.success("🎉 Đây là lịch trình gợi ý dành cho bạn!")
                    st.markdown(response.text)

                    # --- BẢN ĐỒ & HÌNH ẢNH ---
                    st.markdown("---")
                    st.subheader("🗺️ Khám phá thêm")

                    encoded = quote(user_input)
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded}"
                    images_url = f"https://www.google.com/search?tbm=isch&q={encoded}"

                    st.markdown(f"- 📍 [Xem trên Google Maps]({maps_url})")
                    st.markdown(f"- 🖼️ [Xem hình ảnh về {user_input}]({images_url})")

                except Exception as e:
                    st.error(f"❌ Lỗi khi tạo lịch trình: {e}")

with col2:
    st.image(
        "https://images.unsplash.com/photo-1523906834658-6e24ef2386f9?q=80&w=1883&auto=format&fit=crop",
        caption="Lên kế hoạch cho chuyến phiêu lưu tiếp theo của bạn",
        use_column_width=True
    )
    st.info(
        "**💡 Mẹo:**\n"
        "- Cung cấp thông tin càng chi tiết, gợi ý càng chính xác.\n"
        "- Thử nhập: 'Phượt Tây Bắc mùa lúa chín' hoặc 'Nghỉ dưỡng sang trọng tại Phú Quốc'."
    )
