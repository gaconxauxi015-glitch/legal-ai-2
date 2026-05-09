import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from docx.shared import Pt
from PIL import Image
import pytesseract
import io

# ======================
# AI CONFIG
# ======================
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("⚖️ Legal AI PRO MAX - Contract Editor + Word Export")

# ======================
# READ FILES
# ======================
def read_pdf(file):
    reader = PdfReader(file)
    return "\n".join([p.extract_text() or "" for p in reader.pages])

def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def read_txt(file):
    return file.read().decode("utf-8")

def read_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image, lang="eng+vie")

def read_file(file):
    if file.name.endswith(".pdf"):
        return read_pdf(file)
    elif file.name.endswith(".docx"):
        return read_docx(file)
    elif file.name.endswith(".txt"):
        return read_txt(file)
    else:
        return read_image(file)

# ======================
# AI FUNCTIONS
# ======================
def ask_ai(prompt):
    return model.generate_content(prompt).text

def generate_contract(description):
    prompt = f"""
Bạn là luật sư chuyên nghiệp.

Tạo hợp đồng đầy đủ:
- Điều khoản rõ ràng
- Quyền & nghĩa vụ
- Thanh toán
- Chấm dứt hợp đồng
- Tranh chấp

Mô tả:
{description}
"""
    return ask_ai(prompt)

def improve_contract(text):
    prompt = f"""
Bạn là luật sư cao cấp.

Hãy:
- Sửa hợp đồng này cho chặt chẽ hơn
- Loại bỏ rủi ro pháp lý
- Viết lại chuyên nghiệp hơn

HỢP ĐỒNG:
{text}
"""
    return ask_ai(prompt)

# ======================
# EXPORT WORD
# ======================
def export_word(content, filename="contract.docx"):
    doc = Document()
    doc.add_heading("LEGAL CONTRACT", 0)

    for line in content.split("\n"):
        p = doc.add_paragraph(line)
        p.style.font.size = Pt(11)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ======================
# UPLOAD
# ======================
files = st.file_uploader(
    "📂 Upload tài liệu / hợp đồng / ảnh scan",
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

all_text = ""

if files:
    for f in files:
        all_text += f"\n\n=== {f.name} ===\n"
        all_text += read_file(f)

    st.success("Đã đọc toàn bộ tài liệu")

# ======================
# MODE
# ======================
mode = st.selectbox(
    "Chọn chức năng",
    [
        "📊 Phân tích",
        "⚠️ Tìm rủi ro",
        "📝 Tóm tắt",
        "✍️ Sửa hợp đồng (AI rewrite)",
        "🧾 Tạo hợp đồng mới"
    ]
)

# ======================
# RUN
# ======================
if mode != "🧾 Tạo hợp đồng mới":

    if all_text and st.button("🚀 Thực hiện"):

        if mode == "📊 Phân tích":
            result = ask_ai("Phân tích hợp đồng:\n" + all_text)

        elif mode == "⚠️ Tìm rủi ro":
            result = ask_ai("Tìm rủi ro pháp lý:\n" + all_text)

        elif mode == "📝 Tóm tắt":
            result = ask_ai("Tóm tắt hợp đồng:\n" + all_text)

        elif mode == "✍️ Sửa hợp đồng (AI rewrite)":
            result = improve_contract(all_text)

        st.write(result)

        # ======================
        # EXPORT WORD BUTTON
        # ======================
        file = export_word(result)

        st.download_button(
            label="⬇️ Tải file Word",
            data=file,
            file_name="legal_contract.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

else:

    st.subheader("🧾 Tạo hợp đồng từ mô tả")

    desc = st.text_area("Nhập mô tả hợp đồng")

    if st.button("Tạo hợp đồng"):

        result = generate_contract(desc)
        st.write(result)

        file = export_word(result)

        st.download_button(
            label="⬇️ Tải hợp đồng Word",
            data=file,
            file_name="contract.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
