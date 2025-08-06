# nodes/search_youtube.py
import os
from googleapiclient.discovery import build
from langchain.schema import Document
from state import SoVState
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_top_comments(video_id, max_comments=5):
    comments = []
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_comments,
            textFormat="plainText"
        ).execute()
        for item in response.get("items", []):
            comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
    except Exception as e:
        print(f"Could not fetch comments for {video_id}: {e}")
    return comments

def search_youtube_node(state: SoVState) -> SoVState:
    search_response = youtube.search().list(
        q=state.query,
        part="snippet",
        type="video",
        maxResults=10
    ).execute()

    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        video_data = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()["items"][0]

        stats = video_data.get("statistics", {})
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments_count = int(stats.get("commentCount", 0))
        title = video_data["snippet"]["title"]
        description = video_data["snippet"].get("description", "")

        comments = get_top_comments(video_id)
        full_text = f"{title}\n{description}\n" + "\n".join(comments)

        state.documents.append(Document(
            page_content=full_text,
            metadata={
                "platform": "YouTube",
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "views": views,
                "likes": likes,
                "comments_count": comments_count,
                "channel": video_data["snippet"]["channelTitle"]
            }
        ))
    return state
