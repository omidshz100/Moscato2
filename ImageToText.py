from pdf2image import convert_from_path
import pytesseract
import json
import requests



def pdf_to_text(pdf_path, lang="ita"):
    images = convert_from_path(pdf_path)
    full_text = ""
    for img in images:
        full_text += pytesseract.image_to_string(img, lang=lang) + "\n"
    return full_text

print(     pdf_to_text("2309060.pdf", lang="ita")   )



def fetch_section_from_ollama(full_text, section_title, model="gemma3:latest"):
    prompt = (
        f"Please extract the exact text of the section titled '{section_title}' from the following document. "
        "Do not modify or summarize the content. Provide only the verbatim text of the specified section.\n\n"
        + full_text
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    resp_json = response.json()
    if "response" in resp_json:
        return resp_json["response"]
    else:
        return None


def get_sections_by_Algorithm_sections(full_text):
    sections = [
        ("4.1", "Indicazioni terapeutiche", "Posologia e modo di somministrazione"),
        ("4.2", "4.2 Posologia e modo di somministrazione", "4.3 Controindicazioni"),
        ("4.3", "4.3 Controindicazioni", "4.4 Avvertenze speciali e precauzioni per l’uso"),
        ("4.4", "4.4 Avvertenze speciali e precauzioni per l’uso", "4.5 Interazione con altri medicinali e altre forme d’interazione"),
        ("4.5", "4.5 Interazione con altri medicinali e altre forme d’interazione", "4.6 Fertilità, gravidanza e allattamento"),
        ("4.6", "4.6 Fertilità, gravidanza e allattamento", "4.7 Effetti sulla capacità di guidare veicoli e sull'uso di macchinari"),
        ("4.7", "4.7 Effetti sulla capacità di guidare veicoli e sull'uso di macchinari", "4.8 Effetti indesiderati"),
        ("4.8", "4.8 Effetti indesiderati", "4.9 Sovradosaggio"),
        ("4.9", "4.9 Sovradosaggio", "5. PROPRIETÀ FARMACOLOGICHE"),
        ("6.2", "6.2 Incompatibilità", "6.3 Periodo di validità"),
    ]
    return extract_sections(full_text, sections)
# Example usage:
full_text = pdf_to_text("2309060.pdf", lang="ita")
sections_dict = get_sections_by_Algorithm_sections(full_text)
print(sections_dict.get("4.1"))


def save_sections_to_json(sections_dict, filename="sections.json"):
    with open(filename, "w") as f:
        json.dump(sections_dict, f, ensure_ascii=False, indent=2)