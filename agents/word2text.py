from docx import Document

def doc_text_extract(file_path):
    file = Document(file_path)
    doc_text = ''
    for p in file.paragraphs:
        doc_text = doc_text + p.text + '\n'
        
    return doc_text