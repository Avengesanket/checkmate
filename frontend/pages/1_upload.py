import streamlit as st
import os
from pdf_to_images import convert_pdf_to_images
from cheque_border_detector import detect_and_crop_cheque_borders
from gemini_integration import extract_text_from_image
from database import insert_cheque_data
from PIL import Image
import webbrowser

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

ensure_directory("uploads")
st.write("# Upload")
uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

if uploaded_file is not None:
    pdf_path = os.path.join("uploads", uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File {uploaded_file.name} uploaded successfully.")

    with st.spinner("Converting PDF pages to images..."):
        convert_pdf_to_images(pdf_path, "images")

    with st.spinner("Detecting cheque borders..."):
        detect_and_crop_cheque_borders("images", "cropped_cheques")

    st.success("Cheque borders detected and cropped.")

    cropped_folder = "cropped_cheques"
    if os.path.exists(cropped_folder):
        st.write("### Cropped Cheque Images")
        image_files = [f for f in os.listdir(cropped_folder) if f.endswith(".png")]
        for img_file in image_files:
            image = Image.open(os.path.join(cropped_folder, img_file))
            st.image(image, caption=img_file, use_column_width=True)

    if st.button("Extract Text and View Dashboard"):
        for img_file in os.listdir(cropped_folder):
            if img_file.endswith(".png"):
                text = extract_text_from_image(os.path.join(cropped_folder, img_file))
                cheque_data = {
                    "cheque_no": "123456",
                    "date": "2025-02-15",
                    "account_no": "9876543210",
                    "bank_name": "ABC Bank",
                    "payee_name": "John Doe",
                    "amount": 1000.50
                }
                insert_cheque_data(cheque_data)
        webbrowser.open("http://localhost:8501/pages/2_dashboard")

if st.button("Clear Images"):
    for folder in ["images", "cropped_cheques"]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
            st.success(f"All files in {folder} have been cleared.")