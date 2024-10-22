from tika import parser
import pandas as pd
import re


def extract_text_from_pdf(file_path):
    parsed = parser.from_file(file_path)

    content = parsed['content']
    print(content)

    return content


def extract_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df


def find_financial_data(text):
    revenue_pattern = r"(revenue|income|sales|turnover):?\s?\$?(\d+[.,]?\d*)"
    expenses_pattern = r"(expenses|cost|invoice):?\s?\$?(\d+[.,]?\d*)"

    revenues = re.findall(revenue_pattern, text.lower())
    expenses = re.findall(expenses_pattern, text.lower())

    return {"revenues": revenues, "expenses": expenses}
