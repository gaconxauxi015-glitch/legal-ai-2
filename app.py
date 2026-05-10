import streamlit as st
from utils.file_reader import read_file
from core.analyzer import analyze_contract
from core.risk_checker import check_risk
from core.generator import generate_contract
from export.word_export import export_word

st.title("⚖️ AI LEGAL ASSISTANT")

mode = st.selectbox(
    "Chức năng",
    [
        "Phân tích",
        "Rủi ro",
        "Tạo hợp đồng"
    ]
)

file = st.file_uploader(
    "Upload file",
    type=["pdf","docx","txt","png","jpg","jpeg"]
)

text = ""

if file:
    text = read_file(file)

# =====================
# ANALYZE
# =====================

if mode == "Phân tích":

    if file and st.button("Chạy"):
        st.write(analyze_contract(text))

# =====================
# RISK
# =====================

if mode == "Rủi ro":

    if file and st.button("Kiểm tra"):
        st.write(check_risk(text))

# =====================
# GENERATE
# =====================

if mode == "Tạo hợp đồng":

    desc = st.text_area("Mô tả")

    if st.button("Tạo"):
        result = generate_contract(desc)

        st.write(result)

        file_path = export_word(result)

        with open(file_path, "rb") as f:
            st.download_button(
                "⬇️ Download Word",
                f,
                file_name="hop_dong.docx"
            )
