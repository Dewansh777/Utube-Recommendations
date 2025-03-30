import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# YouTube API configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# API configurations
MAX_RESULTS = 5