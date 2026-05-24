import pdfplumber
import docx
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def parse_resume(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    try:
        if suffix == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
        elif suffix == '.docx':
            doc = docx.Document(file_path)
            text = '\n'.join(p.text for p in doc.paragraphs)
        else:
            text = file_path.read_text(encoding='utf-8', errors='ignore')
        if not text.strip():
            raise ValueError("Empty resume text")
        logger.info(f"Parsed {file_path.name}: {len(text)} chars")
        return text.strip()
    except Exception as e:
        logger.error(f"Failed to parse {file_path}: {e}")
        raise