import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

st.title("⚖️ Legal AI OFFLINE SAFE MODE")

# ======================
# READ FILE
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
    img = Image.open(file)
    return pytesseract.image_to_string(img, lang="eng+vie")

def read_file(file):
    name = file.name.lower()
    if name.endswith(".pdf"):
        return read_pdf(file)
    if name.endswith(".docx"):
        return read_docx(file)
    if name.endswith(".txt"):
        return read_txt(file)
    return read_image(file)

# ======================
# SIMPLE AI RULE ENGINE (KHÔNG API)
# ======================
def analyze(text):
    return f"""
📊 PHÂN TÍCH CƠ BẢN

- Độ dài tài liệu: {len(text)} ký tự

⚠️ Gợi ý kiểm tra:
- Điều khoản thanh toán
- Điều khoản chấm dứt
- Điều khoản trách nhiệm
- Điều khoản phạt vi phạm

📄 NỘI DUNG:
{text[:3000]}
"""

def risk(text):
    return """
⚠️ RỦI RO CÓ THỂ GẶP:

- Điều khoản mơ hồ
- Thiếu điều khoản phạt
- Thiếu điều khoản tranh chấp
- Không rõ nghĩa vụ hai bên

👉 Hãy kiểm tra kỹ các phần thanh toán + chấm dứt hợp đồng
""" + text[:2000]

def create_contract(desc):
    return f"""
🧾 HỢP ĐỒNG MẪU (GENERATED TEMPLATE)

Mô tả:
{desc}

1. Bên A: ........
2. Bên B: ........
3. Nội dung hợp đồng: ........
4. Thanh toán: ........
5. Chấm dứt: ........
6. Tranh chấp: ........
"""

# ======================
# UI
# ======================
mode = st.selectbox(
    "Chọn chức năng",
    ["Phân tích", "Rủi ro", "Tạo hợp đồng"]
)

file = st.file_uploader("Upload file", type=["pdf","docx","txt","png","jpg","jpeg"])

text = ""
if file:
    text = read_file(file)
    st.success("Đã đọc file")

# ======================
# RUN
# ======================
if mode == "Phân tích":
    if file and st.button("Chạy"):
        st.write(analyze(text))

if mode == "Rủi ro":
    if file and st.button("Chạy"):
        st.write(risk(text))

if mode == "Tạo hợp đồng":
    desc = st.text_area("Mô tả hợp đồng")
    if st.button("Tạo"):
        st.write(create_contract(desc))o"):
        st.write(create_contract(desc))
