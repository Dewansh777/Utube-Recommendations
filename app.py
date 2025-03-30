from flask import Flask, jsonify, request
from flask_cors import CORS
import youtube_services
import config
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Return top videos for a given topic from JSON input."""

    # Get JSON data from request
    data = request.get_json()

    # Check if topic is provided in JSON
    if not data or 'topic' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing topic in request JSON'
        }), 400

    topic = data['topic']

    if not config.YOUTUBE_API_KEY:
        return jsonify({
            'success': False,
            'error': 'YouTube API key not configured'
        }), 500

    videos = youtube_services.search_videos(topic)

    return jsonify({
        'success': True,
        'topic': topic,
        'count': len(videos),
        'videos': videos
    })

@app.route('/api/health', methods=['HEAD'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'YouTube Recommender API'
    })

if __name__ == '__main__':
    # Use environment port with a fallback to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)