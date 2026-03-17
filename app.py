from flask import Flask, request, jsonify
import yt_dlp
import os
import re

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Video Downloader API is Running!"

def normalize_url(url):
    # m.youtube.com → www.youtube.com
    url = re.sub(r'https?://m\.youtube\.com', 'https://www.youtube.com', url)
    # youtu.be short links ठीक करो
    url = re.sub(r'https?://youtu\.be/([a-zA-Z0-9_-]+)', r'https://www.youtube.com/watch?v=\1', url)
    return url

@app.route('/get-video', methods=['GET'])
def get_video():
    url = request.args.get('url')
    if not url:
        return jsonify({'success': False, 'error': 'URL missing'}), 400

    url = normalize_url(url)

    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'format': 'best[ext=mp4]/best',
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            'http_headers': {
                'User-Agent': 'com.google.ios.youtube/19.09.3 (iPhone14,3; U; CPU iOS 16_1 like Mac OS X)',
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'video')
            thumbnail = info.get('thumbnail', '')
            duration = info.get('duration', 0)

            return jsonify({
                'success': True,
                'video_url': video_url,
                'title': title,
                'thumbnail': thumbnail,
                'duration': duration
            })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
