class AbstractRetriever:
    def process(self):
        raise NotImplementedError("You must implement this method")

    def create_response(self, value):
        raise NotImplementedError("You must implement this method")
