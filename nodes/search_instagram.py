# nodes/search_instagram.py
import os
import requests
from langchain.schema import Document
from state import SoVState
from dotenv import load_dotenv

load_dotenv()
IG_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

def search_instagram_node(state: SoVState) -> SoVState:
    hashtag = state.query.replace(" ", "")
    url = f"https://graph.facebook.com/v17.0/ig_hashtag_search?user_id=YOUR_USER_ID&q={hashtag}&access_token={IG_TOKEN}"
    resp = requests.get(url).json()
    if "data" not in resp:
        return state

    hashtag_id = resp["data"][0]["id"]
    media_url = f"https://graph.facebook.com/v17.0/{hashtag_id}/top_media?user_id=YOUR_USER_ID&fields=caption,permalink,like_count,comments_count&access_token={IG_TOKEN}"
    media = requests.get(media_url).json()

    for post in media.get("data", []):
        caption = post.get("caption", "")
        link = post.get("permalink", "")
        likes = post.get("like_count", 0)
        comments = post.get("comments_count", 0)
        state.documents.append(Document(
            page_content=caption,
            metadata={
                "platform": "Instagram",
                "url": link,
                "views": 0,
                "likes": likes,
                "comments_count": comments
            }
        ))
    return state
