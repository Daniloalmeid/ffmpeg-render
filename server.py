from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route("/render", methods=["POST"])
def render():
    data = request.json

    job_id = str(uuid.uuid4())

    image = data["image"]
    audio = data["audio"]

    # só simula ou inicia processo
    # NÃO bloqueia request

    return jsonify({
        "status": "processing",
        "job_id": job_id
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))