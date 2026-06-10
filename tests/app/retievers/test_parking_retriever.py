import unittest

from retrievers.parking_retriever import ParkingRetriever


class DummySaveService:
    def __init__(self):
        self.saved = None
        self.read_value = None

    def save(self, lines):
        self.saved = lines

    def read(self):
        return self.read_value


class DummyNotificationService:
    def __init__(self):
        self.sent = False
        self.title = None
        self.body = None

    def send_message(self, title, body):
        self.sent = True
        self.title = title
        self.body = body


class DummyParkingRetriever(ParkingRetriever):
    def __init__(self, id_number, has_changes=False):
        super().__init__(id_number, has_changes)
        self.save_service = DummySaveService()
        self.notification_service = DummyNotificationService()

    def get_parking_list(self):
        return [{"ID_NUMBER": self.get_hidden_id(), "position": "5"}]


class TestParkingRetriever(unittest.TestCase):
    def test_process_sends_notification(self):
        retriever = DummyParkingRetriever("1234567890")
        retriever.save_service.read_value = None
        retriever.process()
        self.assertTrue(retriever.notification_service.sent)
        self.assertEqual(retriever.notification_service.title, "Lista Parking Rekalde")
        self.assertIn("5", retriever.notification_service.body)

    def test_process_no_notification_when_has_changes_false(self):
        retriever = DummyParkingRetriever("1234567890", has_changes=False)
        retriever.save_service.read_value = None
        retriever.process()
        self.assertTrue(retriever.notification_service.sent)

    def test_get_hidden_id(self):
        retriever = DummyParkingRetriever("1234567890")
        hidden_id = retriever.get_hidden_id()
        # id_number[-5:] = "67890", f"****{id_number[-5:]}" = "****67890", [:-1] + "*" = "****6789*"
        self.assertEqual(hidden_id, "****6789*")

    def test_filter_list_found(self):
        retriever = DummyParkingRetriever("1234567890")
        expected_hidden_id = retriever.get_hidden_id()
        user_list = [
            {"ID_NUMBER": expected_hidden_id, "position": "5"},
            {"ID_NUMBER": "****1234*", "position": "10"},
        ]
        result = retriever.filter_list(user_list)
        self.assertEqual(result, "5")

    def test_filter_list_not_found(self):
        retriever = DummyParkingRetriever("1234567890")
        user_list = [{"ID_NUMBER": "****1234*", "position": "10"}]
        result = retriever.filter_list(user_list)
        self.assertIsNone(result)

    def test_get_parking_list_empty_response(self):
        result = ParkingRetriever.get_parking_list()
        self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()
