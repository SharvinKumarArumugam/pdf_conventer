import streamlit as st
from pdf2docx import Converter
import pypandoc
from fpdf import FPDF

from PIL import Image
import os
import tempfile

st.set_page_config(page_title="File Converter", layout="centered")
st.title("📁 Universal File Converter")

# Dropdown for conversion type
option = st.selectbox("Choose conversion type", [
    "PDF to Word",
    "Word to PDF",
    "Image to PDF",
    "PDF to Images"
])

# --- Conversion Functions ---

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
        try:
            output = pypandoc.convert_file(temp_word.name, 'pdf', outputfile=output_path)
        except Exception as e:
            st.error(f"❌ Word to PDF conversion failed: {e}")
            return False
    return True

def convert_image_to_pdf(image_file, output_path):
    image = Image.open(image_file).convert("RGB")
    image.save(output_path)



# --- Streamlit UI ---
st.markdown("💡 Upload a file to convert it as per selected option.")

uploaded_file = st.file_uploader("📤 Upload File", type=["pdf", "docx", "jpg", "jpeg", "png"])

if uploaded_file and st.button("Convert"):
    with st.spinner("🔄 Converting..."):
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
                if convert_word_to_pdf(uploaded_file, output_path):
                    st.success("✅ Conversion Successful!")
                    with open(output_path, "rb") as f:
                        st.download_button("📥 Download PDF File", f, file_name="converted.pdf")

            elif option == "Image to PDF":
                output_path = output_file + ".pdf"
                convert_image_to_pdf(uploaded_file, output_path)
                st.success("✅ Conversion Successful!")
                with open(output_path, "rb") as f:
                    st.download_button("📥 Download PDF File", f, file_name="image_to_pdf.pdf")

         
