from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def scrape_website_content(url: str):
    """
    Scrapes the text content of a given URL.
    Use this when the user asks for information about a particular website or live news.
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:2000]
    except Exception as e:
        return f"Error scraping the site: {str(e)}"
