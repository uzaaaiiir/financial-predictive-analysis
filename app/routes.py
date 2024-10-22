from fastapi import APIRouter, File, UploadFile
import shutil

import pandas as pd
from .services.parser import extract_data_from_excel, extract_text_from_pdf, find_financial_data
from .services.industry_classifier import find_competitors
from .services.fin_data_fetcher import competitors_quarterly_revenue, export_to_excel


router = APIRouter()


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploaded_files/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    content = None
    if file.filename.endswith(".pdf"):
        content = extract_text_from_pdf(file_location)

    fin_data = find_financial_data(content)

    return {"filename": file.filename, "financial_data": fin_data}


@router.post("/comp_revenue")
async def classify(url: str):
    # Find Competitors
    competitors_ticker_symbols: list = find_competitors(url)

    # Get quarterly revenue data
    combined_revenue_data: pd.DataFrame = competitors_quarterly_revenue(
        competitors_ticker_symbols)

    # Export data to Excel sheet
    export_to_excel(combined_revenue_data)
    return
