import xml.etree.ElementTree as ET
import html
from src.utils.logger import get_logger

logger = get_logger(__name__)

def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        # Extract all text segments and join them
        raw_text = " ".join(t.strip() for t in root.itertext() if t.strip())
        return html.unescape(raw_text)
    except Exception as e:
        logger.error(f"Error parsing XML {file_path}: {e}")
        return None