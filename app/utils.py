import os


def get_bot_token():
    token = os.environ.get("NOTIFICATION_URL", "None").split("/")
    if token[0] != "None":
        return token[-2]
    raise ValueError("Token not found")
