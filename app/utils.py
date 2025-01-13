import hashlib
import os


def get_bot_token():
    token = os.environ.get("NOTIFICATION_URL", "None").split("/")
    if token[0] != "None":
        return token[-2]
    raise ValueError("Token not found")


def compute_hash(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
