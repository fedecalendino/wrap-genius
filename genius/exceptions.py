class APIException(Exception):
    def __init__(self, status, message, url):
        self.status = status
        self.message = message
        self.url = url

        super().__init__(f"{self.status} > {self.message}")
