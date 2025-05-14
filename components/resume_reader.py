import fitz  # PyMuPDF

class Resume_reader:
    def __init__(self, file):
        self.file = file
        self.text = ""

    def extract_text(self):
        try:
            with fitz.open(stream=self.file.read(), filetype="pdf") as doc:
                text = ""
                for page in doc:
                    text += page.get_text()
                self.text = text
                return text
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""
