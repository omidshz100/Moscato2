from pdf2image import convert_from_path
import pytesseract
import json
import requests
import cv2
import numpy as np
from PIL import Image
from pypdf import PdfReader
import re


sections = [
        ("4.1", "4.1 Indicazioni terapeutiche","4.2 Posologia e modo di somministrazione"),
        ("4.2", "4.2 Posologia e modo di somministrazione","4.3 Controindicazioni"),
        ("4.3", "4.3 Controindicazioni",    "4.4 Avvertenze speciali e precauzioni per l’uso"),
        ("4.4", "4.4 Avvertenze speciali e precauzioni per l’uso", "4.5 Interazione con altri medicinali e altre forme d’interazione"),
        ("4.5", "4.5 Interazione con altri medicinali e altre forme d’interazione", "4.6 Fertilità, gravidanza e allattamento"),
        ("4.6", "4.6 Fertilità, gravidanza e allattamento", "4.7 Effetti sulla capacità di guidare veicoli e sull'uso di macchinari"),
        ("4.7", "4.7 Effetti sulla capacità di guidare veicoli e sull'uso di macchinari", "4.8 Effetti indesiderati"),
        ("4.8", "4.8 Effetti indesiderati", "4.9 Sovradosaggio"),
        ("4.9", "4.9 Sovradosaggio", "5. PROPRIETÀ FARMACOLOGICHE"),
        ("6.2", "6.2 Incompatibilità", "6.3 Periodo di validità"),
    ]
def pdf_to_text(pdf_path, lang="ita"):
    images = convert_from_path(pdf_path)
    full_text = ""
    for img in images:
        full_text += pytesseract.image_to_string(img, lang=lang) + "\n"
    return full_text


def pdf_to_text_advanced(pdf_path, lang="ita"):
    """
    Converts a PDF file to text using OCR, handling multi-column layouts and improving accuracy.
    Returns the extracted text as a single string.
    """

    images = convert_from_path(pdf_path)
    full_text = ""

    for img in images:
        # Convert PIL image to OpenCV format
        open_cv_image = np.array(img)
        if open_cv_image.shape[2] == 4:
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGBA2RGB)
        else:
            open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

        # Convert to grayscale and apply adaptive thresholding for better OCR
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
        )

        # Convert back to PIL Image for pytesseract
        processed_img = Image.fromarray(thresh)

        # Use Tesseract's layout analysis for multi-column documents
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(processed_img, lang=lang, config=custom_config)
        full_text += text + "\n"

    return full_text


def pdf_to_text_pyPdf(pdf_path):
    # importing required modules
    # creating a pdf reader object
    reader = PdfReader(pdf_path)

    # printing number of pages in pdf file
    print(len(reader.pages))

    # getting a specific page from the pdf file
    page = reader.pages[0]

    # extracting text from page
    text = page.extract_text()
    return text

def pdf_to_text_fitz(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text = page.get_text()
    return text



def fetch_section_from_ollima(pdf_path, section_title, next_section_title, model="gemma3:latest", lang="ita"):
    # Extract text from PDF
    full_text = pdf_to_text_pyPdf(pdf_path)

    # Compose prompt for Ollama
    prompt = (
        f"From the provided Italian medical document, find the heading '{section_title}'. "
        f"Extract all text starting from this heading and continuing until the next numbered heading "
        f"(which is '{next_section_title}') begins. Include the heading '{section_title}' in your output.\n"
        f"Here is the text:\n{full_text}"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    print(response.status_code, response.text)



def extract_sections_from_text(text, sections):
    """
    Extracts specified sections from the text based on start and end markers (using regex, non-greedy).
    Returns a dictionary: {section_number: section_text}
    """
    results = {}
    for sec_num, start_marker, end_marker in sections:
        # Flexible pattern: allow optional dot, spaces, and ignore case
        start_pattern = re.escape(start_marker).replace(r'\.', r'\.?').replace(r'\ ', r'\s*')
        end_pattern = re.escape(end_marker).replace(r'\.', r'\.?').replace(r'\ ', r'\s*')
        # Non-greedy match between start and end
        pattern = rf"({start_pattern})(.*?)(?={end_pattern}|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            results[sec_num] = (match.group(1) + match.group(2)).strip()
        else:
            results[sec_num] = ""
    return results



def extract_single_section(text, sections, section_number):
    for sec_num, start_marker, end_marker in sections:
        if sec_num == section_number:
            start_idx = text.find(start_marker)
            end_idx = text.find(end_marker, start_idx + len(start_marker)) if start_idx != -1 else -1
            if start_idx != -1 and end_idx != -1:
                return text[start_idx:end_idx].strip()
            elif start_idx != -1:
                return text[start_idx:].strip()
            else:
                return ""  # Section not found
    return ""  # Section number not in list

import time
if __name__ == "__main__":
    sections = [
        ("4.1", "4.1 Indicazioni terapeutiche","4.2 Posologia e modo di somministrazione"),
        ("4.2", "4.2. Posologia e modo di somministrazione","4.3 Controindicazioni"),
        ("4.3", "4.3 Controindicazioni",    "4.4 Avvertenze speciali e precauzioni per l’uso"),
        ("4.4", "4.4 Avvertenze speciali e precauzioni per l’uso", "4.5 Interazione con altri medicinali e altre forme d’interazione"),
        ("4.5", "4.5 Interazione con altri medicinali e altre forme d’interazione", "4.6 Fertilità, gravidanza e allattamento"),
        ("4.6", "4.6 Fertilità, gravidanza e allattamento", "4.7 Effetti sulla capacità di guidare veicoli e sull'uso di macchinari"),
        ("4.7", "4.7 Effetti sulla capacità di guidare veicoli e sull'uso di macchinari", "4.8 Effetti indesiderati"),
        ("4.8", "4.8 Effetti indesiderati", "4.9 Sovradosaggio"),
        ("4.9", "4.9 Sovradosaggio", "5. PROPRIETÀ FARMACOLOGICHE"),
        ("6.2", "6.2 Incompatibilità", "6.3 Periodo di validità"),
    ]
    sections = extract_sections_from_text(pdf_to_text("output/stampati.pdf"), sections)

    print(sections)

    sections2 = [
            "4.1", "4.1 Indicazioni terapeutiche",
            "4.2", "4.2 Posologia e modo di somministrazione",
            "4.3", "4.3 Controindicazioni",
            "4.4", "4.4 Avvertenze speciali e precauzioni per l’uso",
            "4.5", "4.5 Interazione con altri medicinali e altre forme d’interazione",
            "4.6", "4.6 Fertilità, gravidanza e allattamento",
            "4.7", "4.7 Effetti sulla capacità di guidare veicoli e sull'uso di macchinari", 
            "4.8", "4.8 Effetti indesiderati", 
            "4.9", "4.9 Sovradosaggio", 
            "6.2", "6.2 Incompatibilità"
        ]
