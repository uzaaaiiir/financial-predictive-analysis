import openai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

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
    anchor_texts = [a.get_text() for a in soup.find_all('a')]
    anchor_links = [a['href'] for a in soup.find_all('a', href=True)]

    page_content = ' '.join(headings + paragraphs +
                            alt_texts + anchor_links) + meta_info

    # Write to file
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(page_content)

    return page_content


def infer_industry_from_content(content):
    '''
    Using ChatGPT to determine the industry and additional industry information based on website content.
    '''
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an industry classifier. You will be given content derived from the website of a company using Beautiful Soup. Based on this content, determine what the industry of this company is. This information will be used to find competitors. Data of the competitors will be extracted and used to project future revenue, project future company members, project future marketing, and eventually produce a predictive analysis."},
            {"role": "user", "content": content},
        ]
    )

    return response.choices[0].message


def find_competitors(url: str) -> list:
    '''
    Function retrieves website content for a company. The content is used to infer the industry information. 
    After this, the potential competitors in this industry are found using ChatGPT and returned as a comma-separated list of ticker-symbols. 
    '''

    website_content = scrape_website_content(url)
    industry_information = infer_industry_from_content(website_content)

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI trained to provide competitors for small and medium sized businesses. Based no the company's industry and description, list publicly-traded companies who are competitors. This competitor list will be used to conduct a predictive analysis that finds the projected revenue, marketing and more for the competitors. These will be used to perform the predictive analysis for the target company."},
            {"role": "user",
                "content": f"This is the company industry information: {industry_information}. This is the information scraped from the website: {website_content}. \n\nPlease provide ONLY publicly-traded competitors for this company. Omit any private companies. Only provide the ticker symbol for each competitor separated by commas (Example: BMBL, META, PINS)."},
        ]
    )

    return response.choices[0].message.content.split(', ')


print(find_competitors("https://www.vibeup.io/"))
