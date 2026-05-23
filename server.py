import time
import subprocess

jobs = {}  # ⚠️ aqui só funciona se for DB (vou explicar abaixo)

def pegar_job_queued():
    for job_id, job in jobs.items():
        if job["status"] == "queued":
            return job_id, job
    return None, None


def processar(job_id, job):
    jobs[job_id]["status"] = "processing"

    output = f"/tmp/{job_id}.mp4"

    subprocess.run([
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", job["image"],
        "-i", job["audio"],
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-shortest",
        output
    ])

    jobs[job_id]["status"] = "done"
    jobs[job_id]["video"] = output


while True:
    job_id, job = pegar_job_queued()

    if job_id:
        processar(job_id, job)

    time.sleep(2)