import os
import glob
import requests
import json
import re
from dotenv import load_dotenv
import warnings


load_dotenv()
API_KEY = os.getenv('OPENROUTER_API_KEY')
if not API_KEY:
    raise ValueError('Please set the OPENROUTER_API_KEY environment variable.')

# Optional: set your site info for OpenRouter rankings
REFERER = os.getenv('OPENROUTER_REFERER', '')
TITLE = os.getenv('OPENROUTER_TITLE', '')

txt_dir = os.path.join('files', 'PDFs', 'textFiles')
txt_files = glob.glob(os.path.join(txt_dir, '*.txt'))

API_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'google/gemini-2.0-flash-001'

EXTRACTION_PROMPT = (
    'Please extract the content from Section 4.4 only (inclusive) from the provided document. '
    'Ensure that the extracted text is copied verbatim, without any modifications, summaries, or additional comments.'
)

def extract_section_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    # Try to extract Section 4.4 and its subsections using regex
    section_44_pattern = re.compile(r'(Section\s+4\.4[\s\S]*?)(?=\nSection\s+4\.5|\n4\.5|\nSection\s+5|\n5\.|\Z)', re.IGNORECASE)
    match = section_44_pattern.search(file_content)
    if match:
        section_44_text = match.group(1).strip()
        print(f"Extracted Section 4.4 from file before sending to OpenRouter. Length: {len(section_44_text)} chars.")
    else:
        print("Warning: Section 4.4 not found. Sending full file content.")
        section_44_text = file_content
    MAX_CHARS = 10000
    if len(section_44_text) > MAX_CHARS:
        print(f"Truncating Section 4.4 to {MAX_CHARS} characters before sending to OpenRouter.")
        section_44_text = section_44_text[:MAX_CHARS]
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    if REFERER:
        headers['HTTP-Referer'] = REFERER
    if TITLE:
        headers['X-Title'] = TITLE
    data = {
        'model': MODEL,
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': f"{EXTRACTION_PROMPT}\n\n{section_44_text}"
                    }
                ]
            }
        ]
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"API error details: {response.text}")
        raise e
    result = response.json()
    return result['choices'][0]['message']['content']

if __name__ == '__main__':
    for txt_file in txt_files[0:1]:  # Process only the first file for testing
        print("--------------------------------------------------------")
        print(f'Processing: {txt_file}')
        try:
            section = extract_section_from_file(txt_file)
            print(f'Extracted Section 4.4 from {txt_file}:\n{section}\n')
        except Exception as e:
            print(f'Error processing {txt_file}: {e}')
        print("--------------------------------------------------------")
