import json
import requests
import pandas as pd
from dotenv import load_dotenv
import yfinance as yf


def fetch_quarterly_financial_data_yf(ticker_symbol: str) -> dict:
    '''
    Fetch historical quarterly financial statements (income sheet, balance sheet) for a company using Yahoo Finance.
    '''
    stock = yf.Ticker(ticker_symbol)

    # Get quarterly balance sheet, income statement
    income_statement = stock.quarterly_financials.T
    balance_sheet = stock.quarterly_balance_sheet.T

    if income_statement.empty or balance_sheet.empty:
        print(f"No data available for {ticker_symbol}")
        return None

    # Convert date indices to string
    income_statement.index = income_statement.index.astype(str)
    balance_sheet.index = balance_sheet.index.astype(str)

    # Convert to dictionary format for JSON representation
    financial_data: dict = {
        "ticker_symbol": ticker_symbol,
        "income_statement": income_statement.to_dict(),
        "balance_sheet": balance_sheet.to_dict()
    }

    return financial_data


def competitors_quarterly_revenue_yf(competitor_ticker_symbols: list) -> list:
    '''
    Fetch financial data for all competitors and combine them into a single DataFrame.
    '''
    competitor_data: list = []

    for symbol in competitor_ticker_symbols:
        data = fetch_quarterly_financial_data_yf(symbol)

        if data:
            competitor_data.append(data)

    print(competitor_data)
    return competitor_data
