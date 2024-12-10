from notification_service import NotificationService

class AbstractRetriever:
    def __init__(self):
        self.notification_service = NotificationService()

    def process(self):
        raise NotImplementedError("You must implement this method")

    def create_response(self, value):
        raise NotImplementedError("You must implement this method")
