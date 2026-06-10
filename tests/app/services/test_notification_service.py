import os
import unittest

from services.notification_service import NotificationService


class DummyApprise:
    def __init__(self):
        self.added = None
        self.notified = False
        self.title = None
        self.body = None

    def add(self, url):
        self.added = url

    def notify(self, title, body):
        self.notified = True
        self.title = title
        self.body = body


class TestNotificationService(unittest.TestCase):
    def test_send_message(self):
        os.environ["NOTIFICATION_URL"] = "https://t.me/bot1234/abcd/"
        notif = NotificationService()
        dummy = DummyApprise()
        notif.service = dummy
        notif.send_message("Test Title", "Test Body")
        self.assertEqual(dummy.added, "https://t.me/bot1234/abcd/")
        self.assertTrue(dummy.notified)
        self.assertEqual(dummy.title, "Test Title")
        self.assertEqual(dummy.body, "Test Body")


if __name__ == "__main__":
    unittest.main()
