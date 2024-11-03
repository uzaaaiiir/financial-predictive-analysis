from fastapi import APIRouter, Response, HTTPException
from app.models import ForecastRequest
from app.services.forecasting import generate_forecasting_prompt, generate_predictive_analysis


router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "Welcome to QInvst Automation Tool for Predictive Forecasting"}


@router.post("/forecast")
async def forecast(request: ForecastRequest):
    if (request.website_url is None):
        raise HTTPException(
            status_code=400, detail="Website URL or Company Description are required to forecast revenue.")

    try:
        prompt = generate_forecasting_prompt(request)
        forecast = generate_predictive_analysis(prompt)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while generating the forecast: {e}")

    return Response(forecast, media_type="text/markdown", headers={"Content-Disposition": "attachment; filename = report.md"})
