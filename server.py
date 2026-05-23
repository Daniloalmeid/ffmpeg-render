import time
import subprocess
import uuid
import json
import os

DB_FILE = "jobs.json"


# -------------------------
# CARREGAR JOBS
# -------------------------
def load_jobs():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


# -------------------------
# SALVAR JOBS
# -------------------------
def save_jobs(jobs):
    with open(DB_FILE, "w") as f:
        json.dump(jobs, f)


# -------------------------
# PEGAR JOB QUEUED
# -------------------------
def pegar_job_queued(jobs):
    for job_id, job in jobs.items():
        if job["status"] == "queued":
            return job_id, job
    return None, None


# -------------------------
# PROCESSAR FFMPEG
# -------------------------
def processar(job_id, job, jobs):
    try:
        jobs[job_id]["status"] = "processing"
        save_jobs(jobs)

        output = f"/tmp/{job_id}.mp4"

        cmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", job["image"],
            "-i", job["audio"],
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

        jobs[job_id]["status"] = "done"
        jobs[job_id]["video"] = output
        save_jobs(jobs)

        print(f"Job {job_id} finalizado")

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        save_jobs(jobs)


# -------------------------
# WORKER LOOP
# -------------------------
print("FFmpeg worker iniciado...")

while True:
    jobs = load_jobs()

    job_id, job = pegar_job_queued(jobs)

    if job_id:
        print(f"Processando job {job_id}")
        processar(job_id, job, jobs)

    time.sleep(2)