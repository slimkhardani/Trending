from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Function to get top 10 songs from YouTube
def get_top_songs(artist, api_key):
    # Use YouTube API to get search results
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={artist}&type=video&key={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)

    # Extract video IDs and view counts
    videos = []
    for item in data["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        view_count = get_view_count(video_id, api_key)
        if view_count is None:
            continue
        videos.append((title, view_count, video_id))

    # Sort videos by view count and return top 10
    videos.sort(key=lambda x: x[1], reverse=True)
    return videos[:10]

# Function to get view count of a video
def get_view_count(video_id, api_key):
    # Use YouTube API to get video information
    url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)

    if 'items' not in data or len(data['items']) == 0:
        print(f"Error: data does not contain video information for video_id {video_id}")
        return None

    view_count = int(data["items"][0]["statistics"]["viewCount"])
    return view_count

# Route to render HTML template
@app.route('/')
def index():
    return render_template("index.html")

# Route to handle form submission and return search results
@app.route('/search', methods=['POST'])
def search():
    artist = request.form['artist']
    api_key = 'AIzaSyCuW0ydojIqqjmtqw54ZQdODj-JwdfVtsE'  # Replace with your YouTube API key
    songs = get_top_songs(artist, api_key)
    return jsonify(songs)

if __name__ == "__main__":
    app.run(debug=True)
