from collections import defaultdict
from state import SoVState

# Engagement calculation is now inside this file
def calculate_engagement(meta: dict) -> int:
    """
    Calculate an engagement score from metadata.
    Formula:
        views + (likes * 2) + (comments_count * 3)
    """
    views = int(meta.get("views", 0))
    likes = int(meta.get("likes", 0))
    comments = int(meta.get("comments_count", 0))
    return views + (likes * 2) + (comments * 3)

def sov_calculation_node(state: SoVState) -> SoVState:
    brands = list(state.brand_mentions.keys())

    # 1. Basic SoV
    total_mentions = sum(state.brand_mentions.values()) or 1
    state.sov_results = {b: (state.brand_mentions[b] / total_mentions) * 100 for b in brands}

    # 2. Engagement-Weighted SoV
    engagement_counts = defaultdict(int)
    total_engagement = 0
    for doc in state.documents:
        engagement = calculate_engagement(doc.metadata)
        for brand in brands:
            if brand.lower() in doc.page_content.lower():
                engagement_counts[brand] += engagement
                total_engagement += engagement
    state.engagement_sov_results = {
        b: (engagement_counts[b] / total_engagement) * 100 if total_engagement else 0
        for b in brands
    }

    # 3. Positive & Negative SoV
    total_pos = sum(v.get("POSITIVE", 0) for v in state.sentiment_scores.values()) or 1
    total_neg = sum(v.get("NEGATIVE", 0) for v in state.sentiment_scores.values()) or 1
    state.positive_sov_results = {
        b: (state.sentiment_scores[b].get("POSITIVE", 0) / total_pos) * 100 for b in brands
    }
    state.negative_sov_results = {
        b: (state.sentiment_scores[b].get("NEGATIVE", 0) / total_neg) * 100 for b in brands
    }

    # 4. Platform-wise SoV (restricted to 4 platforms)
    platforms = ["Facebook", "Instagram", "YouTube", "Google"]

        # --- DEBUG: Check Facebook & Instagram ingestion ---
    fb_ig_docs = [doc for doc in state.documents if doc.metadata.get("platform") in ["Facebook", "Instagram"]]
    print(f"[DEBUG] Facebook/Instagram Docs Found: {len(fb_ig_docs)}")

    for doc in fb_ig_docs:
        print(f"[DEBUG] Platform: {doc.metadata.get('platform')}, Content Snippet: {doc.page_content[:100]}")
        for brand in state.brand_mentions:
            if brand.lower() in doc.page_content.lower():
                print(f"[DEBUG] ✅ Brand '{brand}' mentioned in {doc.metadata.get('platform')}")

    platform_mentions = defaultdict(lambda: defaultdict(int))
    for doc in state.documents:
        platform = doc.metadata.get("platform", "unknown")
        for brand in brands:
            if brand.lower() in doc.page_content.lower():
                platform_mentions[platform][brand] += 1
    platform_sov = {}
    for platform in platforms:
        brand_counts = platform_mentions.get(platform, {})
        total_platform_mentions = sum(brand_counts.values()) or 1
        platform_sov[platform] = {
            b: (brand_counts.get(b, 0) / total_platform_mentions) * 100 for b in brands
        }
    state.platform_sov_results = platform_sov

    return state
