import os
import io
from PyPDF2 import PdfReader
import re
import tempfile
import zipfile

# Function to read a PDF file and extract text
def read_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# Function to save a file to a temporary location
def save_file(file, directory="uploads"):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return file_path
    except Exception as e:
        return f"Error saving file: {e}"

# Function to clean and preprocess text (e.g., removing extra spaces, non-alphanumeric characters)
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\W+', ' ', text)  # Remove non-alphanumeric characters
    return text.strip()

# Function to extract text from uploaded resume files (supports both PDF and DOCX)
def extract_text_from_file(file):
    if file.type == "application/pdf":
        return read_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Handle DOCX extraction (implement as per your needs, can use python-docx)
        return "DOCX extraction not implemented yet"
    else:
        return "Unsupported file type"

# Function to generate temporary file (for PDF generation)
def generate_temp_file(content, suffix=".txt"):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(content.encode())
            return tmp_file.name
    except Exception as e:
        return f"Error generating temporary file: {e}"

# Function to create a zip of multiple files
def create_zip_from_files(file_paths, zip_name="archive.zip"):
    try:
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in file_paths:
                zipf.write(file, os.path.basename(file))
        return zip_name
    except Exception as e:
        return f"Error creating zip file: {e}"

# Function to handle uploaded files (generic function to save files to the appropriate folder)
def handle_uploaded_file(uploaded_file, directory="uploads"):
    file_path = save_file(uploaded_file, directory)
    return file_path

# Function to check if a file exists in the directory
def file_exists(file_path):
    return os.path.exists(file_path)

