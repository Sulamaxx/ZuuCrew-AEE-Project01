"""
Data Processing Utilities for Project 01
"""

import re
from typing import List
from pypdf import PdfReader

def load_and_clean_pdf(pdf_path: str) -> str:
    """Load PDF and perform basic cleaning (remove extra whitespace)."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    # Basic cleaning: remove multiple newlines and spaces
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    return text

def chunk_text(text: str, chunk_size: int = 1500, chunk_overlap: int = 200) -> List[str]:
    """Split text into chunks of specified size with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - chunk_overlap
    return chunks
