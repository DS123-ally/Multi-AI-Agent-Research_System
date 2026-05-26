from langchain.tools import tool
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
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
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            )
            page = context.new_page()
            
            # Navigate and wait for network idle to ensure JS loads
            page.goto(url, timeout=15000, wait_until="networkidle")
            html_content = page.content()
            browser.close()

        soup = BeautifulSoup(html_content, "html.parser")
       
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text

    except Exception as e:
        return f"Could not scrape the URL: {str(e)}"



