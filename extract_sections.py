# import re

# section_titles = [
#     "4.1", "4.1 Indicazioni terapeutiche",
#     "4.2", "4.2 Posologia e modo di somministrazione",
#     "4.3", "4.3 Controindicazioni",
#     "4.4", "4.4 Avvertenze speciali e precauzioni per l’uso",
#     "4.5", "4.5 Interazione con altri medicinali e altre forme d’interazione",
#     "4.6", "4.6 Fertilità, gravidanza e allattamento",
#     "4.7", "4.7 Effetti sulla capacità di guidare veicoli e sull'uso di macchinari",
#     "4.8", "4.8 Effetti indesiderati",
#     "4.9", "4.9 Sovradosaggio",
#     "6.2", "6.2 Incompatibilità"
# ]

# # Read the full text
# with open("2309060_all_pages.txt", "r", encoding="utf-8") as file:
#     text = file.read()

# # Combine all titles into a regex pattern
# titles_pattern = "|".join([re.escape(t) for t in section_titles])
# section_regex = re.compile(rf"^({titles_pattern})\b.*", re.MULTILINE)

# # Find all section start points
# matches = list(section_regex.finditer(text))

# # Extract section content
# sections = {}
# for i, match in enumerate(matches):
#     section_title = match.group().strip()
#     start = match.start()
#     end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
#     content = text[start:end].strip()
#     sections[section_title] = content

# # Write to output file
# with open("extracted_sections.txt", "w", encoding="utf-8") as out:
#     for title, content in sections.items():
#         out.write(f"\n=== {title} ===\n\n")
#         out.write(content + "\n")

# print("✅ Fixed: Full section contents written to extracted_sections.txt")


import re
import json

# Original list with both numbers and full titles
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

# Keep only unique section numbers
short_keys = sorted(set([s.split()[0] for s in section_titles]), key=lambda x: (int(x.split('.')[0]), float(x.split('.')[1])))

# Build regex pattern to find section headers
titles_pattern = "|".join([re.escape(t) for t in section_titles])
section_regex = re.compile(rf"^({titles_pattern})\b.*", re.MULTILINE)

# Read file
with open("2309060_all_pages.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Find section start points
matches = list(section_regex.finditer(text))

# Extract content per section, and map it to just the section number
sections = {}
for i, match in enumerate(matches):
    full_title = match.group().strip()
    short_key = full_title.split()[0]  # e.g., "4.1"
    start = match.start()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    content = text[start:end].strip()
    sections[short_key] = content

# Print as JSON
print(sections['4.2'])
# print(json.dumps(sections, indent=2, ensure_ascii=False))
