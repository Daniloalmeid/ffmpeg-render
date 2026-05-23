import time
import requests
import subprocess

API = "https://videoapi-d0wx.onrender.com"

def get_job():
    r = requests.get(f"{API}/job/queued")
    return r.json()

def process(job):
    if not job:
        return

    image = job["image"]
    audio = job["audio"]

    output = "/tmp/output.mp4"

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

    subprocess.run(cmd, check=True)

    requests.post(f"{API}/job/done", json={
        "job_id": job["job_id"],
        "video": output
    })

while True:
    job = get_job()

    if job:
        process(job)

    time.sleep(5)