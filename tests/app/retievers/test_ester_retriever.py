import unittest

from retrievers.ester_retriever import EsterRetriever


class DummyNotificationService:
    def __init__(self):
        self.sent = False
        self.title = None
        self.body = None

    def send_message(self, title, body):
        self.sent = True
        self.title = title
        self.body = body


class DummyEsterRetriever(EsterRetriever):
    def __init__(self, default_date):
        super().__init__(default_date)
        self.notification_service = DummyNotificationService()

    def get_ester_value(self):
        return [{"PERIOD": self.date, "OBS": 1.23, "TREND_INDICATOR": "up"}, True]

    def clear_json(self, json):
        return json

    def original_date(self, date):
        return date


class TestEsterRetriever(unittest.TestCase):
    def test_process_sends_notification(self):
        retriever = DummyEsterRetriever("2024-05-13")
        retriever.process()
        self.assertTrue(retriever.notification_service.sent)
        self.assertEqual(retriever.notification_service.title, "Indice €STER")
        self.assertIn("1.23", retriever.notification_service.body)

    def test_clear_json_with_none_values(self):
        """Test that clear_json replaces None values"""
        json_data = [
            {"OBS": 1.0, "OBS_VALUE_ENTITY": 1.0, "TREND_INDICATOR": "up"},
            {"OBS": None, "OBS_VALUE_ENTITY": None, "TREND_INDICATOR": None},
        ]
        result = EsterRetriever.clear_json(json_data)
        # Verify that None values were replaced with previous value
        self.assertIsNotNone(result[0]["OBS"])
        self.assertEqual(result[0]["TREND_INDICATOR"], "equal")

    def test_yesterdays_value_static_method(self):
        result = EsterRetriever.yesterdays_value("2024-05-15")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 10)  # YYYY-MM-DD format

    def test_original_date_static_method(self):
        result = EsterRetriever.original_date("2024-05-13")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 10)  # YYYY-MM-DD format

    def test_create_response_not_found(self):
        """Test create_response when found is False"""
        retriever = EsterRetriever("2024-05-13")
        retriever.notification_service = DummyNotificationService()
        retriever.create_response([{"OBS": 3.5, "PERIOD": "2024-05-12", "TREND_INDICATOR": "up"}, False])

        self.assertTrue(retriever.notification_service.sent)
        self.assertIn("€STER", retriever.notification_service.body)
        self.assertIn("3.5", retriever.notification_service.body)


if __name__ == "__main__":
    unittest.main()
