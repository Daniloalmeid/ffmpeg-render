while True:
    job = pegar_job_queued()

    if job:
        atualizar_status("processing")

        rodar_ffmpeg(job)

        atualizar_status("done")

    sleep(2)