import os
import re
import subprocess
import time



def list_files_in_folder(folder_path):
    abs_folder_path = os.path.abspath(folder_path)
    if not os.path.exists(abs_folder_path):
        raise FileNotFoundError(f"Directory does not exist: {abs_folder_path}")
    return [os.path.join(folder_path, f)
            for f in os.listdir(abs_folder_path) if os.path.isfile(os.path.join(abs_folder_path, f))]

def process_files_with_ollama(folder_path, exclude_prompt):

    files = list_files_in_folder(folder_path)[:1]
    results = []
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        # Call Ollama Gemma3 (assuming ollama is installed and running locally)
        # You may need to adjust the model name and API usage as per your setup
        ollama_cmd = [
            "ollama", "run", "deepseek-llm",
            f"Exclude the following from the text: {exclude_prompt}\n\n{text}"
        ]
        try:
            output = subprocess.check_output(ollama_cmd, text=True)
            results.append((file_path, output))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    return results



def extract_numbered_part(filename):
    match = re.match(r"(\d+)_", os.path.basename(filename))
    if match:
        return match.group(1)
    return None

def extract_section(file_path, start_marker, end_marker):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    extracting = False
    selected_lines = []

    for line in lines:
        if start_marker in line:
            extracting = True
        elif extracting and (end_marker in line):
            break
        elif extracting:
            selected_lines.append(line.strip())

    return "\n".join(selected_lines)
def extract_all_sections(file_path):
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
        result = {'textName': os.path.basename(file_path), 'aic':extract_numbered_part(file_path)}
        for sec, start, end in sections:
            selected_text = extract_section(file_path, start, end)
            result[sec] = selected_text
        return result

def get_all_file_paths(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


if __name__ == "__main__":
    # folder_path = "files/PDFs/textFiles"
    # files = list_files_in_folder(folder_path)
    # fl = files[0]

    # extracted_sections = extract_all_sections(fl)
    # section = input("Enter the section you want to extract (e.g., 4.1, 4.2, etc.): ")
    # print(extracted_sections[section])
    result = extract_all_sections('24139014_all_pages.txt')
    print(result['4.5'])
