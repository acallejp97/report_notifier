import os
import unittest

from utils import compute_hash
from utils import get_bot_token


class TestUtils(unittest.TestCase):
    def test_get_bot_token(self):
        os.environ["NOTIFICATION_URL"] = "https://t.me/bot1234/abcd/"
        self.assertEqual(get_bot_token(), "abcd")
        os.environ["NOTIFICATION_URL"] = "None"
        with self.assertRaises(ValueError):
            get_bot_token()

    def test_compute_hash(self):
        content = "test content"
        hash1 = compute_hash(content)
        hash2 = compute_hash(content)
        self.assertEqual(hash1, hash2)
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 64)


if __name__ == "__main__":
    unittest.main()
