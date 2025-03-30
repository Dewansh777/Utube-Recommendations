import googleapiclient.discovery
import config  
def search_videos(topic, min_duration=900): # 15 minutes = 900 seconds
    """Searches YouTube videos for a given topic and filters by duration."""

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=config.YOUTUBE_API_KEY)

    # Search for videos
    search_response = youtube.search().list(
        q=topic,
        part="id",
        maxResults=10, # Or whatever max results you wish.
        type="video",
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response.get("items", []) if item["id"].get("videoId")]

    # Retrieve video statistics and duration
    video_stats = []
    if video_ids:
        video_response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(video_ids)
        ).execute()

        for item in video_response.get("items", []):
            duration = item["contentDetails"]["duration"]
            duration_seconds = _parse_duration(duration)

            if duration_seconds >= min_duration:
                video_stats.append({
                    "title": item["snippet"]["title"],
                    "videoId": item["id"],
                    "viewCount": int(item["statistics"].get("viewCount", 0)),
                    "likeCount": int(item["statistics"].get("likeCount", 0)),
                    "duration": duration_seconds,
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                })

    return video_stats

def _parse_duration(duration):
    """Parses ISO 8601 duration format into seconds."""

    import re
    duration_regex = re.compile(r'PT((?P<hours>\d+)H)?((?P<minutes>\d+)M)?((?P<seconds>\d+)S)?')
    match = duration_regex.match(duration)

    if match:
        hours = int(match.group('hours') or 0)
        minutes = int(match.group('minutes') or 0)
        seconds = int(match.group('seconds') or 0)
        return hours * 3600 + minutes * 60 + seconds
    else:
        return 0