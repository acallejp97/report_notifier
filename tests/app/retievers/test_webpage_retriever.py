import os
from unittest.mock import MagicMock
from unittest.mock import patch

from retrievers.webpage_retriever import WebpageRetriever


class DummySaveService:
    def __init__(self):
        self.filename = None
        self.saved = None
        self.read_value = None

    def update_filename(self, filename):
        self.filename = filename

    def save(self, value):
        self.saved = value

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


class DummyWebpageRetriever(WebpageRetriever):
    def __init__(self, send_notification=False):
        super().__init__(send_notification)
        self.save_service = DummySaveService()
        self.notification_service = DummyNotificationService()

    def _fetch_webpage(self, url):
        return "<html><head><title>M.O.D.A</title></head><body>content</body></html>"

    def _get_title(self, content):
        return "M.O.D.A"

    def create_response(self, value):
        title, message = value
        self.notification_service.send_message(title, message)


def test_process_sends_notification(temp_working_dir):
    retriever = DummyWebpageRetriever(True)
    retriever.save_service.read_value = None
    retriever.process()
    assert retriever.notification_service.sent
    assert retriever.notification_service.title == "M.O.D.A"


def test_get_title_with_title_tag():
    content = "<html><head><title>Test Title</title></head></html>"
    result = WebpageRetriever._get_title(content)
    assert result == "Test Title"


def test_get_title_without_title_tag():
    result = WebpageRetriever._get_title("<html><head></head></html>")
    assert result == "No Title"


@patch("retrievers.webpage_retriever.requests.get")
@patch.dict(os.environ, {"WEBPAGE_URLS": "http://example.com"})
def test_process_with_real_request(mock_get, temp_working_dir):
    """Test process method with mocked requests"""
    mock_response = MagicMock()
    mock_response.text = "<html><head><title>Example</title></head><body>test content</body></html>"
    mock_get.return_value = mock_response

    retriever = DummyWebpageRetriever()
    retriever.process()
    # Should save the hash
    assert retriever.save_service.saved is not None


def test_get_title_no_body():
    """Test _get_title with content containing no body tag"""
    content = "<html><head><title>No Body Title</title></head></html>"
    result = WebpageRetriever._get_title(content)
    assert result == "No Body Title"
