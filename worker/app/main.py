import json
import os
import time

import psycopg
import redis


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_QUEUE = os.getenv("REDIS_QUEUE", "votes")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://votingapp:votingapp@localhost:5432/votingapp"
)


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


def save_vote(vote):

    query = """
        INSERT INTO votes (
            voter_id,
            option
        )
        VALUES (%s, %s)
        ON CONFLICT (voter_id) DO NOTHING;
    """

    with psycopg.connect(DATABASE_URL) as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                query,
                (
                    vote["voter_id"],
                    vote["option"]
                )
            )

        connection.commit()


def process_vote(vote):

    if not isinstance(vote, dict):
        raise ValueError("Invalid vote payload")

    if "voter_id" not in vote:
        raise ValueError("Missing voter_id")

    if "option" not in vote:
        raise ValueError("Missing option")

    if vote["option"] not in ("cats", "dogs"):
        raise ValueError("Invalid option")

    save_vote(vote)


def run():

    print("Worker started")

    while True:

        try:

            message = redis_client.blpop(
                REDIS_QUEUE,
                timeout=5
            )

            if message is None:
                continue

            _, payload = message

            vote = json.loads(payload)

            process_vote(vote)

            print(
                f"Vote processed: {vote['voter_id']} "
                f"-> {vote['option']}"
            )

        except Exception as error:

            print(
                f"Error processing vote: {error}"
            )

            time.sleep(2)


if __name__ == "__main__":

    run()