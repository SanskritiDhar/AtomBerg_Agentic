from langgraph.graph import StateGraph
#from state import SoVState

from typing import List, Dict
from langchain.schema import Document
from pydantic import BaseModel
from typing import Optional, Dict,Any

class SoVState(BaseModel):
    query: str
    documents: List[Document] = []
    brand_mentions: Dict[str, int] = {}
    sentiment_scores: Dict[str, Dict[str, int]] = {}
    sov_results: Dict[str, float] = {}
    positive_sov_results: Dict[str, float] = {}
    negative_sov_results: Dict[str, float] = {}
    engagement_sov_results: Dict[str, float] = {}
    platform_sov_results: Dict[str, Dict[str, float]] = {}
    time_sov_results: Dict[str, float] = {}
   # hybrid_sov_results: Optional[Dict[str, Dict[str, float]]] = None
   # platform_insights: Optional[Dict[str, Any]] = None


# Import all nodess
from nodes.search_youtube import search_youtube_node
from nodes.search_google import search_google_node
from nodes.search_instagram import search_instagram_node
from nodes.search_facebook import search_facebook_node
from nodes.brand_detection import brand_detection_node
from nodes.sentiment_analysis import sentiment_analysis_node
from nodes.sov_calculation_multi import sov_calculation_node
from nodes.report_generation import report_node

graph = StateGraph(SoVState)

graph.add_node("youtube_search", search_youtube_node)
graph.add_node("google_search", search_google_node)
graph.add_node("instagram_search", search_instagram_node)
graph.add_node("facebook_search", search_facebook_node)
graph.add_node("brand_detection", brand_detection_node)
graph.add_node("sentiment_analysis", sentiment_analysis_node)
graph.add_node("sov_calc", sov_calculation_node)
graph.add_node("report", report_node)

# Link nodes in order
graph.set_entry_point("youtube_search")
graph.add_edge("youtube_search", "google_search")
graph.add_edge("google_search", "instagram_search")
graph.add_edge("instagram_search", "facebook_search")
graph.add_edge("facebook_search", "brand_detection")
graph.add_edge("brand_detection", "sentiment_analysis")
graph.add_edge("sentiment_analysis", "sov_calc")
graph.add_edge("sov_calc", "report")

app = graph.compile()

if __name__ == "__main__":
    brands = {b: 0 for b in [ "Havells", "Crompton", "Orient", "Usha", "Polycab"]}
    state = SoVState(query="Comparsion smart fan in India  Atomberg vs ", brand_mentions=brands)
    app.invoke(state)



