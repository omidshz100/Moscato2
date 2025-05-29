# [ Welcome to Python PDF WATERMARK REMOVER ]
# [ website : https://ViKi-R.github.io ]
# [ Author : ViKi-R ]

from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_, PdfReadError
import os 
import time
import shutil
from concurrent.futures import ThreadPoolExecutor
import os


def remove_watermark(wmText, inputFile, outputFile):
    # This Function Reads PDF file and Removes the WATERMARK TEXT
    
    with open(inputFile, "rb") as f:
        source = PdfFileReader(f, strict=False)
        output = PdfFileWriter()
        
        #print(output)

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]

                    for i in wmText:
                        if isinstance(text, str) and text.startswith(i):
                            operands[0] = TextStringObject('')
                    
            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        #print(output)
        
        with open(outputFile, "wb") as outputStream:
            output.write(outputStream)


def watermark_text(inputFile, waterMarkTextStarting):
    wmText = []
    try:
        pdfFileObj = open(inputFile, 'rb') 
        pdfReader = PdfFileReader(pdfFileObj) 
        pageObj = pdfReader.getPage(0) 
        watermark = pageObj.extractText() 
        pdfFileObj.close()
        x = watermark.find(waterMarkTextStarting)
        lengthWmText = len(waterMarkTextStarting) 
        wmText.append(watermark[x:x+lengthWmText])
        wmText.append(watermark[x+lengthWmText:])
        return wmText 
    except PdfReadError:
        print(f"Skipping malformed PDF: {inputFile}")
        return None


def creatingFolder(dirName):
    # This Function is used to create Folder, Original-pdf and Watermark-Removed-pdf

    os.makedirs(os.path.dirname(dirName), exist_ok=True)
    time.sleep(2)
    return dirName


def CheckingFiles(dirName):
    # This Function is used to check if any pdf present in Orginal-pdf Folder
    # if present excutes next step
    # else prompts user to add pdf files to folder

    # input(f"Please place the PDF files in the '{dirName}' Folder Created! and Press Enter...")
    # print(f"-"*50)

    while True:
        inputFilesNames = os.listdir(dirName)
        if len(inputFilesNames) == 0:
            input(f"No PDF files Found in '{dirName}' Folder! Please add and Press Enter...")
        else:
            break

    print(f"Total Number of PDF Files Found: {len(inputFilesNames)}")    
    return inputFilesNames    

# Important Function
def process_single_file(args):
    idx, i, inputFileDir, outputFileDir, total_files, processed_files, failed_files, skipped_files, processed_log, failed_log, skipped_log, waterMarkTextStarting, x = args
    inputFile = f'{inputFileDir}{i}'
    outputFile = f'{outputFileDir}{i}'
    if i in processed_files or i in failed_files or i in skipped_files:
        print(f"[SKIPPED] {idx+1}/{total_files} Duplicate file skipped: {i}")
        with open(skipped_log, "a") as f:
            f.write(i + "\n")
        return 'skipped'
    try:
        wm_text = watermark_text(inputFile, waterMarkTextStarting)
        if wm_text is None:
            raise Exception("Malformed PDF or watermark not found")
        remove_watermark(wm_text, inputFile, outputFile)
        print(f'[ {x} ]  {idx+1}/{total_files} Processed: {i}')
        with open(processed_log, "a") as f:
            f.write(i + "\n")
        return 'processed'
    except Exception as e:
        print(f"[FAILED] {idx+1}/{total_files} Failed to process {i}: {e}")
        with open(failed_log, "a") as f:
            f.write(i + "\n")
        return 'failed'

def processingFilesInFolder(inputFileDir, outputFileDir, inputFilesNames, waterMarkTextStarting):
    x = u'\u2713'
    processed_log = "processed_files_WaterMarkRemover.txt"
    failed_log = "failed_files_WaterMarkRemover.txt"
    skipped_log = "skipped_files_WaterMarkRemover.txt"

    processed_files = set()
    if os.path.exists(processed_log):
        with open(processed_log, "r") as f:
            processed_files = set(line.strip() for line in f)
    failed_files = set()
    if os.path.exists(failed_log):
        with open(failed_log, "r") as f:
            failed_files = set(line.strip() for line in f)
    skipped_files = set()
    if os.path.exists(skipped_log):
        with open(skipped_log, "r") as f:
            skipped_files = set(line.strip() for line in f)

    print(f'-'*50)
    files_to_process = [i for i in inputFilesNames]
    total_files = len(files_to_process)

    args_list = [
        (idx, i, inputFileDir, outputFileDir, total_files, processed_files, failed_files, skipped_files, processed_log, failed_log, skipped_log, waterMarkTextStarting, x)
        for idx, i in enumerate(files_to_process)
    ]

    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        results = list(executor.map(process_single_file, args_list))

    print(f"Processing complete. Processed: {results.count('processed')}, Failed: {results.count('failed')}, Skipped: {results.count('skipped')}")
