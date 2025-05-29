from waterMarkRemover import remove_watermark_from_single_pdf
from ImageToText import extract_sections_from_text, pdf_to_text
import os
import shutil
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel



app = FastAPI()

INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

waterMarkTextStarting = "Agenzia Italiana del Farmaco"
new_watermarkTextStarting = """Documento reso disponibile da AIFA il 03/01/2025
Esula dalla competenza dell'AIFA ogni eventuale disputa concernente i diritti di proprieta industriale e la tutela brevettuale dei dati relativi all'AIC dei medicinali e, pertanto, l'Agenzia non puo essere ritenuta responsabile in alcun modo di eventuali violazioni da parte del titolare dell'autorizzazione all'immissione in commercio (o titolare AIC)."""
watermarks = [waterMarkTextStarting, new_watermarkTextStarting  ]

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

class PDFUrlRequest(BaseModel):
    url: str

@app.post("/process_pdf")
async def process_pdf(request: PDFUrlRequest):
    try:
        pdf_url = request.url
        filename = os.path.basename(pdf_url.split("?")[0])
        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"
        input_path = os.path.join(INPUT_FOLDER, filename)
        print(f"Downloading PDF from {pdf_url} to {input_path}")
        # Download PDF
        with requests.get(pdf_url, stream=True, timeout=15) as r:
            r.raise_for_status()
            with open(input_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)

        print("Processing PDF to remove watermark...")
        # Remove watermark
        remove_watermark_from_single_pdf(input_path, watermarks)
        filename_only = os.path.basename(input_path)
        # Convert PDF to text
        text = pdf_to_text("output/" + filename_only)
        # process the text to extract sections
        extract_sections_from_text(text, sections)


        # extract_sections_from_text returns a dictionary, so return it as JSON
        sections_dict = extract_sections_from_text(text, sections)
        return JSONResponse(content={
            "message": "PDF downloaded successfully",
            "file_path": input_path,
            "data": sections_dict
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error downloading PDF: {str(e)}")
