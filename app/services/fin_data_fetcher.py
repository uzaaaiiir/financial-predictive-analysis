import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


def fetch_quarterly_financial_data(ticker_symbol: str) -> pd.DataFrame:
    '''
    Fetch historical financial data (revenue, expenses, etc.) for a company using its stock symbol.
    '''
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={
        ticker_symbol}&apikey={ALPHA_VANTAGE_API_KEY}'

    response = requests.get(url)

    if (response.status_code == 200):
        data = response.json()
        if ("quarterlyReports" in data):
            df = pd.DataFrame(data["quarterlyReports"])
            df = df[['fiscalDateEnding', 'totalRevenue']]
            df['fiscalDateEnding'] = pd.to_datetime(df['fiscalDateEnding'])
            df['totalRevenue'] = pd.to_numeric(
                df['totalRevenue'], errors='coerce')
            df['symbol'] = ticker_symbol
            return df
        else:
            print(f"No data available for {ticker_symbol}")
            return None
    else:
        print(
            f"Failed to fetch data for {ticker_symbol}. Status code: {response.status_code}")
        return None


def competitors_quarterly_revenue(competitor_ticker_symbols: list) -> pd.DataFrame:
    '''
    Function finds the revenue of all competitors in a list and combines them into a data frame which is indexed by the quarter. 
    '''
    combined_rev_data = pd.DataFrame()

    for symbol in competitor_ticker_symbols:
        rev_data = fetch_quarterly_financial_data(symbol)
        if rev_data is not None:
            rev_data = rev_data.rename(columns={'totalRevenue': symbol})

            # Set quarter as the index
            rev_data.set_index('fiscalDateEnding', inplace=True)

            # Combine data into main DataFrame
            if combined_rev_data.empty:
                combined_rev_data = rev_data[[symbol]]
            else:
                combined_rev_data = combined_rev_data.join(rev_data[[symbol]])

    combined_rev_data.index.name = "Quarter"

    # Convert rev data to numeric values
    for symbol in competitor_ticker_symbols:
        combined_rev_data[symbol] = pd.to_numeric(
            combined_rev_data[symbol], errors='coerce')

    return combined_rev_data


def export_to_excel(dataframe):
    '''
    Exports the data into an excel sheet.
    '''
    output_file = 'competitor_data.xlsx'
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        dataframe.to_excel(
            writer, sheet_name='Competitor Revenue His')

    print(f"Wrote data to {output_file}")

# Marketing (Historical) - pitch book
# How many customers? Revenue?
#
