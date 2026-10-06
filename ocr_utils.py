"""
OCR utility functions for extracting text from images.
"""

import numpy as np
from PIL import Image
import streamlit as st
import io

try:
    import easyocr
except Exception:
    easyocr = None

# Initialize EasyOCR reader (only once for performance)
@st.cache_resource(show_spinner=False)
def get_ocr_reader():
    """Initialize and return the EasyOCR reader."""
    if easyocr is None:
        return None
    try:
        reader = easyocr.Reader(['en'], gpu=False)
        return reader
    except Exception as e:
        st.error(f"Failed to initialize OCR: {e}")
        return None

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an image using EasyOCR.
    
    Args:
        image_bytes: Image file as bytes
        
    Returns:
        Extracted text as a string
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Prefer EasyOCR when available; fall back to Tesseract otherwise.
        reader = get_ocr_reader()
        if reader is not None:
            image_array = np.array(image)
            results = reader.readtext(image_array)
            extracted_text = "\n".join([result[1] for result in results])
            return extracted_text

        st.warning("OCR is unavailable because EasyOCR could not be initialized.")
        return ""
        
    except Exception as e:
        st.error(f"OCR extraction failed: {e}")
        return ""

def extract_text_from_uploaded_file(uploaded_file) -> tuple[str, bytes]:
    """
    Extract text from an uploaded image file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple of (extracted_text, image_bytes)
    """
    if uploaded_file is None:
        return "", b""
    
    # Read file bytes
    image_bytes = uploaded_file.read()
    
    # Extract text
    extracted_text = extract_text_from_image(image_bytes)
    
    return extracted_text, image_bytes

