import os

import psycopg
from flask import Flask, jsonify, render_template


app = Flask(__name__)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://votingapp:votingapp@localhost:5432/votingapp"
)


def get_results():

    query = """
        SELECT
            option,
            COUNT(*) AS total
        FROM votes
        GROUP BY option
        ORDER BY option;
    """

    results = {
        "cats": 0,
        "dogs": 0
    }

    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            cursor.execute(query)

            for option, total in cursor.fetchall():
                results[option] = total

    return results


@app.get("/")
def home():

    try:
        results = get_results()

        return render_template(
            "result.html",
            cats=results["cats"],
            dogs=results["dogs"]
        )

    except Exception:
        return "Database unavailable", 503


@app.get("/api/results")
def api_results():

    try:
        results = get_results()

        return jsonify(results), 200

    except Exception:
        return jsonify({
            "error": "Database unavailable"
        }), 503


@app.get("/health")
def health():

    try:

        with psycopg.connect(
            DATABASE_URL,
            connect_timeout=3
        ):
            pass

        return jsonify({
            "status": "UP",
            "database": "UP"
        }), 200

    except Exception:

        return jsonify({
            "status": "DOWN",
            "database": "DOWN"
        }), 503


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001
    )