import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract

# ======================
# API CONFIG
# ======================
API_KEY = st.secrets.get("API_KEY")

if not API_KEY:
    st.error("❌ Thiếu API_KEY trong Streamlit Secrets")
    st.stop()

genai.configure(api_key=API_KEY)

# ======================
# SAFE MODEL LOADER (KHÔNG BAO GIỜ CHẾT)
# ======================
def get_model():
    try:
        return genai.GenerativeModel("gemini-1.5-flash")
    except:
        try:
            return genai.GenerativeModel("gemini-1.5-pro")
        except:
            return genai.GenerativeModel("gemini-pro")

# ======================
# SAFE AI CALL
# ======================
def ask_ai(prompt):
    try:
        model = get_model()
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"❌ AI Error:\n{str(e)}"

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
    img = Image.open(file)
    return pytesseract.image_to_string(img, lang="eng+vie")

def read_file(file):
    name = file.name.lower()

    if name.endswith(".pdf"):
        return read_pdf(file)
    elif name.endswith(".docx"):
        return read_docx(file)
    elif name.endswith(".txt"):
        return read_txt(file)
    else:
        return read_image(file)

# ======================
# UI
# ======================
st.title("⚖️ Legal AI PRO MAX - Stable Version")

mode = st.selectbox(
    "Chọn chức năng",
    [
        "📊 Phân tích hợp đồng",
        "⚠️ Tìm rủi ro pháp lý",
        "🧾 Tạo hợp đồng từ mô tả",
        "🔍 Hỏi đáp theo tài liệu"
    ]
)

# ======================
# UPLOAD FILE
# ======================
file = st.file_uploader(
    "📂 Upload hợp đồng / ảnh scan",
    type=["pdf","docx","txt","png","jpg","jpeg"]
)

text = ""

if file:
    text = read_file(file)
    st.success("Đã đọc file")

# ======================
# FUNCTIONS PROMPT
# ======================
def generate_contract(desc):
    return ask_ai(f"""
Bạn là luật sư Việt Nam.

Tạo hợp đồng đầy đủ:
- rõ ràng
- đúng luật
- có quyền & nghĩa vụ
- có thanh toán
- có chấm dứt hợp đồng
- có tranh chấp

Mô tả:
{desc}
""")

# ======================
# MAIN LOGIC
# ======================
if mode == "📊 Phân tích hợp đồng":

    if file and st.button("Phân tích"):
        prompt = f"Phân tích hợp đồng:\n{text}"
        st.write(ask_ai(prompt))

elif mode == "⚠️ Tìm rủi ro pháp lý":

    if file and st.button("Tìm rủi ro"):
        prompt = f"""
Tìm rủi ro pháp lý:
- điều khoản bất lợi
- điều khoản mơ hồ
- rủi ro tranh chấp

HỢP ĐỒNG:
{text}
"""
        st.write(ask_ai(prompt))

elif mode == "🔍 Hỏi đáp theo tài liệu":

    if file:
        q = st.text_input("Nhập câu hỏi")

        if q and st.button("Trả lời"):
            prompt = f"""
Dựa trên hợp đồng:

{text}

Câu hỏi:
{q}
"""
            st.write(ask_ai(prompt))

elif mode == "🧾 Tạo hợp đồng từ mô tả":

    desc = st.text_area("Nhập mô tả hợp đồng")

    if st.button("Tạo hợp đồng") and desc:
        result = generate_contract(desc)
        st.write(result)
           
