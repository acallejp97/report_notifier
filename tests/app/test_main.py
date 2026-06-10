import os
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from main import get_service
from main import main


class TestMain(unittest.TestCase):
    def test_get_service_parking(self):
        """Test get_service returns ParkingRetriever for 'parking' argument"""
        os.environ["ID_NUMBER"] = "1234567890"
        service = get_service(["main.py", "parking"])

        self.assertIsNotNone(service)
        self.assertEqual(service.__class__.__name__, "ParkingRetriever")
        self.assertFalse(service.has_changes)

    def test_get_service_parking_with_has_changes(self):
        """Test get_service returns ParkingRetriever with has_changes when provided"""
        os.environ["ID_NUMBER"] = "1234567890"
        service = get_service(["main.py", "parking", "has_changes"])

        self.assertIsNotNone(service)
        self.assertEqual(service.__class__.__name__, "ParkingRetriever")
        self.assertTrue(service.has_changes)

    def test_get_service_ester(self):
        """Test get_service returns EsterRetriever for 'ester' argument"""
        service = get_service(["main.py", "ester"])

        self.assertIsNotNone(service)
        self.assertEqual(service.__class__.__name__, "EsterRetriever")

    def test_get_service_ester_with_date(self):
        """Test get_service returns EsterRetriever with date argument"""
        service = get_service(["main.py", "ester", "2024-05-15"])

        self.assertIsNotNone(service)
        self.assertEqual(service.__class__.__name__, "EsterRetriever")

    def test_get_service_webpage(self):
        """Test get_service returns WebpageRetriever for 'webpage' argument"""
        service = get_service(["main.py", "webpage"])

        self.assertIsNotNone(service)
        self.assertEqual(service.__class__.__name__, "WebpageRetriever")
        self.assertFalse(service.force_notification)

    def test_get_service_webpage_with_send_notification(self):
        """Test get_service returns WebpageRetriever with send_notification flag"""
        service = get_service(["main.py", "webpage", "send_notification"])

        self.assertIsNotNone(service)
        self.assertEqual(service.__class__.__name__, "WebpageRetriever")
        self.assertTrue(service.force_notification)

    @patch("main.get_service")
    def test_main_calls_process(self, mock_get_service):
        """Test main function calls process on the service"""
        mock_service = MagicMock()
        mock_get_service.return_value = mock_service

        main()

        mock_get_service.assert_called_once()
        mock_service.process.assert_called_once()

    def test_get_service_parking_case_insensitive(self):
        """Test get_service handles case insensitive command 'PARKING'"""
        os.environ["ID_NUMBER"] = "1234567890"
        service = get_service(["main.py", "PARKING"])

        self.assertEqual(service.__class__.__name__, "ParkingRetriever")

    def test_get_service_ester_case_insensitive(self):
        """Test get_service handles case insensitive command 'ESTER'"""
        service = get_service(["main.py", "ESTER"])

        self.assertEqual(service.__class__.__name__, "EsterRetriever")

    def test_get_service_webpage_case_insensitive(self):
        """Test get_service handles case insensitive command 'WEBPAGE'"""
        service = get_service(["main.py", "WEBPAGE"])

        self.assertEqual(service.__class__.__name__, "WebpageRetriever")


if __name__ == "__main__":
    unittest.main()
