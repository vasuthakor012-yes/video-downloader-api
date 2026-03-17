from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Video Downloader API is Running!"

@app.route('/get-video', methods=['GET'])
def get_video():
    url = request.args.get('url')

    if not url:
        return jsonify({'success': False, 'error': 'URL missing'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'format': 'best[ext=mp4]/best',
            # ✅ YouTube Bot Detection Fix
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
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
