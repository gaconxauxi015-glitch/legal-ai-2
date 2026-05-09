import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract
import io

# ======================
# AI CONFIG
# ======================
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("⚖️ Legal AI ULTRA - Compare & Risk Detector")

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
# AI CORE
# ======================
def ask_ai(prompt):
    return model.generate_content(prompt).text

# ======================
# MODE
# ======================
mode = st.selectbox(
    "Chọn chức năng",
    [
        "📊 Phân tích hợp đồng",
        "⚠️ Tìm rủi ro pháp lý",
        "🆚 So sánh 2 hợp đồng",
        "🔍 Highlight điều khoản nguy hiểm"
    ]
)

# ======================
# UPLOAD
# ======================
if mode in ["📊 Phân tích hợp đồng", "⚠️ Tìm rủi ro pháp lý"]:

    file = st.file_uploader("Upload hợp đồng", type=["pdf","docx","txt","png","jpg","jpeg"])

    if file:
        text = read_file(file)

        if st.button("Thực hiện"):

            if mode == "📊 Phân tích hợp đồng":
                prompt = f"""
Phân tích hợp đồng:
- Nội dung chính
- Điều khoản quan trọng
- Nhận xét pháp lý

{ text }
"""
                st.write(ask_ai(prompt))

            if mode == "⚠️ Tìm rủi ro pháp lý":
                prompt = f"""
Tìm rủi ro pháp lý:
- Điều khoản bất lợi
- Mơ hồ
- Thiếu sót
- Mức độ rủi ro (cao/trung bình/thấp)

{ text }
"""
                st.write(ask_ai(prompt))

# ======================
# COMPARE 2 CONTRACTS
# ======================
elif mode == "🆚 So sánh 2 hợp đồng":

    col1, col2 = st.columns(2)

    with col1:
        file1 = st.file_uploader("Hợp đồng A", type=["pdf","docx","txt","png","jpg","jpeg"], key="a")

    with col2:
        file2 = st.file_uploader("Hợp đồng B", type=["pdf","docx","txt","png","jpg","jpeg"], key="b")

    if file1 and file2:

        text1 = read_file(file1)
        text2 = read_file(file2)

        if st.button("So sánh"):

            prompt = f"""
So sánh 2 hợp đồng:

HỢP ĐỒNG A:
{text1}

HỢP ĐỒNG B:
{text2}

Yêu cầu:
- điểm giống nhau
- điểm khác nhau
- hợp đồng nào lợi hơn
- hợp đồng nào rủi ro hơn
- đề xuất nên chọn cái nào
"""
            st.write(ask_ai(prompt))

# ======================
# HIGHLIGHT RISK
# ======================
elif mode == "🔍 Highlight điều khoản nguy hiểm":

    file = st.file_uploader("Upload hợp đồng", type=["pdf","docx","txt","png","jpg","jpeg"])

    if file:

        text = read_file(file)

        if st.button("Phân tích sâu"):

            prompt = f"""
Bạn là luật sư cao cấp.

Hãy:
- đánh dấu điều khoản nguy hiểm
- chỉ ra đoạn rủi ro
- giải thích vì sao nguy hiểm
- đề xuất sửa lại

HỢP ĐỒNG:
{text}
"""
            st.write(ask_ai(prompt))
