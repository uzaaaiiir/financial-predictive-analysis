import openai
import os

from app.models import ForecastRequest
from app.services.data_fetcher import competitors_quarterly_revenue_yf
from app.services.industry_classifier import find_competitors, infer_industry_from_content, scrape_website_content
from app.utils.format import format_financial_data_for_json
from app.logger import logger

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_forecasting_prompt(requestInformation: ForecastRequest):
    '''
    Generate a forecasting prompt for OpenAI.
    '''

    # Extract the company data from the request
    website_content: str = scrape_website_content(
        requestInformation.website_url)
    industry_information: str = infer_industry_from_content(website_content)
    logger.info(f"Industry information inferred: {industry_information}")

    # Extract competitor data
    competitors: list = find_competitors(website_content, industry_information)

    # Extract competitor data and format it for OpenAI
    competitor_data: dict = competitors_quarterly_revenue_yf(competitors)

    # Format data for OpenAPI (as JSON)
    competitor_data_json: str = format_financial_data_for_json(competitor_data)

    prompt: str = f"""
    You are an experienced financial analyst specializing in predictive analysis for small-to-medium businesses.
    Here is the financial data for the target company's competitors, including quarterly balance sheets and income statements. Use this data to project future revenues for the next five years for the target company, considering industry trends.

    Predictive Analysis Steps:
    1. Data Preparation:
      - Review historical revenue data & ratios for the target company (see details below) and its competitors, particularly focusing on revenue growth.
    2. Forecast:
      - Use an appropriate Machine Learning and time-series model to project revenue trends over the next five years. Providing projections in quarterly increments (Q1, Q2, Q3, Q4) as a well-formatted, readable, table.
      - The model used must be sophisticed enough to take into consideration competitor data to project the revenue for the target company.
      - Use advanced machine learning models to perform the forecasting.
    3. Strategic Breakdown
      - Provide a breakdown of the steps taken and the model used to perform the predictive analysis.
      - Highlight critical insights (e.g., expected break-even point, impact of growth rate changes).
      - Recommend action steps for liquidity management, cost efficiency, or growth strategies.

    Target Company Data:
    Industry Information for the target company: {industry_information}
    Website Content or Description: {website_content}
    Historic Revenue: {requestInformation.historic_revenue}
    Fixed Costs: {requestInformation.fixed_cost}
    Variable Costs: {requestInformation.variable_cost}
    Gross Margin: {requestInformation.gross_margin}
    Operating Margin: {requestInformation.operating_margin}
    Net Margin: {requestInformation.net_margin}
    Current Ratio: {requestInformation.current_ratio}
    Quick Ratio: {requestInformation.quick_ratio}
    Capital Raise: {requestInformation.capital_raise}
    Expected Return: {requestInformation.expected_return}

    Competitors: {competitors}
    Competitor Financial Data: {competitor_data_json}

    Please analyze this data and provide a revenue forecast for the target company over the next 5 years. Return the analysis in a structured format in markdown.
    """

    return prompt


def generate_predictive_analysis(prompt: str) -> str:
    '''
    Perform analysis using OpenAI.
    '''
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        top_p=1,
        messages=[
            {"role": "system", "content": "You are an experienced financial analyst specializing in predictive analysis for small-and-medium sized businesses that have limited financial data."},
            {"role": "user", "content": prompt}
        ]
    )

    logger.info("Generated predictive analysis.")

    return response.choices[0].message.content.strip()
