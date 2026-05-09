import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

# ======================
# AI CONFIG
# ======================
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("⚖️ Legal AI PRO MAX - Contract & Document AI")

# ======================
# READ FILE FUNCTIONS
# ======================
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def read_txt(file):
    return file.read().decode("utf-8")

def read_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image, lang="eng+vie")
    return text

def read_file(file):
    if file.name.endswith(".pdf"):
        return read_pdf(file)
    elif file.name.endswith(".docx"):
        return read_docx(file)
    elif file.name.endswith(".txt"):
        return read_txt(file)
    elif file.name.endswith((".png", ".jpg", ".jpeg")):
        return read_image(file)
    else:
        return ""

# ======================
# UPLOAD MULTIPLE FILES
# ======================
uploaded_files = st.file_uploader(
    "📂 Upload tài liệu (PDF/DOCX/TXT/ẢNH SCAN)",
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

all_text = ""

if uploaded_files:
    for file in uploaded_files:
        all_text += f"\n\n===== FILE: {file.name} =====\n"
        all_text += read_file(file)

    st.success("Đã đọc toàn bộ tài liệu + ảnh scan")

# ======================
# AI FUNCTIONS
# ======================
def ask_ai(prompt):
    return model.generate_content(prompt).text

def generate_contract(description):
    prompt = f"""
Bạn là luật sư chuyên nghiệp tại Việt Nam.

Hãy tạo hợp đồng hoàn chỉnh:

- Văn phong pháp lý chuẩn
- Điều khoản rõ ràng
- Có quyền & nghĩa vụ
- Có thanh toán
- Có chấm dứt hợp đồng
- Có tranh chấp

Mô tả:
{description}
"""
    return ask_ai(prompt)

# ======================
# MODE
# ======================
mode = st.selectbox(
    "Chọn chức năng",
    [
        "📊 Phân tích tổng hợp",
        "⚠️ Tìm rủi ro pháp lý",
        "📝 Tóm tắt hợp đồng",
        "🔍 Hỏi đáp theo tài liệu",
        "🧾 Tạo hợp đồng từ mô tả"
    ]
)

# ======================
# RUN
# ======================

if mode != "🧾 Tạo hợp đồng từ mô tả":

    if all_text:

        if st.button("🚀 Thực hiện"):

            if mode == "📊 Phân tích tổng hợp":
                prompt = f"""
Phân tích tài liệu:
- Nội dung chính
- Điều khoản quan trọng
- Rủi ro pháp lý
- Gợi ý cải thiện

TÀI LIỆU:
{all_text}
"""
                st.write(ask_ai(prompt))

            elif mode == "⚠️ Tìm rủi ro pháp lý":
                prompt = f"""
Tìm rủi ro:
- Điều khoản bất lợi
- Mơ hồ
- Tranh chấp
- Mức độ rủi ro
- Cách sửa

TÀI LIỆU:
{all_text}
"""
                st.write(ask_ai(prompt))

            elif mode == "📝 Tóm tắt hợp đồng":
                prompt = f"""
Tóm tắt:
- Nội dung chính
- Nghĩa vụ
- Điều khoản quan trọng

TÀI LIỆU:
{all_text}
"""
                st.write(ask_ai(prompt))

            elif mode == "🔍 Hỏi đáp theo tài liệu":
                question = st.text_input("Nhập câu hỏi")
                if question:
                    prompt = f"""
Dựa trên tài liệu trả lời chính xác:

TÀI LIỆU:
{all_text}

CÂU HỎI:
{question}
"""
                    st.write(ask_ai(prompt))

    else:
        st.info("Upload tài liệu hoặc ảnh scan trước")

# ======================
# CREATE CONTRACT
# ======================
else:

    st.subheader("🧾 Tạo hợp đồng từ mô tả")

    description = st.text_area("Nhập mô tả hợp đồng")

    if st.button("Tạo hợp đồng"):

        if description:
            result = generate_contract(description)
            st.write(result)
        else:
            st.warning("Nhập mô tả trước")
