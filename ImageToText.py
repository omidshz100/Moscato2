from pdf2image import convert_from_path
import pytesseract
import json


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

def extract_sections(text, sections):
    result = {}
    for key, start, end in sections:
        start_idx = text.find(start)
        end_idx = text.find(end, start_idx + len(start))
        if start_idx != -1 and end_idx != -1:
            content = text[start_idx + len(start):end_idx].strip()
            result[key] = content
    return result

images = convert_from_path("2309060.pdf")
full_text = ""
for img in images:
    full_text += pytesseract.image_to_string(img, lang="ita") + "\n"

sections_dict = extract_sections(full_text, sections)


with open("sections.json", "w") as f:
    json.dump(sections_dict, f, ensure_ascii=False, indent=2)