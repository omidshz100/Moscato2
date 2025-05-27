# Moscato2

Moscato2 is a Python-based project developed by Omid Shojaeian Zanjani, focusing on automating the extraction and processing of textual data from various sources. The project integrates functionalities such as optical character recognition (OCR), text file parsing, and Google Drive connectivity to streamline data handling tasks.

## Features

* **Image to Text Conversion**: Utilize OCR techniques to extract text from image files.
* **Text File Extraction**: Parse and process text from `.txt` files efficiently.
* **Google Drive Integration**: Connect and interact with Google Drive for file retrieval and storage.
* **Automated Writing**: Generate and manage text outputs based on extracted data.
* **Utility Scripts**: Additional tools for tasks like calendar management and data checking.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/omidshz100/Moscato2.git
   cd Moscato2
   ```

2. **Set Up a Virtual Environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: Ensure that `requirements.txt` is present in the repository. If not, manually install necessary packages based on the scripts used.*

## Usage

* **Image to Text**:

  ```bash
  python ImageToText.py --input path_to_image
  ```

* **Text File Extraction**:

  ```bash
  python TextFileExtractor.py --input path_to_text_file
  ```

* **Google Drive Connection**:

  ```bash
  python GoogleDriveConnect_1.py
  ```

* **Automated Writing**:

  ```bash
  python auto_write.py
  ```

*Note: Replace `path_to_image` and `path_to_text_file` with your actual file paths.*

## Project Structure

* `main.py`: Entry point for the application.
* `ImageToText.py`: Handles OCR operations.
* `TextFileExtractor.py`: Processes text files.
* `GoogleDriveConnect_1.py`: Manages Google Drive interactions.
* `auto_write.py`: Automates writing tasks.
* `cal.py`, `check.py`, `extractor.py`, `exampleCode.py`: Utility scripts for various functions.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

