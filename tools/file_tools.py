from langchain.tools import tool
from pathlib import Path
from docx import Document

def check_file(file_path:str) -> str:
    path = Path(file_path)
    if path.exists():
        if path.suffix.lower() == '.docx':
            doc = Document(file_path)
            paragraphs = []
            for paragraph in doc.paragraphs:
                paragraphs.append(paragraph.text)
            return "\n".join(paragraphs)
    return

@tool("file_reader")
def read_file(file_path:str) -> str:
    """Reads a file and returns its contents as plain text.
    
    Accepts .txt and .docx file types.
    
    Args:
        file_path: The full path to the file to read.
    Returns:
        The contents of the file as a plain string.
    """
    path = Path(file_path)
    if path.exists():
        if path.suffix.lower() == '.txt':
            with open(file_path) as f:
                return(f.read())
        elif path.suffix.lower() == '.docx':
            return check_file(file_path)
    else:
        return("No file exists")
    return 