def process_all_files_in_folder(inputFileDir, outputFileDir, inputFilesNames, waterMarkTextStarting):
    x = u'\u2713'
    total_files = len(inputFilesNames)
    for idx, i in enumerate(inputFilesNames):
        inputFile = os.path.join(inputFileDir, i)
        outputFile = os.path.join(outputFileDir, i)
        try:
            wm_text = watermark_text(inputFile, waterMarkTextStarting)
            if wm_text is None:
                raise Exception("Malformed PDF or watermark not found")
            remove_watermark(wm_text, inputFile, outputFile)
            print(f'[ {x} ]  {idx+1}/{total_files} Processed: {i}')
        except Exception as e:
            print(f"[FAILED] {idx+1}/{total_files} Failed to process {i}: {e}")
def deletingFiles(inputDirName, outputDirName):
    # This Function removes the files once the process is completed
    # if the watermark-removed-pdf folder is empty it deletes the folder
    # else prompts the user to empty the folder 

    input(f"Please Cut PDF files found in '{outputDirName}' and Paste in other folder and Press Enter...")
    print(f'-'*50)
    while True:
        outputDir_files = os.listdir(outputDirName)
        if(len(outputDir_files) == 0):
            print(f'-'*50)
            print(f"Deleting Folders {inputDirName} and {outputDirName}")
            shutil.rmtree(inputDirName)
            time.sleep(2)
            shutil.rmtree(outputDirName)
            time.sleep(2)
            print("Done...")
            break
        else:
            input(f"'{outputDirName}' is not empty. Please empty folder and Press Enter...")


def verbosity(inputFilesNames, outputDirName):
    # This Function verboses information
    print(f'-'*50)
    print(f"Watermark for {len(inputFilesNames)} Files has been Removed.")
    print(f'-'*50)
    print(f"Watermark Removed PDF Files can be found in '{outputDirName}' ...")
    print(f'-'*50)

def remove_watermark_from_single_pdf(input_pdf, watermarks, output_dir='output'):
    input_pdf = input_pdf.strip()
    # Use the name of the input PDF for the output
    base_name = os.path.basename(input_pdf)
    output_pdf = os.path.join(output_dir, base_name)
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    temp_input = input_pdf
    temp_output = output_pdf

    for idx, watermark_start in enumerate(watermarks):
        wm_text = watermark_text(temp_input, watermark_start)
        if wm_text is None:
            print(f"Could not find watermark starting with: {watermark_start}")
            continue
        # For all but the last watermark, use a temp file
        if idx < len(watermarks) - 1:
            temp_output = temp_output + f".tmp{idx}"
        else:
            temp_output = output_pdf
        try:
            remove_watermark(wm_text, temp_input, temp_output)
            print(f"Removed watermark {idx+1}/{len(watermarks)}: {watermark_start}")
            # Next round, input is the output of this round
            temp_input = temp_output
        except Exception as e:
            print(f"Failed to remove watermark '{watermark_start}': {e}")
            break

    print(f"Watermark(s) removed. Output saved to {output_pdf}")

def main():
    waterMarkTextStarting = "Agenzia Italiana del Farmaco"
    new_watermarkTextStarting = """Documento reso disponibile da AIFA il 03/01/2025
Esula dalla competenza dell'AIFA ogni eventuale disputa concernente i diritti di proprieta industriale e la tutela brevettuale dei dati relativi all'AIC dei medicinali e, pertanto, l'Agenzia non puo essere ritenuta responsabile in alcun modo di eventuali violazioni da parte del titolare dell'autorizzazione all'immissione in commercio (o titolare AIC)."""
    remove_watermark_from_single_pdf("watermark_2309033.pdf",[waterMarkTextStarting, new_watermarkTextStarting])
    pass
if __name__ == "__main__":
    main()
