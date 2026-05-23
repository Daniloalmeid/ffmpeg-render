from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route("/render", methods=["POST"])
def render():
    data = request.json

    image = data["image"]
    audio = data["audio"]

    output = "/tmp/output.mp4"

    cmd = f'''
ffmpeg -y \
-loop 1 -i "{image}" \
-i "{audio}" \
-c:v libx264 -tune stillimage \
-c:a aac -b:a 192k \
-pix_fmt yuv420p \
-shortest \
-r 30 \
-s 1080x1920 \
"{output}"
'''

    os.system(cmd)

    return send_file(output, mimetype="video/mp4")


app.run(host="0.0.0.0", port=10000)