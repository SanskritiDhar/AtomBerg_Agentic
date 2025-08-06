# nodes/search_facebook.py
import os
import requests
from langchain.schema import Document
from state import SoVState
from dotenv import load_dotenv

load_dotenv()
FB_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

def search_facebook_node(state: SoVState) -> SoVState:
    print("[Facebook] Starting Facebook data collection...")
    if not FB_TOKEN:
        print("[Facebook] ❌ Missing Facebook access token.")
        return state

    url = (
        f"https://graph.facebook.com/v17.0/me/feed"
        f"?fields=message,permalink_url,likes.summary(true),comments.summary(true)"
        f"&access_token={FB_TOKEN}"
    )

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[Facebook] ❌ Error fetching posts: {e}")
        return state

    added = 0
    for post in data.get("data", []):
        text = post.get("message", "")
        if not text:
            continue

        # Optional: Filter for brand keywords to reduce noise
        if not any(brand.lower() in text.lower() for brand in state.brand_mentions.keys()):
            continue

        link = post.get("permalink_url", "")
        likes = post.get("likes", {}).get("summary", {}).get("total_count", 0)
        comments = post.get("comments", {}).get("summary", {}).get("total_count", 0)

        doc = Document(
            page_content=text,
            metadata={
                "platform": "Facebook",
                "url": link,
                "views": 0,
                "likes": likes,
                "comments_count": comments
            }
        )
        state.documents.append(doc)
        added += 1

    print(f"[Facebook] ✅ Added {added} relevant Facebook posts.")
    return state
