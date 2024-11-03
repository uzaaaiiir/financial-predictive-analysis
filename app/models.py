from pydantic import BaseModel
from typing import List


class ForecastRequest(BaseModel):
    website_url: str
    company_description: str = ""
    historic_revenue: List[float] = None
    fixed_cost: float = None
    variable_cost: float = None
    gross_margin: float = None
    operating_margin: float = None
    net_margin: float = None
    current_ratio: float = None
    quick_ratio: float = None
    capital_raise: float = None
    expected_return: float = None
