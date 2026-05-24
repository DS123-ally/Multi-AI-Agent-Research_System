from langchain.tools import tool
from bs4 import BeautifulSoup
import requests
from tavily import TavilyClient
import sys
import os
from dotenv import load_dotenv

# UTF-8 support
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Initialize Tavily client
tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information.
    Returns titles, URLs, and snippets.
    """

    try:
        results = tavily.search(
            query=query,
            max_results=4
        )

        formatted_results = []

        for idx, result in enumerate(results["results"], start=1):

            title = result.get("title", "No Title")
            url = result.get("url", "No URL")
            snippet = result.get("content", "No Content")[:300]

            formatted_results.append(
                f"""
========================
Result {idx}
========================
Title   : {title}

URL     : {url}

Snippet :
{snippet}
"""
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Error: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a URL.
    """

    try:

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        resp = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            resp.text,
            "html.parser"
        )
       
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        return text[:2000]

    except Exception as e:
        return f"Could not scrape the URL: {str(e)}"



