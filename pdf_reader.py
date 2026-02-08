import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


# TESTING
if __name__ == "__main__":
    resume_text = extract_text_from_pdf("sample_resume.pdf")
    print(resume_text)
