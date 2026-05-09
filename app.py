import streamlit as st
from google import genai
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

# ======================
# API KEY
# ======================
API_KEY = st.secrets.get("API_KEY")

if not API_KEY:
    st.error("Thiếu API KEY")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.title("⚖️ Legal AI PRO (Stable Version)")

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
# SAFE AI CALL (KHÔNG LỖI MODEL)
# ======================
def ask_ai(prompt):
    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return res.text
    except Exception as e:
        return f"AI Error: {str(e)}"

# ======================
# UI
# ======================
mode = st.selectbox(
    "Chọn chức năng",
    [
        "Phân tích hợp đồng",
        "Tìm rủi ro pháp lý",
        "Tạo hợp đồng từ mô tả",
        "Hỏi đáp tài liệu"
    ]
)

file = st.file_uploader("Upload file", type=["pdf","docx","txt","png","jpg","jpeg"])

text = ""
if file:
    text = read_file(file)
    st.success("Đã đọc file")

# ======================
# CREATE CONTRACT
# ======================
def create_contract(desc):
    return ask_ai(f"""
Bạn là luật sư Việt Nam.
Tạo hợp đồng đầy đủ, rõ ràng, đúng luật:

Mô tả:
{desc}
""")

# ======================
# LOGIC
# ======================
if mode == "Phân tích hợp đồng":
    if file and st.button("Phân tích"):
        st.write(ask_ai("Phân tích hợp đồng:\n" + text))

elif mode == "Tìm rủi ro pháp lý":
    if file and st.button("Tìm rủi ro"):
        st.write(ask_ai("Tìm rủi ro:\n" + text))

elif mode == "Hỏi đáp tài liệu":
    if file:
        q = st.text_input("Câu hỏi")
        if q and st.button("Trả lời"):
            st.write(ask_ai(text + "\n\nCâu hỏi: " + q))

elif mode == "Tạo hợp đồng từ mô tả":
    desc = st.text_area("Mô tả hợp đồng")
    if st.button("Tạo"):
        st.write(create_contract(desc))
