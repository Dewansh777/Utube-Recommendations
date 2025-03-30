from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

def get_service():
    """Build and return a YouTube API service object."""
    return build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)

def search_videos(topic, max_results=config.MAX_RESULTS):
    """
    Search for videos related to a topic and return top videos by viewCount.
    
    Args:
        topic (str): The topic to search for
        max_results (int): Maximum number of results to return
        
    Returns:
        list: List of video data dictionaries
    """
    try:
        # Create YouTube API service
        youtube = get_service()
        
        # First, search for videos with the topic
        search_response = youtube.search().list(
            q=topic,
            part='id',
            maxResults=50,  # Get more results to filter by view count
            type='video',
            relevanceLanguage='en',
            order='relevance'  # Start with relevant videos
        ).execute()
        
        # Get video IDs from search results
        video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
        
        if not video_ids:
            return []
            
        # Get detailed information about the videos including view count
        videos_response = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids)
        ).execute()
        
        # Process and sort videos by view count
        videos = []
        for item in videos_response.get('items', []):
            # Sometimes videos don't have view counts
            view_count = int(item['statistics'].get('viewCount', 0))
            
            videos.append({
                'id': item['id'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'channel': item['snippet']['channelTitle'],
                'view_count': view_count,
                'url': f"https://www.youtube.com/watch?v={item['id']}"
            })
        
        # Sort by view count (descending) and return top results
        sorted_videos = sorted(videos, key=lambda x: x['view_count'], reverse=True)
        return sorted_videos[:max_results]
        
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []