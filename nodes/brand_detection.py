# AtomBerg/nodes/brand_detection.py
import re
from state import SoVState

# Define your tracked brands here
BRANDS = ["Atomberg", "Havells", "Crompton", "Orient", "Usha", "Polycab"]

def brand_detection_node(state: SoVState) -> SoVState:
    """
    Counts brand mentions in all documents and updates state.brand_mentions.
    """
    brand_counts = {brand: 0 for brand in BRANDS}

    for doc in state.documents:
        content_lower = doc.page_content.lower()
        for brand in BRANDS:
            if re.search(rf"\b{brand.lower()}\b", content_lower):
                brand_counts[brand] += 1

    state.brand_mentions = brand_counts
    return state
