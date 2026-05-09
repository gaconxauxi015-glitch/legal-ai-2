import streamlit as st
import google.generativeai as genai

# lấy API key từ Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("⚖️ Legal AI Assistant")

st.write("Nhập hợp đồng hoặc câu hỏi pháp lý:")

text = st.text_area("Input")

if st.button("Phân tích"):
    response = model.generate_content(
        "Bạn là chuyên gia luật Việt Nam. Phân tích nội dung sau:\n\n" + text
    )
    st.write(response.text)
