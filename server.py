from flask import Flask, request, jsonify
import uuid
import threading
import os
import subprocess

app = Flask(__name__)

JOBS = {}

# ---------------------------
# FUNÇÃO FFmpeg (background)
# ---------------------------
def run_ffmpeg(job_id):
    job = JOBS[job_id]

    image = job["image"]
    audio = job["audio"]

    output = f"/tmp/{job_id}.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image,
        "-i", audio,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-r", "30",
        "-s", "1080x1920",
        output
    ]

    try:
        job["status"] = "processing"

        subprocess.run(cmd, check=True)

        job["status"] = "done"
        job["output"] = output

    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)


# ---------------------------
# CRIAR JOB (n8n chama isso)
# ---------------------------
@app.route("/render", methods=["POST"])
def render():
    data = request.json

    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "status": "queued",
        "image": data.get("image"),
        "audio": data.get("audio"),
        "output": None
    }

    # roda FFmpeg em background
    thread = threading.Thread(target=run_ffmpeg, args=(job_id,))
    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "queued"
    })


# ---------------------------
# CONSULTAR STATUS
# ---------------------------
@app.route("/status/<job_id>", methods=["GET"])
def status(job_id):
    return jsonify(JOBS.get(job_id, {"error": "not found"}))


# ---------------------------
# HOME
# ---------------------------
@app.route("/")
def home():
    return "FFmpeg API OK"


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))