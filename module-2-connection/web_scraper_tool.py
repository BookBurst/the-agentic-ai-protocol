from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def scrape_website_content(url: str):
    """
    Scrapes the text content of a given URL to provide real-time data to the agent.
    Use this when the user asks for information about a particular website or live news.
    """
    # We perform a standard GET request to fetch the raw HTML data.
    # We wrap this in a try-block to catch network failures before they crash the agent.
    try:
        response = requests.get(url, timeout=10)
        # We use BeautifulSoup to strip away HTML tags and extract only the readable text.
        # This reduces token waste by removing headers, scripts, and styling info.
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        # We return a truncated version to stay within the context window limits.
        return text[:2000]
    except Exception as e:
        # We return the error as a string so the agent can reason about the failure.
        return f"Error scraping the site: {str(e)}"

# Why we use this logic:
# The docstring tells the LLM EXACTLY when to use this tool.
# The URL type hint (str) makes sure the LLM sends the correct data type.
