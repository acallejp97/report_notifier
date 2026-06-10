import unittest

from retrievers.abstract_retriever import AbstractRetriever


class DummyNotificationService:
    def __init__(self):
        self.sent = False

    def send_message(self, title, body):
        self.sent = True


class DummySaveService:
    def __init__(self):
        self.saved = None

    def save(self, lines):
        self.saved = lines


class DummyRetriever(AbstractRetriever):
    def __init__(self):
        super().__init__()
        self.notification_service = DummyNotificationService()
        self.save_service = DummySaveService()

    def process(self):
        self.save_service.save(["test"])
        self.create_response("test")

    def create_response(self, value):
        self.notification_service.send_message("title", value)


class TestAbstractRetriever(unittest.TestCase):
    def test_process_and_create_response(self):
        retriever = DummyRetriever()
        retriever.process()
        self.assertEqual(retriever.save_service.saved, ["test"])
        self.assertTrue(retriever.notification_service.sent)

    def test_abstract_process_raises_not_implemented(self):
        retriever = AbstractRetriever()
        with self.assertRaises(NotImplementedError):
            retriever.process()

    def test_abstract_create_response_raises_not_implemented(self):
        retriever = AbstractRetriever()
        with self.assertRaises(NotImplementedError):
            retriever.create_response("test")


if __name__ == "__main__":
    unittest.main()
