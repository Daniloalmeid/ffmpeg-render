FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg curl

WORKDIR /app

COPY . .

RUN pip install flask

EXPOSE 10000

CMD ["python", "server.py"]