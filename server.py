from flask import Flask, request, send_file
import os
import uuid

app = Flask(__name__)

@app.route("/render", methods=["POST"])
def render():
    data = request.json

    image = data["image"]
    audio = data["audio"]

    output = f"/tmp/{uuid.uuid4()}.mp4"

    cmd = f"""
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
"""

    result = os.system(cmd)

    if result != 0:
        return {"error": "ffmpeg failed"}, 500

    return send_file(output, mimetype="video/mp4")


# 🔥 IMPORTANTE: Render precisa disso
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))