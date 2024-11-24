from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # Set up download options
            ydl_opts = {
                'format': 'best[ext=mp4]',  # Download the best quality video in MP4
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to downloads folder with title as filename
            }
            
            # Download the video using yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info['title']
                file_path = f"downloads/{video_title}.mp4"

            # Send the file to the user
            return send_file(file_path, as_attachment=True)

        except Exception as e:
            return render_template('index.html', error=f"Error: {str(e)}")

    return render_template('index.html', error=None)

if __name__ == '__main__':
    os.makedirs("downloads", exist_ok=True)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)))
