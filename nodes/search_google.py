# nodes/search_google.py
import os
from langchain.schema import Document
from state import SoVState
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_google_node(state: SoVState) -> SoVState:
    """
    Searches Google via Tavily API and stores results in state.documents
    """
    tavily_search = TavilySearchResults(max_results=10)
    results = tavily_search.run(state.query)  # returns list of dicts

    for r in results:
        title = r.get("title", "")
        snippet = r.get("content", "")
        link = r.get("url", "")

        state.documents.append(Document(
            page_content=f"{title}\n{snippet}",
            metadata={
                "platform": "Google",
                "url": link,
                "views": 0,
                "likes": 0,
                "comments_count": 0
            }
        ))
    return state
