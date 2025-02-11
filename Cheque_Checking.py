# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jbecjWG06BduiUiVdaT_hl6j9wm4lj4E
"""
'''pip install PyPDF2 pytesseract

apt-get update
apt install -y tesseract-ocr
pip install pytesseract
apt-get install -y poppler-utils  # For PDF to image conversion
pip install pdf2image  # If you are working with PDFs
'''

import PyPDF2
import cv2
import numpy as np
import pytesseract
from datetime import datetime
from PIL import Image
import io
import re
def pdf_to_image(pdf_path, page_num=0):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[page_num]
        xObject = page['/Resources']['/XObject'].get_object()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].get_data()

                # Check if the image data is compressed using a filter
                if '/Filter' in xObject[obj]:
                    filters = xObject[obj]['/Filter']
                    if isinstance(filters, PyPDF2.generic.NameObject):  # Check if the Filter type is correct
                        filters = [filters] # Convert single filter to list type
                    # Handle different filter types (e.g., /FlateDecode)
                    # For example, if the filter is FlateDecode, you can use:
                    if PyPDF2.generic.NameObject('/FlateDecode') in filters:
                        import zlib
                        data = zlib.decompress(data)


                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"

                # Use io.BytesIO to wrap the image data before passing it to Image.open()
                img = Image.open(io.BytesIO(data))

                # Convert the image to the desired mode (if different from original mode)
                if img.mode != mode:
                    img = img.convert(mode)


                # Resize the image if needed (using img.resize, if necessary)
                if img.size != size:
                    img = img.resize(size)

                return np.array(img)

    return None
# Function to extract text from image using OCR
def extract_text(image):
    return pytesseract.image_to_string(image)

# Function to check if date is predated
def check_date(text, current_date=None):
    if current_date is None:
        current_date = datetime.now()

    # Extract date from text
    date_patterns = [
        r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',  # DD-MM-YYYY or DD/MM/YYYY or DD-MM-YY etc.
        r'(Month \d{1,2}, \d{4})'  # Month DD, YYYY
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                # Convert matched string to date object, assuming pattern like 'DD-MM-YYYY'
                cheque_date = datetime.strptime(match.group(1), '%d-%m-%Y')
                return cheque_date.date() < current_date.date()
            except ValueError:
                # If the date format is different, you might need to handle it here
                pass
    return None  # If no valid date found

# Function to compare numeric and written amount
def compare_amounts(text):
    numeric_pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d{2})?'
    written_pattern = r'(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|and|\s)+'

    numeric_amount = re.search(numeric_pattern, text)
    written_amount = re.search(written_pattern, text)

    if numeric_amount and written_amount:
        # Convert numeric string to float for comparison
        numeric_value = float(numeric_amount.group().replace(',', ''))

        # Convert written amount to numeric - this is a very basic conversion
        written_words = written_amount.group().lower().split()
        # Implement a more complex function to convert to number here
        written_value = 0  # Placeholder for actual conversion

        return numeric_value == written_value
    return False  # If either amount is missing

# Function to check signature (mock implementation)
def check_signature(image, bank_sign_db):
    # This is a placeholder. In a real scenario, you would use image comparison algorithms
    # or machine learning models for signature verification
    return True

def process_cheque(pdf_path, bank_sign_db):
    image = pdf_to_image(pdf_path)
    if image is None:
        return "Failed to extract image from PDF"

    text = extract_text(image)

    # Check if cheque is predated
    is_predated = check_date(text)
    if is_predated is None:
        return "Could not determine cheque date."

    # Compare numeric and written amounts
    amounts_match = compare_amounts(text)

    # Check signature
    signature_valid = check_signature(image, bank_sign_db)

    return {
        "is_predated": is_predated,
        "amounts_match": amounts_match,
        "signature_valid": signature_valid
    }

bank_sign_db = {'Sign DB'}  # Placeholder for actual database of signatures
result = process_cheque('<PDF Location>', bank_sign_db)
print(result)

