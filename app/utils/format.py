import pandas as pd
import json
from app.logger import logger


def format_financial_data_for_json(competitor_data: list) -> str:
    '''
    Format competitor financial data into JSON format for OpenAI.
    '''
    formatted_data = {
        "competitor_data": [competitor_data]
    }

    formatted_json: str = json.dumps(formatted_data, indent=4)
    logger.info(f"Formatted financial data for OpenAI.")
    return formatted_json
