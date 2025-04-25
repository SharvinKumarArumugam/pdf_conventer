import streamlit as st
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert
from fpdf import FPDF
from pdf2image import convert_from_bytes
from PIL import Image
import os
import tempfile

st.set_page_config(page_title="File Converter", layout="centered")
st.title("📁 Universal File Converter")

option = st.selectbox("Choose conversion type", [
    "PDF to Word",
    "Word to PDF",
    "Image to PDF",
    "PDF to Images"
])

def convert_pdf_to_word(pdf_bytes, output_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_bytes)
        temp_pdf.flush()
        cv = Converter(temp_pdf.name)
        cv.convert(output_path)
        cv.close()

def convert_word_to_pdf(word_file, output_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_word:
        temp_word.write(word_file.read())
        temp_word.flush()
        docx2pdf_convert(temp_word.name, output_path)

def convert_image_to_pdf(image_file, output_path):
    image = Image.open(image_file).convert("RGB")
    image.save(output_path)

def convert_pdf_to_images(pdf_bytes, output_folder):
    images = convert_from_bytes(pdf_bytes)
    image_paths = []
    for i, img in enumerate(images):
        img_path = os.path.join(output_folder, f"page_{i+1}.png")
        img.save(img_path, 'PNG')
        image_paths.append(img_path)
    return image_paths

st.markdown("💡 Upload a file to convert it as per selected option.")

uploaded_file = st.file_uploader("Upload File")

if uploaded_file and st.button("Convert"):
    with st.spinner("Processing..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "output")

            if option == "PDF to Word":
                output_path = output_file + ".docx"
                convert_pdf_to_word(uploaded_file.read(), output_path)
                st.success("✅ Conversion Successful!")
                with open(output_path, "rb") as f:
                    st.download_button("📥 Download Word File", f, file_name="converted.docx")

            elif option == "Word to PDF":
                output_path = output_file + ".pdf"
                convert_word_to_pdf(uploaded_file, output_path)
                st.success("✅ Conversion Successful!")
                with open(output_path, "rb") as f:
                    st.download_button("📥 Download PDF File", f, file_name="converted.pdf")

            elif option == "Image to PDF":
                output_path = output_file + ".pdf"
                convert_image_to_pdf(uploaded_file, output_path)
                st.success("✅ Conversion Successful!")
                with open(output_path, "rb") as f:
                    st.download_button("📥 Download PDF File", f, file_name="image_to_pdf.pdf")

            elif option == "PDF to Images":
                output_folder = tmpdir
                image_paths = convert_pdf_to_images(uploaded_file.read(), output_folder)
                for img_path in image_paths:
                    st.image(img_path)
                    with open(img_path, "rb") as f:
                        st.download_button(f"📥 Download {os.path.basename(img_path)}", f, file_name=os.path.basename(img_path))

