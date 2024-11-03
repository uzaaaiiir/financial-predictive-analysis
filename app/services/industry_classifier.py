import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from app.logger import logger

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def scrape_website_content(url):
    '''
    Scrape relevant content from a website that can be used to determine the industry a company belongs to.
    '''
    # Send a request to a website
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    for script in soup(['script', 'style']):
        script.extract()  # remove unnecessary tags

    # Retrieve any meta-data
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})

    meta_info = ''
    if meta_description:
        meta_info += meta_description['content']
    if meta_keywords:
        meta_info += " " + meta_keywords['content']

    # Retrieve any text data that could be useful: headings, paragrams, alt_texts, etc
    headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    alt_texts = [img['alt'] for img in soup.find_all('img', alt=True)]
    anchor_links = [a['href'] for a in soup.find_all('a', href=True)]

    page_content = ' '.join(headings + paragraphs +
                            alt_texts + anchor_links) + meta_info

    logger.info(f"Scraped website content: {url}")
    return page_content


def infer_industry_from_content(content):
    '''
    Using OpenAI to determine the industry based on the website content.
    '''
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an industry classifier. You will be given content derived from the website of a company using Beautiful Soup. Based on this content, determine what the industry of this company is. This information will be used to find competitors. Data of the competitors will be extracted and used to project future revenue, project future company members, project future marketing, and eventually produce a predictive analysis."},
            {"role": "user", "content": content},
        ]
    )

    return response.choices[0].message


def find_competitors(website_content: str, industry_information: str) -> list:
    '''
    Retrieves website content of a company, infers the industry, and uses OpenAI to find competitors. Competitors are returned as a comma-separated list of ticker-symbols.
    '''

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI trained to provide publicly-traded competitors for a company. Based on the company's industry and description, list the ticker symbols of publicly-traded competitors. This competitor list will be used to conduct a predictive analysis for a target company."},
            {"role": "user",
                "content": f"Company industry information: {industry_information}.\nWebsite Content: {website_content}.\n\nPlease provide ONLY publicly-traded competitors for this company. Only provide the ticker symbol for each competitor separated by commas (Example: BMBL, META, PINS, SHOP, AMZN)."},
        ]
    )

    competitors_raw = response.choices[0].message.content

    # Debug: print the raw response from OpenAI to see what it returns
    logger.info(f"Raw OpenAI response: {competitors_raw}")

    ticker_symbols = competitors_raw.split(", ")

    # Debug: print the ticker symbols extracted
    logger.info(f"Extracted ticker symbols: {ticker_symbols}")

    return ticker_symbols
