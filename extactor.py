import re

# These are your section headers
section_titles = [
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

# Build a pattern from titles
title_pattern = "|".join([re.escape(title) for title in section_titles])
regex_pattern = rf"^({title_pattern})\b.*?(?=^\d+\.\d+|\Z)"  # Match until next section or end

# Read the file
with open("2309060_all_pages.txt", "r", encoding="utf-8") as file:
    print("📄 Reading file...")
    text = file.read()

# Match all desired sections
matches = re.findall(regex_pattern, text, flags=re.MULTILINE | re.DOTALL)

# Save to file
with open("extracted_sections.txt", "w", encoding="utf-8") as out:
    for match in matches:
        out.write(match.strip() + "\n\n")

print("✅ Sections extracted successfully to extracted_sections.txt")
