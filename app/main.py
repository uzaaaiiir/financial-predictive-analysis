from fastapi import FastAPI
from .routes import router


app = FastAPI(
    title="QInvst Automation Tool for Predictive Forecast",
    description="This is a tool to automate the financial data extraction, competitor analysis, and revenue forecasting for a target company.",
    version="0.1.0"

)

app.include_router(router)
