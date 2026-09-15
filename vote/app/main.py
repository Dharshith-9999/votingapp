import os
import uuid
import json

import redis
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "votes")


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/votes")
def cast_vote():

    data = request.get_json(silent=True) or {}

    option = data.get("option")
    voter_id = data.get("voter_id")

    if option not in ("cats", "dogs"):
        return jsonify({
            "error": "Invalid voting option"
        }), 400

    if not voter_id:
        voter_id = str(uuid.uuid4())

    try:
        uuid.UUID(voter_id)
    except ValueError:
        return jsonify({
            "error": "Invalid voter_id"
        }), 400

    vote = {
        "voter_id": voter_id,
        "option": option
    }

    redis_client.rpush(
        REDIS_QUEUE,
        json.dumps(vote)
    )

    return jsonify({
        "message": "Vote accepted",
        "voter_id": voter_id,
        "option": option
    }), 202


@app.get("/health")
def health():
    return jsonify({
        "status": "UP"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
