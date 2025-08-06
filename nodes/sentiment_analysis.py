# AtomBerg/nodes/sentiment_analysis.py
from state import SoVState
import torch
from transformers import pipeline
import re

# Load sentiment model once
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def sentiment_analysis_node(state: SoVState) -> SoVState:
    """
    Performs sentiment analysis for each brand mention and updates state.sentiment_scores.
    """
    sentiment_results = {brand: {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0} 
                         for brand in state.brand_mentions}

    for doc in state.documents:
        content_lower = doc.page_content.lower()
        for brand in state.brand_mentions:
            if re.search(rf"\b{brand.lower()}\b", content_lower):
                result = sentiment_model(doc.page_content[:512])[0]
                label = result["label"].upper()
                if label not in sentiment_results[brand]:
                    label = "NEUTRAL"  # fallback if model returns something else
                sentiment_results[brand][label] += 1

    state.sentiment_scores = sentiment_results
    return state
