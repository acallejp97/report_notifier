import os

from apprise import Apprise


class NotificationService:
    def __init__(self):
        self.service = Apprise()
        self.notification_bot = os.environ.get("NOTIFICATION_URL", "None")

    def send_message(self, title: str, body: str):
        self.service.add(self.notification_bot)
        self.service.notify(title=title, body=body)
