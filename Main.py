from youtube_transcript_api import YouTubeTranscriptApi
import re
from together import Together
import os

def get_video_id(url):
    match = re.search(r"(?:https?:\/\/(?:www\.)?youtube\.com\/(?:[^\/]+\/[^\?\/]+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def summarize_transcript(transcript):
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("API key not found")
    
    client = Together(api_key=api_key)

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[
            {"role": "system", "content": "User provided a YouTube URL. Code generated a transcript using the YouTube API. Summarize this video."},
            {"role": "user", "content": transcript}
        ]
    )

    return response.choices[0].message.content

url = input("Enter YouTube URL: ").strip()
if not url:
    raise ValueError("URL cannot be empty.")

try:
    video_id = get_video_id(url)
except Exception as e:
    print(f"Invalid URL: {e}")
    exit()

try:
    raw_transcript = YouTubeTranscriptApi.get_transcript(video_id)
except Exception as e:
    print(f"Failed to retrieve transcript: {e}")
    exit()

final_transcript = " ".join([entry['text'] for entry in raw_transcript])

print(summarize_transcript(transcript=final_transcript))
