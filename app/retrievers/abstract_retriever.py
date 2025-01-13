from services.notification_service import NotificationService
from services.save_file_service import SaveService


class AbstractRetriever:
    def __init__(self, file_name: str = "mock_file"):
        self.notification_service = NotificationService()
        self.save_service = SaveService(file_name)

    def process(self):
        raise NotImplementedError("You must implement this method")

    def create_response(self, value):
        raise NotImplementedError("You must implement this method")
